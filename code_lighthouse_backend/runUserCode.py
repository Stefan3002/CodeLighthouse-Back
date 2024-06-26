import datetime
import os
import subprocess
import time
import uuid

import dateparser

import docker
from celery import shared_task
from django.db import transaction
from django.db.models import Q

from code_lighthouse_backend.dockerConfigurations import docker_config, docker_config_js, docker_config_ruby, \
    docker_config_python_hard, docker_config_ruby_hard, docker_config_js_hard
from code_lighthouse_backend.models import Challenge, AppUser, Code, Submission

SCORES = {
    -5: 100,
    -4: 500,
    -3: 1000,
    -2: 1500,
    -1: 2000,
    1: 4000,
    2: 5000,
    3: 6000,
    4: 7000,
    5: 10000
}


def compute_exec_time(container):
    cmdS = "docker inspect --format='{{.State.StartedAt}}' " + container.name
    cmdF = "docker inspect --format='{{.State.FinishedAt}}' " + container.name
    start_time = subprocess.check_output(cmdS, shell=True)
    finish_time = subprocess.check_output(cmdF, shell=True)

    start_time = start_time.decode("utf-8").strip()
    finish_time = finish_time.decode("utf-8").strip()

    start_time = dateparser.parse(start_time).timestamp()
    finish_time = dateparser.parse(finish_time).timestamp()

    exec_time = finish_time - start_time
    # print(exec_time)
    return exec_time


def saveSubmission(user_id, challenge, code, language, exec_time):
    user = AppUser.objects.get(user_id=user_id)
    new_submission = Submission(user=user, challenge=challenge, code=code, language=language, exec_time=exec_time)
    new_submission.save()


def checkExitCode(exit_code, user_id, challenge, code, language, mode, exec_time):
    user = AppUser.objects.get(user_id=user_id)
    if mode != 'hard' and challenge not in user.solved_challenges.all():
        challenge.attempts += 1
        challenge.save()
    # print('aa', exit_code)
    if exit_code == 0:
        if mode != 'hard' and challenge not in user.solved_challenges.all():
            user.score += SCORES[challenge.difficulty]
            challenge.solved += 1
            challenge.save()
        if mode != 'hard':
            user.solved_challenges.add(challenge)
        with transaction.atomic():
            user.save()
            if mode != 'hard':
                saveSubmission(user_id, challenge, code, language, exec_time)
    elif exit_code == 124:
        raise Exception('<strong><italic><h3>Solution timed out!</h3></italic></strong>\n<p><strong>Hard</strong> time limit reached!</p>')
    else:
        raise Exception('<strong><italic><h3>Wrong solution submitted!</h3></italic></strong>\n')


def removeFilesFromSystem(container, language, file_id, user_file, author_file, random_file, hard_file, case, extension):
    # user_file = ''
    # author_file = ''
    # random_file = ''
    # hard_file = ''
    #
    # extension = ''
    # case = ''
    #
    # if language == 'Python':
    #     extension = '.py'
    #     case = 'Camel'
    # elif language == 'Javascript':
    #     extension = '.js'
    #     case = 'Camel'
    # elif language == 'Ruby':
    #     extension = '.rb'
    #     case = 'Snake'
    #
    # if case == 'Snake':
    #     user_file = f'user_file-{file_id}{extension}'
    #     author_file = f'author_file-{file_id}{extension}'
    #     random_file = f'random_file-{file_id}{extension}'
    #     hard_file = f'hard_file{extension}'
    # elif case == 'Camel':
    #     user_file = f'userFile-{file_id}{extension}'
    #     author_file = f'authorFile-{file_id}{extension}'
    #     random_file = f'randomFile-{file_id}{extension}'
    #     hard_file = f'hardFile-{file_id}{extension}'

    os.remove(f'{user_file}-{file_id}{extension}')
    os.remove(f'{author_file}-{file_id}{extension}')
    os.remove(f'{random_file}-{file_id}{extension}')
    os.remove(f'{hard_file}-{file_id}{extension}')
    container.stop()
    container.remove()


def verify_functions(true_f, user, random, language):
    case = ''

    if language == 'Python':
        case = 'Camel'
    elif language == 'Javascript':
        case = 'Camel'
    elif language == 'Ruby':
        case = 'Snake'

    if case == 'Snake':
        user_function_name = f'user_function'

    elif case == 'Camel':
        user_function_name = f'userFunction'

    if len(user) <= 1:
        raise Exception(f'<p>You did <b>not</b> provide a function called: {user_function_name}</p>')

    if len(random) <= 1:
        raise Exception(f'<p>The author did <b>not</b> provide a random function.</p>')

    if len(true_f) <= 1:
        raise Exception(f'<p>The author did <b>not</b> provide a true function.</p>')

    return case



def create_files(code, true_solution, tests, custom_hard_tests, hard_tests, mode, file_id, case='Camel', language='python'):

    extension = '.py'

    if language == 'Python':
        extension = '.py'
    elif language == 'Ruby':
        extension = '.rb'
    elif language == 'Javascript':
        extension = '.js'

    if case == 'Camel':
        user_file = 'userFile'
        author_file = 'authorFile'
        random_file = 'randomFile'
        hard_file = 'hardFile'
    elif case == 'Snake':
        user_file = 'user_file'
        author_file = 'author_file'
        random_file = 'random_file'
        hard_file = 'hard_file'

    # Create the file with the user's code
    with open(f'{user_file}-{file_id}{extension}', 'w') as file:
        file.write(code)
    # Create the file with the author's correct code
    with open(f'{author_file}-{file_id}{extension}', 'w') as file2:
        file2.write(true_solution)
    # Create the file with the author's test cases
    with open(f'{random_file}-{file_id}{extension}', 'w') as file3:
        file3.write(tests)
    # Create the file with the author's hard test cases
    with open(f'{hard_file}-{file_id}{extension}', 'w') as file4:
        if mode == 'hard':
            file4.write(custom_hard_tests)
        else:
            file4.write(hard_tests)

    return user_file, author_file, random_file, hard_file, extension

def runUserCode(code, user_id, slug, mode, custom_hard_tests, soft_time_limit=6, language='Python'):
    challenge = Challenge.objects.filter(slug=slug)[0]
    challenge_code = Code.objects.get(Q(challenge=challenge) & Q(language=language))
    true_solution = challenge_code.solution
    tests = challenge_code.random_tests
    hard_tests = challenge_code.hard_tests
    if language == 'Javascript':
        # Add the export of the userFunction
        code += '\n module.exports = userFunction'

    try:
        case = verify_functions(true_solution, code, tests, language)
        file_id = uuid.uuid4()
        user_file, author_file, random_file, hard_file, extension = create_files(code, true_solution, tests, custom_hard_tests, hard_tests, mode, file_id, case, language)
        client = docker.from_env()

        if language == 'Python':
            docker_config_hard_file = docker_config_python_hard
            docker_config_file = docker_config
        elif language == 'Javascript':
            docker_config_hard_file = docker_config_js_hard
            docker_config_file = docker_config_js
        elif language == 'Ruby':
            docker_config_hard_file = docker_config_ruby_hard
            docker_config_file = docker_config_ruby


        if mode == 'hard':
            container = client.containers.create(**docker_config_hard_file)
        else:
            container = client.containers.create(**docker_config_file)


        os.system(f'docker cp {user_file}-{file_id}{extension} {container.name}:/app/vol/{user_file}{extension}')
        os.system(f'docker cp {author_file}-{file_id}{extension} {container.name}:/app/vol/{author_file}{extension}')
        os.system(f'docker cp {random_file}-{file_id}{extension} {container.name}:/app/vol/{random_file}{extension}')
        os.system(f'docker cp {hard_file}-{file_id}{extension} {container.name}:/app/vol/{hard_file}{extension}')

        # Start with that config that stops it after a number of seconds

        container.start()

        # Get the logs as a stream of bytes
        logs = container.logs(stdout=True, stderr=True, stream=True)
        log_bytes = b''
        # Accumulate the bytes
        for line in logs:
            log_bytes += line
        # Decode the bytes into str
        logs_str = log_bytes.decode('utf-8')
        # print(logs_str)

        exit_code = subprocess.check_output(["docker", "wait", container.name])

        exit_code = exit_code.decode("utf-8").strip()
        exit_code = int(exit_code)

        # Get the exec. time of the container.
        exec_time = compute_exec_time(container)

        # Return error if it passed the challenge author's max time
        if exec_time > soft_time_limit:
            raise Exception(
                f'<strong><italic><h3>Solution timed out!</h3></italic></strong>\n<p><strong>Soft</strong> time limit '
                f'reached: {soft_time_limit}s! Your execution time: {str(exec_time)[:4]}s.</p>')

        checkExitCode(exit_code, user_id, challenge, code, language, mode, exec_time)
        # Sure to not have failed
        removeFilesFromSystem(container, language, file_id, user_file, author_file, random_file, hard_file, case, extension)
        return logs_str, exec_time
    except Exception as e:
        removeFilesFromSystem(container, language, file_id, user_file, author_file, random_file, hard_file, case, extension)
        raise Exception(f'{e} {logs_str}')
        # return Response({'OK': False, 'data': e}, status=status.HTTP_200_OK)


    # return Response({'OK': True, 'data': logs_str}, status=status.HTTP_200_OK)


# def runJavascriptCode(request, slug, mode, custom_hard_tests):
#     challenge = Challenge.objects.filter(slug=slug)[0]
#     challenge_code = Code.objects.get(Q(challenge=challenge) & Q(language='Javascript'))
#     true_solution = challenge_code.solution
#     hard_tests = challenge_code.hard_tests
#     tests = challenge_code.random_tests
#
#     code = request.data['code']
#
#     # Add the export of the userFunction
#
#     code += '\n module.exports = userFunction'
#
#     user_id = request.data['userId']
#     try:
#         with transaction.atomic():
#             # Create the file with the user's code
#             with open('userFile.js', 'w') as file:
#                 file.write(code)
#             # Create the file with the author's correct code
#             with open('authorFile.js', 'w') as file2:
#                 file2.write(true_solution)
#             # Create the file with the author's test cases
#             with open('randomFile.js', 'w') as file3:
#                 file3.write(tests)
#             # Create the file with the author's test cases
#             with open('hardFile.js', 'w') as file4:
#                 if mode == 'hard':
#                     file4.write(custom_hard_tests)
#                 else:
#                     file4.write(hard_tests)
#
#             client = docker.from_env()
#             if mode == 'hard':
#                 container = client.containers.create(**docker_config_js_hard)
#             else:
#                 container = client.containers.create(**docker_config_js)
#
#             os.system(f'docker cp userFile.js {container.name}:/app/vol/userFile.js')
#             os.system(f'docker cp authorFile.js {container.name}:/app/vol/authorFile.js')
#             os.system(f'docker cp randomFile.js {container.name}:/app/vol/randomFile.js')
#             os.system(f'docker cp hardFile.js {container.name}:/app/vol/hardFile.js')
#             container.start()
#             # Get the logs as a stream of bytes
#             logs = container.logs(stdout=True, stderr=True, stream=True)
#             log_bytes = b''
#             # Accumulate the bytes
#             for line in logs:
#                 log_bytes += line
#             # Decode the bytes into str
#             logs_str = log_bytes.decode('utf-8', errors='replace').replace('\u2714', '')
#             print(logs_str)
#
#             exit_code = subprocess.check_output(["docker", "wait", container.name])
#
#             exit_code = exit_code.decode("utf-8").strip()
#             exit_code = int(exit_code)
#
#             checkExitCode(exit_code, user_id, challenge, code, 'Javascript')
#
#             # Sure to not have failed
#             return logs_str
#     except Exception as e:
#         raise Exception(f'{e} {logs_str}')
#         # return Response({'OK': False, 'data': e}, status=status.HTTP_200_OK)
#     finally:
#         removeFilesFromSystem(container, 'Javascript')
#
#
# def runRubyCode(request, slug, mode, custom_hard_tests):
#     challenge = Challenge.objects.filter(slug=slug)[0]
#     challenge_code = Code.objects.get(Q(challenge=challenge) & Q(language='Ruby'))
#     true_solution = challenge_code.solution
#     tests = challenge_code.random_tests
#     hard_tests = challenge_code.hard_tests
#     code = request.data['code']
#     user_id = request.data['userId']
#     try:
#         with transaction.atomic():
#             # Create the file with the user's code
#             with open('user_file.rb', 'w') as file:
#                 file.write(code)
#             # Create the file with the author's correct code
#             with open('author_file.rb', 'w') as file2:
#                 file2.write(true_solution)
#             # Create the file with the author's test cases
#             with open('random_file.rb', 'w') as file3:
#                 file3.write(tests)
#             # Create the file with the author's hard test cases
#             with open('hard_file.rb', 'w') as file4:
#                 if mode == 'hard':
#                     file4.write(custom_hard_tests)
#                 else:
#                     file4.write(hard_tests)
#
#             client = docker.from_env()
#             if mode == 'hard':
#                 container = client.containers.create(**docker_config_ruby_hard)
#             else:
#                 container = client.containers.create(**docker_config_ruby)
#
#             os.system(f'docker cp user_file.rb {container.name}:/app/vol/user_file.rb')
#             os.system(f'docker cp author_file.rb {container.name}:/app/vol/author_file.rb')
#             os.system(f'docker cp random_file.rb {container.name}:/app/vol/random_file.rb')
#             os.system(f'docker cp hard_file.rb {container.name}:/app/vol/hard_file.rb')
#
#             container.start()
#             # Get the logs as a stream of bytes
#             logs = container.logs(stdout=True, stderr=True, stream=True)
#             log_bytes = b''
#             # Accumulate the bytes
#             for line in logs:
#                 log_bytes += line
#             # Decode the bytes into str
#             logs_str = log_bytes.decode('utf-8', errors='replace').replace('\u2714', '')
#             print(logs_str)
#
#             exit_code = subprocess.check_output(["docker", "wait", container.name])
#
#             exit_code = exit_code.decode("utf-8").strip()
#             exit_code = int(exit_code)
#
#             checkExitCode(exit_code, user_id, challenge, code, 'Ruby')
#             # Sure to not have failed
#             return logs_str
#
#     except Exception as e:
#         raise Exception(f'{e} {logs_str}')
#         # return Response({'OK': False, 'data': e}, status=status.HTTP_200_OK)
#     finally:
#         removeFilesFromSystem(container, 'Ruby')

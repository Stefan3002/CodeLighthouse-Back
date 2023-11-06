import os
import subprocess

import docker
from django.db import transaction
from django.db.models import Q

from code_lighthouse_backend.dockerConfigurations import docker_config, docker_config_js, docker_config_ruby
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

def saveSubmission(user_id, challenge, code, language):
    user = AppUser.objects.get(user_id=user_id)
    new_submission = Submission(user=user, challenge=challenge, code=code, language=language)
    new_submission.save()
def checkExitCode(exit_code, user_id, challenge, code, language):
    if exit_code == 0:
        user = AppUser.objects.get(user_id=user_id)
        user.solved_challenges.add(challenge)
        if challenge not in user.solved_challenges.all():
            user.score += SCORES[challenge.difficulty]
        user.save()

        saveSubmission(user_id, challenge, code, language)

    else:
        raise Exception('Wrong solution submitted!')


def removeFilesFromSystem(container, language):
    user_file = ''
    author_file = ''
    random_file = ''

    extension = ''
    case = ''

    if language == 'Python':
        extension = '.py'
        case = 'Camel'
    elif language == 'Javascript':
        extension = '.js'
        case = 'Camel'
    elif language == 'Ruby':
        extension = '.rb'
        case = 'Snake'

    if case == 'Snake':
        user_file = f'user_file{extension}'
        author_file = f'author_file{extension}'
        random_file = f'random_file{extension}'
    elif case == 'Camel':
        user_file = f'userFile{extension}'
        author_file = f'authorFile{extension}'
        random_file = f'randomFile{extension}'

    os.remove(user_file)
    os.remove(author_file)
    os.remove(random_file)
    container.stop()
    container.remove()

def runPythonCode(request, slug):
    challenge = Challenge.objects.filter(slug=slug)[0]
    challenge_code = Code.objects.get(Q(challenge=challenge) & Q(language='Python'))
    true_solution = challenge_code.solution
    tests = challenge_code.random_tests
    code = request.data['code']
    user_id = request.data['userId']
    try:
        with transaction.atomic():
            # Create the file with the user's code
            with open('userFile.py', 'w') as file:
                file.write(code)
            # Create the file with the author's correct code
            with open('authorFile.py', 'w') as file2:
                file2.write(true_solution)
            # Create the file with the author's test cases
            with open('randomFile.py', 'w') as file3:
                file3.write(tests)

            client = docker.from_env()
            container = client.containers.create(**docker_config)

            os.system(f'docker cp userFile.py {container.name}:/app/vol/userFile.py')
            os.system(f'docker cp authorFile.py {container.name}:/app/vol/authorFile.py')
            os.system(f'docker cp randomFile.py {container.name}:/app/vol/randomFile.py')
            container.start()
            # Get the logs as a stream of bytes
            logs = container.logs(stdout=True, stderr=True, stream=True)
            log_bytes = b''
            # Accumulate the bytes
            for line in logs:
                log_bytes += line
            # Decode the bytes into str
            logs_str = log_bytes.decode('utf-8')
            print(logs_str)

            exit_code = subprocess.check_output(["docker", "wait", container.name])

            exit_code = exit_code.decode("utf-8").strip()
            exit_code = int(exit_code)

            checkExitCode(exit_code, user_id, challenge, code, 'Python')

    except Exception as e:
        raise Exception(e)
        # return Response({'OK': False, 'data': e}, status=status.HTTP_200_OK)
    finally:
        removeFilesFromSystem(container, 'Python')

    return logs_str
    # return Response({'OK': True, 'data': logs_str}, status=status.HTTP_200_OK)


def runJavascriptCode(request, slug):
    challenge = Challenge.objects.filter(slug=slug)[0]
    challenge_code = Code.objects.get(Q(challenge=challenge) & Q(language='Javascript'))
    true_solution = challenge_code.solution
    tests = challenge_code.random_tests

    code = request.data['code']
    user_id = request.data['userId']
    try:
        with transaction.atomic():
            # Create the file with the user's code
            with open('userFile.js', 'w') as file:
                file.write(code)
            # Create the file with the author's correct code
            with open('authorFile.js', 'w') as file2:
                file2.write(true_solution)
            # Create the file with the author's test cases
            with open('randomFile.js', 'w') as file3:
                file3.write(tests)

            client = docker.from_env()
            container = client.containers.create(**docker_config_js)

            os.system(f'docker cp userFile.js {container.name}:/app/vol/userFile.js')
            os.system(f'docker cp authorFile.js {container.name}:/app/vol/authorFile.js')
            os.system(f'docker cp randomFile.js {container.name}:/app/vol/randomFile.js')
            container.start()
            # Get the logs as a stream of bytes
            logs = container.logs(stdout=True, stderr=True, stream=True)
            log_bytes = b''
            # Accumulate the bytes
            for line in logs:
                log_bytes += line
            # Decode the bytes into str
            logs_str = log_bytes.decode('utf-8', errors='replace').replace('\u2714', '')
            print(logs_str)

            exit_code = subprocess.check_output(["docker", "wait", container.name])

            exit_code = exit_code.decode("utf-8").strip()
            exit_code = int(exit_code)

            checkExitCode(exit_code, user_id, challenge, code, 'Javascript')

    except Exception as e:
        raise Exception(e)
        # return Response({'OK': False, 'data': e}, status=status.HTTP_200_OK)
    finally:
        removeFilesFromSystem(container, 'Javascript')

    return logs_str

def runRubyCode(request, slug):
    challenge = Challenge.objects.filter(slug=slug)[0]
    challenge_code = Code.objects.get(Q(challenge=challenge) & Q(language='Ruby'))
    true_solution = challenge_code.solution
    tests = challenge_code.random_tests
    code = request.data['code']
    user_id = request.data['userId']
    try:
        with transaction.atomic():
            # Create the file with the user's code
            with open('user_file.rb', 'w') as file:
                file.write(code)
            # Create the file with the author's correct code
            with open('author_file.rb', 'w') as file2:
                file2.write(true_solution)
            # Create the file with the author's test cases
            with open('random_file.rb', 'w') as file3:
                file3.write(tests)

            client = docker.from_env()
            container = client.containers.create(**docker_config_ruby)

            os.system(f'docker cp user_file.rb {container.name}:/app/vol/user_file.rb')
            os.system(f'docker cp author_file.rb {container.name}:/app/vol/author_file.rb')
            os.system(f'docker cp random_file.rb {container.name}:/app/vol/random_file.rb')
            container.start()
            # Get the logs as a stream of bytes
            logs = container.logs(stdout=True, stderr=True, stream=True)
            log_bytes = b''
            # Accumulate the bytes
            for line in logs:
                log_bytes += line
            # Decode the bytes into str
            logs_str = log_bytes.decode('utf-8', errors='replace').replace('\u2714', '')
            print(logs_str)

            exit_code = subprocess.check_output(["docker", "wait", container.name])

            exit_code = exit_code.decode("utf-8").strip()
            exit_code = int(exit_code)

            checkExitCode(exit_code, user_id, challenge, code, 'Ruby')

    except Exception as e:
        raise Exception(e)
        # return Response({'OK': False, 'data': e}, status=status.HTTP_200_OK)
    finally:
        removeFilesFromSystem(container, 'Ruby')

    return logs_str

import os
import subprocess

import docker
from django.db.models import Q

from code_lighthouse_backend.dockerConfigurations import docker_config, docker_config_js
from code_lighthouse_backend.models import Challenge, AppUser, Code


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


def runPythonCode(request, slug):
    challenge = Challenge.objects.filter(slug=slug)[0]
    challenge_code = Code.objects.get(Q(challenge=challenge) & Q(language='Python'))
    true_solution = challenge_code.solution
    tests = challenge_code.random_tests
    code = request.data['code']
    user_id = request.data['userId']
    try:
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

        if exit_code == 0:
            user = AppUser.objects.get(user_id=user_id)
            user.solved_challenges.add(challenge)
            user.score += SCORES[challenge.difficulty]
            user.save()
        else:
            raise Exception('Wrong solution submitted!')

    except Exception as e:
        raise Exception(e)
        # return Response({'OK': False, 'data': e}, status=status.HTTP_200_OK)
    finally:
        os.remove('userFile.py')
        os.remove('authorFile.py')
        os.remove('randomFile.py')
        container.stop()
        container.remove()

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

        if exit_code == 0:
            user = AppUser.objects.get(user_id=user_id)
            user.solved_challenges.add(challenge)
            user.score += SCORES[challenge.difficulty]
            user.save()
        else:
            raise Exception('Wrong solution submitted!')

    except Exception as e:
        raise Exception(e)
        # return Response({'OK': False, 'data': e}, status=status.HTTP_200_OK)
    finally:
        os.remove('userFile.js')
        os.remove('authorFile.js')
        os.remove('randomFile.js')
        container.stop()
        # container.remove()

    return logs_str

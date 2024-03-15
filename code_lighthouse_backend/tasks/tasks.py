from celery import shared_task
from rest_framework.response import Response
from code_lighthouse_backend.runUserCode import runPythonCode
from rest_framework import status


def format_logs_for_html(logs):
    html_logs = '<p>' + logs.replace('\n', '</p><p>')
    html_logs = html_logs.replace('\t', '&nbsp;&nbsp;')
    return html_logs

def handle_code_error(e):
    error_str = format_logs_for_html(str(e))
    return {'OK': False, 'data': error_str}



@shared_task
def send_email_celery():
    return 1 + 12


@shared_task
def runPythonCodeCelery(code, user_id, slug, mode, custom_hard_tests, soft_time_limit=6):
    try:
        results = runPythonCode(code, user_id, slug, mode, custom_hard_tests, soft_time_limit)
        logs_str = results[0]
        exec_time = results[1]
        # Success!
        logs_str = format_logs_for_html(logs_str)
    except Exception as e:
        return handle_code_error(e)
    print('aaaaa')
    return {'OK': True, 'data': {'logs': logs_str, 'time': exec_time}}


from django_cron import CronJobBase, Schedule

from code_lighthouse_backend.models import Challenge


class purge_denied_challenges_cron(CronJobBase):
    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'purge_denied_challenges'

    def do(self):
        print('Starting to purge!')
        denied_challenges = Challenge.objects.filter(denied=True)
        for challenge in denied_challenges:
            print(f'Purging: {challenge}')
            challenge.delete()
        print('Done purging!')
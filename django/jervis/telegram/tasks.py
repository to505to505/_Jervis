from django.core.management import call_command
from crontab import CronTab

def my_cron_job():
    call_command(print('my_command'))
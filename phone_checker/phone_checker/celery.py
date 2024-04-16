import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'phone_checker.settings')

app = Celery('phone_checker' , broker='redis://localhost:14000/0', backend="redis://localhost:14000/1" )
app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()



# заносим таски в очередь
app.conf.beat_schedule = {
    'every': { 
        'task': 'main_app.tasks.repeat_order_make',
        'schedule': crontab(),
    },                                                              

}



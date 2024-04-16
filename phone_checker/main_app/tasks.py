from phone_checker.celery import app
from .models import Person 
import requests
import json
import time

@app.task
def repeat_order_make():
    # Стягивание данных 
    pass
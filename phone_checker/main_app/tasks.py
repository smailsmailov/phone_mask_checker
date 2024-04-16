from phone_checker.celery import app
import urllib.request

@app.task
def repeat_order_make():
    file_1  = "https://opendata.digital.gov.ru/downloads/ABC-3xx.csv?1710948258581"
    file_2  = "https://opendata.digital.gov.ru/downloads/ABC-3xx.csv?1710948258581"
    file_3  = "https://opendata.digital.gov.ru/downloads/ABC-3xx.csv?1710948258581"
    file_4  = "https://opendata.digital.gov.ru/downloads/ABC-3xx.csv?1710948258581"
    
    destination = '../files/'
    
    urllib.request.urlretrieve(file_1, destination)
    urllib.request.urlretrieve(file_2, destination)
    urllib.request.urlretrieve(file_3, destination)
    urllib.request.urlretrieve(file_4, destination)
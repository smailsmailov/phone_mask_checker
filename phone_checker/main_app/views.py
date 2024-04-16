from django.shortcuts import render
from rest_framework.decorators import api_view , throttle_classes
from rest_framework.response import Response 
from rest_framework.throttling import UserRateThrottle
from django.core.files.storage import DefaultStorage
from rest_framework import status
import os
import pandas as pd
from django.conf import settings
from pathlib import Path
# ------------------------ SUPPORT FUNC ------------------------
def check_value_in_range(item:str , l_range:int , r_range:int , ABC:int):
    """Функция проверят находится ли объект в диапазоне чисел
    

    Args:
        item (str): Число str
        l_range (int): Левая граница
        r_range (int): Правая граница

    Returns:
        bool: Находится ли объект в границах ? 
    """
    if int(item[4:]) in range(l_range , r_range+1) and item[1:4] == str(ABC):
        return True
    else : 
        return False
    
    
    
# ---------------------- SUPPORT FUNC END ----------------------


# Защита на кол-во запросов 
class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'

# Основной рендер
def render_index(request):
    return render(request , "index.html")


# Один эндпоинт апи
@api_view(["POST"])
# @throttle_classes([OncePerDayUserThrottle])
def check_phone(request):
    dict_of_files = {
        "3" : Path("/files/ABC-3xx.csv"),
        "4" : Path("/files/ABC-4xx.csv"),
        "8" : Path("/files/ABC-8xx.csv"),
        "9" : Path("/files/DEF-9xx.csv"),
    }
    storage = DefaultStorage()
    
    error_response =  Response({
                "type": "validation_error",
                "errors": [{
                    "code": "required",
                    "detail": "Phone field wrong!",
                    "attr": "phone"
                }]} , status=status.HTTP_400_BAD_REQUEST )
    
    
    
    if request.method == 'POST':
        if request.POST["phone"] : 
            phone = request.POST["phone"]
            if phone[1] in  dict_of_files.keys() : 
                file_path =  Path( str(settings.BASE_DIR) +  str(dict_of_files[phone[1]]))
                file_data = pd.read_csv( file_path , sep=';', comment='#' )
                flag = False
                for i in zip( file_data["АВС/ DEF"].values , file_data["От"].values , file_data["До"].values): 
                    if check_value_in_range(phone , i[1] , i[2] , i[0]) : 
                        data = file_data.loc[(file_data['От'] == i[1]) & (file_data['До'] == i[2]) & (file_data['АВС/ DEF'] == i[0])  ]
                        print(data , )
                        flag = True
                        
                        return Response({'provider' : data["Оператор"].values[0] , 'position' :data["Регион"].values[0]})

                if flag == False : 
                    return Response({
                        "type": "404_error",
                        "errors": [{
                            "code": "required",
                            "detail": "Phone is not found",
                            "attr": "phone"
                        }]}  , status=status.HTTP_404_NOT_FOUND )


                return Response({
                "type": "validation_error",
                "errors": [{
                    "code": "required",
                    "detail": "Phone field wrong!",
                    "attr": "phone"
                }]}  , status=status.HTTP_400_BAD_REQUEST )
    
            else : 
                return error_response
        else: 
            return error_response
        
    return error_response

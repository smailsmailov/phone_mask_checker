# ----------------IMPORT--------------------
import pandas as pd
import fnmatch
from functools import lru_cache , wraps
import asyncio
import datetime
import time
import matplotlib.pyplot  as plt
# ----------------FUNC----------------------
def time_decorator(func):
    """Классический декоратор на время выполнения программы 

    Args:
        function (_any_): Любая функция 
    """
    @wraps(func)
    def time_wraper(*args, **kwargs):
        print(f'Функция {func.__name__} начала работать' + '\n'*3)
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print( '\n'*3 + f'Функция {func.__name__} работала {total_time:.2f} секунд')
        return result
    return time_wraper

def check_quintile(percent , value ) : 
    """Функция для проверки значений в процентном соотношении     
        
        Наиболее продаваемый - верхний квантиль: 0,9;
        Средне продаваемый - между квантилями 0,9 и 0,3;
        Наименее продаваемый: все что ниже 0,3.
    Args:
        percent (float): 1% измерения 
        value (int): Проверяемый объект 

    Returns:
        str : Значение в которое попадает объект 
    """
    try:
        range_of_quintile = [0*percent , 30*percent , 90*percent , 100*percent ]
        if value < 0 :
            return "Наименее продаваемый(Кол-во продаж отрицательное)"
        elif value >= range_of_quintile[2] :
            return "Наиболее продаваемый"
        elif value >= range_of_quintile[1] and value<range_of_quintile[2]:
            return "Средне продаваемый"
        elif value < range_of_quintile[1]:
            return "Наименее продаваемый"
        else:
            return "Наименее продаваемый"
    except Exception as e: 
        print(f"Ошибка : {e}" )
        raise RuntimeError("DATA ERROR")

def merge_dicts(dict1, dict2):
    """Слияние двух словарей с сохранением ключей 

    Args:
        dict1 (dict): Словарь 1 
        dict2 (dict): Словарь 2

    Returns:
        dict: Словарь 1 и Словарь 2
    """
    return {k: dict1.get(k, 0) + dict2.get(k, 0) for k in set(dict1) | set(dict2)}


def get_city(link:str , cities):
    """Получение города по ссылке

    Args:
        link (str): Ссылка на город
        cities (File): Фаил с городами
    Returns:
        str : Название города 
    """
    return(cities.loc[cities['Ссылка'] == link]["Наименование"].values[0])

def check_time_range(time:str ):
    """Получение временного диапазона 

    Args:
        time (str): Время в виде строчки формата "H:M:S"

    Returns:
        array : datetime.time range  
    """
    a_ =datetime.time( int(time.split(":")[0]) , int(time.split(":")[1]) ,int(time.split(":")[2]) )
    
    times_range = []
    for i in range(23) : 
        times_range.append( (datetime.time(hour = i, minute = 0, second = 0) , datetime.time(hour = i+1, minute = 0, second = 0)))
    times_range.append((datetime.time(hour = 23, minute = 0, second = 0) , datetime.time(hour = 0, minute = 0, second = 0)))


    for i in times_range : 
        if i[0] <= a_ <=i[1] : 
            return i

@time_decorator
def first_task(cities,branches,products,sales):    
    """Функция на первую группу заданий 

    Args:
        cities (File): Фаил из задания 
        branches (File): Фаил из задания 
        products (File): Фаил из задания 
        sales (File): Фаил из задания 
    """
    # словарь {Филиал : Кол-во продаж}
    top_sales_dict = sales["Филиал"].value_counts().to_dict()
    # словарь {Наименование склада  : Ссылка на склад}
    dict_of_stocks = {}
    # словарь для отображения первых складов по количеству продаж  {Кол-во продаж : Наименование}
    dict_of_stock_by_value = {}
    # словарь {Наименование магазина  : Ссылка на магазин}
    dict_of_stores = {}
    # словарь для отображения первых магазинов по количеству продаж  {Кол-во продаж : Наименование}
    dict_of_stores_by_value = {}
    
    
    # Получение всех магазинов с ссылками 
    for i in range(len(branches["Наименование"])) :
        if not fnmatch.fnmatch( branches["Наименование"][i] , "*Склад*") and  not fnmatch.fnmatch( branches["Наименование"][i] , "*склад*") and not fnmatch.fnmatch( branches["Наименование"][i] , "*cклад*"):
            dict_of_stores[branches["Наименование"][i]] = branches["Ссылка"][i]

    # Получение кол-во продаж у магазина 
    for i in dict_of_stores.keys() :
        dict_of_stores_by_value[top_sales_dict[dict_of_stores[i]]] = i 
            
    # Получение всех складов с ссылками 
    for i in range(len(branches["Наименование"])) :
        if fnmatch.fnmatch( branches["Наименование"][i] , "*Склад*") or fnmatch.fnmatch( branches["Наименование"][i] , "*склад*") or fnmatch.fnmatch( branches["Наименование"][i] , "*cклад*"):
            dict_of_stocks[branches["Наименование"][i]] = branches["Ссылка"][i]
            
    # Получение кол-во продаж у склада 
    for i in dict_of_stocks.keys() :
        dict_of_stock_by_value[top_sales_dict[dict_of_stocks[i]]] = i 
        
    # Задание 1.1,1.2 P.S(В задании 1.2 указано 10 складов, но в фаиле всего их 9 :-(,  
    # 10-й Склад под названием "ЕКБ старый cклад" в названии содержит символы не
    # из кириллицы и по маске его найти тяжко, пришлось проверять все объекты 
    # на соответствие символам кириллицы
     
    print("\n"*5 + "десять первых складов по количеству продаж")
    print ( dict(sorted(dict_of_stock_by_value.items() , reverse=True)[:10]) )
    print("\n"*5 + "десять первых магазинов по количеству продаж")
    print ( dict(sorted(dict_of_stores_by_value.items(), reverse=True)[:10]) )

    top_items_sales = sales[["Номенклатура","Филиал"]].value_counts().to_dict()
    # словарь для отображения первых складов по количеству продаж  {Кол-во продаж : Наименование}
    dict_of_items_by_value = {}
    # словарь для отображения первых магазинов по количеству продаж  {Кол-во продаж : Наименование}
    dict_of_items_store_by_value = {}
    
    
    # Буферы для вывода данных 
    all_sales_stock = []
    all_sales_stores = []
    
    # Создание пустых массивов для будущей сортировке по типу (магазин, склад)
    # for i in top_items_sales.keys():
    #     if i[1] in  dict_of_stocks.values() : 
    #         dict_of_items_by_value[i[1]] = []
    #     else : 
    #         dict_of_items_store_by_value[i[1]] = []

    # Создание пустых массивов для будущей сортировке по типу (магазин, склад)
    for i in top_items_sales.keys():
        if i[1] in  dict_of_stocks.values() : 
            dict_of_items_by_value[i[1]] = 0
        else : 
            dict_of_items_store_by_value[i[1]] = 0

    # Создание словаря {Магазин : (Товар,кол-во)} PS.Думал что пригодится, в итоге не пригодилось
    # Создание списка товаров которые были куплены либо в магазине, либо на складе 
    # for i in top_items_sales.keys():
    #     if i[1] in  dict_of_stocks.values() : 
    #         all_sales_stock.append({i[0] :top_items_sales[i]})
    #         dict_of_items_by_value[i[1]].append({i[0]:top_items_sales[i] })
    #     else : 
    #         all_sales_stores.append({i[0] :top_items_sales[i]})
    #         dict_of_items_store_by_value[i[1]].append({i[0]:top_items_sales[i] })
    
    # Создание словаря {Магазин : Общее кол-во}
    # Создание списка товаров которые были куплены либо в магазине, либо на складе 
    for i in top_items_sales.keys():
        if i[1] in  dict_of_stocks.values() : 
            all_sales_stock.append({i[0] :top_items_sales[i]})
            dict_of_items_by_value[i[1]] += top_items_sales[i]
        else : 
            all_sales_stores.append({i[0] :top_items_sales[i]})
            dict_of_items_store_by_value[i[1]] += top_items_sales[i] 
    
    
    # Задание 1.3,1.4
    # Топ продаж по всем складам 
    print("\n"*5 + "Топ продаж по складам")
    holder = {}
    for i in all_sales_stock : 
        holder = merge_dicts(holder, i)
    print(dict(sorted(holder.items(),reverse=True, key=lambda item: item[1])[:10]))
    
    # Топ продаж по всем магазинам 
    print("\n"*5 + "Топ продаж по магазинам")
    holder = {}
    for i in all_sales_stores : 
        holder = merge_dicts(holder, i)
    
    print(dict(sorted(holder.items(),reverse=True, key=lambda item: item[1])[:10]))
    # print(all_sales_stores)
    
    
    # Сливаем словари с продажами складов и магазинов
    holder = merge_dicts(dict_of_items_store_by_value, dict_of_items_by_value)
    # Сортируем весь словарь по кол-ву продаж
    top_of_stores = dict(sorted(holder.items(),reverse=True, key=lambda item: item[1]))
    # Буфер для записи всех городов в порядке убывания         
    top_cites = []
    for i in top_of_stores.keys() :
        for j in range(len(branches[['Ссылка',"Город"]])):
            if i == branches["Ссылка"][j]:
                top_cites.append(get_city(branches["Город"][j] , cities))
    # Убираем все дубликаты сохраняя позиции объектов
    top_cites = [i for n, i in enumerate(top_cites) if i not in top_cites[:n]]
    
    # Задание 1.5
    print(top_cites[:10])
    
@time_decorator
def second_task(cities,branches,products,sales):
    """Функция на вторую и третью группу заданий 
    
    Args:
        cities (File): Фаил из задания 
        branches (File): Фаил из задания 
        products (File): Фаил из задания 
        sales (File): Фаил из задания 
    """
    # Задание можно выполнить через встроенные метод в pandas date_range, но тогда время выполнения больше и код труднее читать
    # Использовал словари...
    
    # Дни недели 
    name_of_days = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
    
    # Временные диапазоны 
    times_range = []
    for i in range(23) : 
        times_range.append( (datetime.time(hour = i, minute = 0, second = 0) , datetime.time(hour = i+1, minute = 0, second = 0)))
    times_range.append((datetime.time(hour = 23, minute = 0, second = 0) , datetime.time(hour = 0, minute = 0, second = 0)))
    
    # Общий счетчик продаж по периоду 
    count_of_sales_by_time = sales["Период"].value_counts()
    
    # Словарь {день продажи : всё время проданных товар за этот день }
    dict_of_dates_with_time_sales = {}
    dict_of_dates_with_time_iso_sales = {}
    
    all_times = []
    
    # Считывание данных  в словарь {День недели : значение продаж массив }
    for i in count_of_sales_by_time.items() : 
        dict_of_dates_with_time_iso_sales[datetime.datetime.strptime(i[0].split(" ")[0] ,"%Y-%m-%d")] = []
        
    for i in count_of_sales_by_time.items() : 
        dict_of_dates_with_time_iso_sales[datetime.datetime.strptime(i[0].split(" ")[0] ,"%Y-%m-%d")].append(i[0].split(" ")[1])

    # Общий список времени продаж
    for i in count_of_sales_by_time.items() : 
        all_times.append(i[0].split(" ")[1])
    
    # Считывание данных  в словарь {День недели : значение продаж массив }
    for i in count_of_sales_by_time.items() : 
        dict_of_dates_with_time_sales[datetime.datetime.strptime(i[0].split(" ")[0] ,"%Y-%m-%d").weekday()] = []
        
    # Подсчет кол-ва продаж в определенный день недели  
    for i in count_of_sales_by_time.items() : 
        dict_of_dates_with_time_sales[datetime.datetime.strptime(i[0].split(" ")[0] ,"%Y-%m-%d").weekday()].append(i[0].split(" ")[1])
    
    # Печать {День продажи : Все продажи в этот день}
    # print('\n'*5)
    # print(dict_of_dates_with_time_sales)
    # print('\n'*5)
    
    dict_of_dats_with_sales = {}
    for i in dict(sorted(dict_of_dates_with_time_iso_sales.items() , reverse=True)).keys() :
        dict_of_dats_with_sales[i] = len(dict_of_dates_with_time_iso_sales[i])

    # Получаем сортированный список по кол-ву продаж в день 
    # for i in dict(sorted(dict_of_dats_with_sales.items() , reverse=True,key=lambda item: item[1] )).keys() : 
    #     print(i , dict_of_dats_with_sales[i])
    
    # Задание №2.2
    # Локальный максимум будет 0 элемент словаря, так же его день недели 
    holder = dict(sorted(dict_of_dats_with_sales.items() , reverse=True,key=lambda item: item[1] ))
    print("\n"*5+f"Локальный максимум : \n День недели:{name_of_days[list(holder.keys())[0].weekday()]} \n Дата :{list(holder.keys())[0]}" )
    all_times_dict = {}
    for i in all_times : 
        all_times_dict[check_time_range(i)] = []
    for i in all_times : 
        all_times_dict[check_time_range(i)].append(i)
        
    counted_times_range = {}
    for i in all_times_dict : 
        counted_times_range[i] = len(all_times_dict[i])

    time_holder = dict(sorted(counted_times_range.items() , reverse=True,key=lambda item: item[1] ))
    best_time = list(time_holder.keys())[0]
    print(f"Время в которое больше всего делают покупки : c {best_time[0].strftime('%H:%M:%S')} по {best_time[1].strftime('%H:%M:%S')}")
    # Отсортированный словарь где 0 индекс является ответом на задание №2.1
    
    # ------------------------------------------------------------------------------------------------------
    print('\n'*5)
    dict_of_day_to_count = {}
    for i in dict_of_dates_with_time_sales.keys():
        dict_of_day_to_count [name_of_days[i]] = len(dict_of_dates_with_time_sales[i])
    
    # Отрисовка данных для продаж по дням недели
    x_day = []
    y_day_value = []
    
    # Вывод с сортировкой доп задание на дни недели (№3) 
    for j in name_of_days:
        y_day_value.append(dict_of_day_to_count[j])
        
    plt.figure(1)
    plt.bar(name_of_days, y_day_value,alpha=0.5 , label='Кол-во продаж по дням недели ')
    plt.plot(name_of_days, y_day_value, color='red', marker='o', markersize=7)
    plt.xlabel('День недели')
    plt.ylabel('Кол-во')
    plt.title('Данные по дням недели ')
    plt.legend()
   
    
    # отрисовка данных по временным диапазонам 
    range_of_time = []
    count_of_values_of_time = []
    for i in counted_times_range.keys() :
        # print(type(i))
        if i is None:
            range_of_time.append(f"23:00:00 - 00:00:00")
        else:
            range_of_time.append(f"{i[0].strftime('%H:%M:%S')} - {i[1].strftime('%H:%M:%S')}")
    
    
    for i in counted_times_range.values():
        count_of_values_of_time.append(i)
    
    # Второй график построен без сортировки по временным рамкам ( построен от большего к меньшему )
    plt.figure(2)
    plt.bar(range_of_time, count_of_values_of_time,alpha=0.5 , label='Кол-во продаж по времени')
    plt.plot(range_of_time, count_of_values_of_time, color='green', marker='o', markersize=7)
    plt.xlabel('Время')
    plt.ylabel('Кол-во')
    plt.title('Данные по временным рамкам')
    plt.legend()
    plt.show()

@time_decorator
def third_task(sales):
    """Функция на задание по расчетной части

    Args:
        sales (File): Фаил по заданию 
    """
    # Словарь {Ссылка : кол-во продаж }
    dict_of_all_items_with_counter = {}
    
    for i in range(len(sales['Номенклатура'])) : 
        if sales['Номенклатура'][i] in dict_of_all_items_with_counter : 
            dict_of_all_items_with_counter[sales['Номенклатура'][i]] += sales['Количество'][i] 
        else :
            dict_of_all_items_with_counter[sales['Номенклатура'][i]] = sales['Количество'][i]  
    
    dict_of_all_items_with_counter = dict(sorted(dict_of_all_items_with_counter.items(),reverse=True, key=lambda item: item[1]))
    
    #Нельзя брать максимальный элемент, потому что он аномально большой, первые 50 элементов аномально большие, я взял 100 элемент как опорный 
    # Если брать максимум исключив только аномальные значения, то почти все значения в таблице будут мало продаваемыми. 
    max_value = dict_of_all_items_with_counter[list(dict_of_all_items_with_counter.keys())[100]]
    min_value = dict_of_all_items_with_counter[list(dict_of_all_items_with_counter.keys())[-1]] 
    # min и max нужны для процентного расчета квантиля , где max это 1.0(100%) квантиль а min это 0.0( 0,000(0)1% ) квантиль 
    # 1 процент от макс кол-ва 
    percent = max_value/100
    
    
    # списки для записи в EXEL и CSV
    value_of_item = []
    value_of_item_quintile = []
    val_test = []
    
    for i in dict_of_all_items_with_counter.keys() : 
        res = check_quintile(percent ,dict_of_all_items_with_counter[i] )
        value_of_item.append(i)
        value_of_item_quintile.append(res)
        val_test.append(dict_of_all_items_with_counter[i] )
    df = pd.DataFrame({'Номенклатура': value_of_item, 'КлассТовара': value_of_item_quintile })
    # df = pd.DataFrame({'Номенклатура': value_of_item, 'КлассТовара': value_of_item_quintile , "Значение" :val_test})
    
    df.to_excel("quintile.xlsx", engine='xlsxwriter')  
    df.to_csv("quintile.csv")
    
# ------------------------------------------
if __name__ == '__main__':
    # Все данные из таблиц считанные в переменные
    cities = pd.read_csv("t_cities.csv")
    branches = pd.read_csv("t_branches.csv")
    products = pd.read_csv("t_products.csv")
    sales = pd.read_csv("t_sales.csv")
    
    # Первое задание 
    first_task(cities,branches,products,sales)
    
    # Второе и третье задание
    second_task(cities,branches,products,sales)
    
    # Задание по расчету 
    third_task(sales)
    
# ------------------------------------------

import os

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import  Mebel
from .parser.parsing_kufar import Parser_postgresql

parsing = Parser_postgresql()


def app_1_mainpage(request):
    return render(request, 'app_1/app_1_index.html')

def go_to_mainpage(request):
    return redirect('index')


def show_all(request):
    # mebels = Mebel.objects.all().order_by('price')
    mebels = Mebel.objects.all().order_by('id')

    # connection = parser.connect_to_db()
    # parser.delete_all_data_from_table_db(connection=connection)
    # mebels = parser.get_data_from_db(connection=connection)
    # parser.close_connection_db(connection)
    return render(request, f"app_1/show_data.html", {'find_id':True, 'mebels': mebels})

def show_index(request, item_index):
    try:
        print('====')
        mebel = Mebel.objects.get(id=item_index)
        print('===', mebel)
    except:
        return render(request, 'app_1/show_data.html', {'find_id': False, 'item_index':item_index})
    else:
        return render(request, 'app_1/show_data.html', {'find_id':True, 'mebels':(mebel, )})




def run_scripts(request):
    try:
        parsing.run()
        message = "Данные получены!"
        return render(request, 'app_1/after_processing.html', {'message':message})
    except:
        return HttpResponse("Произошла ошибка при получении данных!")


def erase_db(request):
    try:
        parsing.erase_db(parsing.connect_to_db())
        message = "Данные очищены!"
        return render(request, 'app_1/after_processing.html', {'message':message})
    except:
        return HttpResponse("Произошла ошибка при очищении базы данных!")

def page_not_found_app_1(request):
    '''
    сделано через re_path() работаеть только по пути '/app_1/' далее можно указать любой адрес
    '''
    return render(request, 'app_1/page_not_found.html')


def page_not_found(request, *args, **kwargs):
    return redirect('index')
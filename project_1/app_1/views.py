import os

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import  Mebel
from .parser.parsing_kufar import Parser_postgresql

parsing = Parser_postgresql()


def app_1_mainpage(request):
    return render(request, 'app_1/app_1_index.html')

def go_to_mainpage(request):
    return redirect('app_1_index')


def show_all(request):
    # mebels = Mebel.objects.all().order_by('price')
    mebels = Mebel.objects.all()

    # connection = parser.connect_to_db()
    # parser.delete_all_data_from_table_db(connection=connection)
    # mebels = parser.get_data_from_db(connection=connection)
    # parser.close_connection_db(connection)
    return render(request, f"app_1/show_all.html", {'mebels': mebels})


def run_scripts(request):
    try:
        parsing.run()
        return HttpResponse("Данные получены!")
    except:
        return HttpResponse("Произошла ошибка при получении данных!")


def erase_db(request):
    parsing.erase_db(parsing.connect_to_db())
    return HttpResponse("База данных очищена!")


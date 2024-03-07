import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Mebel
from .parser.parsing_kufar import Parser_postgresql
from .forms import UpdateDataForm


parsing = Parser_postgresql()


def app_1_mainpage(request):
    return render(request, 'app_1/app_1_index.html')


def go_to_mainpage(request):
    return redirect('index')

def show_admin(request):
    mebels = Mebel.objects.all().order_by('-parse_datetime')
    form = UpdateDataForm()

    return render(request, 'app_1/show_admin.html', {'mebels':mebels, 'forms':form})


def update_item(request, item_index):
    new_price = request.POST.get('price', '')
    new_description = request.POST.get('description', '')

    mebels = Mebel.objects.filter(pk=item_index).update(
        price=new_price,
        description=new_description
    )

    return redirect('admin_page')

def delete_item(request, item_index):
    if request.method == "POST":
        mebel = Mebel.objects.filter(pk=item_index).delete()

    return redirect('admin_page')

def show_all(request):
    mebels = Mebel.objects.all().order_by('id')
    # комментарии ниже это для добавления в ДБ без использования модели
    # connection = parser.connect_to_db()
    # parser.delete_all_data_from_table_db(connection=connection)
    # mebels = parser.get_data_from_db(connection=connection)
    # parser.close_connection_db(connection)
    return render(request, f"app_1/show_data.html", {'find_id': True, 'mebels': mebels})


def show_index(request, item_index):
    '''
    используется один и тот же шаблон для show_all() & shot_index() не знаю на сколько так используется
    но очень хотелось их разнести, что бы не городить многоэтажные ифы в шаблоне =)
    '''
    try:
        mebel = Mebel.objects.get(id=item_index)
    except:
        return render(request, 'app_1/show_data.html', {'find_id': False, 'item_index': item_index})
    else:
        return render(request, 'app_1/show_data.html', {'find_id': True, 'mebels': (mebel,)})


def run_scripts(request):
    try:
        parsing.run()
        message = "Данные получены!"
        return render(request, 'app_1/after_processing.html', {'message': message})
    except:
        return HttpResponse("Произошла ошибка при получении данных!")


def erase_db(request):
    try:
        parsing.erase_db(parsing.connect_to_db())
        message = "Данные очищены!"
        return render(request, 'app_1/after_processing.html', {'message': message})
    except:
        return HttpResponse("Произошла ошибка при очищении базы данных!")


def page_not_found_app_1(request):
    '''
    сделано через re_path() работаеть только по пути '/app_1/' далее можно указать любой адрес
    '''
    return render(request, 'app_1/page_not_found.html')


def page_not_found(request, *args, **kwargs):
    return redirect('index')

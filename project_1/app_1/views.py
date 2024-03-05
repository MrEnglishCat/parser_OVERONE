from django.shortcuts import render
from django.http import HttpResponse

from .models import  Mebel
from .parser.parsing_kufar import Parser_postgresql

parsing = Parser_postgresql()


def show_all(request):
    # mebels = Mebel.objects.all().order_by('price')
    mebels = Mebel.objects.all()

    # connection = parser.connect_to_db()
    # parser.delete_all_data_from_table_db(connection=connection)
    # mebels = parser.get_data_from_db(connection=connection)
    # parser.close_connection_db(connection)
    return render(request, "app_1/show_all.html", {'mebels': mebels})


def run_scripts(request):
    try:
        parsing.delete_all_data_from_table_db(parsing.connect_to_db())
        parsing.run()
        return HttpResponse("Данные получены!")
    except:
        return HttpResponse("Произошла ошибка при получении данных!")


def url3(request):
    return HttpResponse(request)

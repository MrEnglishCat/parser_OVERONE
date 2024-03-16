from datetime import datetime, timezone

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Mebel
from .parser.parsing_kufar import Parser_postgresql
from .forms import UpdateDataForm
from .serializers import GetAllDataSerializer
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import logout as lg_out
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response

parsing = Parser_postgresql()


def app_1_mainpage(request):
    return render(request, 'app_1/app_1_index.html')


def go_to_mainpage(request):
    return redirect('index')


def show_admin(request):
    if request.method == "GET":
        mebels = Mebel.objects.filter().order_by('-update_datetime')
        form = UpdateDataForm()
        paginator = Paginator(
            mebels,
            per_page=10,
            error_messages={"no_results": "Page does not exist"},
        )
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        context = {
            # 'mebels': mebels,
            'queryset': page_obj,
            'forms': form
        }
    elif request.method == "POST":
        pass

    return render(request, 'app_1/show_admin.html', context=context)


def update_item(request, item_index):
    if request.method == "POST" and request.user.is_superuser:
        new_price = float(request.POST.get('price', ''))
        new_description = request.POST.get('description', '')
        new_update_datetime = datetime.now(timezone.utc)
        Mebel.objects.filter(pk=item_index).update(
            price=new_price,
            description=new_description,
            update_datetime=new_update_datetime
        )
    if 'app_1/items/' in request.META.get('HTTP_REFERER', ''):
        return redirect(f'/app_1/items/{item_index}')
    else:
        return redirect('admin_page')


def delete_item(request, item_index):
    if request.method == "POST" and request.user.is_superuser:
        mebel = Mebel.objects.filter(pk=item_index).delete()

    if 'app_1/items/' in request.META.get('HTTP_REFERER', ''):
        return redirect('items')
    else:
        return redirect('admin_page')


def show_all(request):
    mebels = Mebel.objects.all().order_by('id')
    paginator = Paginator(
        mebels,
        25,
        error_messages={"no_results": "Page does not exist"},
    )
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {
        # 'mebels': mebels,
        'queryset': page_obj
    }
    # page_obj = paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=2)
    # комментарии ниже это для добавления в ДБ без использования модели
    # connection = parser.connect_to_db()
    # parser.delete_all_data_from_table_db(connection=connection)
    # mebels = parser.get_data_from_db(connection=connection)
    # parser.close_connection_db(connection)

    return render(
        request,
        f"app_1/show_data.html",
        context=context
    )


def show_index(request, item_index):
    '''
    используется один и тот же шаблон для show_all() & shot_index() не знаю на сколько так используется
    но очень хотелось их разнести, что бы не городить многоэтажные ифы в шаблоне =)
    '''
    try:
        mebel = Mebel.objects.get(id=item_index)
        form = UpdateDataForm()
    except:
        return render(request, 'app_1/show_item.html', {'find_id': False, 'item_index': item_index})
    else:
        return render(request, 'app_1/show_item.html', {'find_id': True, 'mebels': (mebel,), 'form': form})


def run_scripts(request):
    try:
        parsing.run()
        message = "Данные получены!"
        return render(request, 'app_1/after_processing.html', {'message': message})
    except Exception as err:
        return HttpResponse("Произошла ошибка при получении данных!")


def erase_db(request):
    if request.method == "GET" and request.user.is_superuser:
        try:
            parsing.erase_db(parsing.connect_to_db())
            message = "Данные очищены!"
            return render(request, 'app_1/after_processing.html', {'message': message})
        except:
            return HttpResponse("Произошла ошибка при очищении базы данных!")
    else:
        return HttpResponse("Пройдите авторизацию перед удалением всех записей из БД!")


def page_not_found_app_1(request):
    '''
    сделано через re_path() работаеть только по пути '/app_1/' далее можно указать любой адрес
    '''
    return render(request, 'app_1/page_not_found.html')


def page_not_found(request, *args, **kwargs):
    return redirect('index')


def login(request):
    # print(request.user)
    # return render(request, 'registration/login.html')
    ...


def logout(request):
    lg_out(request)
    return redirect('login')


def user_settings(request):
    form = UserChangeForm()
    if request.method == "GET":
        pass
    elif request.method == "POST":
        new_first_name = request.POST.get('first_name', '')
        new_last_name = request.POST.get('last_name', '')
        new_email = request.POST.get('email', '')
        user_id = request.user.id
        user = User.objects.filter(pk=user_id).update(
            first_name=new_first_name,
            last_name=new_last_name,
            email=new_email
        )
        # user = User.objects.filter(pk=user_id)

    return render(request, 'app_1/settings.html', {'form': form})


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'


# class Logout(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('logout')
#     template_name = 'registration/logout.html'


class APIGetAllData(APIView):
    def get(self, request, start:int=None, end:int=None):
        start = start if isinstance(start, int) else 0
        end = end if isinstance(end, int) else 0
        if not end and not start:
            # print('start is NONE and end is NONE', 'START:', start, 'END:', end)
            queryset = Mebel.objects.all()
        elif end and not start:
            # print('start is NONE and end', 'START:', start, 'END:', end)
            queryset = Mebel.objects.all()[:end]
        else:
            # print('start and end', 'START:', start, 'END:', end)
            queryset = Mebel.objects.all()[start:end]
        serializer_for_reading = GetAllDataSerializer(instance=queryset, many=True)

        return Response(serializer_for_reading.data)


class APIGetAllDataSorted(APIView):

    def get(self, request, filter:str=None):
        if filter is None:
            queryset = Mebel.objects.all()
        elif isinstance(filter, str):
            if hasattr(Mebel, filter[1:] if filter.startswith('-') else filter
                       ):
                queryset = Mebel.objects.all().order_by(filter)
            else:
                queryset = []
        serializer_for_reading = GetAllDataSerializer(instance=queryset, many=True)

        return Response(serializer_for_reading.data)


class APIGetSliceDataSorted(APIView):
    def get(self, request, filter:str=None, start:int=None, end:int=None):
        start = start if isinstance(start, int) else 0
        end = end if isinstance(end, int) else 0
        if isinstance(filter, str):
            if hasattr(Mebel, filter[1:] if filter.startswith('-') else filter
                       ):
                if end is None and start is None:
                    queryset = Mebel.objects.all().order_by(filter)
                elif end and start is None:
                    queryset = Mebel.objects.all().order_by(filter)[:end]
                elif end and start:
                    queryset = Mebel.objects.all().order_by(filter)[start:end]

        else:
            queryset = []

        serialyzer_for_reading = GetAllDataSerializer(instance=queryset, many=True)

        return Response(serialyzer_for_reading.data)

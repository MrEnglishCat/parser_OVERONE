from django.urls import path, re_path
from . import views


urlpatterns = [
    path('1', views.show_all),
    path('2', views.run_scripts),
    path('app_1_main', views.app_1_mainpage, name='index'),
    path('erase_db', views.erase_db),
    path('', views.go_to_mainpage),
    re_path(r'.*', views.page_not_found_app_1)
]


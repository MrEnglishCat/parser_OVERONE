from django.urls import path, re_path
from . import views


urlpatterns = [

    path('items', views.show_all),
    path('items_admin', views.show_admin),
    path('items/<int:item_index>', views.show_index),
    path('get_data', views.run_scripts),
    path('app_1_main', views.app_1_mainpage, name='index'),
    path('erase_db', views.erase_db),
    path('update_item', views.update_item, name='update_item'),
    path('', views.go_to_mainpage),
    re_path(r'.*', views.page_not_found_app_1)
]


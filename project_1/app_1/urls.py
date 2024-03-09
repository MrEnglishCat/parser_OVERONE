from django.urls import path, re_path
from . import views

urlpatterns = [
    path('items', views.show_all),
    path('items_admin', views.show_admin, name='admin_page'),
    path('items/<int:item_index>', views.show_index),
    path('get_data', views.run_scripts),
    path('app_1_main', views.app_1_mainpage, name='index'),
    path('erase_db', views.erase_db),
    path('update_item/<int:item_index>', views.update_item, name='update_item'),
    path('delete_item/<int:item_index>', views.delete_item, name='delete_item'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='log_out'),
    # path('logout', views.Logout.as_view(), name='logout'),
    path('settings', views.user_settings, name ='user_settings'),
    path('registration', views.SignUp.as_view(), name='registration'),
    path('', views.go_to_mainpage),
    re_path(r'.*', views.page_not_found_app_1)
]

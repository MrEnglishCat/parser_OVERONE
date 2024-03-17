from django.urls import path, re_path, include
from rest_framework import routers
from . import views


##############  Добавлен только для того что бы посмотреть какр он работает         ########
##############  кроме стандартного функционала "mebel/{id}" ничего не реализовано   ########
##############  разобрался что можно в роутере добавлять path-объекты в список router.urls  ########
router = routers.DefaultRouter()
router.register(r'mebel', views.ConstructorAPIView)

urlpatterns = [
    path('items', views.show_all, name='items'),
    path('items_admin', views.show_admin, name='admin_page'),
    path('items/<int:item_index>', views.show_index, name='show_item'),
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
    ##############      API ########################
    path('api/', include(router.urls)),
    path('api/create_item', views.CreateOneUnitDataAPIView.as_view()),
    path('api/update_item/<int:pk>', views.UpdateOneUnitDataAPIView.as_view()),
    path('api/delete_item/<int:pk>', views.DeleteOneUnitDataAPIView.as_view()),
    path('api/get_all_data', views.GetAllDataAPIView.as_view()),
    path('api/filter/get_all_data/<str:order_sorted>', views.GetAllDataSortedAPIView.as_view()),
    path('api/filter/slice/<str:order_sorted>/<int:end>', views.GetDataSortedSliceAPIView.as_view()),
    path('api/filter/slice/<str:order_sorted>/<int:start>/<int:end>', views.GetDataSortedSliceAPIView.as_view()),
    path('api/slice/get_item/<int:end>', views.GetAllDataAPIView.as_view()),
    path('api/slice/get_item/<int:start>/<int:end>', views.GetAllDataAPIView.as_view()),
##############      /API ########################
    path('', views.go_to_mainpage),
    re_path(r'.*', views.page_not_found_app_1)
]






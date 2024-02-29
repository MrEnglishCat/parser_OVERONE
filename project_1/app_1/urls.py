from django.urls import path
from . import views


urlpatterns = [
    path('1', views.show_all),
    path('2', views.run_scripts),
    path('3', views.url3)
]


from django.contrib import admin
from .models import Mebel


class MebelAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'description', 'parse_datetime')
    list_per_page = 25
    list_max_show_all = 5000
    list_filter = ('parse_datetime', 'price')
    # list_editable = ('price', 'description')
    list_editable = ('price',)
    ordering = ('id', 'price')

admin.site.register(Mebel, MebelAdmin)

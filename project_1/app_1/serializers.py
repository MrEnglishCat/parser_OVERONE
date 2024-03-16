import time
from datetime import datetime
from django.utils.timezone import  tzinfo
from rest_framework import serializers



class GetAllDataSerializer(serializers.Serializer):

    # не получилось получить offset current timezone =(
    get_name_timezone = time.localtime().tm_zone
    get_offset_tz = datetime.now().astimezone().strftime("%z")
    link = serializers.CharField()
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=4,
        min_value=0
    )
    description = serializers.CharField()
    update_datetime = serializers.DateTimeField(read_only=True, format=f'%Y-%m-%d %H:%M:%S {get_offset_tz}UTC [{get_name_timezone}]')
    parse_datetime = serializers.DateTimeField(read_only=True, format=f'%Y-%m-%d %H:%M:%S {get_offset_tz}UTC [{get_name_timezone}]', input_formats=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"])

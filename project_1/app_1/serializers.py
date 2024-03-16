import datetime
import time
from datetime import timezone, datetime, timedelta

from django.utils.timezone import timezone, localtime, template_localtime
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
    update_datetime = serializers.DateTimeField(read_only=True, format='%Y-%d-%m %H:%M:%S:%f %z')
    parse_datetime = serializers.DateTimeField(read_only=True, format=f'%d-%m-%Y %H:%M:%S:%f {get_offset_tz} {get_name_timezone}')
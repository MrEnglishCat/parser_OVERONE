from rest_framework import serializers


class GetAllDataSerializer(serializers.Serializer):

    link = serializers.CharField()
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=4,
        min_value=0
    )
    description = serializers.CharField()
    update_datetime = serializers.DateTimeField(format='%Y-%d-%m %H:%M:%S:%f %z')

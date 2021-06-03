from rest_framework import serializers

class my_controlSerializer(serializers.Serializer):
    identificator = serializers.CharField(max_length=10)
    dev_1 = serializers.BooleanField()
    dev_2 = serializers.BooleanField()
    dev_3 = serializers.BooleanField()

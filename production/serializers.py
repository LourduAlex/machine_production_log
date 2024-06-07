from rest_framework import serializers
from .models import Machine, ProductionLog


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class ProductionLogSerializer(serializers.ModelSerializer):
    machine_name = serializers.CharField(source= "machine_name", read_only=True)

    class Meta:
        model = ProductionLog
        fields = ['machine_name', '__all__']
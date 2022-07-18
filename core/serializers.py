from rest_framework import serializers

from .models import Elevator, ElevatorRequests


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'

class ElevatorRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorRequests
        fields = '__all__'

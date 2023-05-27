from rest_framework import serializers
from .models import Xamp320EventwiseJsondataReceived



# Table-5:
class Xamp320EventwiseJsondataReceivedSerializer(serializers.ModelSerializer):
    # Specify the model    
    class Meta:
        model = Xamp320EventwiseJsondataReceived

        # Specify the fields to serialize
        fields = ('event_name_t130_t530_x320', 'event_id_from_t520_x320', 'event_code_from_t520_x320', 'ticket_prefix_x320', 'faretype_x320', 'adult_rt_x320', 'child_rt_x320', 'perticket_rt_x320')


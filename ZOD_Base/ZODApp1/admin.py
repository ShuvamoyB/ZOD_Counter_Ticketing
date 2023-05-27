from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Xamp100Constants)  # Table-1

admin.site.register(Xamp200LoadsheddingInfo)  # Table-2

admin.site.register(Xamp220DailySummary)  # Table-3

admin.site.register(Xamp300Log)  # Table-4

admin.site.register(Xamp320EventwiseJsondataReceived)  # Table-5

admin.site.register(Xamp330TicketGrpGist)  # Table-6

admin.site.register(Xamp340TicketSoldDetails)  # Table-7

admin.site.register(Xamp350SetellementDetailed)  # Table-8
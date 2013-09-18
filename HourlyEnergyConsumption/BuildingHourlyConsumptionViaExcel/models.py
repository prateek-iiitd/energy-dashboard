from django.db import models
from datetime import datetime

# Create your models here.

class Building(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    where_clause = models.CharField(max_length=75)

    def __unicode__(self):
        return self.name

class FileRequest(models.Model):

    start_time = models.DateTimeField(blank=False, verbose_name="Start Time")
    end_time = models.DateTimeField(blank=False, verbose_name="End Time")
    building = models.ForeignKey(Building, blank=False, verbose_name="Building")

    request_time = models.DateTimeField(default=datetime.now(),blank=False)
    request_IP = models.IPAddressField(blank=False)

    def __unicode__(self):
        return "%s Start: %s End: %s" %(self.building, self.start_time.strftime("%d/%m/%Y "))
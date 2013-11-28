from django.db import models

# Create your models here.
class Building(models.Model):
    name = models.CharField(max_length=40)
    where_clause = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
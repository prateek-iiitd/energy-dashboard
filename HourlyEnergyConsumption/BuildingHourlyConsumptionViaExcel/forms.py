__author__ = 'prateek'
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django import forms
from models import FileRequest
from django.contrib.admin import widgets

class FileRequestForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FileRequestForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FileRequest
        fields = ['start_time','end_time','building']
        widgets = {'start_time': SelectDateWidget(years=range(2013,2016,1)), 'end_time':  SelectDateWidget(years=range(2013,2016,1))}

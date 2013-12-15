from django import forms
from models import Building

class MatchingMetersForm(forms.Form):
    BUILDING_CHOICES = [(str(t),str(t)) for t in Building.objects.all()]
    #BUILDING_CHOICES = [('Academic Building','Academic Building'),]
    BLOCK_CHOICES = [('0','0'),('Academic Block','Academic Block'),('Lecture Block','Lecture Block')]
    FLOOR_CHOICES = [(str(x),str(x)) for x in xrange(0,12)]
    WING_CHOICES = [('0','0'),('A','A'),('B','B'),('C','C'),('AB','AB'),('BC','BC')]

    building = forms.ChoiceField(choices=BUILDING_CHOICES, widget=forms.Select(attrs={'onchange':'get_blocks();'}))
    block = forms.ChoiceField(choices=BLOCK_CHOICES, widget=forms.Select(attrs={'onchange':'get_floors());'}))
    floor = forms.ChoiceField(choices=FLOOR_CHOICES,widget=forms.Select(attrs={'onchange':'get_wings();'}))
    wing = forms.ChoiceField(choices=WING_CHOICES,widget=forms.Select())

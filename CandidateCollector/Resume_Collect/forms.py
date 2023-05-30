from django.forms import ModelForm
from django import forms
from .models import Opening, Candidate

class OpeningForm(ModelForm):
    class Meta:
        model = Opening
        fields = ['name']
    
    def __init__(self, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter Job Title'})

class CandidateForm(ModelForm):
    class Meta:
        file = forms.FileField()
        model = Candidate
        fields =['name', 'phone', 'email', 'education', 'experience', 'text_list', 'opening', 'resume']
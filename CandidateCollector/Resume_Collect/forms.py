from django.forms import ModelForm
from django import forms
from .models import Opening, Candidate
from .utils import *

class OpeningForm(ModelForm):
    class Meta:
        model = Opening
        fields = ['name']
    
    def __init__(self, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter Job Title'})

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CandidateForm(forms.Form):
    opening = forms.ModelChoiceField(queryset=Opening.objects.all(), empty_label="Select a Job Opening")
    resumes = MultipleFileField()



"""class CandidateForm(ModelForm):
    opening = forms.ModelChoiceField(queryset=Opening.objects.all())
    class Meta:
        model = Candidate
        fields = ['opening', 'resume']

    def save(self, commit=True):
        candidate = super(CandidateForm, self).save(commit=False)

        # process request.FILES content here
        file = self.cleaned_data.get('resume')
        if file is not None:
            text = read_pdf(file)
            text = remove_null_bytes(text)
            candidate.name = extract_name(text)
            candidate.phone = extract_phone(text)
            candidate.email = extract_email(text)
            candidate.education = extract_education(text)
            candidate.experience = extract_experience(text)
            candidate.text_list = list_text(text)

        if commit:
            candidate.save()

        return candidate"""
from django import forms
from django.forms import ModelForm, RadioSelect
from .models import SectionPreference


class SectionPreferenceForm(ModelForm):
    class Meta:
        model = SectionPreference
        fields = ['section', 'preference']
        #widgets = {'preference':RadioSelect(),}


class LandingForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
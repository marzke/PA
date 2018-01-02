from django import forms
from django.forms import ModelForm, RadioSelect, TextInput
from .models import SectionPreference
#from Academics.widgets import SectionPreferenceWidget

#w = SectionPreferenceWidget()
#print w.media
class SectionPreferenceForm(ModelForm):
    class Meta:
        model = SectionPreference
        fields = ['preference']
        labels = {'preference':''}
        widgets = {'preference':RadioSelect()}

    class Media:
        css = {'all': ('Academics/css/sectionPreference.css',)}

    def set_for_conflict(self):
        #self.fields['preference'].widget
        self.fields['preference'].widget.attrs['disabled']=True
        #self.save()

#w = SectionPreferenceForm()
#print w.media

class LandingForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
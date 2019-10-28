from django import forms
from django.forms import ModelForm, RadioSelect, CheckboxInput
from .models import Section, SectionPreference, WithdrawalPreferences, Reason, College, Term


# from Academics.widgets import SectionPreferenceWidget

# w = SectionPreferenceWidget()
# print w.media
class SectionPreferenceForm(ModelForm):
    class Meta:
        model = SectionPreference
        fields = ['preference']
        labels = {'preference': ''}
        widgets = {'preference': RadioSelect()}

    class Media:
        css = {'all': ('Academics/css/sectionPreference.css',)}

    def set_for_conflict(self):
        # self.fields['preference'].widget
        self.fields['preference'].widget.attrs['disabled'] = True
        # self.save()


class CollegeTTSFRForm(forms.Form):

    college = forms.ModelChoiceField(College.objects.all().order_by('description'),
                                     empty_label=None,
                                     to_field_name='name',
                                     label='')
    term = forms.ModelChoiceField(Term.objects.all().order_by('number'),
                                  empty_label=None,
                                  to_field_name='number',
                                  label='')

    class Media:
        css = {'all': ('Academics/css/collegeTTSFR.css',
                       'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
                       )}
        js = ('https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js',
              'https://unpkg.com/web-animations-js@2.3.1/web-animations.min.js',
              'https://unpkg.com/hammerjs@2.0.8/hammer.min.js',
              'https://unpkg.com/muuri@0.7.1/dist/muuri.min.js',
              'Academics/js/collegeTTSFR.js',
        )


class SectionForm(forms.Form):
    class Meta:
        model = Section
        fields = ['session', 'number']



# w = SectionPreferenceForm()
# print w.media

# class WithdrawalPreferencesForm(ModelForm):
#     class Meta:
#         model = WithdrawalPreferences
#         fields = ['reasons']
#         labels = {'reasons':''}
#         widgets = {'reasons':CheckboxInput()}

class ReasonPreferenceForm(ModelForm):
    class Meta:
        model = Reason
        fields = ['name']
        labels = {'name': ''}
        widgets = {'name': CheckboxInput()}

    class Media:
        css = {'all': ('Academics/css/reasonPreferences.css',)}


class LandingForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

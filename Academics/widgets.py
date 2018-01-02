from django import forms


class SectionPreferenceWidget(forms.RadioSelect):
    class Media:
        css = {'all': ('sectionPreference.css',)}

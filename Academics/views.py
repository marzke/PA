from django.shortcuts import render
from django.views import generic
from .models import *
from .forms import LandingForm, SectionPreferenceForm
from django.views.generic.edit import UpdateView

from django.http import HttpResponse

def index(request):
    env = request.environ
    print request.user
    context = {'user':env['USER'],
               'shell':env['SHELL'],
               'uid':'900041849',
               'displayName': 'Ron Marzke'
    }
    return render(request, 'academics/index.html', context)


class LandingView(generic.ListView):
    template_name = 'bootstrap.html'
    form_class = LandingForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(ContactView, self).form_valid(form)


class Sections(generic.ListView):
    template_name = 'academics/section_list.html'
    context_object_name = 'section_list'

    def get_queryset(self):
        return Section.objects.order_by(
            '-session__term',
            'session__course__subject__name',
            'session__course__number',
            'number'
        )

class DetailView(generic.DetailView):
    model = Section
    template_name = 'academics/section_detail.html'






class SectionPreferenceClassView(UpdateView):
    template_name = 'academics/section_preference_form.html'
    context_object_name = 'pref'
    model = SectionPreference
    fields = ['preference']


def SectionPreferenceFunctionView(request, pk):
    if request.method == 'POST':
        print 'nothin doin', pk
    else:
        print 'pk=', pk
        form = SectionPreferenceForm()
        pref = {'form':form, 'pk':pk}

    return render(request, 'academics/section_preference_form.html', pref)


def SectionPreferencesView(request, termNumber):
    print request.user.last_name
    sectionPreferences = SectionPreference.objects.filter(
        section__session__term__number=termNumber,
        instructor__pk=request.user.pk,
    )
    context = {'sectionPreferences': sectionPreferences}
    return render(request, 'academics/sectionPreferences.html', context)
from django.shortcuts import render
from django.db.models import Q
from django.views import generic
from django.forms import modelformset_factory, formset_factory, TextInput
from django.http import HttpResponseRedirect
from .models import *
from .forms import LandingForm, SectionPreferenceForm, ReasonPreferenceForm, CollegeTTSFRForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

from django.http import HttpResponse

def isInstructor(user):
    return user.has_perm('section_view')

def index(request):
    env = request.environ
    print request.user
    print request.user.username
    context = {'user':request.user, #env['USER'],
               #'shell':env['SHELL'],
               'username':request.user.username,
               'displayName': request.user.first_name + request.user.last_name
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

@login_required
#@permission_required('Academics.view_section')
def SectionPreferencesView(request, termNumber):
    print request.user.last_name
    queryset = SectionPreference.objects.filter(
        section__session__term__number=termNumber,
        instructor__pk=request.user.pk,
    ).order_by('section__session__course__subject',
               'section__session__course__number',
               'section__number')
    sectionsAsStudent = set(SectionStudent.objects.filter(student=request.user))
    sectionsAsInstructor = set(Section.objects.filter(instructor=request.user))
    print sectionsAsStudent.union(sectionsAsInstructor)
    comments = []
    for pref in queryset:
        conflicts = set(list(pref.section.conflicts.all()))
        print conflicts
        conflictedSections = conflicts.intersection(sectionsAsStudent.union(sectionsAsInstructor))
        print conflictedSections
        if conflictedSections:
            comment = 'Conflicts with {0}'.format(', '.join(conflictedSections))
            pref.preference = 0
            pref.save()
        else:
            comment = ''
        comments.append(comment)

    SectionPreferenceFormSet = modelformset_factory(SectionPreference,
                                                    form=SectionPreferenceForm, extra=0,
                                                    )
    formset = SectionPreferenceFormSet(queryset=queryset)
    for form, comment in zip(formset, comments):
        print comment
        if comment:
            form.fields['preference'].widget.attrs['disabled']=True
    context = {'formset': formset, 'zip':zip(formset.queryset, formset, comments), 'request':request}
    return render(request, 'academics/sectionPreferences.html', context)


@login_required
def WithdrawalPreferencesView(request, collegeName):
    try:
        withdrawalReasons = WithdrawalReason.objects.filter(withdrawalPreferences__college__name=collegeName)
    except:
        print 'Failed to get withdrawal reasons object'
    queryset = withdrawalReasons.order_by('rank')
    ReasonFormSet = modelformset_factory(Reason, form=ReasonPreferenceForm, extra=0)
    formset = ReasonFormSet(queryset=queryset)
    context = {'formset': formset, 'zip':zip(formset.queryset, formset),'request':request}
    return render(request, 'academics/reasonPreferences.html', context)

@login_required
def CollegeTTSFRView(request):
    departments = None
    TTSFRs = None
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CollegeTTSFRForm(request.POST)
        print request.POST['college']
        print request.POST['term']
        departments = Department.objects.filter(college__name=request.POST['college']).order_by(
            'name'
        )
        TTSFRs = {}
        for department in departments:
            TTSFRs[department]=department.TTSFR(request.POST['term'])
            print TTSFRs[department]
        info = zip(departments, TTSFRs)
        # check whether it's valid:
        if form.is_valid():
            print 'Form is valid'
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/PA/TTSFR/{0}/{1}'.format(college, ))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CollegeTTSFRForm()

    return render(request, 'academics/collegeTTSFR.html', {'form': form,
                                                           'departments': departments,
                                                           'TTSFRs':TTSFRs,
                                                           }
                  )







    # CollegeTTSFRFormSet = formset_factory(CollegeTTSFRForm)
    # formset = CollegeTTSFRFormSet(queryset=departments)
    #
    # departments = college.department_set.all()
    # schools = college.school_set.all()
    # programs = college.program_set.all()
    # qhost = Q(session__course__subject__host__in=departments) | \
    #         Q(session__course__subject__host__in=schools) | \
    #         Q(session__course__subject__host__in=programs)
    # sections = Section.objects.filter(
    #     qhost,
    #     session__term__number=termNumber,
    # ).order_by('session__course__subject',
    #            'session__course__number',
    #            'number')
    #
    # context = {'college':college,
    #            'departments':departments,
    #            'schools':schools,
    #            'programs':programs,
    #            'sections':sections,
    # }
    # return render(request, 'academics/collegeTTSFR.html', context)
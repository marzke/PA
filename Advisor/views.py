from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from Academics.models import *

def start(request):
    return render(request, 'advisor.html')

def student_grades_json(request):
    data = serializers.serialize("json",
        StudentGrade.objects.filter(student__uid='910731710'),
        fields=('course','grade'),
        use_natural_foreign_keys=True, use_natural_primary_keys=True
    )
    return HttpResponse(content=data, content_type='application/json')

def courses_json(request):
#    return JsonResponse(Course.objects.all()[0], safe=False)
    data = serializers.serialize("json",
        Course.objects.all().order_by('subject','number'),
        fields=('subject','number','title'),
        use_natural_foreign_keys=True, use_natural_primary_keys=True
    )
    return HttpResponse(content=data, content_type='application/json')
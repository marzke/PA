from django.db import models
from django.core.exceptions import ValidationError

import People.models as people

import re
from datetime import time


class Days(frozenset):

    orderedList = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    validSet = frozenset(orderedList)

    def __new__(cls, aString):
        if isinstance(aString, basestring):
            newSet = frozenset(re.findall('[A-Z][a-z]', aString))
            if newSet.issubset(Days.validSet):
                return frozenset.__new__(cls, newSet)

    def stringify(self):
        listDays = list(self)
        return ''.join(sorted(listDays, 
                              key=lambda day: self.orderedList.index(day)))

    def __str__(self):
        listDays = list(self)
        return ''.join(sorted(listDays,
                              key=lambda day: self.orderedList.index(day)))


class DaysField(models.Field):

    description = "Days of the week treated as a mathematical set."

    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        super(DaysField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(DaysField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def to_python(self, value):
        if isinstance(value, Days):
            return value
        newInstance = Days(value)
        if newInstance is None:
            raise ValidationError("Invalid input for a Days instance")
        return newInstance

    def get_prep_value(self, aDaysInstance):
        if isinstance(aDaysInstance, basestring): return aDaysInstance
        return aDaysInstance.stringify() 

    def db_type(self, connection):
        return 'VARCHAR'
            

class Event(models.Model):

    description = models.CharField(max_length=60, blank=True)
    days = DaysField(blank=False, null=False, default='MoTuWeThFrSaSu')
    start = models.TimeField()
    end = models.TimeField()
    attendees = models.ManyToManyField(people.Person, blank=True, null=True,
                                       related_name='attendeeFor')
    available = models.ManyToManyField(people.Person, blank=True, null=True,
                                       related_name='availableFor')
    coordinator = models.ForeignKey(people.Person, blank=True, null=True,
                                    related_name='coordinatorFor')

    def clean(self):
       if self.start > self.end:
           raise ValidationError("Event ends before it starts.") 

    def conflictsWith(self, other):
        return not ((not (bool(self.days.intersection(other.days)))
                or (self.end < other.start)
                or (self.start > other.end)))

    def __unicode__(self):
        s = "{0}:   {1}   ".format(self.description, self.days)
        s += "{0}-{1}".format(self.start, self.end) 
        return s



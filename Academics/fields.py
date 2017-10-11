from django.db import models
from django.utils.deconstruct import deconstructible

@deconstructible
class Grade(object):

    validGrades = {'A': (4.0, 11),
                        'A-': (3.7, 10),
                        'B+': (3.3, 9),
                        'B': (3.0, 8),
                        'B-': (2.7, 7),
                        'C+': (2.3, 6),
                        'C': (2.0, 5),
                        'C-': (1.7, 4),
                        'D+': (1.3, 3),
                        'D': (1.0, 2),
                        'D-': (0.7, 1),
                        'F': (0.0, 0),
                        'WU': (0.0, 0),
                        'W': (None, 0),
                        'WM': (None, 0),
                        'CR': (None, 0),
                        'NC': (None, 0),
                        'I': (None, 0),
                        'IC': (0.0, 0),
                        'IP': (None, 0),
                        'Conc': (None, 0),
                        'RP': (None, 0),
                        'RD': (None, 0),
                        '': (None, 0),
                        'AU': (None, 0),
                        'AUD': (None, 0),
                        }

    def __init__(self, value):

        try:
            if value is None: value = ''
            self.gradePoint = self.validGrades[value][0]
            self.gradeRank = self.validGrades[value][1]
            self.letterGrade = value
        except:
            raise ValueError('Grade not valid')

    def __unicode__(self):
        return self.letterGrade

    def __lt__(self, other):
        if hasattr(other, 'gradePoint'):
            return self.gradePoint < other.gradePoint
    def __le__(self, other):
        if hasattr(other, 'gradePoint'):
            return self.gradePoint <= other.gradePoint
    def __gt__(self, other):
        if hasattr(other, 'gradePoint'):
            return self.gradePoint > other.gradePoint
    def __ge__(self, other):
        if hasattr(other, 'gradePoint'):
            return self.gradePoint >= other.gradePoint
    def __eq__(self, other):
        if hasattr(other, 'gradePoint'):
            return self.gradePoint == other.gradePoint
    def __ne__(self, other):
        if hasattr(other, 'gradePoint'):
            return self.gradePoint != other.gradePoint


class GradeField(models.Field):

    description = "Grade fields for grade objects with rich comparisons"
#    __metaclass__ = models.SubfieldBase; DEPRECATED IN v1.8

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 4
        super(GradeField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return "varchar(4)" #% self.max_length

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if isinstance(value, Grade):
            return value
        else:
            return Grade(value)

    def get_prep_value(self, value):
        print type(value)
        print "value = ", value
        if isinstance(value, Grade):
            print 'in get prep value'
            return value.letterGrade
        else:
            return ''

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
from __future__ import absolute_import
import rules

@rules.predicate
def is_department_chair(user, department):
    try:
        return user == department.chair
    except:
        return False

@rules.predicate
def is_program_director(user, program):
    try:
        return user == program.director
    except:
        return False

@rules.predicate
def is_school_director(user, school):
    try:
        return user == school.director
    except:
        return False

is_head_of_acad_org = is_department_chair | is_program_director | is_school_director

@rules.predicate
def is_instructor_of_section(user, section):
    return user == section.instructor

@rules.predicate
def is_head_of_section_acad_org(user, section):
    return is_head_of_acad_org(user, section.session.course.subject.host)

rules.add_perm('Academics.can_view_section_roster',
               is_instructor_of_section | is_head_of_section_acad_org
               )
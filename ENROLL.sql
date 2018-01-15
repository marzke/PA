create table ENROLL as
select to_number(concat(e.STRM, e.CLASS_NBR)) as id, e.status, e.enrolled_status,
		m.strm, m.class_nbr, m.subject, m.catalog_nbr, m.session_code, m.class_section, 
		m.emplid, m.first_name, m.last_name, m.email_addr, m.acad_plan, m.descr, m.acad_level_bot,
		m.class_level, m.PERMISSION_NBR_USED, m.APR, m.GRADING_BASIS_ENRL, m.CRSE_GRADE_OFF

from CMSCOMMON.SFO_CR_ENROLL_MV e
join CMSCOMMON.SFO_CR_MAIN_MV m
on e.emplid=m.emplid and e.strm=m.strm and e.class_nbr=m.class_nbr
and to_number(m.strm)>=2173 and (m.subject='PHYS' or m.subject='ASTR')
join AASCIEPT.SECTION s
on s.STRM=e.strm and s.CLASS_NBR=e.class_nbr
order by e.subject, e.catalog_nbr, e.class_section

CREATE VIEW AASCIEPT.ENROLL_VW AS select to_number(concat(e.STRM, e.CLASS_NBR)) as id, e.status, e.enrolled_status,
		m.strm, m.class_nbr, m.subject, m.catalog_nbr, m.session_code, m.class_section, 
		m.emplid, m.first_name, m.last_name, m.email_addr, m.acad_plan, m.descr, m.acad_level_bot,
		m.class_level, m.PERMISSION_NBR_USED, m.APR, m.GRADING_BASIS_ENRL, m.CRSE_GRADE_OFF

from CMSCOMMON.SFO_CR_ENROLL_VW e
join CMSCOMMON.SFO_CR_MAIN_VW m
on e.emplid=m.emplid and e.strm=m.strm and e.class_nbr=m.class_nbr and e.strm='2183' and e.subject='PHYS'
and m.strm='2183' and m.subject='PHYS'

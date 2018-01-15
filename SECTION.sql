create table SECTION as
select to_number(concat(t.STRM, t.CLASS_NBR)) as id,
		t.strm, t.class_nbr, t.CRSE_ID, t.subject, t.catalog_nbr, t.CLASS_SECTION, t.descr, t.SESSION_CODE,
		i.units_acad_prog, i.SSR_COMPONENT, i.meeting_days, i.start_time, i.end_time, i.start_date, i.end_date,
		i.bldg_cd, i.room, i.enrl_cap, i.wait_cap, i.emplid, i.first_name, i.last_name, i.email_addr,
		t.enrl_tot, t.WAIT_TOT, t.enrl_stat, t.class_stat, t.class_type, t.associated_class, t.schedule_print,
		t.acad_org, t.acad_career, t.ACAD_GROUP, t.institution, t.campus, t.campus_event_nbr, t.combined_section
from CMSCOMMON.SFO_CLASS_TBL t
join (select * from CMSCOMMON.SFO_CR_IOC_MV union select * from CMSCOMMON.SFO_CR_IOC_NO_MV) i
on i.strm=t.strm and i.CLASS_NBR=t.CLASS_NBR
and t.class_type = 'E'
where to_number(t.strm)>=2173 and t.acad_org like '572%'
order by subject, catalog_nbr, class_section

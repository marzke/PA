create table EMPLOYEE as
select j.emplid, min(p.first_name) as first_name, min(p.last_name) as last_name, min(e.email_addr) as email_addr,
listagg(j.jobcode, ' | ') within group (order by j.jobcode) as job_code, 
listagg(j.DESCR, ' | ') within group (order by j.jobcode) as job_description, 
listagg(j.descrshort, ' | ') within group (order by j.jobcode) as job_abbr, 
listagg(j.JOB_FUNCTION, ' | ') within group (order by j.jobcode) as job_function, 
listagg(j.JOB_DESCR, ' | ') within group (order by j.jobcode) as job_title, 
listagg(j.GRADE, ' | ') within group (order by j.jobcode) as job_grade
from CMSCOMMON.SFO_INSTR_JOBTYPE_INFO_MV j
join CMSCOMMON.SFO_EF_PERSON_NAME_MV p
on p.emplid=j.emplid
join CMSCOMMON.SFO_EMAILADR_MV e
on e.emplid=p.emplid and e.addr_type='OCMP'
where (j.DEPTID like '3610' or j.DEPTID like '3611') and j.descrshort not like 'IF 12'
group by j.emplid
order by last_name, first_name

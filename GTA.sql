create table GTA as
select c.emplid, min(p.first_name) as first_name, min(p.last_name) as last_name, min(e.email_addr) as email_addr,
max(c.strm) keep (dense_rank last order by c.STRM) "STRM",
min(c.cum_gpa) keep (dense_rank last order by c.STRM) "CUM_GPA"
from CMSCOMMON.SFO_INSTR_JOBTYPE_INFO_MV j
join CMSCOMMON.SFO_EF_PERSON_NAME_MV p
on p.emplid=j.emplid
join CMSCOMMON.SFO_EMAILADR_MV e
on e.emplid=p.emplid and e.addr_type='OCMP'
join cmscommon.sfo_stdnt_car_term c
on c.emplid=j.emplid and c.ACAD_CAREER like 'PBAC'
where (j.DEPTID like '3610' or j.DEPTID like '3611') and JOB_FUNCTION like 'TA'
group by c.emplid
order by last_name, first_name

create table DEGREE_STUDENT as
select concat(EMPLID, ACAD_PLAN) as id,
emplid, acad_career, stdnt_car_nbr, effdt, effseq, acad_plan, declare_dt, plan_sequence,
req_term, completion_term, stdnt_degr, degr_chkout_stat
from cmscommon.sfo_acad_plan
where acad_plan like 'PHYS%'



create table AASCIEPT.HR as
select e.emplid, g.subject, g.catalog_nbr, g.crse_grade_off

from

(select distinct emplid from CMSCOMMON.SFO_CR_ENROLL_MV
where (SUBJECT='PHYS' or SUBJECT='ASTR') and enrolled_status!='DROPPED' and strm='2183') e

join

(
(select emplid, subject, catalog_nbr, crse_grade_off from CMSCOMMON.SFO_CR_MAIN_MV
where (subject='PHYS' or SUBJECT='ASTR') and regexp_like(crse_grade_off, '\S'))

union

(select emplid, subject, catalog_nbr, crse_grade_off from CMSCOMMON.SFO_CR_PREV_GRADE_TRNF_MV
where (SUBJECT='PHYS' or SUBJECT='ASTR') and regexp_like(crse_grade_off, '\S'))
) g


on g.emplid=e.emplid
order by emplid


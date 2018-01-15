create table DEGREE as
select acad_plan, acad_org,
min(effdt) KEEP (DENSE_RANK FIRST ORDER BY effdt) "DATE_CREATED",
max(effdt) KEEP (DENSE_RANK LAST ORDER BY effdt) "LAST_MODIFIED",
min(percent_owned) KEEP (DENSE_RANK LAST ORDER BY effdt) "PERCENT_OWNED"
from cmscommon.SFO_ACAD_PLAN_OWNER
group by ACAD_PLAN, acad_org

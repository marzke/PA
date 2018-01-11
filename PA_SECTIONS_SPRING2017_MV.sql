select to_number(concat(STRM, CLASS_NBR)) as id, t.*
from
(
(select * from CMSCOMMON.SFO_CR_IOC_VW
where STRM like '2177' and (SUBJECT like 'PHYS' or SUBJECT like 'ASTR') and SSR_COMPONENT not like 'SUP')

union

(select * from CMSCOMMON.SFO_CR_IOC_NO_VW
where STRM like '2177' and (SUBJECT like 'PHYS' or SUBJECT like 'ASTR') and SSR_COMPONENT not like 'SUP')
) t
order by STRM, subject, CATALOG_NBR,class_section,ssr_component
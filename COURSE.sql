select o.subject, o.catalog_nbr, 
			min(o.crse_id) keep (dense_rank last order by o.effdt) CRSE_ID,
			min(c.descr) keep (dense_rank last order by o.effdt) DESCR,
			min(c.descrlong) keep (dense_rank last order by o.effdt) DESCRLONG		
from cmscommon.sfo_crse_catalog c
join cmscommon.sfo_crse_offer o
on o.CRSE_ID=c.crse_id and o.effdt=c.effdt
/*where o.acad_org like '572%'*/
group by o.subject, o.catalog_nbr
order by o.subject, o.catalog_nbr

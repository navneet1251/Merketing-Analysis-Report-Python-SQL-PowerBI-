select * from customer_journey;

--cte to identify and tag duplicate records 
with duplicateRecords as (
	select 
	*,
	ROW_NUMBER() over(partition by CustomerID, ProductID, VisitDate, Stage, Action order by JourneyID) as row_no
	from dbo.customer_journey
) 
-- Find duplicate records from cte
select * 
from duplicateRecords 
where row_no >1
order by JourneyID;


--

select JourneyID, CustomerID, ProductID, VisitDate,Stage, Action,
coalesce(Duration, avg_duration) as Duration
from (
Select JourneyID, CustomerID, ProductID, VisitDate, UPPER(Stage) as Stage, Action, Duration, 
Avg(Duration) over (partition by VisitDate) as avg_duration ,
ROW_NUMBER() over(partition by CustomerID, ProductID, VisitDate, Stage, Action order by JourneyID) as row_num
from dbo.customer_journey
) as subQuery
where row_num =1
order by JourneyID;

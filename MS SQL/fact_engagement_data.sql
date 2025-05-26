select * from dbo.engagement_data;

-- Query to clean and normalize the engaement_date table

select 
EngagementID,
ContentID,
CampaignID,
ProductID,
upper(replace(ContentType, 'Socialmedia','Social Media')) as ContentType,
left(ViewsClicksCombined, CHARINDEX('-',ViewsClicksCombined)-1) as Views,
Right(ViewsClicksCombined, len(ViewsClicksCombined) - CHARINDEX('-', ViewsClicksCombined)) as Clicks,
Likes,
FORMAT(convert(Date,EngagementDate),'dd.MM.yyy') as EngagementDate
from dbo.engagement_data
where ContentType != 'Newsletter';
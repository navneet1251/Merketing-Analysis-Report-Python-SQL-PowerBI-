select * from dbo.customers;

select * from dbo.geography;



-- sql query to find the relation btween them 

select 
c.CustomerID, c.CustomerName, c.Email, c.Age, c.Gender,g.City, g.Country
from dbo.customers c 
left join 
dbo.geography g on g.GeographyID= c.GeographyID;





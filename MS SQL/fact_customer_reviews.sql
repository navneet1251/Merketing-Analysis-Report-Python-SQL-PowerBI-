select * from customer_reviews;

-- Query to remove wide spaces from  the review text

select 
ReviewID,
CustomerID,
ProductID,
ReviewDate,
Rating,
REPLACE(ReviewText, '  ',' ') as ReviewText
from dbo.customer_reviews;
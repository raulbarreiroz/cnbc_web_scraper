--SELECT COUNT(*) FROM stock;
-- distinct types of stocks in table
--SELECT symbol FROM stock GROUP BY symbol;
-- Query all data for a single stock
-- SELECT * FROM stock WHERE symbol = 'AAPL';
-- Rows with price between 40 and 50
--SELECT * FROM stock WHERE price BETWEEN 40 and 50;
-- sort table by price
--SELECT price FROM stock GROUP BY price ORDER BY price;
-- explore using aggregate functions by symbol
/*
SELECT symbol,
min(price) min_price,
max(price) max_price,
avg(price) avg_price,
CASE WHEN
round(AVG(price),2) = round(min(price), 2)
AND
round(AVG(price), 2) = round(MAX(price), 2)
THEN 'NO'
ELSE 'YES'
END price_change
FROM stock
GROUP BY symbol
ORDER BY symbol;
*/
-- explore using aggregate functions by year and month
/*
select strftime('%m', datetime) month,
strftime('%Y', datetime) year,
min(price) min_price,
max(price) max_price,
avg(price) avg_price
from stock
group by strftime('%m', datetime),
strftime('%Y', datetime)
order by strftime('%m', datetime),
strftime('%Y', datetime);
*/
-- explore using aggregate functions by year and month and day and hour
-- for this dataset, time doesn't affect price
/*
select strftime('%m', datetime) month,
strftime('%Y', datetime) year,
strftime('%d', datetime) day,
strftime('%H', datetime) hour,
min(price) min_price,
max(price) max_price,
avg(price) avg_price
from stock
group by strftime('%m', datetime),
strftime('%Y', datetime),
strftime('%d', datetime),
strftime('%H', datetime)
order by strftime('%m', datetime),
strftime('%Y', datetime),
strftime('%d', datetime),
strftime('%H', datetime);
*/
-- 196.861333333333
--Which of the rows have a price greater than the average of all prices in the dataset?
/*
select s1.symbol,
avg(s1.price)
from stock s1
cross JOIN ( select avg(price) avg_price from stock ) s2
group by   s1.symbol
HAVING avg(s1.price) > s2.avg_price
*/
/*
In addition to the built-in aggregate functions,
explore ways to calculate other key statistics about the data,
such as the median or variance.
*/
select s1.symbol,
avg(s1.price) avg_price,
s2.avg_price avg_table_price,
s2.sum_price sum_table_price,
s2.median_price median_table_price,
sum(
(s1.price - s2.median_price) * (s1.price - s2.median_price))
/
s2.count_price variance_price
from stock s1
cross JOIN (
select avg(price) avg_price,
sum(price) sum_price,
sum(price) / count(price) median_price,
count(price) count_price
from stock
) s2
group by   s1.symbol
HAVING avg(s1.price) > s2.avg_price
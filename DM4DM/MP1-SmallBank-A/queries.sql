-- Comm3220 (DM4DM), McIntire School of Commerce, UVA
-- MP1: SmallBank (A) -- single-table SQL        Due: Thu 09/03
-- Server: SQL Server (T-SQL), database SmallBankDB
-- Tables used: CUSTOMER (c_id, f_name, l_name, city, state)
--              LOAN (l_id, principal, rate, date_due, purpose, lo_id)
-- Note: see ../README.md "Things to verify" (rate scale, GETDATE()).

-- Q1. Customers in Dallas, alphabetized
SELECT *
FROM CUSTOMER
WHERE city = 'Dallas'
ORDER BY l_name ASC, f_name ASC;

-- Q2. All loans above $200K, largest principal first
SELECT *
FROM LOAN
WHERE principal > 200000
ORDER BY principal DESC;

-- Q3. How many loans are below $75K?
SELECT COUNT(*) AS 'Loans Below $75K'
FROM LOAN
WHERE principal < 75000;

-- Q4. The ten smallest loans
SELECT TOP 10
    l_id AS 'Loan ID',
    rate AS 'Interest Rate',
    principal AS 'Principal'
FROM LOAN
ORDER BY principal ASC;

-- Q5. Total exposure on non-expired loans as of today
SELECT SUM(principal) AS 'Total Exposure'
FROM LOAN
WHERE date_due >= GETDATE();

-- Q6. Average loan size at the 5% rate
SELECT AVG(principal) AS 'Average Loan at 5%'
FROM LOAN
WHERE rate = 5;  -- first draft used 0.05; check how rate is stored

-- Q7. Customer ID and address for N. Grover (full first name unknown)
SELECT c_id AS 'Customer ID',
       f_name AS 'First Name',
       l_name AS 'Last Name',
       city AS 'City',
       state AS 'State'
FROM CUSTOMER
WHERE f_name LIKE 'N%' AND l_name = 'Grover';

-- Q8. Customers in each city
SELECT city AS 'City',
       state AS 'State',
       COUNT(*) AS 'Number of Customers'
FROM CUSTOMER
GROUP BY city, state
ORDER BY COUNT(*) DESC;

-- Q9. Average loan size by rate
SELECT rate AS 'Interest Rate',
       AVG(principal) AS 'Average Loan Size'
FROM LOAN
GROUP BY rate
ORDER BY rate DESC;

-- Q10. Do we have a customer with the initials NM?
SELECT *
FROM CUSTOMER
WHERE f_name LIKE 'N%' AND l_name LIKE 'M%';

-- Q11. How many customers are last-named Echevarria?
SELECT COUNT(*) AS 'Echevarria Customers'
FROM CUSTOMER
WHERE l_name = 'Echevarria';

-- Q12. Average rate and principal by year of maturity
SELECT YEAR(date_due) AS 'Maturity Year',
       AVG(rate) AS 'Average Rate',
       AVG(principal) AS 'Average Principal'
FROM LOAN
GROUP BY YEAR(date_due)
ORDER BY YEAR(date_due) ASC;

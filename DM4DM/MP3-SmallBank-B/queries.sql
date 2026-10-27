-- Comm3220 (DM4DM), McIntire School of Commerce, UVA
-- MP3: SmallBank (B) -- joins, HAVING, TOP PERCENT, COUNT DISTINCT    Due: Thu 09/17
-- Server: SQL Server (T-SQL), database SmallBankDB
-- Tables: CUSTOMER, LOAN, LOAN_OFFICER, CUSTOMER_IN_LOAN (association), INSURANCE_PLAN
-- Q7, Q9, Q10, Q11 are RECONSTRUCTED from notes, not copied from the submission.
-- Q11's original question wording could not be recovered. Verify before use.

-- Q1. Customers with loans, their city, their loan officer and the officer's phone
SELECT DISTINCT
    c.c_id AS 'Customer ID',
    c.f_name AS 'Customer First Name',
    c.l_name AS 'Customer Last Name',
    c.city AS 'City',
    c.state AS 'State',
    lo.lo_id AS 'Loan Officer ID',
    lo.f_name AS 'Officer First Name',
    lo.l_name AS 'Officer Last Name',
    lo.phone AS 'Officer Phone'
FROM customer c
    JOIN customer_in_loan cil ON c.c_id = cil.c_id
    JOIN loan l ON cil.l_id = l.l_id
    JOIN loan_officer lo ON l.lo_id = lo.lo_id
ORDER BY c.city, c.l_name, c.f_name;

-- Q2. Carl Dyer's clients (lo_id = 8), alphabetized
SELECT DISTINCT
    c.c_id AS 'Customer ID',
    c.f_name AS 'First Name',
    c.l_name AS 'Last Name'
FROM customer c
    JOIN customer_in_loan cil ON c.c_id = cil.c_id
    JOIN loan l ON cil.l_id = l.l_id
WHERE l.lo_id = 8
ORDER BY c.l_name, c.f_name;

-- Q3. Loan officer managing the least money on loans not yet past due
SELECT TOP 1
    lo.lo_id AS 'Loan Officer ID',
    lo.f_name AS 'First Name',
    lo.l_name AS 'Last Name',
    FORMAT(SUM(l.principal), 'C0') AS 'Total Managed'
FROM loan_officer lo
    JOIN loan l ON lo.lo_id = l.lo_id
WHERE l.date_due > CAST(GETDATE() AS DATE)
GROUP BY lo.lo_id, lo.f_name, lo.l_name
ORDER BY SUM(l.principal) ASC;

-- Q4. All customers with their insurance information (LEFT JOIN keeps uninsured)
SELECT
    c.c_id AS 'Customer ID',
    c.f_name AS 'First Name',
    c.l_name AS 'Last Name',
    ISNULL(FORMAT(ip.coverage, 'C0'), '-') AS 'Coverage',
    ISNULL(FORMAT(ip.premium, 'C0'), '-') AS 'Premium'
FROM customer c
    LEFT JOIN insurance_plan ip ON c.c_id = ip.c_id
ORDER BY c.l_name, c.f_name;

-- Q5. Loan officers whose average rate is below 13%
SELECT
    lo.lo_id AS 'Loan Officer ID',
    lo.f_name AS 'First Name',
    lo.l_name AS 'Last Name',
    FORMAT(AVG(l.rate), '0.000') AS 'Average Rate'
FROM loan_officer lo
    JOIN loan l ON lo.lo_id = l.lo_id
GROUP BY lo.lo_id, lo.f_name, lo.l_name
HAVING AVG(l.rate) < 13  -- first draft used 0.13; check how rate is stored
ORDER BY AVG(l.rate) ASC;

-- Q6. Top-quartile borrowers by total borrowed
SELECT TOP 25 PERCENT
    c.c_id AS 'Customer ID',
    c.f_name AS 'First Name',
    c.l_name AS 'Last Name',
    FORMAT(SUM(l.principal), 'C0') AS 'Total Borrowed'
FROM customer c
    JOIN customer_in_loan cil ON c.c_id = cil.c_id
    JOIN loan l ON cil.l_id = l.l_id
GROUP BY c.c_id, c.f_name, c.l_name
ORDER BY SUM(l.principal) DESC;

-- Q7. Richmond customer who borrowed the most (RECONSTRUCTED)
SELECT TOP 1
    c.c_id AS 'Customer ID',
    c.f_name AS 'First Name',
    c.l_name AS 'Last Name',
    FORMAT(SUM(l.principal), 'C0') AS 'Total Borrowed'
FROM customer c
    JOIN customer_in_loan cil ON c.c_id = cil.c_id
    JOIN loan l ON cil.l_id = l.l_id
WHERE c.city = 'Richmond'
GROUP BY c.c_id, c.f_name, c.l_name
ORDER BY SUM(l.principal) DESC;

-- Q8. How many clients does Carl Dyer have?
SELECT COUNT(DISTINCT cil.c_id) AS 'Number of Clients'
FROM customer_in_loan cil
    JOIN loan l ON cil.l_id = l.l_id
WHERE l.lo_id = 8;

-- Q9. Insurance exposure (total coverage) by city (RECONSTRUCTED)
SELECT
    c.city AS 'City',
    c.state AS 'State',
    FORMAT(ISNULL(SUM(ip.coverage), 0), 'C0') AS 'Insurance Exposure'
FROM customer c
    LEFT JOIN insurance_plan ip ON c.c_id = ip.c_id
GROUP BY c.city, c.state
ORDER BY c.city, c.state;

-- Q10. How many Charlottesville customers have no insurance? (RECONSTRUCTED)
SELECT COUNT(DISTINCT c.c_id) AS 'Uninsured Charlottesville Customers'
FROM customer c
    LEFT JOIN insurance_plan ip ON c.c_id = ip.c_id
WHERE c.city = 'Charlottesville'
  AND ip.c_id IS NULL;

-- Q11. Insured customers per loan officer (RECONSTRUCTED, wording uncertain)
SELECT
    lo.lo_id AS 'Loan Officer ID',
    lo.f_name AS 'First Name',
    lo.l_name AS 'Last Name',
    COUNT(DISTINCT ip.c_id) AS 'Insured Customers'
FROM loan_officer lo
    JOIN loan l ON lo.lo_id = l.lo_id
    JOIN customer_in_loan cil ON l.l_id = cil.l_id
    LEFT JOIN insurance_plan ip ON cil.c_id = ip.c_id
GROUP BY lo.lo_id, lo.f_name, lo.l_name
ORDER BY COUNT(DISTINCT ip.c_id) DESC;

-- Q12. Loan officers with Charlottesville customers, by amount managed
SELECT
    lo.lo_id AS 'Loan Officer ID',
    lo.f_name AS 'First Name',
    lo.l_name AS 'Last Name',
    FORMAT(SUM(l.principal), 'C0') AS 'Amount Managed in Charlottesville'
FROM customer c
    JOIN customer_in_loan cil ON c.c_id = cil.c_id
    JOIN loan l ON cil.l_id = l.l_id
    JOIN loan_officer lo ON l.lo_id = lo.lo_id
WHERE c.city = 'Charlottesville'
GROUP BY lo.lo_id, lo.f_name, lo.l_name
ORDER BY SUM(l.principal) DESC;

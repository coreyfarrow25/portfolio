"""Build MP1 and MP3 notebooks (VS Code SQL notebook format, same as MP6 Farrow.ipynb)."""
import json, sys, os

OUT = sys.argv[1]

def nb(cells):
    out = []
    for kind, text in cells:
        src = text.strip("\n").splitlines(keepends=True)
        if kind == "md":
            out.append({"cell_type": "markdown", "metadata": {}, "source": src})
        else:
            out.append({"cell_type": "code", "metadata": {"language": "sql"},
                        "execution_count": None, "outputs": [], "source": src})
    return {"cells": out, "metadata": {"language_info": {"name": "sql"}},
            "nbformat": 4, "nbformat_minor": 2}

# ---------------------------------------------------------------- MP1
mp1 = [
("md", """
# MP1 - SmallBank (A)
**Corey Farrow** · SQL & Data Modeling portfolio

Database `SmallBankDB` (T-SQL).

Formatting rules from the assignment: money with `$`, commas and no decimals (`FORMAT(x,'C0')`); integers with commas (`'N0'`); interest rates with three decimals (`'N3'`). `FORMAT` returns text, so every `ORDER BY` sorts on the original numeric column.
"""),
("md", "**Q1.** Produce an alphabetized list of our customers who live in Dallas. Sort by last name, then first name."),
("sql", """
-- No columns specified, so show them all.
SELECT *
FROM CUSTOMER
WHERE city = 'Dallas'
ORDER BY l_name, f_name;
"""),
("md", "**Q2.** Show all the loans above $200K, print out all the info we have on them from that table. Order by principal, descending."),
("sql", """
-- "All the info ... from that table" overrides the formatting bullet, so SELECT *.
SELECT *
FROM LOAN
WHERE principal > 200000
ORDER BY principal DESC;
"""),
("md", "**Q3.** How many loans below $75K do we have in the DB?"),
("sql", """
SELECT FORMAT(COUNT(*), 'N0') AS 'Loans Below $75K'
FROM LOAN
WHERE principal < 75000;
"""),
("md", "**Q4.** Show id, rate, and principal for our ten smallest loans. Smallest on top. Tip: check the results!"),
("sql", """
-- "Check the results": rows with a missing principal would sort first in ascending
-- order and are not real loans, so exclude them.
SELECT TOP 10
    l_id                      AS 'Loan ID',
    FORMAT(rate, 'N3')        AS 'Interest Rate (%)',
    FORMAT(principal, 'C0')   AS 'Principal'
FROM LOAN
WHERE principal IS NOT NULL
ORDER BY principal ASC;
"""),
("md", "**Q5.** What is our total exposure for non-expired loans as of today? (exposure = sum of borrowed principals; today = date in which we run the query)."),
("sql", """
-- GETDATE() returns the date the query runs; a loan is not expired if it is due today or later.
SELECT FORMAT(SUM(principal), 'C0') AS 'Total Exposure (Non-Expired Loans)'
FROM LOAN
WHERE date_due >= CAST(GETDATE() AS DATE);
"""),
("md", "**Q6.** What is the average loan size at the 5% rate?"),
("sql", """
-- Rates are stored as percent numbers (the handout filters on 7.5 and 8.5), so 5% = 5.
SELECT FORMAT(AVG(principal), 'C0') AS 'Average Loan Size at 5%'
FROM LOAN
WHERE rate = 5;
"""),
("md", "**Q7.** Show customer ID and address for N. Grover. Do not assume you know the full first name."),
("sql", """
-- Match only the first initial. CUSTOMER stores city and state as the address.
SELECT
    c_id    AS 'Customer ID',
    f_name  AS 'First Name',
    l_name  AS 'Last Name',
    city    AS 'City',
    state   AS 'State'
FROM CUSTOMER
WHERE f_name LIKE 'N%'
  AND l_name = 'Grover';
"""),
("md", "**Q8.** How many customers do we have in each city?"),
("sql", """
-- Group on city AND state so same-named cities in different states stay separate.
SELECT
    city                    AS 'City',
    state                   AS 'State',
    FORMAT(COUNT(*), 'N0')  AS 'Number of Customers'
FROM CUSTOMER
GROUP BY city, state
ORDER BY COUNT(*) DESC, city;
"""),
("md", "**Q9.** What is the average loan size by rate? Order by rate, descending. Tip: check the results!"),
("sql", """
-- "Check the results": a NULL rate would appear as its own group, so leave it out.
SELECT
    FORMAT(rate, 'N3')            AS 'Interest Rate (%)',
    FORMAT(AVG(principal), 'C0')  AS 'Average Loan Size'
FROM LOAN
WHERE rate IS NOT NULL
GROUP BY rate
ORDER BY rate DESC;
"""),
("md", "**Q10.** Do we have a customer who has the initials NM? (print out all the info we have in the customer table on them)"),
("sql", """
SELECT *
FROM CUSTOMER
WHERE f_name LIKE 'N%'
  AND l_name LIKE 'M%';
"""),
("md", "**Q11.** How many customers last-named \"Echevarria\" do we have?"),
("sql", """
-- Exact match, so = rather than LIKE.
SELECT FORMAT(COUNT(*), 'N0') AS 'Customers Named Echevarria'
FROM CUSTOMER
WHERE l_name = 'Echevarria';
"""),
("md", "**Q12.** What are our average rates and average principals by year of maturity? Order by year."),
("sql", """
-- YEAR() pulls the year out of the due (maturity) date.
SELECT
    YEAR(date_due)                AS 'Maturity Year',
    FORMAT(AVG(rate), 'N3')       AS 'Average Rate (%)',
    FORMAT(AVG(principal), 'C0')  AS 'Average Principal'
FROM LOAN
GROUP BY YEAR(date_due)
ORDER BY YEAR(date_due);
"""),
]

# ---------------------------------------------------------------- MP3
mp3 = [
("md", """
# MP3 - SmallBank (B)
**Corey Farrow** · SQL & Data Modeling portfolio

Database `SmallBankDB` (T-SQL).

Join path: `LOAN_OFFICER` -> `LOAN` (lo_id) -> `CUSTOMER_IN_LOAN` (l_id) -> `CUSTOMER` (c_id). `INSURANCE_PLAN` hangs off `CUSTOMER` (c_id) and is optional, so it is reached with a LEFT JOIN.

Formatting rules: money `FORMAT(x,'C0')`, integers `'N0'`, interest rates `'N3'`. `FORMAT` returns text, so sorting always uses the unformatted value.
"""),
("md", "**Q1:** List our customers who have a loan, where they live, their loan officers, and their phones. Alphabetical by city and then by customer last and first name. Column names specify who is who."),
("sql", """
SELECT DISTINCT
    c.c_id     AS 'Customer ID',
    c.l_name   AS 'Customer Last Name',
    c.f_name   AS 'Customer First Name',
    c.city     AS 'Customer City',
    c.state    AS 'Customer State',
    lo.lo_id   AS 'Loan Officer ID',
    lo.l_name  AS 'Loan Officer Last Name',
    lo.f_name  AS 'Loan Officer First Name',
    lo.phone   AS 'Loan Officer Phone'
FROM CUSTOMER c
    JOIN CUSTOMER_IN_LOAN cil ON c.c_id = cil.c_id
    JOIN LOAN l               ON cil.l_id = l.l_id
    JOIN LOAN_OFFICER lo      ON l.lo_id = lo.lo_id
ORDER BY c.city, c.l_name, c.f_name;
"""),
("md", "**Q2:** Who are Carl Dyer's (id = 8) clients? Alphabetized list by last and first name."),
("sql", """
-- DISTINCT: a client with two of Carl's loans should appear once.
SELECT DISTINCT
    c.c_id    AS 'Customer ID',
    c.l_name  AS 'Last Name',
    c.f_name  AS 'First Name'
FROM CUSTOMER c
    JOIN CUSTOMER_IN_LOAN cil ON c.c_id = cil.c_id
    JOIN LOAN l               ON cil.l_id = l.l_id
WHERE l.lo_id = 8
ORDER BY c.l_name, c.f_name;
"""),
("md", "**Q3:** We measure loan officer performance in terms of the amount they manage. Who manages the least money that is not yet past due as of the time the query is run?"),
("sql", """
-- WITH TIES returns every officer tied for the lowest total.
SELECT TOP 1 WITH TIES
    lo.lo_id                   AS 'Loan Officer ID',
    lo.l_name                  AS 'Last Name',
    lo.f_name                  AS 'First Name',
    FORMAT(SUM(l.principal), 'C0') AS 'Amount Managed (Not Past Due)'
FROM LOAN_OFFICER lo
    JOIN LOAN l ON lo.lo_id = l.lo_id
WHERE l.date_due >= CAST(GETDATE() AS DATE)
GROUP BY lo.lo_id, lo.l_name, lo.f_name
ORDER BY SUM(l.principal) ASC;
"""),
("md", "**Q4:** List all customers alphabetically, including insurance information for those who have it. Print out 0 (zero) or '-' rather than 'Null' if they do not."),
("sql", """
-- LEFT JOIN keeps customers with no plan; ISNULL swaps the NULLs for '-'.
SELECT
    c.c_id     AS 'Customer ID',
    c.l_name   AS 'Last Name',
    c.f_name   AS 'First Name',
    ISNULL(FORMAT(ip.coverage, 'C0'), '-') AS 'Insurance Coverage',
    ISNULL(FORMAT(ip.premium,  'C0'), '-') AS 'Insurance Premium'
FROM CUSTOMER c
    LEFT JOIN INSURANCE_PLAN ip ON c.c_id = ip.c_id
ORDER BY c.l_name, c.f_name;
"""),
("md", "**Q5:** Create a report showing which loan officers has offered an average rate less than 13%. Order by rate ascending."),
("sql", """
-- The condition is on an aggregate, so it goes in HAVING. Rates are percent numbers (13 = 13%).
SELECT
    lo.lo_id                 AS 'Loan Officer ID',
    lo.l_name                AS 'Last Name',
    lo.f_name                AS 'First Name',
    FORMAT(AVG(l.rate), 'N3') AS 'Average Rate Offered (%)'
FROM LOAN_OFFICER lo
    JOIN LOAN l ON lo.lo_id = l.lo_id
GROUP BY lo.lo_id, lo.l_name, lo.f_name
HAVING AVG(l.rate) < 13
ORDER BY AVG(l.rate) ASC;
"""),
("md", "**Q6:** Who are our top quartile borrowers? Show customers and total borrowed. Order by total principal borrowed, largest on top."),
("sql", """
SELECT TOP 25 PERCENT
    c.c_id     AS 'Customer ID',
    c.l_name   AS 'Last Name',
    c.f_name   AS 'First Name',
    FORMAT(SUM(l.principal), 'C0') AS 'Total Borrowed'
FROM CUSTOMER c
    JOIN CUSTOMER_IN_LOAN cil ON c.c_id = cil.c_id
    JOIN LOAN l               ON cil.l_id = l.l_id
GROUP BY c.c_id, c.l_name, c.f_name
ORDER BY SUM(l.principal) DESC;
"""),
("md", "**Q7:** Who borrowed the most money in Richmond? (do not show the $ amount)."),
("sql", """
-- Sort on the total but do not display it, as instructed.
SELECT TOP 1 WITH TIES
    c.c_id    AS 'Customer ID',
    c.l_name  AS 'Last Name',
    c.f_name  AS 'First Name',
    c.city    AS 'City',
    c.state   AS 'State'
FROM CUSTOMER c
    JOIN CUSTOMER_IN_LOAN cil ON c.c_id = cil.c_id
    JOIN LOAN l               ON cil.l_id = l.l_id
WHERE c.city = 'Richmond'
GROUP BY c.c_id, c.l_name, c.f_name, c.city, c.state
ORDER BY SUM(l.principal) DESC;
"""),
("md", "**Q8:** How many clients does Carl Dyer have? Assume you know his lo_id."),
("sql", """
-- COUNT(DISTINCT) because one client can hold several of Carl's loans.
SELECT FORMAT(COUNT(DISTINCT cil.c_id), 'N0') AS 'Number of Carl Dyer''s Clients'
FROM LOAN l
    JOIN CUSTOMER_IN_LOAN cil ON l.l_id = cil.l_id
WHERE l.lo_id = 8;
"""),
("md", "**Q9:** What is our insurance exposure by city? (Exposure = sum of coverages)"),
("sql", """
SELECT
    c.city   AS 'City',
    c.state  AS 'State',
    FORMAT(SUM(ip.coverage), 'C0') AS 'Insurance Exposure'
FROM CUSTOMER c
    JOIN INSURANCE_PLAN ip ON c.c_id = ip.c_id
GROUP BY c.city, c.state
ORDER BY SUM(ip.coverage) DESC;
"""),
("md", "**Q10:** How many of our Charlottesville customers are not insured?"),
("sql", """
-- Anti-join: LEFT JOIN, then keep the rows with no matching plan.
SELECT FORMAT(COUNT(*), 'N0') AS 'Uninsured Charlottesville Customers'
FROM CUSTOMER c
    LEFT JOIN INSURANCE_PLAN ip ON c.c_id = ip.c_id
WHERE c.city = 'Charlottesville'
  AND ip.c_id IS NULL;
"""),
("md", "**Q11:** List all the loan officers and how many insured customers each has. Alphabetic by officer."),
("sql", """
-- LEFT JOINs all the way down so officers with no loans or no insured clients still show 0.
-- COUNT(DISTINCT ip.c_id) counts only customers who have a plan, each once.
SELECT
    lo.lo_id   AS 'Loan Officer ID',
    lo.l_name  AS 'Last Name',
    lo.f_name  AS 'First Name',
    FORMAT(COUNT(DISTINCT ip.c_id), 'N0') AS 'Insured Customers'
FROM LOAN_OFFICER lo
    LEFT JOIN LOAN l               ON lo.lo_id = l.lo_id
    LEFT JOIN CUSTOMER_IN_LOAN cil ON l.l_id = cil.l_id
    LEFT JOIN INSURANCE_PLAN ip    ON cil.c_id = ip.c_id
GROUP BY lo.lo_id, lo.l_name, lo.f_name
ORDER BY lo.l_name, lo.f_name;
"""),
("md", "**Q12:** List all the loan officers who have customers in Charlottesville, order by total amount managed in that town, largest on top."),
("sql", """
-- DISTINCT subquery so a loan shared by two Charlottesville co-borrowers is counted once.
SELECT
    lo.lo_id   AS 'Loan Officer ID',
    lo.l_name  AS 'Last Name',
    lo.f_name  AS 'First Name',
    FORMAT(SUM(cvl.principal), 'C0') AS 'Amount Managed in Charlottesville'
FROM LOAN_OFFICER lo
    JOIN (SELECT DISTINCT l.l_id, l.lo_id, l.principal
          FROM LOAN l
              JOIN CUSTOMER_IN_LOAN cil ON l.l_id = cil.l_id
              JOIN CUSTOMER c           ON cil.c_id = c.c_id
          WHERE c.city = 'Charlottesville') cvl
        ON lo.lo_id = cvl.lo_id
GROUP BY lo.lo_id, lo.l_name, lo.f_name
ORDER BY SUM(cvl.principal) DESC;
"""),
]

for name, cells in [("MP1-SmallBank-A/MP1 Farrow.ipynb", mp1), ("MP3-SmallBank-B/MP3 Farrow.ipynb", mp3)]:
    p = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(nb(cells), open(p, "w"), indent=1)
    print("wrote", p)

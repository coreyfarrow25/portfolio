# COMM 3220: Data Management for Decision Making (DM4DM)

UVA McIntire School of Commerce, Fall 2026. Course site: https://webs.comm.virginia.edu/Comm3220/Schedule.html

The course has ten mini projects (MPs) across three parts: relational tables and SQL, business intelligence and data warehousing, and managing data. This folder holds my SQL work.

## Mini projects

| MP | Topic | Due | In this folder |
| --- | --- | --- | --- |
| MP1 | SmallBank (A): single-table SQL | Thu 09/03 | [MP1-SmallBank-A](./MP1-SmallBank-A/queries.sql) |
| MP2 | Notflix: ERD data modeling (Draw.io) | Thu 09/10 | Not included |
| MP3 | SmallBank (B): joins, HAVING, TOP PERCENT, COUNT DISTINCT | Thu 09/17 | [MP3-SmallBank-B](./MP3-SmallBank-B/queries.sql) |
| MP4 | DigiSonos and UBC: ERD (individual, MySQL Workbench) | Thu 10/08 | Not included |
| MP5 | B2B data integration (team) | Thu 10/15 | Not included |
| MP6-MP10 | Pressley, REI_Not, Acme Global, Nolex, WWI (data warehousing, Power BI, large DBs) | Oct to Dec | Not yet done |

## SmallBank schema (SQL Server / T-SQL)

| Table | Columns |
| --- | --- |
| CUSTOMER | c_id (PK), f_name, l_name, city, state |
| LOAN | l_id (PK), principal, rate, date_due, purpose, lo_id (FK) |
| LOAN_OFFICER | lo_id (PK), f_name, l_name, phone |
| CUSTOMER_IN_LOAN | c_id (FK), l_id (FK), composite PK (customers and loans are many-to-many) |
| INSURANCE_PLAN | c_id (PK and FK), coverage, premium |

## Notes and caveats

- These queries were rebuilt from my earlier working sessions, not copied from the submitted notebooks. MP3 Q7, Q9, Q10 and Q11 are reconstructions, and Q11's original question wording was not recoverable. They are marked in the file.
- None of the queries was re-run against SmallBankDB when this folder was assembled. Check the rate scale (`rate = 5` vs `0.05`) with `SELECT DISTINCT rate FROM LOAN` before relying on MP1 Q6 or MP3 Q5.
- MP2, MP4 and MP5 are ERD diagrams (Draw.io and MySQL Workbench files). Those files were not available to upload. MP4 and MP5 also include teammates' work, so check with them before publishing it.
- Course materials are the work of Prof. Stefano Grazioli; use of them must acknowledge the author.

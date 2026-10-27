# SQL & Data Modeling for Product Work

**What this is:** the SQL and data-modeling work I use to answer business questions without waiting on an analyst, and to talk to engineers about schemas as a peer. Six projects across T-SQL, MySQL and relational design, each framed by the question it answers and the product decision it supports.

**What I can do with it:**

- **Answer product and business questions directly in SQL.** Segment users, rank performance, size exposure and find the gaps, with joins I can defend.
- **Catch the traps that make a metric wrong.** Double-counted records, NULLs that sort first, ties that vanish, and "no match" rows that silently drop out of a report.
- **Model data before anything gets built.** Turn a vague business description into an ERD and a schema, and normalize a messy source into something that stays consistent.
- **Design data contracts between systems.** Map what moves between two companies' systems field by field, and find the gaps before launch.
- **Serve the people who don't write SQL.** Put a view over a clean schema so non-technical stakeholders still get the report they know.

| Project | Business question | SQL and modeling used | Output |
| --- | --- | --- | --- |
| [Loan portfolio analytics (1)](./MP1-SmallBank-A/) | How big is our exposure, who are our customers, and what does pricing look like? | `WHERE`, `ORDER BY`, `TOP`, aggregates, `GROUP BY`, `LIKE`, date functions, `FORMAT` | 12 queries |
| [Loan portfolio analytics (2)](./MP3-SmallBank-B/) | Which officers manage the most risk, who is uninsured, who are our top borrowers? | Multi-table joins, `LEFT JOIN` and anti-joins, `HAVING`, `TOP n PERCENT`, `WITH TIES`, `COUNT(DISTINCT)` | 12 queries |
| [Streaming service data model](./MP2-Notflix/) | What data does a streaming product need to track accounts, viewing and ratings? | ERD design, many-to-many resolution, 1:1, cardinality, check constraints | ERD and DDL |
| [Sales order data model](./MP4-UBC-Sales/) | How should a B2B sales function store orders, discounts and price changes? | Requirements to schema, optional relationships, audit-friendly design | ERD and MySQL DDL |
| [B2B data integration](./MP5-B2B-Integration/) | How does data flow between a supplier and its customer, and where does it break? | Merging models as a team, foreign key decisions, data-flow mapping | 2 integrated ERDs, data-flow diagram, DDL |
| [Spreadsheet to database](./MP6-Pressly/) | How do you fix a one-big-table database without breaking the people who use it? | Normalization to 3NF, `CREATE TABLE`, `INSERT`, `UPDATE`, `VIEW` | Notebook with schema, load and view |

---

## Loan portfolio analytics (T-SQL)

A five-table lending database: customers and loans (many-to-many through a bridge table), one officer per loan, and optional insurance plans. I wrote 24 queries against it. The ones below show the judgment, not just the syntax.

**Sizing exposure without overstating it.** Total exposure is the sum of principal on loans that haven't matured, using `GETDATE()` so the number is current whenever it runs. A loan with two co-borrowers is counted once, not twice, by summing over a `DISTINCT` subquery of loans before grouping. Skipping that step would inflate any officer-by-city total.

**Ranking without losing ties.** "Who manages the least money?" and "who borrowed the most in Richmond?" use `TOP 1 WITH TIES`. A plain `TOP 1` returns one arbitrary row and hides everyone tied with it. In a real report, that is a wrong answer that looks right.

**Finding the people who aren't in the data.** Insurance is optional, so reporting on it needs a `LEFT JOIN`. Counting uninsured customers is an anti-join (`LEFT JOIN ... WHERE ip.c_id IS NULL`). The per-officer report joins `LEFT` all the way down so officers with no insured clients show 0 instead of disappearing. This is the same pattern as "users who never activated" or "accounts with no usage."

**Cleaning inputs before they distort a result.** Missing principals would sort first in a "smallest loans" list, and a NULL rate would form its own group in an average-by-rate report. Both queries filter them out and say why in a comment.

**Segmenting.** "Top quartile borrowers" is `TOP 25 PERCENT` over a grouped total. Officer performance by average rate offered uses `HAVING` because the condition is on an aggregate.

**Presenting results for a reader.** Money is formatted as `$` with commas, rates to three decimals, and every `ORDER BY` sorts on the raw number, not the formatted text. Formatting returns a string, and sorting on it puts "$9" after "$10,000."

Notebooks: [`MP1 Farrow.ipynb`](./MP1-SmallBank-A/MP1%20Farrow.ipynb) · [`MP3 Farrow.ipynb`](./MP3-SmallBank-B/MP3%20Farrow.ipynb)

---

## Data modeling

**Streaming service ([ERD and DDL](./MP2-Notflix/)).** Each customer has one account, which holds several user profiles and a monthly payment history. Shows-to-genres and user-ratings-of-shows are many-to-many, so each gets an association table (`SHOW_GENRE`, `SHOW_RATING`, `GENRE_RATING`), with a check constraint keeping ratings between -1 and +2. A `VIEWING` table records which user watched which segment of which show, and when. That is the table a product team would build engagement and retention metrics on.

**Sales order system ([ERD and DDL](./MP4-UBC-Sales/)).** I modeled the sales function from a vague business write-up, and the decisions are the interesting part:

- Orders arrive electronically or by phone, so the sales employee is optional and an `order_type` field records which kind it is.
- Discounts are stored at both the line and order level, so managers can report on discounts and on who gave them.
- Suggested prices are kept over time in `price_history`, with who set each one, so pricing decisions can be audited.
- The system stores *when* a confirmation was sent and when the order went to shipping, but not the message text. That is a deliberate scope call.

**B2B data integration ([ERDs and data-flow diagram](./MP5-B2B-Integration/)).** I merged three functional models into one company model with a team of four, then joined a second team of three to map the data moving between the two companies.

| Step | Flow | From | To |
| --- | --- | --- | --- |
| 0 | Product and price info | Supplier `product`, `price_history` | Customer `product`, `historical_price` |
| 1 | Purchase order | Customer `purchase_order`, `order_line` | Supplier `customer_order` (`customer_po_number`), `order_line` |
| 2 | Packing slip (travels with the goods) | Supplier `shipment`, `shipment_line` | Customer `shipment`, `shipment_line` |
| 3 | Acceptance and returned goods | Customer `shipment_line` | Supplier `shipment_line.qty_accepted`, `shipment.customer_signature` |
| 4 | Payment (EFT) | Customer `payment` | Supplier `payment` |
| 5 | Reconciliation (both ways) | Customer `reconciliation` | Supplier `reconciliation` |

Tracing each step exposed two gaps that neither company's separate model covered, and I added fields to close them:

- The supplier had nowhere to store the customer's own PO number, so I added `customer_order.customer_po_number`.
- The supplier had nowhere to store what the customer actually accepted, so I added `shipment_line.qty_accepted`. Accounts receivable needs that quantity to check payments.

Other decisions that came out of the merge: one order can be fulfilled by several shipments, each shipment line points back to the order line it fulfills, and `shipment_line.order_line_id` is nullable so goods that arrive without an order can still be recorded and returned. A delivery-quality metric is calculated rather than stored, so it can't drift out of sync.

---

## Spreadsheet to database: normalizing an ad agency's data (T-SQL)

**The problem.** A previous consultant had loaded an ad agency's campaign spreadsheet straight into the database as one big table, so campaign details and manager names were repeated on every row. My job was to normalize it while still giving staff who don't know SQL the same spreadsheet layout.

**The design.** The key of the original table is (campaign, ad type). I split it into four tables:

- `AD_CAMPAIGN`: name, start date, duration. These depend only on the campaign.
- `AD_TYPE`: media, range, responsible manager. These depend only on the ad type.
- `CAMPAIGN_TYPE`: budget share, which depends on both. This is the association table.
- `MANAGER`: manager name depends on the manager, not on the key, so it moved out.

**The build.** The notebook drops existing objects in dependency order, creates the tables with primary and foreign keys and proper types, loads parents before children, applies an `UPDATE` to rename a manager, and creates a `BIG_TABLE` view that rebuilds the original spreadsheet's columns, order and formats.

**The result.** Each fact is stored once, so renaming a manager is one `UPDATE` instead of a find-and-replace across rows. Anyone who wants the old spreadsheet can still query one table. This is the tradeoff I'd make as a PM: clean structure underneath, familiar surface on top.

Notebook: [`MP6 Farrow.ipynb`](./MP6-Pressly/MP6%20Farrow.ipynb)

---

## Opening the models

Each `*_schema.sql` file is a MySQL create script. In MySQL Workbench 8.x, go to **File > Import > Reverse Engineer MySQL Create Script**, tick "Place imported objects on a diagram," and you get an editable model with keys and crow's-foot relationships. The diagrams in this repo are generated from code in [`_tools/`](./_tools/): `models.py` holds every table and relationship, and `render.py` draws the ERDs and writes the DDL.

## Provenance

- These files were rebuilt from the original assignment write-ups, so they are not the exact files I submitted. The original integration diagrams were built together with my teammates, as described above.
- The queries were syntax-checked but not re-run against the original database, which sits behind a university network.
- The datasets and scenarios come from a University of Virginia McIntire data management course taught by Prof. Stefano Grazioli, used with acknowledgment.

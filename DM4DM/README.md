# COMM 3220: Data Management for Decision Making (DM4DM)

UVA McIntire School of Commerce, Fall 2026, taught by Prof. Stefano Grazioli. [Course schedule](https://webs.comm.virginia.edu/Comm3220/Schedule.html)

The course runs from relational SQL and data modeling into business intelligence and data warehousing. This folder holds my mini projects (MPs) so far: SQL on a banking database, ER modeling for a streaming startup, and a two-company B2B data model.

| MP | Topic | Skills | Deliverables |
| --- | --- | --- | --- |
| [MP1](./MP1-SmallBank-A/) | SmallBank (A) | Single-table T-SQL: filtering, sorting, `TOP`, aggregates, `GROUP BY`, `LIKE`, date functions, `FORMAT` | `MP1 Farrow.ipynb` (12 queries) |
| [MP2](./MP2-Notflix/) | Notflix | ER modeling: resolving many-to-many with association tables, 1:1, cardinalities | ERD (PDF/PNG) and DDL |
| [MP3](./MP3-SmallBank-B/) | SmallBank (B) | Multi-table joins, `LEFT JOIN` and anti-joins, `HAVING`, `TOP n PERCENT`, `WITH TIES`, `COUNT(DISTINCT)` | `MP3 Farrow.ipynb` (12 queries) |
| [MP4](./MP4-UBC-Sales/) | DigiSonos and UBC: one business function | Modeling a function from a vague business write-up (my function: UBC Sales) | ERD (PDF/PNG) and MySQL DDL |
| [MP5](./MP5-B2B-Integration/) | B2B data integration (team of 4, then 7) | Merging our individual functional models into one company model as a team of four, then mapping the data that flows between the two companies with a second team of three | Two integrated ERDs, a data-flow diagram, MySQL DDL |
| [MP6](./MP6-Pressly/) | Pressly Ad Agency | Normalization to 3NF, `CREATE TABLE`, `INSERT`, and a view that rebuilds the old spreadsheet | `MP6 Farrow.ipynb` |

## MP1 and MP3: SmallBank (SQL Server)

SmallBankDB has five tables. `CUSTOMER` and `LOAN` are many-to-many through `CUSTOMER_IN_LOAN`. Each `LOAN` has one `LOAN_OFFICER`, and `INSURANCE_PLAN` is optional per customer.

The notebooks follow the assignment's output rules:

- Every person shown has an ID, and every city has its state.
- Money is formatted `$` with commas and no decimals (`FORMAT(x,'C0')`), and interest rates get three decimals.
- `FORMAT` returns text, so every `ORDER BY` sorts on the raw number.

A few choices worth explaining:

- **MP1 Q4 and Q9 ("check the results!"):** these exclude `NULL` principals and rates, which would otherwise sort first or form their own group.
- **MP3 Q3 and Q7:** these use `TOP 1 WITH TIES`, so a tie for first or last isn't silently dropped. Q7 also sorts on total borrowed without showing it, as the question asks.
- **MP3 Q11:** this LEFT JOINs all the way down, so officers with no insured clients still appear with 0.
- **MP3 Q12:** this totals principal over distinct loans, so a loan shared by two Charlottesville co-borrowers isn't counted twice.

## MP2: Notflix

Each customer has one account, which holds several users and a monthly payment history. Two many-to-many relationships are resolved into association tables:

- shows and genres, through `SHOW_GENRE`
- users rating shows and genres, through `SHOW_RATING` and `GENRE_RATING`, with a rating check of -1 to +2

`VIEWING` records which user watched which segment of which show, and when.

## MP4: UBC Sales (my function)

- **Orders:** an order is placed by a customer and shipped to exactly one of that customer's `ship_address`es. Orders can come in electronically (no employee) or by phone (the sales employee who took the call), so `employee_id` is optional and `order_type` records which kind it is.
- **Discounts:** these are stored at both levels, `order_line.line_discount` and `customer_order.order_discount`. That lets managers report on discounts and on who gave them.
- **Prices:** managers' suggested prices are kept over time in `price_history`, along with who set each one.
- **Timestamps:** the system records when the confirmation email was sent and when the order went to Shipping. The message text itself is not stored.

## MP5: B2B integration

MP5 was a team project in two stages:

- **Part one (four people):** I worked with three other consultants assigned to UBC. Each of us brought our own MP4 diagram to the table. We had to agree on one version of the tables we had all modeled differently (customer, order, line item, product, employee), decide where each foreign key belonged, and keep every function's requirements working in the merged model.
- **Part two (seven people):** our group of four joined a group of three who had modeled DigiSonos. Together we traced each step of the B2B process across both companies' models. That meant agreeing on which fields one company sends and where the other company stores them, and fixing the gaps we found along the way.

**Task One** merges three functional models per company and removes the duplicate tables (customer, order, line item, product, employee):

- **UBC (Sales, Shipping, A/R):**
  - An order can be fulfilled by several shipments, and each `shipment_line` points back to the `order_line` it fulfills.
  - Packers are recorded per shipment line, which supports the "who packed which item with errors" report. Inspectors are recorded per shipment.
  - Payments arrive per shipment (pay upon receipt), and reconciliations reference the shipment, the payment being modified and the A/R employee.
- **DigiSonos (Purchasing, Receiving, A/P):**
  - Teams review product classes and authorize order lines item by item, which changes the line status from Requested to Submitted.
  - Products carry an approval status and `% delivery error`. Delivery quality is calculated, so it isn't stored.
  - `shipment_line.order_line_id` is nullable, so items that were received but never ordered can be recorded and returned.
  - The vendor's bank details for EFT live on `vendor`.

**Task Two** shows which fields move between the two companies at each step of the B2B process:

| Step | Flow | From | To |
| --- | --- | --- | --- |
| 0 | Product and price info | UBC `product`, `price_history` | DigiSonos `product`, `historical_price` |
| 1 | Purchase order | DigiSonos `purchase_order`, `order_line` | UBC `customer_order` (`customer_po_number`), `order_line` |
| 2 | Packing slip (travels with the goods) | UBC `shipment`, `shipment_line` | DigiSonos `shipment`, `shipment_line` |
| 3 | Acceptance and returned goods | DigiSonos `shipment_line` (accepted and returned quantities) | UBC `shipment_line.qty_accepted`, `shipment.customer_signature` |
| 4 | Payment (EFT) | DigiSonos `payment` | UBC `payment` |
| 5 | Reconciliation (both ways) | DigiSonos `reconciliation` | UBC `reconciliation` |

Mapping the flows exposed two gaps in the separate models, and I added fields to fix them:

- UBC had nowhere to store DigiSonos's own PO number, so I added `customer_order.customer_po_number`.
- UBC had nowhere to store what the customer actually accepted, so I added `shipment_line.qty_accepted`. A/R needs that quantity to check payments.

## Opening the models in MySQL Workbench

Each `*_schema.sql` file is a MySQL create script. In MySQL Workbench 8.x, go to **File > Import > Reverse Engineer MySQL Create Script**, tick "Place imported objects on a diagram", and you get an editable `.mwb` model with the PK and FK symbols and crow's-foot relationships.

## Notes

- These files were rebuilt from the assignment write-ups and the instructor's hint models. They are not the files I originally submitted. The original MP5 diagrams were built together with my teammates, as described above.
- The queries were syntax-checked but not re-run against SmallBankDB, which needs the UVA VPN.
- The diagrams are generated from code in [`_tools/`](./_tools/): `models.py` holds every table and relationship, and `render.py` draws the ERDs and writes the DDL.
- The course materials are the work of Prof. Stefano Grazioli and are used with acknowledgment.

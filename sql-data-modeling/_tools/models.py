"""Data models for MP2 (Notflix), MP4 (UBC Sales) and MP5 (UBC + DigiSonos integrated).

Table:  name -> list of (column, sql_type, flags)  flags: 'PK', 'FK', 'PK FK', 'NN' (not null), ''
Rel:    (parent, child, fk_column, label, child_card, parent_card)
        child_card:  '0..*' | '1..*' | '0..1'
        parent_card: '1' (mandatory) | '0..1' (optional, nullable FK)
"""

# ------------------------------------------------------------------ MP2 Notflix
NOTFLIX = dict(
title="MP2: Notflix ERD  -  Corey Farrow",
tables={
 'CUSTOMER': [('customer_id','INT','PK'),('name','VARCHAR(80)','NN'),('email','VARCHAR(120)','NN'),('date_of_birth','DATE','')],
 'ACCOUNT': [('account_number','INT','PK'),('password','VARCHAR(64)','NN'),('status','VARCHAR(20)','NN'),('customer_id','INT','FK UQ')],
 'USER': [('user_id','INT','PK'),('username','VARCHAR(40)','NN'),('date_of_birth','DATE',''),('account_number','INT','FK')],
 'PAYMENT': [('payment_id','INT','PK'),('payment_date','DATE','NN'),('amount','DECIMAL(8,2)','NN'),('account_number','INT','FK')],
 'SHOW': [('show_id','INT','PK'),('title','VARCHAR(120)','NN'),('length_min','INT',''),('release_date','DATE','')],
 'GENRE': [('genre_id','INT','PK'),('genre_name','VARCHAR(40)','NN')],
 'SHOW_GENRE': [('show_id','INT','PK FK'),('genre_id','INT','PK FK')],
 'VIEWING': [('viewing_id','INT','PK'),('user_id','INT','FK'),('show_id','INT','FK'),('viewed_at','DATETIME','NN'),('segment_start_sec','INT','NN'),('segment_end_sec','INT','NN')],
 'SHOW_RATING': [('user_id','INT','PK FK'),('show_id','INT','PK FK'),('rating','TINYINT','NN')],
 'GENRE_RATING': [('user_id','INT','PK FK'),('genre_id','INT','PK FK'),('rating','TINYINT','NN')],
},
rels=[
 ('CUSTOMER','ACCOUNT','customer_id','opens','0..1','1'),
 ('ACCOUNT','USER','account_number','has','0..*','1'),
 ('ACCOUNT','PAYMENT','account_number','pays','0..*','1'),
 ('USER','VIEWING','user_id','watches','0..*','1'),
 ('SHOW','VIEWING','show_id','is viewed in','0..*','1'),
 ('SHOW','SHOW_GENRE','show_id','belongs to','1..*','1'),
 ('GENRE','SHOW_GENRE','genre_id','classifies','0..*','1'),
 ('USER','SHOW_RATING','user_id','rates','0..*','1'),
 ('SHOW','SHOW_RATING','show_id','is rated in','0..*','1'),
 ('USER','GENRE_RATING','user_id','rates','0..*','1'),
 ('GENRE','GENRE_RATING','genre_id','is rated in','0..*','1'),
],
checks=["CHECK (rating BETWEEN -1 AND 2)"],
)

# ------------------------------------------------------------------ UBC (Sales, Shipping, A/R)
UBC_T = {
 'customer': [('customer_id','INT','PK'),('name','VARCHAR(80)','NN'),('email','VARCHAR(120)',''),('phone','VARCHAR(20)',''),('bank_name','VARCHAR(80)','')],
 'ship_address': [('address_id','INT','PK'),('customer_id','INT','FK'),('street','VARCHAR(120)','NN'),('city','VARCHAR(60)','NN'),('state','CHAR(2)','NN'),('zip','VARCHAR(10)','NN')],
 'employee': [('employee_id','INT','PK'),('name','VARCHAR(80)','NN'),('role','VARCHAR(40)','')],
 'product': [('product_id','INT','PK'),('description','VARCHAR(120)','NN'),('qty_in_inventory','INT','NN')],
 'price_history': [('price_id','INT','PK'),('product_id','INT','FK'),('employee_id','INT','FK'),('suggested_price','DECIMAL(10,2)','NN'),('effective_date','DATE','NN')],
 'customer_order': [('order_id','INT','PK'),('customer_id','INT','FK'),('address_id','INT','FK'),('employee_id','INT','FK NULL'),('order_type','VARCHAR(10)','NN'),('customer_po_number','VARCHAR(30)',''),('order_date','DATETIME','NN'),('desired_ship_date','DATE',''),('order_discount','DECIMAL(10,2)',''),('confirmation_sent_at','DATETIME',''),('sent_to_shipping_at','DATETIME','')],
 'order_line': [('order_line_id','INT','PK'),('order_id','INT','FK'),('product_id','INT','FK'),('quantity','INT','NN'),('unit_price','DECIMAL(10,2)','NN'),('line_discount','DECIMAL(10,2)','')],
 'shipment': [('shipment_id','INT','PK'),('order_id','INT','FK'),('inspector_id','INT','FK NULL'),('ship_date','DATETIME',''),('packing_slip_printed_at','DATETIME',''),('notification_sent_at','DATETIME',''),('customer_signature','VARCHAR(255)',''),('accepted_at','DATETIME','')],
 'shipment_line': [('shipment_line_id','INT','PK'),('shipment_id','INT','FK'),('order_line_id','INT','FK'),('packer_id','INT','FK'),('qty_shipped','INT','NN'),('qty_accepted','INT',''),('error_flag','BOOLEAN',''),('error_note','VARCHAR(255)','')],
 'payment': [('payment_id','INT','PK'),('shipment_id','INT','FK'),('reviewed_by','INT','FK NULL'),('amount','DECIMAL(12,2)','NN'),('received_at','DATETIME','NN'),('bank_reference','VARCHAR(40)','')],
 'reconciliation': [('reconciliation_id','INT','PK'),('shipment_id','INT','FK'),('payment_id','INT','FK'),('employee_id','INT','FK'),('rec_date','DATE','NN'),('amount','DECIMAL(12,2)','NN'),('note','VARCHAR(255)','')],
}
UBC_R = [
 ('customer','ship_address','customer_id','has','1..*','1'),
 ('customer','customer_order','customer_id','places','0..*','1'),
 ('ship_address','customer_order','address_id','ships to','0..*','1'),
 ('employee','customer_order','employee_id','enters','0..*','0..1'),
 ('customer_order','order_line','order_id','contains','1..*','1'),
 ('product','order_line','product_id','ordered in','0..*','1'),
 ('product','price_history','product_id','priced in','0..*','1'),
 ('employee','price_history','employee_id','sets','0..*','1'),
 ('customer_order','shipment','order_id','fulfilled by','0..*','1'),
 ('shipment','shipment_line','shipment_id','contains','1..*','1'),
 ('order_line','shipment_line','order_line_id','shipped in','0..*','1'),
 ('employee','shipment_line','packer_id','packs','0..*','1'),
 ('employee','shipment','inspector_id','inspects','0..*','0..1'),
 ('shipment','payment','shipment_id','paid by','0..*','1'),
 ('employee','payment','reviewed_by','reviews','0..*','0..1'),
 ('shipment','reconciliation','shipment_id','reconciled in','0..*','1'),
 ('payment','reconciliation','payment_id','modified by','0..*','1'),
 ('employee','reconciliation','employee_id','performs','0..*','1'),
]

# MP4 = Corey's individual function: UBC Sales
SALES_TABLES = ['customer','ship_address','employee','product','price_history','customer_order','order_line']
UBC_SALES = dict(
 title="MP4: UBC Sales ERD  -  Corey Farrow, Sales",
 tables={t: [c for c in UBC_T[t] if not (t=='customer' and c[0]=='bank_name')
             and not (t=='customer_order' and c[0]=='customer_po_number')] for t in SALES_TABLES},
 rels=[r for r in UBC_R if r[0] in SALES_TABLES and r[1] in SALES_TABLES],
)
UBC = dict(title="MP5 Task One: UBC integrated ERD (Sales + Shipping + Accounts Receivable)", tables=UBC_T, rels=UBC_R)

# ------------------------------------------------------------------ DigiSonos (Purchasing, Receiving, A/P)
DS_T = {
 'vendor': [('vendor_id','INT','PK'),('name','VARCHAR(80)','NN'),('phone','VARCHAR(20)',''),('bank_routing_number','CHAR(9)','NN'),('bank_account_number','VARCHAR(20)','NN')],
 'team': [('team_id','INT','PK'),('team_name','VARCHAR(60)','NN'),('manager_id','INT','FK NULL')],
 'employee': [('employee_id','INT','PK'),('name','VARCHAR(80)','NN'),('department','VARCHAR(20)','NN'),('team_id','INT','FK NULL')],
 'product_class': [('class_id','INT','PK'),('class_name','VARCHAR(60)','NN'),('team_id','INT','FK')],
 'product': [('product_id','INT','PK'),('vendor_id','INT','FK'),('class_id','INT','FK'),('vendor_product_code','VARCHAR(30)',''),('name','VARCHAR(120)','NN'),('status','VARCHAR(15)','NN'),('pct_delivery_error','DECIMAL(5,2)',''),('qty_in_inventory','INT','NN'),('point_of_use','VARCHAR(255)','')],
 'historical_price': [('price_id','INT','PK'),('product_id','INT','FK'),('price','DECIMAL(10,2)','NN'),('effective_date','DATE','NN')],
 'purchase_order': [('order_id','INT','PK'),('vendor_id','INT','FK'),('employee_id','INT','FK'),('order_date','DATETIME','NN'),('ship_to_address','VARCHAR(255)','NN'),('date_alert_sent','DATETIME','')],
 'order_line': [('order_line_id','INT','PK'),('order_id','INT','FK'),('product_id','INT','FK'),('team_id','INT','FK NULL'),('quantity','INT','NN'),('unit_price','DECIMAL(10,2)','NN'),('status','VARCHAR(15)','NN')],
 'shipment': [('shipment_id','INT','PK'),('order_id','INT','FK'),('vendor_id','INT','FK'),('received_by','INT','FK'),('packing_slip_number','VARCHAR(30)',''),('received_at','DATETIME','NN'),('ap_alert_sent_at','DATETIME','')],
 'shipment_line': [('shipment_line_id','INT','PK'),('shipment_id','INT','FK'),('order_line_id','INT','FK NULL'),('product_id','INT','FK'),('qty_shipped','INT','NN'),('qty_accepted','INT','NN'),('qty_returned','INT','')],
 'payment': [('payment_id','INT','PK'),('shipment_id','INT','FK'),('amount','DECIMAL(12,2)','NN'),('eft_date','DATETIME','NN'),('eft_reference','VARCHAR(40)','')],
 'reconciliation': [('reconciliation_id','INT','PK'),('shipment_id','INT','FK'),('payment_id','INT','FK'),('employee_id','INT','FK'),('rec_date','DATE','NN'),('note','VARCHAR(255)','')],
}
DS_R = [
 ('team','employee','team_id','includes','0..*','0..1'),
 ('employee','team','manager_id','manages','0..1','0..1'),
 ('team','product_class','team_id','reviews','0..*','1'),
 ('vendor','product','vendor_id','sells','0..*','1'),
 ('product_class','product','class_id','groups','0..*','1'),
 ('product','historical_price','product_id','priced in','0..*','1'),
 ('vendor','purchase_order','vendor_id','receives','0..*','1'),
 ('employee','purchase_order','employee_id','enters','0..*','1'),
 ('purchase_order','order_line','order_id','contains','1..*','1'),
 ('product','order_line','product_id','ordered in','0..*','1'),
 ('team','order_line','team_id','authorizes','0..*','0..1'),
 ('purchase_order','shipment','order_id','fulfilled by','0..*','1'),
 ('vendor','shipment','vendor_id','sends','0..*','1'),
 ('employee','shipment','received_by','receives','0..*','1'),
 ('shipment','shipment_line','shipment_id','lists','1..*','1'),
 ('order_line','shipment_line','order_line_id','fulfilled in','0..*','0..1'),
 ('product','shipment_line','product_id','delivered in','0..*','1'),
 ('shipment','payment','shipment_id','paid by','0..*','1'),
 ('shipment','reconciliation','shipment_id','reconciled in','0..*','1'),
 ('payment','reconciliation','payment_id','modified by','0..*','1'),
 ('employee','reconciliation','employee_id','performs','0..*','1'),
]
DIGISONOS = dict(title="MP5 Task One: DigiSonos integrated ERD (Purchasing + Receiving + Accounts Payable)", tables=DS_T, rels=DS_R)

# ------------------------------------------------------------------ MP5 Task Two: B2B data flows
# (step, label, [(from_company, table, [cols]) ...] -> [(to_company, table, [cols]) ...])
FLOWS = [
 ('0', 'Product & price info',
   [('U','product',['product_id','description']),('U','price_history',['suggested_price','effective_date'])],
   [('D','product',['vendor_product_code','name']),('D','historical_price',['price','effective_date'])]),
 ('1', 'Purchase order',
   [('D','purchase_order',['order_id','order_date','ship_to_address']),('D','order_line',['product_id','quantity','unit_price'])],
   [('U','customer_order',['customer_po_number','order_date','address_id']),('U','order_line',['product_id','quantity','unit_price'])]),
 ('2', 'Packing slip (with goods)',
   [('U','shipment',['shipment_id','ship_date']),('U','shipment_line',['order_line_id','qty_shipped'])],
   [('D','shipment',['packing_slip_number','received_at']),('D','shipment_line',['order_line_id','qty_shipped'])]),
 ('3', 'Acceptance / returned goods',
   [('D','shipment_line',['qty_accepted','qty_returned'])],
   [('U','shipment_line',['qty_accepted']),('U','shipment',['customer_signature','accepted_at'])]),
 ('4', 'Payment (EFT)',
   [('D','payment',['amount','eft_date','eft_reference'])],
   [('U','payment',['amount','received_at','bank_reference'])]),
 ('5', 'Reconciliation (both ways)',
   [('D','reconciliation',['rec_date','note'])],
   [('U','reconciliation',['rec_date','amount','note'])]),
]

-- MP5 Task One: DigiSonos integrated ERD (Purchasing + Receiving + Accounts Payable)
-- MySQL DDL. Open in MySQL Workbench 8.x: File > Import > Reverse Engineer MySQL Create Script,
-- tick 'Place imported objects on a diagram', then arrange the tables.

CREATE SCHEMA IF NOT EXISTS digisonos;
USE digisonos;

CREATE TABLE `vendor` (
  `vendor_id` INT NOT NULL,
  `name` VARCHAR(80) NOT NULL,
  `phone` VARCHAR(20),
  `bank_routing_number` CHAR(9) NOT NULL,
  `bank_account_number` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`vendor_id`)
) ENGINE=InnoDB;

CREATE TABLE `team` (
  `team_id` INT NOT NULL,
  `team_name` VARCHAR(60) NOT NULL,
  `manager_id` INT,
  PRIMARY KEY (`team_id`)
) ENGINE=InnoDB;

CREATE TABLE `employee` (
  `employee_id` INT NOT NULL,
  `name` VARCHAR(80) NOT NULL,
  `department` VARCHAR(20) NOT NULL,
  `team_id` INT,
  PRIMARY KEY (`employee_id`),
  CONSTRAINT `fk_employee_team_id` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`)
) ENGINE=InnoDB;

CREATE TABLE `product_class` (
  `class_id` INT NOT NULL,
  `class_name` VARCHAR(60) NOT NULL,
  `team_id` INT NOT NULL,
  PRIMARY KEY (`class_id`),
  CONSTRAINT `fk_product_class_team_id` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`)
) ENGINE=InnoDB;

CREATE TABLE `product` (
  `product_id` INT NOT NULL,
  `vendor_id` INT NOT NULL,
  `class_id` INT NOT NULL,
  `vendor_product_code` VARCHAR(30),
  `name` VARCHAR(120) NOT NULL,
  `status` VARCHAR(15) NOT NULL,
  `pct_delivery_error` DECIMAL(5,2),
  `qty_in_inventory` INT NOT NULL,
  `point_of_use` VARCHAR(255),
  PRIMARY KEY (`product_id`),
  CONSTRAINT `fk_product_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`vendor_id`),
  CONSTRAINT `fk_product_class_id` FOREIGN KEY (`class_id`) REFERENCES `product_class` (`class_id`)
) ENGINE=InnoDB;

CREATE TABLE `historical_price` (
  `price_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `effective_date` DATE NOT NULL,
  PRIMARY KEY (`price_id`),
  CONSTRAINT `fk_historical_price_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`)
) ENGINE=InnoDB;

CREATE TABLE `purchase_order` (
  `order_id` INT NOT NULL,
  `vendor_id` INT NOT NULL,
  `employee_id` INT NOT NULL,
  `order_date` DATETIME NOT NULL,
  `ship_to_address` VARCHAR(255) NOT NULL,
  `date_alert_sent` DATETIME,
  PRIMARY KEY (`order_id`),
  CONSTRAINT `fk_purchase_order_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`vendor_id`),
  CONSTRAINT `fk_purchase_order_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB;

CREATE TABLE `order_line` (
  `order_line_id` INT NOT NULL,
  `order_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `team_id` INT,
  `quantity` INT NOT NULL,
  `unit_price` DECIMAL(10,2) NOT NULL,
  `status` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`order_line_id`),
  CONSTRAINT `fk_order_line_order_id` FOREIGN KEY (`order_id`) REFERENCES `purchase_order` (`order_id`),
  CONSTRAINT `fk_order_line_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  CONSTRAINT `fk_order_line_team_id` FOREIGN KEY (`team_id`) REFERENCES `team` (`team_id`)
) ENGINE=InnoDB;

CREATE TABLE `shipment` (
  `shipment_id` INT NOT NULL,
  `order_id` INT NOT NULL,
  `vendor_id` INT NOT NULL,
  `received_by` INT NOT NULL,
  `packing_slip_number` VARCHAR(30),
  `received_at` DATETIME NOT NULL,
  `ap_alert_sent_at` DATETIME,
  PRIMARY KEY (`shipment_id`),
  CONSTRAINT `fk_shipment_order_id` FOREIGN KEY (`order_id`) REFERENCES `purchase_order` (`order_id`),
  CONSTRAINT `fk_shipment_vendor_id` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`vendor_id`),
  CONSTRAINT `fk_shipment_received_by` FOREIGN KEY (`received_by`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB;

CREATE TABLE `shipment_line` (
  `shipment_line_id` INT NOT NULL,
  `shipment_id` INT NOT NULL,
  `order_line_id` INT,
  `product_id` INT NOT NULL,
  `qty_shipped` INT NOT NULL,
  `qty_accepted` INT NOT NULL,
  `qty_returned` INT,
  PRIMARY KEY (`shipment_line_id`),
  CONSTRAINT `fk_shipment_line_shipment_id` FOREIGN KEY (`shipment_id`) REFERENCES `shipment` (`shipment_id`),
  CONSTRAINT `fk_shipment_line_order_line_id` FOREIGN KEY (`order_line_id`) REFERENCES `order_line` (`order_line_id`),
  CONSTRAINT `fk_shipment_line_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`)
) ENGINE=InnoDB;

CREATE TABLE `payment` (
  `payment_id` INT NOT NULL,
  `shipment_id` INT NOT NULL,
  `amount` DECIMAL(12,2) NOT NULL,
  `eft_date` DATETIME NOT NULL,
  `eft_reference` VARCHAR(40),
  PRIMARY KEY (`payment_id`),
  CONSTRAINT `fk_payment_shipment_id` FOREIGN KEY (`shipment_id`) REFERENCES `shipment` (`shipment_id`)
) ENGINE=InnoDB;

CREATE TABLE `reconciliation` (
  `reconciliation_id` INT NOT NULL,
  `shipment_id` INT NOT NULL,
  `payment_id` INT NOT NULL,
  `employee_id` INT NOT NULL,
  `rec_date` DATE NOT NULL,
  `note` VARCHAR(255),
  PRIMARY KEY (`reconciliation_id`),
  CONSTRAINT `fk_reconciliation_shipment_id` FOREIGN KEY (`shipment_id`) REFERENCES `shipment` (`shipment_id`),
  CONSTRAINT `fk_reconciliation_payment_id` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`payment_id`),
  CONSTRAINT `fk_reconciliation_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB;

ALTER TABLE `team` ADD CONSTRAINT `fk_team_manager_id` FOREIGN KEY (`manager_id`) REFERENCES `employee` (`employee_id`);

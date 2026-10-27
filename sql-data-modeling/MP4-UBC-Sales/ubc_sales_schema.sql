-- MP4: UBC Sales ERD  -  Corey Farrow, Sales
-- MySQL DDL. Open in MySQL Workbench 8.x: File > Import > Reverse Engineer MySQL Create Script,
-- tick 'Place imported objects on a diagram', then arrange the tables.

CREATE SCHEMA IF NOT EXISTS ubc_sales;
USE ubc_sales;

CREATE TABLE `customer` (
  `customer_id` INT NOT NULL,
  `name` VARCHAR(80) NOT NULL,
  `email` VARCHAR(120),
  `phone` VARCHAR(20),
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB;

CREATE TABLE `ship_address` (
  `address_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `street` VARCHAR(120) NOT NULL,
  `city` VARCHAR(60) NOT NULL,
  `state` CHAR(2) NOT NULL,
  `zip` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`address_id`),
  CONSTRAINT `fk_ship_address_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`)
) ENGINE=InnoDB;

CREATE TABLE `employee` (
  `employee_id` INT NOT NULL,
  `name` VARCHAR(80) NOT NULL,
  `role` VARCHAR(40),
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB;

CREATE TABLE `product` (
  `product_id` INT NOT NULL,
  `description` VARCHAR(120) NOT NULL,
  `qty_in_inventory` INT NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB;

CREATE TABLE `price_history` (
  `price_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `employee_id` INT NOT NULL,
  `suggested_price` DECIMAL(10,2) NOT NULL,
  `effective_date` DATE NOT NULL,
  PRIMARY KEY (`price_id`),
  CONSTRAINT `fk_price_history_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  CONSTRAINT `fk_price_history_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB;

CREATE TABLE `customer_order` (
  `order_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `address_id` INT NOT NULL,
  `employee_id` INT,
  `order_type` VARCHAR(10) NOT NULL,
  `order_date` DATETIME NOT NULL,
  `desired_ship_date` DATE,
  `order_discount` DECIMAL(10,2),
  `confirmation_sent_at` DATETIME,
  `sent_to_shipping_at` DATETIME,
  PRIMARY KEY (`order_id`),
  CONSTRAINT `fk_customer_order_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`),
  CONSTRAINT `fk_customer_order_address_id` FOREIGN KEY (`address_id`) REFERENCES `ship_address` (`address_id`),
  CONSTRAINT `fk_customer_order_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB;

CREATE TABLE `order_line` (
  `order_line_id` INT NOT NULL,
  `order_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `quantity` INT NOT NULL,
  `unit_price` DECIMAL(10,2) NOT NULL,
  `line_discount` DECIMAL(10,2),
  PRIMARY KEY (`order_line_id`),
  CONSTRAINT `fk_order_line_order_id` FOREIGN KEY (`order_id`) REFERENCES `customer_order` (`order_id`),
  CONSTRAINT `fk_order_line_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`)
) ENGINE=InnoDB;


-- MP2: Notflix ERD  -  Corey Farrow
-- MySQL DDL. Open in MySQL Workbench 8.x: File > Import > Reverse Engineer MySQL Create Script,
-- tick 'Place imported objects on a diagram', then arrange the tables.

CREATE SCHEMA IF NOT EXISTS notflix;
USE notflix;

CREATE TABLE `CUSTOMER` (
  `customer_id` INT NOT NULL,
  `name` VARCHAR(80) NOT NULL,
  `email` VARCHAR(120) NOT NULL,
  `date_of_birth` DATE,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB;

CREATE TABLE `ACCOUNT` (
  `account_number` INT NOT NULL,
  `password` VARCHAR(64) NOT NULL,
  `status` VARCHAR(20) NOT NULL,
  `customer_id` INT NOT NULL,
  PRIMARY KEY (`account_number`),
  UNIQUE (`customer_id`),
  CONSTRAINT `fk_ACCOUNT_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `CUSTOMER` (`customer_id`)
) ENGINE=InnoDB;

CREATE TABLE `USER` (
  `user_id` INT NOT NULL,
  `username` VARCHAR(40) NOT NULL,
  `date_of_birth` DATE,
  `account_number` INT NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_USER_account_number` FOREIGN KEY (`account_number`) REFERENCES `ACCOUNT` (`account_number`)
) ENGINE=InnoDB;

CREATE TABLE `PAYMENT` (
  `payment_id` INT NOT NULL,
  `payment_date` DATE NOT NULL,
  `amount` DECIMAL(8,2) NOT NULL,
  `account_number` INT NOT NULL,
  PRIMARY KEY (`payment_id`),
  CONSTRAINT `fk_PAYMENT_account_number` FOREIGN KEY (`account_number`) REFERENCES `ACCOUNT` (`account_number`)
) ENGINE=InnoDB;

CREATE TABLE `SHOW` (
  `show_id` INT NOT NULL,
  `title` VARCHAR(120) NOT NULL,
  `length_min` INT,
  `release_date` DATE,
  PRIMARY KEY (`show_id`)
) ENGINE=InnoDB;

CREATE TABLE `GENRE` (
  `genre_id` INT NOT NULL,
  `genre_name` VARCHAR(40) NOT NULL,
  PRIMARY KEY (`genre_id`)
) ENGINE=InnoDB;

CREATE TABLE `SHOW_GENRE` (
  `show_id` INT NOT NULL,
  `genre_id` INT NOT NULL,
  PRIMARY KEY (`show_id`, `genre_id`),
  CONSTRAINT `fk_SHOW_GENRE_show_id` FOREIGN KEY (`show_id`) REFERENCES `SHOW` (`show_id`),
  CONSTRAINT `fk_SHOW_GENRE_genre_id` FOREIGN KEY (`genre_id`) REFERENCES `GENRE` (`genre_id`)
) ENGINE=InnoDB;

CREATE TABLE `VIEWING` (
  `viewing_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `show_id` INT NOT NULL,
  `viewed_at` DATETIME NOT NULL,
  `segment_start_sec` INT NOT NULL,
  `segment_end_sec` INT NOT NULL,
  PRIMARY KEY (`viewing_id`),
  CONSTRAINT `fk_VIEWING_user_id` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`),
  CONSTRAINT `fk_VIEWING_show_id` FOREIGN KEY (`show_id`) REFERENCES `SHOW` (`show_id`)
) ENGINE=InnoDB;

CREATE TABLE `SHOW_RATING` (
  `user_id` INT NOT NULL,
  `show_id` INT NOT NULL,
  `rating` TINYINT NOT NULL,
  PRIMARY KEY (`user_id`, `show_id`),
  CHECK (rating BETWEEN -1 AND 2),
  CONSTRAINT `fk_SHOW_RATING_user_id` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`),
  CONSTRAINT `fk_SHOW_RATING_show_id` FOREIGN KEY (`show_id`) REFERENCES `SHOW` (`show_id`)
) ENGINE=InnoDB;

CREATE TABLE `GENRE_RATING` (
  `user_id` INT NOT NULL,
  `genre_id` INT NOT NULL,
  `rating` TINYINT NOT NULL,
  PRIMARY KEY (`user_id`, `genre_id`),
  CHECK (rating BETWEEN -1 AND 2),
  CONSTRAINT `fk_GENRE_RATING_user_id` FOREIGN KEY (`user_id`) REFERENCES `USER` (`user_id`),
  CONSTRAINT `fk_GENRE_RATING_genre_id` FOREIGN KEY (`genre_id`) REFERENCES `GENRE` (`genre_id`)
) ENGINE=InnoDB;


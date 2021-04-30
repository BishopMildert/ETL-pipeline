-- CREATE DATABASE production_db;

CREATE TABLE IF NOT EXISTS products (
    id varchar(36) PRIMARY KEY NOT NULL,
    product_name varchar(255) NOT NULL,
    size varchar(100) NOT NULL,
    price float NOT NULL
);

CREATE TABLE IF NOT EXISTS payments (
    id varchar(36) PRIMARY KEY NOT NULL,
    payment_type varchar(36) NOT NULL
);
CREATE TABLE IF NOT EXISTS franchises (
    id varchar(36) PRIMARY KEY NOT NULL,
    cafe_location varchar(36) NOT NULL --,
    -- address varchar(255)
);
CREATE TABLE IF NOT EXISTS transactions (
    id varchar(36) PRIMARY KEY NOT NULL,
    payment varchar(36) DEFAULT NULL,
    franchise varchar(100),
    date_time TIMESTAMP,
    cost_total float,

    FOREIGN KEY (payment) REFERENCES payments(id),
    FOREIGN KEY (franchise) REFERENCES franchises(id)
);
CREATE TABLE IF NOT EXISTS baskets (
    id varchar(36) PRIMARY KEY NOT NULL,
    transaction_id varchar(36) NOT NULL,
    product_id varchar(36) NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
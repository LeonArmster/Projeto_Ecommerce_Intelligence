CREATE SCHEMA IF NOT EXISTS raw;


CREATE TABLE IF NOT EXISTS raw.customers (
    customer_id     BIGINT PRIMARY KEY,
    birth_date      DATE,
    state           VARCHAR(2),
    created_at      TIMESTAMP
);


CREATE TABLE IF NOT EXISTS raw.products (
    product_id      BIGINT PRIMARY KEY,
    category        VARCHAR(50),
    brand           VARCHAR(100),
    base_price      NUMERIC(12,2),
    weight_kg       NUMERIC(10,3)
);


CREATE TABLE IF NOT EXISTS raw.orders (
    order_id        BIGINT PRIMARY KEY,
    customer_id     BIGINT,
    order_date      TIMESTAMP,
    order_status    VARCHAR(30),
    shipping_type   VARCHAR(30)
);


CREATE TABLE IF NOT EXISTS raw.order_items (
    order_item_id   BIGINT PRIMARY KEY,
    order_id        BIGINT,
    product_id      BIGINT,
    quantity        INTEGER,
    unit_price      NUMERIC(12,2),
    discount_pct    NUMERIC(5,2)
);


CREATE TABLE IF NOT EXISTS raw.payments (
    payment_id      BIGINT PRIMARY KEY,
    order_id        BIGINT,
    payment_method  VARCHAR(30),
    payment_amount  NUMERIC(14,2),
    installments    INTEGER,
    payment_status  VARCHAR(30),
    paid_at         TIMESTAMP
);


CREATE TABLE IF NOT EXISTS raw.shipments (
    shipment_id                BIGINT PRIMARY KEY,
    order_id                   BIGINT,
    shipped_at                 TIMESTAMP,
    estimated_delivery_date    TIMESTAMP,
    delivered_at               TIMESTAMP
);


CREATE TABLE IF NOT EXISTS raw.reviews (
    review_id       BIGINT PRIMARY KEY,
    order_id        BIGINT,
    rating          INTEGER,
    created_at      TIMESTAMP
);
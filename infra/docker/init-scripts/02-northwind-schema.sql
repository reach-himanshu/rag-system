-- Northwind Database Schema for PostgreSQL
-- Connect to northwind database
\c northwind;

CREATE TABLE categories (
    category_id SMALLINT PRIMARY KEY,
    category_name VARCHAR(15) NOT NULL,
    description TEXT
);

CREATE TABLE suppliers (
    supplier_id SMALLINT PRIMARY KEY,
    company_name VARCHAR(40) NOT NULL,
    contact_name VARCHAR(30),
    contact_title VARCHAR(30),
    address VARCHAR(60),
    city VARCHAR(15),
    region VARCHAR(15),
    postal_code VARCHAR(10),
    country VARCHAR(15),
    phone VARCHAR(24),
    fax VARCHAR(24),
    homepage TEXT
);

CREATE TABLE products (
    product_id SMALLINT PRIMARY KEY,
    product_name VARCHAR(40) NOT NULL,
    supplier_id SMALLINT REFERENCES suppliers(supplier_id),
    category_id SMALLINT REFERENCES categories(category_id),
    quantity_per_unit VARCHAR(20),
    unit_price REAL,
    units_in_stock SMALLINT,
    units_on_order SMALLINT,
    reorder_level SMALLINT,
    discontinued INTEGER NOT NULL
);

CREATE TABLE regions (
    region_id SMALLINT PRIMARY KEY,
    region_description VARCHAR(60) NOT NULL
);

CREATE TABLE territories (
    territory_id VARCHAR(20) PRIMARY KEY,
    territory_description VARCHAR(60) NOT NULL,
    region_id SMALLINT NOT NULL REFERENCES regions(region_id)
);

CREATE TABLE shippers (
    shipper_id SMALLINT PRIMARY KEY,
    company_name VARCHAR(40) NOT NULL,
    phone VARCHAR(24)
);

CREATE TABLE customers (
    customer_id VARCHAR(5) PRIMARY KEY,
    company_name VARCHAR(40) NOT NULL,
    contact_name VARCHAR(30),
    contact_title VARCHAR(30),
    address VARCHAR(60),
    city VARCHAR(15),
    region VARCHAR(15),
    postal_code VARCHAR(10),
    country VARCHAR(15),
    phone VARCHAR(24),
    fax VARCHAR(24)
);

CREATE TABLE employees (
    employee_id SMALLINT PRIMARY KEY,
    last_name VARCHAR(20) NOT NULL,
    first_name VARCHAR(10) NOT NULL,
    title VARCHAR(30),
    title_of_courtesy VARCHAR(25),
    birth_date DATE,
    hire_date DATE,
    address VARCHAR(60),
    city VARCHAR(15),
    region VARCHAR(15),
    postal_code VARCHAR(10),
    country VARCHAR(15),
    home_phone VARCHAR(24),
    extension VARCHAR(4),
    notes TEXT,
    reports_to SMALLINT REFERENCES employees(employee_id)
);

CREATE TABLE employee_territories (
    employee_id SMALLINT NOT NULL REFERENCES employees(employee_id),
    territory_id VARCHAR(20) NOT NULL REFERENCES territories(territory_id),
    PRIMARY KEY (employee_id, territory_id)
);

CREATE TABLE orders (
    order_id SMALLINT PRIMARY KEY,
    customer_id VARCHAR(5) REFERENCES customers(customer_id),
    employee_id SMALLINT REFERENCES employees(employee_id),
    order_date DATE,
    required_date DATE,
    shipped_date DATE,
    ship_via SMALLINT REFERENCES shippers(shipper_id),
    freight REAL,
    ship_name VARCHAR(40),
    ship_address VARCHAR(60),
    ship_city VARCHAR(15),
    ship_region VARCHAR(15),
    ship_postal_code VARCHAR(10),
    ship_country VARCHAR(15)
);

CREATE TABLE order_details (
    order_id SMALLINT NOT NULL REFERENCES orders(order_id),
    product_id SMALLINT NOT NULL REFERENCES products(product_id),
    unit_price REAL NOT NULL,
    quantity SMALLINT NOT NULL,
    discount REAL NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

-- Grant read-only access to rag_readonly role
GRANT USAGE ON SCHEMA public TO rag_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO rag_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO rag_readonly;

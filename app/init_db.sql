DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS Shops CASCADE;
DROP TABLE IF EXISTS Products CASCADE;
DROP TABLE IF EXISTS Orders CASCADE;
DROP TABLE IF EXISTS OrderedProducts CASCADE;

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY, 
    firstname VARCHAR(25),
    lastname VARCHAR(25),
    password VARCHAR(255),
    email VARCHAR(25) UNIQUE NOT NULL,
    streetaddress VARCHAR(25),
    postalcode VARCHAR(5),
    city VARCHAR(25),
    is_admin BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE Shops (
    shop_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    is_available BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id),
    shop_id INTEGER REFERENCES Shops(shop_id),
    name VARCHAR(25),
    description TEXT,
    image_type VARCHAR(50),
    image BYTEA,
    price REAL,
    quantity INTEGER,
    is_available BOOLEAN DEFAULT TRUE NOT NULL
);

CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id),
    ordered TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE OrderedProducts (
    item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES Orders(order_id),
    product_id INTEGER REFERENCES Products(product_id),
    quantity INTEGER,
    price REAL);

INSERT INTO Users (firstname, lastname, password, email, is_admin) VALUES ('Admin', 'User', '{{supersecret}}', 'admin@kauppakeskus.local', TRUE);

COMMIT;

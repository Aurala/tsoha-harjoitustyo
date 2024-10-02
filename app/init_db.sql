DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Shops;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS OrderedProducts;

CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY, 
    firstname TEXT,
    lastname TEXT,
    password TEXT,
    email TEXT UNIQUE NOT NULL,
    streetaddress TEXT,
    postalcode TEXT,
    city TEXT,
    is_admin INTEGER DEFAULT FALSE NOT NULL
);

CREATE TABLE Shops (
    shop_id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id),
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    is_available INTEGER DEFAULT FALSE NOT NULL
);

CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id),
    shop_id INTEGER REFERENCES Categories(category_id),
    name TEXT,
    description TEXT,
    image BLOB,
    price REAL,
    quantity INTEGER,
    is_available INTEGER DEFAULT TRUE NOT NULL
);

CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id),
    ordered DATETIME DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE OrderedProducts (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES Orders(order_id),
    product_id INTEGER REFERENCES Products(product_id),
    quantity INTEGER,
    price REAL);

INSERT INTO Users (firstname, lastname, password, email, is_admin) VALUES ('Admin', 'User', '{{supersecret}}', 'admin@kauppakeskus.local', TRUE);

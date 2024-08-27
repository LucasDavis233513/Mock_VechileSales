CREATE TABLE IF NOT EXISTS Seller (
    seller_id               INT NOT NULL,
    name                    VARCHAR(255),
    state                   VARCHAR(255),
    PRIMARY KEY (seller_id)
);

CREATE TABLE IF NOT EXISTS Details (
    detail_id               INT NOT NULL,
    transmission            VARCHAR(10),
    color                   VARCHAR(10),
    interior_color          VARCHAR(10),
    body                    VARCHAR(25),
    trim                    VARCHAR(255),
    condition               INT,
    odometer                INT,
    VIN                     VARCHAR(255),
    MMR                     FLOAT,
    PRIMARY KEY (detail_id)
);

CREATE TABLE IF NOT EXISTS Cars (
    car_id                  INT NOT NULL,
    make                    VARCHAR(25),
    model                   VARCHAR(50),
    year                    INT,
    selling_price           FLOAT,
    seller_id               INT NOT NULL,
    detail_id               INT NOT NULL,
    PRIMARY KEY (car_id),
    FOREIGN KEY (seller_id) REFERENCES Seller(seller_id),
    FOREIGN KEY (detail_id) REFERENCES Details(detail_id)
);

CREATE TABLE IF NOT EXISTS Users (
    user_id                 INT NOT NULL,
    username                VARCHAR(255),
    password                VARCHAR(255),
    email                   VARCHAR(50),
    city                    VARCHAR(255),
    state                   VARCHAR(255),
    zip_code                VARCHAR(255),
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS Purchases (
    purchase_id             INT NOT NULL,
    user_id                 INT NOT NULL,
    car_id                  INT NOT NULL,
    date                    DATE,
    price                   FLOAT,
    payment_info            VARCHAR(25),
    PRIMARY KEY (purchase_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (car_id) REFERENCES Cars(car_id)
);

COPY Seller(seller_id, name, state)
FROM '/Users/lucasdavis/Documents/vault/School notes/Database Mgt Systems/finalProject/Data/seller.csv'
DELIMITER ','
CSV HEADER;

COPY Details(detail_id, transmission, color, interior_color, body, trim, condition, odometer, VIN, MMR)
FROM '/Users/lucasdavis/Documents/vault/School notes/Database Mgt Systems/finalProject/Data/details.csv'
DELIMITER ','
CSV HEADER;

COPY Cars(car_id, make, model, year, selling_price, seller_id, detail_id)
FROM '/Users/lucasdavis/Documents/vault/School notes/Database Mgt Systems/finalProject/Data/cars.csv'
DELIMITER ','
CSV HEADER;
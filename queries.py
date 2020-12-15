from random import randint

####################################

consumers = [
    ('Арина', 'Дементьева'),
    ('Алексей', 'Андреев'),
    ('Лев', 'Поликарпов'),
    ('Марк', 'Егоров'),
    ('Дарья', 'Ульянова'),
    ('Максим', 'Родионов'),
    ('Анна', 'Токарева'),
    ('Кристина', 'Кузнецова'),
    ('Денис', 'Воробьев'),
    ('Андрей', 'Гаврилов')
]

products = [
    ('Гитара', 7990),
    ('Ноутбук', 39990),
    ('Коньки', 1990),
    ('Кроссовки', 3990),
    ('Робот-пылесос', 12990)
]

orders = []
for i in range(len(consumers) + len(products)):
    consumer_id = randint(1, len(consumers))
    product_id = randint(1, len(products))

    order = (consumer_id, product_id)
    if order not in orders:
        orders.append(order)

####################################

CREATE_CONSUMERS_TABLE = """
CREATE TABLE IF NOT EXISTS Consumers (
    id INTEGER AUTO_INCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    PRIMARY KEY (id)
);
"""
 
CREATE_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER AUTO_INCREMENT,
    title TEXT NOT NULL,
    price INTEGER NOT NULL,
    PRIMARY KEY (id)
);
"""

CREATE_ORDERS_TABLE = """
CREATE TABLE IF NOT EXISTS Orders (
    id INTEGER AUTO_INCREMENT,
    consumer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (consumer_id)
        REFERENCES consumers(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
"""

####################################

INSERT_CONSUMER = """
INSERT INTO
    Consumers (name, surname)
VALUES
    (%s, %s);
"""

INSERT_PRODUCT = """
INSERT INTO
    Products (title, price)
VALUES
    (%s, %s);
"""

INSERT_ORDER = """
INSERT INTO
    Orders (consumer_id, product_id)
VALUES
    (%s, %s);
"""

####################################

SELECT_BESTSELLER = """
SELECT
    *
FROM
    Products
WHERE
    id = (SELECT
               product_id
           FROM
               Orders
           GROUP BY
               product_id
           ORDER BY
               COUNT(*)
           DESC LIMIT 1);
"""

####################################

UPDATE_BESTSELLER_PRICE = """
UPDATE
    Products
SET
    price = 1.1 * price + 110
WHERE
    id = (SELECT
               product_id
           FROM
               Orders
           GROUP BY
               product_id
           ORDER BY
               COUNT(*)
           DESC LIMIT 1);
"""

####################################

DROP_CONSUMERS_TABLE = 'DROP TABLE Consumers;'
DROP_PRODUCTS_TABLE = 'DROP TABLE Products;'
DROP_ORDERS_TABLE = 'DROP TABLE Orders;'

####################################

queries = {
    'CREATE': [
        CREATE_CONSUMERS_TABLE,
        CREATE_PRODUCTS_TABLE,
        CREATE_ORDERS_TABLE
    ],
    'INSERT': [
        (INSERT_CONSUMER, consumers),
        (INSERT_PRODUCT, products),
        (INSERT_ORDER, orders)
    ],
    'SELECT': [
        SELECT_BESTSELLER
    ],
    'UPDATE': [
        UPDATE_BESTSELLER_PRICE
    ],
    'DROP': [
        DROP_ORDERS_TABLE,
        DROP_PRODUCTS_TABLE,
        DROP_CONSUMERS_TABLE
    ]
}

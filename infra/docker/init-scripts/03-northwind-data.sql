-- Northwind Sample Data for PostgreSQL
\c northwind;

-- Categories
INSERT INTO categories VALUES (1, 'Beverages', 'Soft drinks, coffees, teas, beers, and ales');
INSERT INTO categories VALUES (2, 'Condiments', 'Sweet and savory sauces, relishes, spreads, and seasonings');
INSERT INTO categories VALUES (3, 'Confections', 'Desserts, candies, and sweet breads');
INSERT INTO categories VALUES (4, 'Dairy Products', 'Cheeses');
INSERT INTO categories VALUES (5, 'Grains/Cereals', 'Breads, crackers, pasta, and cereal');
INSERT INTO categories VALUES (6, 'Meat/Poultry', 'Prepared meats');
INSERT INTO categories VALUES (7, 'Produce', 'Dried fruit and bean curd');
INSERT INTO categories VALUES (8, 'Seafood', 'Seaweed and fish');

-- Suppliers
INSERT INTO suppliers VALUES (1, 'Exotic Liquids', 'Charlotte Cooper', 'Purchasing Manager', '49 Gilbert St.', 'London', NULL, 'EC1 4SD', 'UK', '(171) 555-2222', NULL, NULL);
INSERT INTO suppliers VALUES (2, 'New Orleans Cajun Delights', 'Shelley Burke', 'Order Administrator', 'P.O. Box 78934', 'New Orleans', 'LA', '70117', 'USA', '(100) 555-4822', NULL, NULL);
INSERT INTO suppliers VALUES (3, 'Grandma Kellys Homestead', 'Regina Murphy', 'Sales Representative', '707 Oxford Rd.', 'Ann Arbor', 'MI', '48104', 'USA', '(313) 555-5735', '(313) 555-3349', NULL);
INSERT INTO suppliers VALUES (4, 'Tokyo Traders', 'Yoshi Nagase', 'Marketing Manager', '9-8 Sekimai Musashino-shi', 'Tokyo', NULL, '100', 'Japan', '(03) 3555-5011', NULL, NULL);
INSERT INTO suppliers VALUES (5, 'Cooperativa de Quesos Las Cabras', 'Antonio del Valle Saavedra', 'Export Administrator', 'Calle del Rosal 4', 'Oviedo', 'Asturias', '33007', 'Spain', '(98) 598 76 54', NULL, NULL);
INSERT INTO suppliers VALUES (6, 'Mayumis', 'Mayumi Ohno', 'Marketing Representative', '92 Setsuko Chuo-ku', 'Osaka', NULL, '545', 'Japan', '(06) 431-7877', NULL, NULL);
INSERT INTO suppliers VALUES (7, 'Pavlova Ltd.', 'Ian Devling', 'Marketing Manager', '74 Rose St. Moonie Ponds', 'Melbourne', 'Victoria', '3058', 'Australia', '(03) 444-2343', '(03) 444-6588', NULL);
INSERT INTO suppliers VALUES (8, 'Specialty Biscuits Ltd.', 'Peter Wilson', 'Sales Representative', '29 Kings Way', 'Manchester', NULL, 'M14 GSD', 'UK', '(161) 555-4448', NULL, NULL);

-- Regions
INSERT INTO regions VALUES (1, 'Eastern');
INSERT INTO regions VALUES (2, 'Western');
INSERT INTO regions VALUES (3, 'Northern');
INSERT INTO regions VALUES (4, 'Southern');

-- Shippers
INSERT INTO shippers VALUES (1, 'Speedy Express', '(503) 555-9831');
INSERT INTO shippers VALUES (2, 'United Package', '(503) 555-3199');
INSERT INTO shippers VALUES (3, 'Federal Shipping', '(503) 555-9931');

-- Products
INSERT INTO products VALUES (1, 'Chai', 1, 1, '10 boxes x 20 bags', 18, 39, 0, 10, 0);
INSERT INTO products VALUES (2, 'Chang', 1, 1, '24 - 12 oz bottles', 19, 17, 40, 25, 0);
INSERT INTO products VALUES (3, 'Aniseed Syrup', 1, 2, '12 - 550 ml bottles', 10, 13, 70, 25, 0);
INSERT INTO products VALUES (4, 'Chef Antons Cajun Seasoning', 2, 2, '48 - 6 oz jars', 22, 53, 0, 0, 0);
INSERT INTO products VALUES (5, 'Chef Antons Gumbo Mix', 2, 2, '36 boxes', 21.35, 0, 0, 0, 1);
INSERT INTO products VALUES (6, 'Grandmas Boysenberry Spread', 3, 2, '12 - 8 oz jars', 25, 120, 0, 25, 0);
INSERT INTO products VALUES (7, 'Uncle Bobs Organic Dried Pears', 3, 7, '12 - 1 lb pkgs.', 30, 15, 0, 10, 0);
INSERT INTO products VALUES (8, 'Northwoods Cranberry Sauce', 3, 2, '12 - 12 oz jars', 40, 6, 0, 0, 0);
INSERT INTO products VALUES (9, 'Mishi Kobe Niku', 4, 6, '18 - 500 g pkgs.', 97, 29, 0, 0, 1);
INSERT INTO products VALUES (10, 'Ikura', 4, 8, '12 - 200 ml jars', 31, 31, 0, 0, 0);
INSERT INTO products VALUES (11, 'Queso Cabrales', 5, 4, '1 kg pkg.', 21, 22, 30, 30, 0);
INSERT INTO products VALUES (12, 'Queso Manchego La Pastora', 5, 4, '10 - 500 g pkgs.', 38, 86, 0, 0, 0);
INSERT INTO products VALUES (13, 'Konbu', 6, 8, '2 kg box', 6, 24, 0, 5, 0);
INSERT INTO products VALUES (14, 'Tofu', 6, 7, '40 - 100 g pkgs.', 23.25, 35, 0, 0, 0);
INSERT INTO products VALUES (15, 'Genen Shouyu', 6, 2, '24 - 250 ml bottles', 15.5, 39, 0, 5, 0);
INSERT INTO products VALUES (16, 'Pavlova', 7, 3, '32 - 500 g boxes', 17.45, 29, 0, 10, 0);
INSERT INTO products VALUES (17, 'Alice Mutton', 7, 6, '20 - 1 kg tins', 39, 0, 0, 0, 1);
INSERT INTO products VALUES (18, 'Carnarvon Tigers', 7, 8, '16 kg pkg.', 62.5, 42, 0, 0, 0);
INSERT INTO products VALUES (19, 'Teatime Chocolate Biscuits', 8, 3, '10 boxes x 12 pieces', 9.2, 25, 0, 5, 0);
INSERT INTO products VALUES (20, 'Sir Rodneys Marmalade', 8, 3, '30 gift boxes', 81, 40, 0, 0, 0);

-- Customers
INSERT INTO customers VALUES ('ALFKI', 'Alfreds Futterkiste', 'Maria Anders', 'Sales Representative', 'Obere Str. 57', 'Berlin', NULL, '12209', 'Germany', '030-0074321', '030-0076545');
INSERT INTO customers VALUES ('ANATR', 'Ana Trujillo Emparedados y helados', 'Ana Trujillo', 'Owner', 'Avda. de la Constitucion 2222', 'Mexico D.F.', NULL, '05021', 'Mexico', '(5) 555-4729', '(5) 555-3745');
INSERT INTO customers VALUES ('ANTON', 'Antonio Moreno Taqueria', 'Antonio Moreno', 'Owner', 'Mataderos 2312', 'Mexico D.F.', NULL, '05023', 'Mexico', '(5) 555-3932', NULL);
INSERT INTO customers VALUES ('AROUT', 'Around the Horn', 'Thomas Hardy', 'Sales Representative', '120 Hanover Sq.', 'London', NULL, 'WA1 1DP', 'UK', '(171) 555-7788', '(171) 555-6750');
INSERT INTO customers VALUES ('BERGS', 'Berglunds snabbkop', 'Christina Berglund', 'Order Administrator', 'Berguvsvagen 8', 'Lulea', NULL, 'S-958 22', 'Sweden', '0921-12 34 65', '0921-12 34 67');
INSERT INTO customers VALUES ('BLAUS', 'Blauer See Delikatessen', 'Hanna Moos', 'Sales Representative', 'Forsterstr. 57', 'Mannheim', NULL, '68306', 'Germany', '0621-08460', '0621-08924');
INSERT INTO customers VALUES ('BLONP', 'Blondel pere et fils', 'Frederique Citeaux', 'Marketing Manager', '24 place Kleber', 'Strasbourg', NULL, '67000', 'France', '88.60.15.31', '88.60.15.32');
INSERT INTO customers VALUES ('BOLID', 'Bolido Comidas preparadas', 'Martin Sommer', 'Owner', 'C/ Araquil 67', 'Madrid', NULL, '28023', 'Spain', '(91) 555 22 82', '(91) 555 91 99');
INSERT INTO customers VALUES ('BONAP', 'Bon app', 'Laurence Lebihan', 'Owner', '12 rue des Bouchers', 'Marseille', NULL, '13008', 'France', '91.24.45.40', '91.24.45.41');
INSERT INTO customers VALUES ('BOTTM', 'Bottom-Dollar Markets', 'Elizabeth Lincoln', 'Accounting Manager', '23 Tsawassen Blvd.', 'Tsawassen', 'BC', 'T2F 8M4', 'Canada', '(604) 555-4729', '(604) 555-3745');
INSERT INTO customers VALUES ('BSBEV', 'Bs Beverages', 'Victoria Ashworth', 'Sales Representative', 'Fauntleroy Circus', 'London', NULL, 'EC2 5NT', 'UK', '(171) 555-1212', NULL);
INSERT INTO customers VALUES ('CACTU', 'Cactus Comidas para llevar', 'Patricio Simpson', 'Sales Agent', 'Cerrito 333', 'Buenos Aires', NULL, '1010', 'Argentina', '(1) 135-5555', '(1) 135-4892');
INSERT INTO customers VALUES ('CENTC', 'Centro comercial Moctezuma', 'Francisco Chang', 'Marketing Manager', 'Sierras de Granada 9993', 'Mexico D.F.', NULL, '05022', 'Mexico', '(5) 555-3392', '(5) 555-7293');
INSERT INTO customers VALUES ('CHOPS', 'Chop-suey Chinese', 'Yang Wang', 'Owner', 'Hauptstr. 29', 'Bern', NULL, '3012', 'Switzerland', '0452-076545', NULL);
INSERT INTO customers VALUES ('COMMI', 'Comercio Mineiro', 'Pedro Afonso', 'Sales Associate', 'Av. dos Lusíadas 23', 'Sao Paulo', 'SP', '05432-043', 'Brazil', '(11) 555-7647', NULL);

-- Employees
INSERT INTO employees VALUES (2, 'Fuller', 'Andrew', 'Vice President Sales', 'Dr.', '1952-02-19', '1992-08-14', '908 W. Capital Way', 'Tacoma', 'WA', '98401', 'USA', '(206) 555-9482', '3457', 'Andrew received his BTS commercial and a Ph.D. in marketing.', NULL);
INSERT INTO employees VALUES (5, 'Buchanan', 'Steven', 'Sales Manager', 'Mr.', '1955-03-04', '1993-10-17', '14 Garrett Hill', 'London', NULL, 'SW1 8JR', 'UK', '(71) 555-4848', '3453', 'Steven Buchanan graduated from St. Andrews University in Scotland.', 2);
INSERT INTO employees VALUES (1, 'Davolio', 'Nancy', 'Sales Representative', 'Ms.', '1968-12-08', '1992-05-01', '507 20th Ave. E. Apt. 2A', 'Seattle', 'WA', '98122', 'USA', '(206) 555-9857', '5467', 'Education includes a BA in psychology from Colorado State University.', 2);
INSERT INTO employees VALUES (3, 'Leverling', 'Janet', 'Sales Representative', 'Ms.', '1963-08-30', '1992-04-01', '722 Moss Bay Blvd.', 'Kirkland', 'WA', '98033', 'USA', '(206) 555-3412', '3355', 'Janet has a BS degree in chemistry from Boston College.', 2);
INSERT INTO employees VALUES (4, 'Peacock', 'Margaret', 'Sales Representative', 'Mrs.', '1958-09-19', '1993-05-03', '4110 Old Redmond Rd.', 'Redmond', 'WA', '98052', 'USA', '(206) 555-8122', '5176', 'Margaret holds a BA in English literature from Concordia College.', 2);
INSERT INTO employees VALUES (6, 'Suyama', 'Michael', 'Sales Representative', 'Mr.', '1963-07-02', '1993-10-17', 'Coventry House Miner Rd.', 'London', NULL, 'EC2 7JR', 'UK', '(71) 555-7773', '428', 'Michael is a graduate of Sussex University (MA economics).', 5);
INSERT INTO employees VALUES (7, 'King', 'Robert', 'Sales Representative', 'Mr.', '1960-05-29', '1994-01-02', 'Edgeham Hollow Winchester Way', 'London', NULL, 'RG1 9SP', 'UK', '(71) 555-5598', '465', 'Robert King served in the Peace Corps and traveled extensively.', 5);
INSERT INTO employees VALUES (8, 'Callahan', 'Laura', 'Inside Sales Coordinator', 'Ms.', '1958-01-09', '1994-03-05', '4726 11th Ave. N.E.', 'Seattle', 'WA', '98105', 'USA', '(206) 555-1189', '2344', 'Laura received a BA in psychology from the University of Washington.', 2);
INSERT INTO employees VALUES (9, 'Dodsworth', 'Anne', 'Sales Representative', 'Ms.', '1969-07-02', '1994-11-15', '7 Houndstooth Rd.', 'London', NULL, 'WG2 7LT', 'UK', '(71) 555-4444', '452', 'Anne has a BA degree in English from St. Lawrence College.', 5);

-- Orders (sample - 30 orders for demo)
INSERT INTO orders VALUES (10248, 'ALFKI', 5, '1996-07-04', '1996-08-01', '1996-07-16', 3, 32.38, 'Alfreds Futterkiste', 'Obere Str. 57', 'Berlin', NULL, '12209', 'Germany');
INSERT INTO orders VALUES (10249, 'ANATR', 6, '1996-07-05', '1996-08-16', '1996-07-10', 1, 11.61, 'Ana Trujillo Emparedados y helados', 'Avda. de la Constitucion 2222', 'Mexico D.F.', NULL, '05021', 'Mexico');
INSERT INTO orders VALUES (10250, 'BLAUS', 4, '1996-07-08', '1996-08-05', '1996-07-12', 2, 65.83, 'Blauer See Delikatessen', 'Forsterstr. 57', 'Mannheim', NULL, '68306', 'Germany');
INSERT INTO orders VALUES (10251, 'AROUT', 3, '1996-07-08', '1996-08-05', '1996-07-15', 1, 41.34, 'Around the Horn', '120 Hanover Sq.', 'London', NULL, 'WA1 1DP', 'UK');
INSERT INTO orders VALUES (10252, 'BLONP', 4, '1996-07-09', '1996-08-06', '1996-07-11', 2, 51.30, 'Blondel pere et fils', '24 place Kleber', 'Strasbourg', NULL, '67000', 'France');
INSERT INTO orders VALUES (10253, 'BOLID', 3, '1996-07-10', '1996-07-24', '1996-07-16', 2, 58.17, 'Bolido Comidas preparadas', 'C/ Araquil 67', 'Madrid', NULL, '28023', 'Spain');
INSERT INTO orders VALUES (10254, 'CHOPS', 5, '1996-07-11', '1996-08-08', '1996-07-23', 2, 22.98, 'Chop-suey Chinese', 'Hauptstr. 29', 'Bern', NULL, '3012', 'Switzerland');
INSERT INTO orders VALUES (10255, 'BONAP', 9, '1996-07-12', '1996-08-09', '1996-07-15', 3, 148.33, 'Bon app', '12 rue des Bouchers', 'Marseille', NULL, '13008', 'France');
INSERT INTO orders VALUES (10256, 'BERGS', 3, '1996-07-15', '1996-08-12', '1996-07-17', 2, 13.97, 'Berglunds snabbkop', 'Berguvsvagen 8', 'Lulea', NULL, 'S-958 22', 'Sweden');
INSERT INTO orders VALUES (10257, 'CENTC', 4, '1996-07-16', '1996-08-13', '1996-07-22', 3, 81.91, 'Centro comercial Moctezuma', 'Sierras de Granada 9993', 'Mexico D.F.', NULL, '05022', 'Mexico');
INSERT INTO orders VALUES (10258, 'ANATR', 1, '1996-07-17', '1996-08-14', '1996-07-23', 1, 140.51, 'Ana Trujillo Emparedados y helados', 'Avda. de la Constitucion 2222', 'Mexico D.F.', NULL, '05021', 'Mexico');
INSERT INTO orders VALUES (10259, 'CENTC', 4, '1996-07-18', '1996-08-15', '1996-07-25', 3, 3.25, 'Centro comercial Moctezuma', 'Sierras de Granada 9993', 'Mexico D.F.', NULL, '05022', 'Mexico');
INSERT INTO orders VALUES (10260, 'BOTTM', 4, '1996-07-19', '1996-08-16', '1996-07-29', 1, 55.09, 'Bottom-Dollar Markets', '23 Tsawassen Blvd.', 'Tsawassen', 'BC', 'T2F 8M4', 'Canada');
INSERT INTO orders VALUES (10261, 'CACTU', 4, '1996-07-19', '1996-08-16', '1996-07-30', 2, 3.05, 'Cactus Comidas para llevar', 'Cerrito 333', 'Buenos Aires', NULL, '1010', 'Argentina');
INSERT INTO orders VALUES (10262, 'ALFKI', 8, '1996-07-22', '1996-08-19', '1996-07-25', 3, 48.29, 'Alfreds Futterkiste', 'Obere Str. 57', 'Berlin', NULL, '12209', 'Germany');
INSERT INTO orders VALUES (10263, 'BLONP', 9, '1996-07-23', '1996-08-20', '1996-07-31', 3, 146.06, 'Blondel pere et fils', '24 place Kleber', 'Strasbourg', NULL, '67000', 'France');
INSERT INTO orders VALUES (10264, 'AROUT', 6, '1996-07-24', '1996-08-21', '1996-08-23', 3, 3.67, 'Around the Horn', '120 Hanover Sq.', 'London', NULL, 'WA1 1DP', 'UK');
INSERT INTO orders VALUES (10265, 'BLONP', 2, '1996-07-25', '1996-08-22', '1996-08-12', 1, 55.28, 'Blondel pere et fils', '24 place Kleber', 'Strasbourg', NULL, '67000', 'France');
INSERT INTO orders VALUES (10266, 'COMMI', 3, '1996-07-26', '1996-09-06', '1996-07-31', 3, 25.73, 'Comercio Mineiro', 'Av. dos Lusíadas 23', 'Sao Paulo', 'SP', '05432-043', 'Brazil');
INSERT INTO orders VALUES (10267, 'BERGS', 4, '1996-07-29', '1996-08-26', '1996-08-06', 1, 208.58, 'Berglunds snabbkop', 'Berguvsvagen 8', 'Lulea', NULL, 'S-958 22', 'Sweden');
INSERT INTO orders VALUES (10268, 'BOLID', 8, '1996-07-30', '1996-08-27', '1996-08-02', 3, 66.29, 'Bolido Comidas preparadas', 'C/ Araquil 67', 'Madrid', NULL, '28023', 'Spain');
INSERT INTO orders VALUES (10269, 'BOTTM', 5, '1996-07-31', '1996-08-14', '1996-08-09', 1, 4.56, 'Bottom-Dollar Markets', '23 Tsawassen Blvd.', 'Tsawassen', 'BC', 'T2F 8M4', 'Canada');
INSERT INTO orders VALUES (10270, 'BSBEV', 1, '1996-08-01', '1996-08-29', '1996-08-02', 1, 136.54, 'Bs Beverages', 'Fauntleroy Circus', 'London', NULL, 'EC2 5NT', 'UK');
INSERT INTO orders VALUES (10271, 'ALFKI', 6, '1996-08-01', '1996-08-29', '1996-08-30', 2, 4.54, 'Alfreds Futterkiste', 'Obere Str. 57', 'Berlin', NULL, '12209', 'Germany');
INSERT INTO orders VALUES (10272, 'ANATR', 6, '1996-08-02', '1996-08-30', '1996-08-06', 2, 98.03, 'Ana Trujillo Emparedados y helados', 'Avda. de la Constitucion 2222', 'Mexico D.F.', NULL, '05021', 'Mexico');
INSERT INTO orders VALUES (10273, 'BERGS', 3, '1996-08-05', '1996-09-02', '1996-08-12', 3, 76.07, 'Berglunds snabbkop', 'Berguvsvagen 8', 'Lulea', NULL, 'S-958 22', 'Sweden');
INSERT INTO orders VALUES (10274, 'BSBEV', 6, '1996-08-06', '1996-09-03', '1996-08-16', 1, 6.01, 'Bs Beverages', 'Fauntleroy Circus', 'London', NULL, 'EC2 5NT', 'UK');
INSERT INTO orders VALUES (10275, 'BLONP', 1, '1996-08-07', '1996-09-04', '1996-08-09', 1, 26.93, 'Blondel pere et fils', '24 place Kleber', 'Strasbourg', NULL, '67000', 'France');
INSERT INTO orders VALUES (10276, 'BOTTM', 8, '1996-08-08', '1996-08-22', '1996-08-14', 3, 13.84, 'Bottom-Dollar Markets', '23 Tsawassen Blvd.', 'Tsawassen', 'BC', 'T2F 8M4', 'Canada');
INSERT INTO orders VALUES (10277, 'CACTU', 2, '1996-08-09', '1996-09-06', '1996-08-13', 3, 125.77, 'Cactus Comidas para llevar', 'Cerrito 333', 'Buenos Aires', NULL, '1010', 'Argentina');

-- Order Details (line items for the orders above)
INSERT INTO order_details VALUES (10248, 11, 14, 12, 0);
INSERT INTO order_details VALUES (10248, 14, 23.25, 10, 0);
INSERT INTO order_details VALUES (10248, 1, 18, 5, 0);
INSERT INTO order_details VALUES (10249, 14, 23.25, 9, 0);
INSERT INTO order_details VALUES (10249, 1, 18, 40, 0);
INSERT INTO order_details VALUES (10250, 6, 25, 10, 0.05);
INSERT INTO order_details VALUES (10250, 16, 17.45, 35, 0.15);
INSERT INTO order_details VALUES (10250, 20, 81, 15, 0.15);
INSERT INTO order_details VALUES (10251, 3, 10, 20, 0.05);
INSERT INTO order_details VALUES (10251, 6, 25, 15, 0.05);
INSERT INTO order_details VALUES (10252, 1, 18, 40, 0.05);
INSERT INTO order_details VALUES (10252, 20, 81, 25, 0.05);
INSERT INTO order_details VALUES (10253, 14, 23.25, 20, 0);
INSERT INTO order_details VALUES (10253, 20, 81, 42, 0);
INSERT INTO order_details VALUES (10254, 7, 30, 15, 0);
INSERT INTO order_details VALUES (10254, 18, 62.5, 21, 0);
INSERT INTO order_details VALUES (10255, 2, 19, 20, 0);
INSERT INTO order_details VALUES (10255, 16, 17.45, 35, 0);
INSERT INTO order_details VALUES (10256, 2, 19, 15, 0);
INSERT INTO order_details VALUES (10257, 11, 21, 25, 0);
INSERT INTO order_details VALUES (10257, 12, 38, 60, 0);
INSERT INTO order_details VALUES (10258, 2, 19, 50, 0.2);
INSERT INTO order_details VALUES (10258, 5, 21.35, 65, 0.25);
INSERT INTO order_details VALUES (10258, 8, 40, 6, 0.2);
INSERT INTO order_details VALUES (10259, 13, 6, 10, 0);
INSERT INTO order_details VALUES (10260, 16, 17.45, 50, 0);
INSERT INTO order_details VALUES (10260, 20, 81, 21, 0);
INSERT INTO order_details VALUES (10261, 12, 38, 20, 0);
INSERT INTO order_details VALUES (10262, 1, 18, 12, 0.2);
INSERT INTO order_details VALUES (10262, 7, 30, 15, 0);
INSERT INTO order_details VALUES (10263, 16, 17.45, 60, 0.25);
INSERT INTO order_details VALUES (10263, 20, 81, 28, 0);
INSERT INTO order_details VALUES (10264, 2, 19, 35, 0);
INSERT INTO order_details VALUES (10265, 17, 39, 30, 0);
INSERT INTO order_details VALUES (10265, 18, 62.5, 12, 0.2);
INSERT INTO order_details VALUES (10266, 12, 38, 12, 0.05);
INSERT INTO order_details VALUES (10267, 3, 10, 50, 0);
INSERT INTO order_details VALUES (10267, 4, 22, 70, 0.15);
INSERT INTO order_details VALUES (10268, 1, 18, 10, 0);
INSERT INTO order_details VALUES (10268, 4, 22, 25, 0);
INSERT INTO order_details VALUES (10269, 5, 21.35, 40, 0.05);
INSERT INTO order_details VALUES (10270, 1, 18, 30, 0);
INSERT INTO order_details VALUES (10270, 2, 19, 25, 0);
INSERT INTO order_details VALUES (10271, 11, 21, 24, 0);
INSERT INTO order_details VALUES (10272, 1, 18, 6, 0);
INSERT INTO order_details VALUES (10272, 14, 23.25, 40, 0);
INSERT INTO order_details VALUES (10273, 10, 31, 24, 0.05);
INSERT INTO order_details VALUES (10274, 1, 18, 20, 0.05);
INSERT INTO order_details VALUES (10275, 1, 18, 12, 0.05);
INSERT INTO order_details VALUES (10276, 10, 31, 15, 0);
INSERT INTO order_details VALUES (10277, 2, 19, 20, 0);
INSERT INTO order_details VALUES (10277, 11, 21, 12, 0);

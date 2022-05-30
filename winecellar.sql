SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE Wines (
   wineID int(11) NOT NULL,
   vintage year(4) NOT NULL,
   vineyard varchar(45) NOT NULL,
   variety varchar(45) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO Wines (wineID, vintage, vineyard, variety) 
VALUES
(1, 2019, 'Philo Wines', 'Zinfandel'),
(2, 2020, 'Napa Special', 'Pinot Noir'),
(3, 2021, 'Monterey Majestic', 'Gewürztraminer'),
(4, 2020, 'Anderson Valley', 'Nerello Mascalese'),
(5, 2021, 'Confluence Vineyard', 'Chardonnay');

-- -------------------------------------------------------

CREATE TABLE Winemakers(
    winemakerID INT(11) NOT NULL,
    firstName VARCHAR(45) NOT NULL,
    lastName VARCHAR(45) NOT NULL,
    location VARCHAR(45) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO Winemakers (winemakerID, firstName, lastName, location) 
VALUES
(1, 'Alex', 'Ryan', 'Napa, CA'),
(2, 'Michael', 'Fay', 'Philo, CA'),
(3, 'Bruce', 'Zoecklein', 'Walla Walla, WA'),
(4, 'Erin', 'Amaral', 'Willamette, OR'),
(5, 'Jamie', 'Leffert', 'Santa Ynez, CA');


-- ----------------------------------------------------------

CREATE TABLE Winemaker_Details(
    winemakerDetailsID INT(11) NOT NULL,
    winemakerID INT(11) NOT NULL,
    wineID int(11) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO Winemaker_Details (winemakerDetailsID, winemakerID, wineID) 
VALUES
(1, 2, 1),
(2, 3, 1),
(3, 2, 2),
(4, 1, 3),
(5, 5, 4),
(6, 4, 4),
(7, 4, 5);

-- ---------------------------------------------------------

CREATE TABLE Invoices(
    invoiceID INT(11) NOT NULL,
    wineID INT(11) DEFAULT NULL,
    dateReceived DATE NOT NULL,
    price decimal(19,2),
    quantityGallons INT(11)
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO Invoices (invoiceID, wineType, dateReceived, price, quantityGallons) 
VALUES
(1, 4, '2022-01-15', '80000.00', 500),
(2, 5, '2022-01-15', '200000.00', 2000),
(3, 1, '2022-03-14', '500000.00', 4500),
(4, 3, '2022-03-25', '425000.00', 3750),
(5, 2, '2021-12-29', '90000.00', 650),
(6, 2, '2022-01-13', '100000.00', 750);

-- -------------------------------------------------------------

CREATE TABLE WorkOrders(
    workOrderID INT(11) NOT NULL,
    task VARCHAR(400) NOT NULL,
    winemakerID INT(11) DEFAULT NULL,
    dateOrdered DATE NOT NULL,
    status enum('Incomplete','Complete') NOT NULL DEFAULT 'Incomplete'
)ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO WorkOrders (workOrderID, task, winemakerID, dateOrdered) 
VALUES
(1, 'Take sugar readings from 9/1/2021 -> 9/15/2021 for tanks 2-10', 4, '2021-08-05'),
(2, 'Check SO2 and vineyard PWines manager with monthly update ', 1, '2021-08-12'),
(3, 'Perform pump overs in Tank Hall 4', 5, '2021-08-21'),
(4, 'Fill barrels for Michael and add notes on procedure before vacation.', 2, '2021-09-02'),
(5, 'Take samples for blending trial and document process for new mix Chardonnay', 3, '2021-09-18');


-- -----------------------------------------------------------------

ALTER TABLE Wines
   ADD PRIMARY KEY (wineID);

ALTER TABLE Winemakers
   ADD PRIMARY KEY (winemakerID);

ALTER TABLE Winemaker_Details
   ADD PRIMARY KEY (winemakerDetailsID),
   ADD KEY winemakerID (winemakerID),
   ADD KEY wineID (wineID);

ALTER TABLE Wines
   MODIFY wineID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

ALTER TABLE Winemakers
   MODIFY winemakerID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

ALTER TABLE Winemaker_Details
   MODIFY winemakerDetailsID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

ALTER TABLE Winemaker_Details
   ADD CONSTRAINT winemakerID_FK FOREIGN KEY (winemakerID) REFERENCES Winemakers(winemakerID) ON DELETE CASCADE,
   ADD CONSTRAINT wineID_FK FOREIGN KEY (wineID) REFERENCES Wines(wineID) ON DELETE CASCADE;


ALTER TABLE Invoices
   ADD PRIMARY KEY (invoiceID),
   ADD KEY wineType (wineType);

ALTER TABLE WorkOrders
   ADD PRIMARY KEY (workOrderID),
   ADD KEY winemaker (winemaker);

ALTER TABLE WorkOrders
   MODIFY workOrderID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

ALTER TABLE WorkOrders
   ADD CONSTRAINT `WorkOrders_ibfk_1` FOREIGN KEY (`winemaker`) REFERENCES `Winemakers` (`winemakerID`) ON DELETE SET NULL;

ALTER TABLE Invoices
   MODIFY invoiceID int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

ALTER TABLE Invoices
   ADD CONSTRAINT `Invoices_ibfk_1` FOREIGN KEY (`wineType`) REFERENCES `Wines` (`wineID`) ON DELETE SET NULL;

COMMIT;

SET FOREIGN_KEY_CHECKS=0;

SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE Wines(
    wineID INT(11) AUTO_INCREMENT,
    vintage year(4) NOT NULL,
    vineyard VARCHAR(45) NOT NULL,
    variety VARCHAR(45) NOT NULL,
    PRIMARY KEY(wineID)
);

CREATE TABLE Winemakers(
    winemakerID INT(11) AUTO_INCREMENT,
    firstName VARCHAR(45) NOT NULL,
    lastName VARCHAR(45) NOT NULL,
    location VARCHAR(45) NOT NULL,
    PRIMARY KEY(winemakerID)
);

CREATE TABLE Winemaker_Details(
    winemakerDetailsID INT(11) NOT NULL AUTO_INCREMENT,
    winemakerID INT(11) NOT NULL,
    wineID int(11) NOT NULL,
    PRIMARY KEY(winemakerDetailsID),
    FOREIGN KEY (winemakerID) REFERENCES Winemakers(winemakerID)
    ON DELETE CASCADE,
    FOREIGN KEY (wineID) REFERENCES Wines(wineID)
    ON DELETE CASCADE
);

CREATE TABLE Invoices(
    invoiceID INT(11) NOT NULL AUTO_INCREMENT,
    wineID INT(11) NULL,
    dateReceived DATE NOT NULL,
    price decimal(19,2),
    quantityGallons INT(11),
    PRIMARY KEY(invoiceID),
    CONSTRAINT wineID_FK FOREIGN KEY (wineID) REFERENCES Wines(wineID)
    ON DELETE SET NULL
);

CREATE TABLE WorkOrders(
    workOrderID INT(11) NOT NULL AUTO_INCREMENT,
    task VARCHAR(400) NOT NULL,
    winemakerID INT(11) NULL,
    dateOrdered DATE NOT NULL,
    status enum('Incomplete','Complete') NOT NULL DEFAULT 'Incomplete',
    PRIMARY KEY(workOrderID),
    CONSTRAINT winemakerID_FK FOREIGN KEY (winemakerID) REFERENCES Winemakers(winemakerID)
    ON DELETE SET NULL
    ON UPDATE SET NULL
);

--
-- Add Data 
--

INSERT INTO Wines (vintage, vineyard, variety) 
VALUES
(2019, 'Philo Wines', 'Zinfandel'),
(2020, 'Napa Special', 'Pinot Noir'),
(2021, 'Monterey Majestic', 'Gewürztraminer'),
(2020, 'Anderson Valley', 'Nerello Mascalese'),
(2021, 'Confluence Vineyard', 'Chardonnay');

INSERT INTO Winemakers (firstName, lastName, location) 
VALUES
('Alex', 'Ryan', 'Napa, CA'),
('Michael', 'Fay', 'Philo, CA'),
('Bruce', 'Zoecklein', 'Walla Walla, WA'),
('Erin', 'Amaral', 'Willamette, OR'),
('Jamie', 'Leffert', 'Santa Ynez, CA');

INSERT INTO Invoices (wineID, dateReceived, price, quantityGallons) 
VALUES
(4, '2022-01-15', '80000.00', 500),
(5, '2022-01-15', '200000.00', 2000),
(1, '2022-03-14', '500000.00', 4500),
(3, '2022-03-25', '425000.00', 3750),
(2, '2021-12-29', '90000.00', 650),
(2, '2022-01-13', '100000.00', 750);


INSERT INTO Winemaker_Details (winemakerID, wineID) 
VALUES
(2, 1),
(3, 1),
(2, 2),
(1, 3),
(5, 4),
(4, 4),
(4, 5);


INSERT INTO WorkOrders (task, winemakerID, dateOrdered) 
VALUES
('Take sugar readings from 9/1/2021 -> 9/15/2021 for tanks 2-10', 4, '2021-08-05'),
('Check SO2 and vineyard PWines manager with monthly update ', 1, '2021-08-12'),
('Perform pump overs in Tank Hall 4', 5, '2021-08-21'),
('Fill barrels for Michael and add notes on procedure before vacation.', 2, '2021-09-02'),
('Take samples for blending trial and document process for new mix Chardonnay', 3, '2021-09-18');

SET FOREIGN_KEY_CHECKS=1;

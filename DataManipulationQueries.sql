-- Data Manipulation Queries for CellarTracker
-- Written by Group 3: Victoria Patterson & Alexandra Sciocchetti

--
-- Wines Entity
-- get all info from Wines to populate the main page
SELECT wineID, vintage, vineyard, variety FROM Wines;

-- add a wine
INSERT INTO Wines (vintage, vineyard, variety) 
VALUES (:vintageInput, :vineyardInput, :varietyInput);

-- delete a wine
DELETE FROM Wines WHERE wineID = :wineID_selected_from_wines_page

-- search for a wine
SELECT * FROM Wines WHERE MATCH (vineyard, variety) AGAINST ('{search_query[2:]}' IN NATURAL LANGUAGE MODE)


--
-- WorkOrders Entity
-- get (read) all WorkOrders with winemaker first name and last name to list 
SELECT WorkOrders.workOrderID, WorkOrders.task, Winemakers.winemakerID, Winemakers.firstName, Winemakers.lastName, WorkOrders.dateOrdered, WorkOrdersstatus 
AS winemaker FROM WorkOrders 
LEFT JOIN Winemakers ON winemaker = Winemakers.winemakerID;


-- add a workorder
INSERT INTO WorkOrders (winemaker, task, dateOrdered)
VALUES (:winemaker_from_dropdown_Input, :taskInput, :dateOrderedInput)

-- update/edit Workorder based on Edit Workorder form
SELECT * FROM WorkOrders WHERE workOrderID = workOrderID_from_dropdown;
-- if winemaker = NULL
UPDATE WorkOrders SET WorkOrders.task = :taskInput, WorkOrders.winemaker = NULL, WorkOrders.dateOrdered = :dateOrderedInput, WorkOrders.status = :statusInput WHERE WorkOrders.workOrderID = :workOrderID_selected
-- if winemaker is not NULL
UPDATE WorkOrders SET WorkOrders.task = :taskInput, WorkOrders.winemaker = :winemaker_from_dropdown, WorkOrders.dateOrdered = :dateOrderedInput, WorkOrders.status = :statusInput WHERE WorkOrders.workOrderID = :workOrderID_selected

-- delete a Workorder
DELETE FROM WorkOrders WHERE WorkOrderID =:workOrderID_selected_from_workOrders_page


--
-- Invoices Entity
-- get all Invoices with wine vinyard and variety to list
SELECT Invoices.invoiceID, Wines.wineID, Invoices.dateReceived, Invoices.price, Invoices.quantityGallons, Wines.vineyard, Wines.Variety 
AS wineType FROM Invoices 
LEFT JOIN Wines ON wineType = Wines.wineID;

-- create new invoice
INSERT INTO Invoices (wineType, dateReceived, price, quantityGallons)
VALUES (:wineType_from_dropdown_Input, :dateReceivedInput, :priceInput, :quantityGallonsInput)

-- delete an invoice
DELETE FROM Invoices WHERE invoiceID = :invoiceID_selected

--
-- Winemakers Entity
-- get all Winemakers firstName, lastName, and location
SELECT winemakerID, firstName, lastName, location FROM Winemakers;

-- add a winemaker
INSERT INTO Winemakers (firstName, lastName, location)
VALUES (:firstNameInput, :lastNameInput, :locationInput)

-- update information about a winemaker
SELECT * FROM Winemakers WHERE winemakerID = :winemakerID_selected
-- Once winemakerID has been selected, update details
UPDATE Winemakers SET Winemakers.firstName = :firstNameInput, Winemakers.lastName = :lastNameInput, Winemakers.location = :locationInput WHERE Winemakers.winemakerID = :winemakerID_selected

-- delete a winemaker
DELETE FROM Winemakers WHERE winemakerID =:winemakerID_selected_from_Winemakers_page;

--
--Winemaker_Details (Intersection Table)
-- get all winemaker_details, including winemaker first and last name and location of winery
SELECT Winemakers.firstName, Winemakers.lastName, Wines.variety, Wines.vineyard, Winemaker_Details.winemakerID, Winemaker_Details.wineID
FROM Winemaker_Details
INNER JOIN Winemakers ON Winemakers.winemakerID = Winemaker_Details.winemakerID
INNER JOIN Wines ON Wines.wineID = Winemaker_Details.wineID;

-- add new relationship (insert)
INSERT INTO Winemaker_Details (wineID, winemakerID)
VALUES (:wineID_from_dropdown_Input, :winemakerID_from_dropdown_Input)

-- update relationship (either change wineID or winemakerID)
SELECT * FROM Winemaker_Details WHERE winemakerDetailsID = :winemakerDetailsID_selected
UPDATE Winemaker_Details SET winemakerID =: winemakerID_from_dropdown_Input, wineID =: wineID_from_dropdown_Input WHERE Winemaker_Details.winemakerDetailsID = :winemakerDetailsID_selected;

-- delete relationship
DELETE FROM Winemaker_Details WHERE winemakerDetailsID = :winemakerDetailsID_selected






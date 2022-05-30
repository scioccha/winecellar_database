from logging.config import IDENTIFIER
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_scioccha'
app.config['MYSQL_PASSWORD'] = '0474'  # last 4 of onid
app.config['MYSQL_DB'] = 'cs340_scioccha'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# Routes
# Homepage routes to /wines page
@app.route("/")
def home():
    return render_template("index.html")


################# route for wines page ##################

@app.route("/wines", methods=["POST", "GET"])
def wines():
    # insert a new wine
    if request.method == "POST":
        if request.form.get("Add_Wine"):
            # grab user form inputs
            vintage = request.form["vintage"]
            vineyard = request.form["vineyard"]
            variety = request.form["variety"]

            # add data
            query = "INSERT INTO Wines (vintage, vineyard, variety) VALUES (%s, %s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (vintage, vineyard, variety))
            mysql.connection.commit()

            # redirect bback to wines
            return redirect("/wines")

    # display wines using query to grab all wines in Wines
    if request.method == "GET":
        search_query = request.query_string.decode()
        if search_query:
            query = f"SELECT * FROM Wines WHERE MATCH (vineyard, variety) AGAINST ('{search_query[2:]}' IN NATURAL LANGUAGE MODE);"
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()
        else:
            query1 = "SELECT wineID, vintage, vineyard, variety FROM Wines"
            cur = mysql.connection.cursor()
            cur.execute(query1)
            data = cur.fetchall()
        return render_template("wines.j2", data=data)


# route for delete wines functionality
@app.route("/delete_wines/<int:wineID>")
def delete_wine(wineID):
    # delete based on wineID value
    query = "DELETE FROM Wines WHERE wineID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (wineID,))
    mysql.connection.commit()

    # redirect back to wines
    return redirect("/wines")


###################### END route for wines page ######################


###################### route for invoices page #######################
@app.route("/invoices", methods=["POST", "GET"])
def invoices():
    # insert a new invoice
    if request.method == "POST":
        if request.form.get("Add_Invoice"):
            # grab user form inputs
            wineType = request.form["wineType"]
            dateReceived = request.form["dateReceived"]
            price = request.form["price"]
            quantityGallons = request.form["quantityGallons"]

            if wineType == "":
                # add data
                query = "INSERT INTO Invoices (dateReceived, price, quantityGallons) VALUES (%s, %s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (dateReceived, price, quantityGallons))
                mysql.connection.commit()

            else:
                # add data
                query = "INSERT INTO Invoices (wineType, dateReceived, price, quantityGallons) VALUES (%s, %s, %s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (wineType, dateReceived, price, quantityGallons))
                mysql.connection.commit()

            return redirect("/invoices")

    if request.method == "GET":
        # mySQL query to grab all invoices in Invoices
        query = "SELECT invoiceID, Wines.wineID, dateReceived, price, quantityGallons, Wines.vineyard, Wines.Variety AS wineType FROM Invoices LEFT JOIN Wines ON wineType = Wines.wineID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab winemaker ids for our dropdown
        query2 = "SELECT wineID FROM Wines;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        wineID_data = cur.fetchall()

        return render_template("invoices.j2", data=data, wineIDs=wineID_data)

# route for delete invoice functionality
@app.route("/delete_invoices/<int:invoiceID>")
def delete_invoices(invoiceID):
    # delete based on invoiceID value
    query = "DELETE FROM Invoices WHERE invoiceID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (invoiceID,))
    mysql.connection.commit()

    return redirect("/invoices")


###################### END route for invoices page ##########################


###################### route for winemakers page ############################
@app.route("/winemakers", methods=["POST", "GET"])
def winemakers():
    # insert new winemaker
    if request.method == "POST":
        if request.form.get("Add_Winemaker"):
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            location = request.form["location"]

            # add data
            query = "INSERT INTO Winemakers (firstName, lastName, location) VALUES (%s, %s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, location))
            mysql.connection.commit()

            return redirect("/winemakers")

    # Display all winemaker data
    if request.method == "GET":
        query = "SELECT winemakerID, firstName, lastName, location FROM Winemakers"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("winemakers.j2", data=data)


# Delete a winemaker. Function is passed winemakerID value
@app.route("/delete_winemakers/<int:winemakerID>")
def delete_winemaker(winemakerID):
    query = "DELETE FROM Winemakers WHERE winemakerID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (winemakerID,))
    mysql.connection.commit()
    return redirect("/winemakers")


# Edit a current winemaker based on winemakerID
@app.route("/edit_winemakers/<int:winemakerID>", methods=["POST", "GET"])
def edit_winemaker(winemakerID):
    if request.method == "GET":
        query = "SELECT * FROM Winemakers WHERE winemakerID = %s" % (winemakerID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit_winemakers.j2", data=data)

    # Main update functionality, used if user clicks on the 'Edit Winemaker' button
    if request.method == "POST":
        if request.form.get("Edit_Winemaker"):
            # grab user form inputs
            winemakerID = request.form["winemakerID"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            location = request.form["location"]

            query = "UPDATE Winemakers SET Winemakers.firstName = %s, Winemakers.lastName = %s, Winemakers.location = %s WHERE Winemakers.winemakerID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, location, winemakerID))
            mysql.connection.commit()
            return redirect("/winemakers")


############################## END route for winemakers page #######################


############################## route for workOrders page ###########################
@app.route("/workOrders", methods=["POST", "GET"])
def workOrders():
    # insert new workOrder
    if request.method == "POST":
        if request.form.get("Add_WorkOrder"):
            task = request.form["task"]
            winemaker = request.form["winemaker"]
            dateOrdered = request.form["dateOrdered"]

            if winemaker == "":
                # add data
                query = "INSERT INTO WorkOrders (task, dateOrdered) VALUES (%s,%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (task, dateOrdered))
                mysql.connection.commit()
            else:
                # add data
                query = "INSERT INTO WorkOrders (task, winemaker, dateOrdered) VALUES (%s,%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (task, winemaker, dateOrdered))
                mysql.connection.commit()

            return redirect("/workOrders")

    # Display all workOrder data
    if request.method == "GET":
        query = "SELECT workOrderID, task, Winemakers.winemakerID, Winemakers.firstName, Winemakers.lastName, dateOrdered, status AS winemaker FROM WorkOrders LEFT JOIN Winemakers ON winemaker = Winemakers.winemakerID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab winemaker ids for our dropdown
        query2 = "SELECT winemakerID FROM Winemakers;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        winemakerID_data = cur.fetchall()

        return render_template("workOrders.j2", data=data, winemakerIDs=winemakerID_data)


# Edit a current workOrder based on workOrderID
@app.route("/edit_workOrder/<int:workOrderID>", methods=["POST", "GET"])
def edit_workOrder(workOrderID):
    if request.method == "GET":
        query = "SELECT * FROM WorkOrders WHERE workOrderID = %s" % (workOrderID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab winemaker ids for our dropdown
        query2 = "SELECT winemakerID FROM Winemakers;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        winemakerID_data = cur.fetchall()

        return render_template("edit_workOrders.j2", data=data, winemakerIDs=winemakerID_data)

    # Main update functionality, used if user clicks on the 'Edit Work Order' button
    if request.method == "POST":
        if request.form.get("edit_workOrder"):
            # grab user form inputs
            workOrderID = request.form["workOrderID"]
            task = request.form["task"]
            winemaker = request.form["winemaker"]
            dateOrdered = request.form["dateOrdered"]
            status = request.form['status']
            if winemaker == "":
                query = "UPDATE WorkOrders SET WorkOrders.task = %s, WorkOrders.winemaker = NULL, WorkOrders.dateOrdered = %s, WorkOrders.status = %s WHERE WorkOrders.workOrderID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (task, dateOrdered, status, workOrderID))
                mysql.connection.commit()

            else:
                query = "UPDATE WorkOrders SET WorkOrders.task = %s, WorkOrders.winemaker = %s, WorkOrders.dateOrdered = %s, WorkOrders.status = %s WHERE WorkOrders.workOrderID = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (task, winemaker, dateOrdered, status, workOrderID))
                mysql.connection.commit()
            return redirect("/workOrders")

        # route for delete workOrder functionality


@app.route("/delete_workOrder/<int:workOrderID>")
def delete_workOrder(workOrderID):
    # delete based on invoiceID value
    query = "DELETE FROM WorkOrders WHERE workOrderID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (workOrderID,))
    mysql.connection.commit()

    return redirect("/workOrders")


############################ END route for workorders page ################################

############################## route for Winemaker Details page ###########################

@app.route("/winemaker_details", methods=["POST", "GET"])
def winemaker_details():
    # insert a assignment
    if request.method == "POST":
        if request.form.get("Add_Details"):
            # grab user form inputs
            winemakerID = request.form["winemakerID"]
            wineID = request.form["wineID"]

            # add data
            query = "INSERT INTO Winemaker_Details (winemakerID, wineID) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (winemakerID, wineID))
            mysql.connection.commit()

            return redirect("/winemaker_details")

    # display all winemaker_details including first and last name, vineyard and variety of wine
    if request.method == "GET":
        query = "SELECT Winemaker_Details.winemakerDetailsID, Winemakers.firstName, Winemakers.lastName, Wines.variety, Wines.vineyard, Winemaker_Details.winemakerID, Winemaker_Details.wineID FROM Winemaker_Details INNER JOIN Winemakers ON Winemakers.winemakerID = Winemaker_Details.winemakerID INNER JOIN Wines ON Wines.wineID = Winemaker_Details.wineID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab winemaker ids for our dropdown
        query2 = "SELECT winemakerID FROM Winemakers;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        winemakerID_data = cur.fetchall()

        # mySQL query to grab winemaker ids for our dropdown
        query3 = "SELECT wineID FROM Wines;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        wineID_data = cur.fetchall()

        return render_template("winemaker_details.j2", data=data, winemakerIDs=winemakerID_data, wineIDs=wineID_data)

@app.route("/delete_winemaker_details/<int:winemakerDetailsID>")
def delete_winemaker_details(winemakerDetailsID):
    query = "DELETE FROM Winemaker_Details WHERE winemakerDetailsID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (winemakerDetailsID,))
    mysql.connection.commit()

    # redirect back to wines
    return redirect("/winemaker_details")

@app.route("/edit_winemaker_details/<int:winemakerDetailsID>", methods=["POST", "GET"])
def edit_winemaker_details(winemakerDetailsID):
    if request.method == "GET":
        query = "SELECT * FROM Winemaker_Details WHERE winemakerDetailsID = %s" % (winemakerDetailsID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab winemaker ids for our dropdown
        query2 = "SELECT winemakerID FROM Winemakers;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        winemakerID_data = cur.fetchall()

        # mySQL query to grab winemaker ids for our dropdown
        query3 = "SELECT wineID FROM Wines;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        wineID_data = cur.fetchall()

        return render_template("edit_winemaker_details.j2", data=data, winemakerIDs = winemakerID_data, wineIDs = wineID_data)

    # Main update functionality, used if user clicks on the 'Edit Winemaker' button
    if request.method == "POST":
        if request.form.get("Edit_Winemaker_Details"):
            # grab user form inputs
            winemakerDetailsID = request.form["winemakerDetailsID"]
            winemakerID = request.form["winemakerID"]
            wineID = request.form["wineID"]

            query = "UPDATE Winemaker_Details SET Winemaker_Details.winemakerID = %s, Winemaker_Details.wineID = %s WHERE Winemaker_Details.winemakerDetailsID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (winemakerID, wineID, winemakerDetailsID))
            mysql.connection.commit()
            return redirect("/winemaker_details")

if __name__ == "__main__":
    app.run(port=5227, debug=True)
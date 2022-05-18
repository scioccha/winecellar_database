from logging.config import IDENTIFIER
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_pattersv'
app.config['MYSQL_PASSWORD'] =  '7058'#last 4 of onid
app.config['MYSQL_DB'] = 'cs340_pattersv'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# Routes
# Homepage routes to /wines page
@app.route("/")
def home():
    return redirect("/wines")


###### route for wines page ######

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
        query = "SELECT wineID, vintage, vineyard, variety FROM Wines"
        cur = mysql.connection.cursor()
        cur.execute(query)
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

###### END route for wines page ######

###### route for invoices page ######
@app.route("/invoices", methods=["POST", "GET"])
def invoices():
    # Separate out the request methods, in this case this is for a POST
    # insert a new wine
    if request.method == "POST":
        if request.form.get("Add_Invoice"):

            # grab user form inputs
            dateReceived = request.form["Date Received"]
            price = request.form["Price"]
            quantityGallons = request.form["Quantity (gallons)"]

            # add data
            query = "INSERT INTO Invoices (dateReceived, price, quantityGallons) VALUES (%s, %s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (dateReceived, price, quantityGallons))
            mysql.connection.commit()


            # redirect back to people page
            return redirect("/invoices")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all wines in Wines
        query = "SELECT invoiceID, wineID, dateReceived, price, quantityGallons FROM Invoices"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("invoices.j2", data=data)

###### END route for invoices page ######




# route for winenakers page
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


if __name__ == "__main__":
    app.run(port=13227, debug=True)

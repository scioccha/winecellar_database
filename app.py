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
# have homepage route to /people by default for convenience, generally this will be your home route with its own template
@app.route("/")
def home():
    return redirect("/wines")


###### route for wines page ######

@app.route("/wines", methods=["POST", "GET"])
def wines():
    # Separate out the request methods, in this case this is for a POST
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


            # redirect back to people page
            return redirect("/wines")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all wines in Wines
        query = "SELECT wineID, vintage, vineyard, variety FROM Wines"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("wines.j2", data=data)


# route for delete functionality
# we want to pass the 'id' value of that wine on button click (see HTML) via the route
@app.route("/delete_wines/<int:wineID>")
def delete_wine(wineID):
    # mySQL query to delete the person with our passed id
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





# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=1227, debug=True)
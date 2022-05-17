from logging.config import IDENTIFIER
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_scioccha'
app.config['MYSQL_PASSWORD'] = '0474' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_scioccha'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes
# have homepage route to /people by default for convenience, generally this will be your home route with its own template
@app.route("/")
def home():
    return redirect("/wines")


# route for wines page
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



# route for wines page
@app.route("/winemakers", methods=["POST", "GET"])
def winemakers():
    # Separate out the request methods, in this case this is for a POST
    # insert a new wine
    if request.method == "POST":
        if request.form.get("Add_Winemaker"):

            # grab user form inputs
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            location = request.form["location"]

            # add data
            query = "INSERT INTO Winemakers (firstName, lastName, location) VALUES (%s, %s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, location))
            mysql.connection.commit()


            # redirect back to people page
            return redirect("/winemakers")

    # Grab bsg_people data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all wines in Wines
        query = "SELECT winemakerID, firstName, lastName, location FROM Winemakers"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("winemakers.j2", data=data)


@app.route("/delete_winemakers/<int:winemakerID>")
def delete_winemaker(winemakerID):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Winemakers WHERE winemakerID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (winemakerID,))
    mysql.connection.commit()

    # redirect back to wines
    return redirect("/winemakers")

# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=5227, debug=True)
from flask import Flask, render_template, url_for, request, redirect, session, Response
import mysql.connector

import re

app = Flask(__name__)

try:
    mydb = mysql.connector.connect(host="localhost", port=3306, user="root", password="", database="ics_project")
    print("--------------------------------------------------")
    print("[DONE]   CONNECTED SUCCESSFULLY!!")
    print("--------------------------------------------------")
except:
    print("--------------------------------------------------")
    print("[WARN]   CONNECTION FAILED")
    print("--------------------------------------------------")


@app.route("/", methods=['GET'])
def Home():
    return render_template("home.html")


@app.route("/cross-site", methods=['GET'])
def XSSInjection():
    return render_template("xss.html")


@app.route("/sql", methods=['GET','POST'])
def SqlInjection():                                #  ' OR 1=1 #
    result = ""
    if request.method == 'POST':
        Uname = request.form.get("user")
        Upass = request.form.get("pass")
        try:
            mycursor = mydb.cursor()
            sql = "SELECT * FROM app_users WHERE username = '{0}' AND password = '{1}'".format(Uname, Upass)
            print(sql)
            mycursor.execute(sql)
            response = mycursor.fetchall()
            print(response)
            if(len(response) != 0):
                result = "Sucessfully LoggedIn"
            else:
                result = "Invalid Crediantial"
        except:
            result = "Server Error"
    return render_template("sql.html", msg=result)


@app.route("/secure_sql", methods=['GET','POST'])
def Secure_Sql():
    result = ""
    if request.method == 'POST':
        regex = re.compile('[_!#$%^&*()<>?/\|}{~:]')
        Uname = request.form.get("User")
        Upass = request.form.get("Pass")
        if(regex.search(Uname) != None or regex.search(Upass) != None):
            result = "Invalid Crediantial"
        elif(len(Upass) < 8):
            result = "pasword must contain 8-characters."
        else:
            try:
                mycursor = mydb.cursor()
                sql = "SELECT * FROM app_users WHERE username = '{0}' AND password = '{1}'".format(Uname, Upass)
                print(sql)
                mycursor.execute(sql)
                response = mycursor.fetchall()
                print(response)
                if(len(response) == 1):
                    result = "Sucessfully LoggedIn"
                else:
                    result = "Invalid Crediantial"
            except:
                result = "Server Error"
    return render_template("sql.html", msg=result)


@app.errorhandler(403)
def error403(error):
    return render_template("error.html", error=403, head="ACCESS DENIED! IT LOOKS LIKE YOU'RE LOST", tail="Sorry, but you don't have permission to access requested page."), 403

@app.errorhandler(404)
def error404(error):
    return render_template("error.html", error=404, head="Oops!! YOU JUST MISSED THIS PAGE", tail="Hakuna-Matata! Try searching for something else."), 404

@app.errorhandler(405)
def error403(error):
    return render_template("error.html", error=405, head="UNFORTUNATELY, SOMETHING HAS GONE WRONG", tail="We're unable to fulfill your reqest. Try to reload page again."), 405

@app.errorhandler(500)
def error500(error):
    return render_template("error.html", error=500, head="SORRY :( OUR SERVER IS ON A BREAK", tail="It's not you - it's we, We have a problem. Please visit again later."), 500

if __name__=="__main__":
    app.run(debug=True)

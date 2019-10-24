from flask import Flask, render_template, request, redirect
import mysql.connector
#===============================import dingen==================================#
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "usbw",
    database = "applicatie"

)

mycursor = mydb.cursor()

app = Flask(__name__)
#==============================maakt connectie met de database=================#

@app.route('/')
def index():
    return render_template ("index.html")

@app.route('/edit/<string:id>/',  methods=['GET'])
def edit_functie(id):
    global idnow
    idnow = id
    sql = "SELECT * from servers WHERE ID = " + idnow
    mycursor.execute(sql)
    data = mycursor.fetchall()

    return render_template('edit_functie.html', data=data)

@app.route('/edit_now/',  methods=['POST'])
def edit_now():
    Start = '"' + request.form['Start'] + '"'
    Eind = '"' + request.form['Eind'] + '"'
    StudentNummer = '"' + request.form['StudentNummer'] + '"'

    sql = "UPDATE servers SET Start = " + Start + " WHERE id = " + idnow
    mycursor.execute(sql)
    sql = "UPDATE servers SET Eind = " + Eind + " WHERE id = " + idnow
    mycursor.execute(sql)
    sql = "UPDATE servers SET StudentNummer = " + StudentNummer + " WHERE id = " + idnow
    mycursor.execute(sql)

    mydb.commit()
    return redirect('http://localhost/rekkenlijst')

@app.route('/del/<string:id>/',  methods=['GET'])
def del_now(id):
    global idnow
    idnow = id
    var = ("", idnow)
    sql = "UPDATE servers SET Start = %s WHERE id = %s"
    mycursor.execute(sql, var)
    sql = "UPDATE servers SET Eind = %s WHERE id = %s"
    mycursor.execute(sql, var)
    sql = "UPDATE servers SET StudentNummer = %s WHERE id = %s"
    mycursor.execute(sql, var)

    mydb.commit()
    return redirect('http://localhost/rekkenlijst')


@app.route('/rekkenlijst')
def rekkenlijst():
    try:
        mycursor.execute("SELECT * from servers")
        data = mycursor.fetchall()

    except Exception as e:
        (str(e))
    return render_template ("rekkenlijst.html", data = data)



@app.route('/registratie_formulier', methods=["GET", "POST"])
def registratie_formulier():
    if request.method == "POST":
        Servernaam = request.form["Servernaam"]
        Start = request.form["Start"]
        Eind = request.form["Eind"]
        StudentNummer = request.form["StudentNummer"]
        query = "INSERT INTO servers (Servernaam, Start, Eind, StudentNummer) Values (%s, %s, %s, %s)"
        val= (Servernaam, Start, Eind, StudentNummer)
        mycursor.execute(query, val, )
        mydb.commit()
    return render_template ("registratie_formulier.html")




@app.route('/info')
def info():
    return render_template ("about.html")


@app.route('/lid_bijwerken')
def lid_bijwerken():
    return render_template ("lid_bijwerken.html")


if __name__ == '__main__':
    app.run(debug = True, port=80)

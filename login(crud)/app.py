from flask import*
import secrets
import mysql.connector

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="projectx",
    password="")

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/aksi_login', methods =["POST", "GET"])
def aksi_login():
    cursor = mydb.cursor()
    query = ("select * from user where username = %s and password = md5(%s)")
    data = (request.form['username'], request.form['password'],)
    cursor.execute( query, data )
    value = cursor.fetchone()

    username = request.form['username']
    if value:
        session["user"] = username
        return redirect(url_for('admin'))
    else:
        return f"salah !!!"

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route('/admin')
def admin():
    if session.get("user"):
        return render_template("admin.html")
    else:
        return redirect(url_for("home"))

@app.route('/simpan', methods = ["POST", "GET"] )
def simpan():
    if session.get("user"):
        cursor = mydb.cursor()
        id = request.form["id"]
        nama_brand = request.form["nama_brand"]
        cpu = request.form["cpu"]
        tahun_produksi = request.form["tahun_produksi"]
        seri = request.form["seri"]
        query = ("insert into Handphone values( %s, %s, %s, %s, %s)")
        data = ( id, nama_brand, cpu, tahun_produksi, seri)
        cursor.execute( query, data )
        mydb.commit()
        cursor.close()
        return redirect("/tampil")
    else:
        return redirect(url_for("home"))

@app.route('/tampil')
def tampil():
    if session.get("user"):
        cursor = mydb.cursor()
        cursor.execute("select * from Handphone")
        data = cursor.fetchall()
        return render_template('tampil.html',data=data) 
    else:
        return redirect(url_for("home"))
    
@app.route('/hapus/<id>')
def hapus(id):
    if session.get("user"):
        cursor = mydb.cursor()
        query = ("delete from Handphone where id = %s")
        data = (id,)
        cursor.execute( query, data )
        mydb.commit()
        cursor.close()
        return redirect('/tampil')
    else:
        return redirect(url_for("home"))
    

@app.route('/update/<id>')
def update(id):
    if session.get("user"):
        cursor = mydb.cursor()
        query = ("select * from Handphone where id = %s")
        data = (id,)
        cursor.execute( query, data )
        value = cursor.fetchone()
        return render_template('update.html',value=value) 
    else:
        return redirect(url_for("home"))
    

@app.route('/aksiupdate', methods = ["POST", "GET"] )
def aksiupdate():
    if session.get("user"):
        cursor = mydb.cursor()
        id = request.form["id"]
        nama_brand = request.form["nama_brand"]
        cpu = request.form["cpu"]
        tahun_produksi = request.form["tahun_produksi"]
        seri = request.form["seri"]
        query = ("update Handphone setwhere nama_brand = %s, cpu = %s, tahun_produksi = %s, seri = %s")
        data = (  nama_brand, cpu,tahun_produksi,seri)
        cursor.execute( query, data )
        mydb.commit()
        cursor.close()
        return redirect('/tampil')
    else:
        return redirect(url_for("home"))
    

if __name__ == "__main__":
    app.run(debug=True)
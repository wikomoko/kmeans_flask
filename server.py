from flask import Flask,render_template,session,url_for,request,redirect,jsonify,make_response
import csv,io
import mysql.connector as connection
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from datetime import datetime
from sklearn.metrics import davies_bouldin_score

app = Flask(__name__)

app.secret_key = '1911500583'

db = connection.connect(
    host="localhost",
    user="root",
    password="root",
    database="kmeans_ta_flask"
 )

@app.route('/')
def index():
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/login',methods=['POST','GET'])
def login():
    pesan = 'akun tidak ada'
    if request.method == 'GET':
        if session.get('sudah_login'):
            return redirect(url_for('home'))
        return render_template('pages/login.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor(dictionary=True)
        sql = 'SELECT * FROM users WHERE username = %s AND password = %s'
        cursor.execute(sql,(username,password))
        account = cursor.fetchone()
        # print(account)
        cursor.close()
        db.commit()
        if account :
            session['sudah_login'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            pesan = "Sepertinya user / pass salah / akun tidak ada"
            return render_template('pages/login.html',pesan=pesan)
        

@app.route('/home',methods=['POST','GET'])
def home():
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    pesan = ''
    status = False
    if request.method == 'GET':
        cursor = db.cursor(dictionary=True)
        sql = 'SELECT * FROM dataset'
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        cursor.close()
        # db.commit()   
        return render_template('pages/home.html',data=results)

    if request.method == 'POST':
        file = request.files['file']
        if file :
            # print('ada isi')
            muat_data = io.StringIO(file.stream.read().decode('UTF-8'), newline=None)
            baca_csv = csv.reader(muat_data)
            next(baca_csv)
            for baris in baca_csv:
                cursor = db.cursor()
                sql = "INSERT INTO dataset (sintaid, nidn, nama, afiliasi, prodi, pendidikan, jabatan, gelar_depan, gelar_belakang, sinta_overall_v2, sinta_3y_v2, sinta_overall_v3, sinta_3y_v3, afiliasi_overall, afiliasi_3y, dok_scopus, sit_scopus, dok_sit_scopus, h_i_scopus, g_i_scopus, i10_i_scopus, dok_gs, sit_gs, dok_sit_gs, h_i_gs, g_i_gs, i10_i_gs, dok_wos, sit_wos, dok_sit_wos, h_i_wos, g_i_wos, i10_i_wos, dok_garuda, sit_garuda,dok_sit_garuda, stat_aktif, stat_verif) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                val = (baris[0],baris[1],baris[2],baris[3],baris[4],baris[5],baris[6],baris[7],baris[8],baris[9],baris[10],baris[11],baris[12],baris[13],baris[14],baris[15],baris[16],baris[17],baris[18],baris[19],baris[20],baris[21],baris[22],baris[23],baris[24],baris[25],baris[26],baris[27],baris[28],baris[29],baris[30],baris[31],baris[32],baris[33],baris[34],baris[35],baris[36],baris[37])

                cursor.execute(sql, val)
                db.commit()
                

    return redirect(url_for('index'))
    

@app.route('/elbow')
def elbow():
    if not session.get('sudah_login'):
        return redirect(url_for('index'))
    return render_template('pages/elbow.html')

@app.route('/hitung_elbow',methods=['POST','GET'])
def hitung_elbow():
    if request.method == 'POST':
        klaster = int(request.form['klaster'])

        tarik_data = pd.read_sql('SELECT sinta_overall_v2,sinta_3y_v2,sinta_overall_v3,sinta_3y_v3,afiliasi_overall,afiliasi_3y,dok_scopus,sit_scopus,dok_sit_scopus,h_i_scopus,g_i_scopus,i10_i_scopus,dok_gs,sit_gs,dok_sit_gs,h_i_gs,g_i_gs,i10_i_gs,dok_wos,sit_wos,dok_sit_wos,h_i_wos,g_i_wos,i10_i_wos,dok_garuda,sit_garuda,dok_sit_garuda FROM dataset',db)
        db.commit()
        wcss = []

        for i in range(1,klaster+1):
            kmeans = KMeans(n_clusters=i,n_init='auto')
            kmeans.fit_predict(tarik_data)
            wcss.append(kmeans.inertia_)
        
        plt.plot(range(1,klaster+1),wcss,marker='o')
        plt.ylabel('wcss')
        plt.xlabel('Jumlah Klaster')
        plt.title('Perhitungan Elbow')
        stempel_waktu = datetime.now().strftime("%H-%M-%S")
        nama_baru = stempel_waktu+'plot.png'
        plt.savefig(f'static/temp/{nama_baru}')
        plt.close('all')
        return render_template('pages/hasil_elbow.html', gambar=nama_baru)

@app.route('/klastering')
def klastering():
    info_data = 'Kosong'
    info_instruksi = 'Kosong'
    saran = 'Syarat Terpenuhi! Proses dapat Dilaksanakan'
    lanjut = False

    sqlan = 'SELECT parameter FROM instruksi ORDER BY id DESC'
    cursor = db.cursor(dictionary=False)
    cursor.execute(sqlan)
    sql_data = cursor.fetchall()[0][0]
    # print(sql_data)
    db.commit()
    cursor.close()
    # # sql_data = "SELECT sinta_overall_v2,sinta_3y_v2,sinta_overall_v3,sinta_3y_v3,afiliasi_overall,afiliasi_3y,dok_scopus,sit_scopus,dok_sit_scopus,h_i_scopus,g_i_scopus,i10_i_scopus,dok_gs,sit_gs,dok_sit_gs,h_i_gs,g_i_gs,i10_i_gs,dok_wos,sit_wos,dok_sit_wos,h_i_wos,g_i_wos,i10_i_wos,dok_garuda,sit_garuda,dok_sit_garuda FROM dataset"
    sql_instruksi = "SELECT * FROM instruksi ORDER BY id DESC" 
    sql_id = "SELECT id FROM dataset" 
    # # print(sql_data)

    hasil_data = pd.read_sql(sql_data,db)
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql_instruksi)
    hasil_instruksi = cursor.fetchall()
    db.commit()
    cursor.execute(sql_id)
    hasil_id = cursor.fetchall()
    db.commit()
    cursor.close()

    if len(hasil_data) > 0 :
        info_data = 'Tersedia'
        lanjut = True
    else:
        info_data = 'Kosong'
        saran = '! Silahkan isi data yang kosong dahulu !'
        lanjut = False
    
    if len(hasil_instruksi) > 0 :
        info_instruksi = 'Tersedia'
        lanjut = True
    else:
        info_instruksi = 'Kosong'
        saran = '! Silahkan isi data yang kosong dahulu !'
        lanjut = False

    if not lanjut :
        return render_template('pages/klastering.html',info_data=info_data,info_instruksi=info_instruksi,saran=saran)

    permintaan_klaster = hasil_instruksi[0]['kluster']
    permintaan_iterasi = hasil_instruksi[0]['iterasi']

    kmeans = KMeans(n_clusters=permintaan_klaster,n_init='auto',max_iter=permintaan_iterasi)
    label = np.array(kmeans.fit_predict(hasil_data))

    dbi = davies_bouldin_score(hasil_data,kmeans.fit_predict(hasil_data))

    session['dbi'] = dbi
   
    for k,m in enumerate(hasil_id):

        cursor = db.cursor()
        sql = "UPDATE dataset SET cluster = %s WHERE id  = %s"
        val = (str(label[k]),str(m['id']))
        cursor.execute(sql, val)
        db.commit()



    return render_template('pages/klastering.html',info_data=info_data,info_instruksi=info_instruksi,saran=saran)

@app.route('/instruksi',methods=['POST','GET'])
def instruksi():
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('pages/instruksi.html')
    if request.method == 'POST':
        klaster = request.form['klaster']
        iterasi = request.form['iterasi']

        temp_sql = []
        sqlan = 'SELECT '

        if request.form.get('sinta_overall_v2') :
            temp_sql.append(request.form.get('sinta_overall_v2'))
        if request.form.get('sinta_3y_v2') :
             temp_sql.append(request.form.get('sinta_3y_v2'))
        if request.form.get('sinta_overall_v3') :
            temp_sql.append(request.form.get('sinta_overall_v3'))
        if request.form.get('sinta_3y_v3') :
            temp_sql.append(request.form.get('sinta_3y_v3'))
        if request.form.get('afiliasi_overall') :
            temp_sql.append(request.form.get('afiliasi_overall'))
        if request.form.get('afiliasi_3y') :
            temp_sql.append(request.form.get('afiliasi_3y'))
        if request.form.get('dok_scopus') :
            temp_sql.append(request.form.get('dok_scopus'))
        if request.form.get('sit_scopus') :
            temp_sql.append(request.form.get('sit_scopus'))
        if request.form.get('dok_sit_scopus') :
            temp_sql.append(request.form.get('dok_sit_scopus'))
        if request.form.get('h_i_scopus') :
            temp_sql.append(request.form.get('h_i_scopus'))
        if request.form.get('g_i_scopus') :
            temp_sql.append(request.form.get('g_i_scopus'))
        if request.form.get('i10_i_scopus') :
            temp_sql.append(request.form.get('i10_i_scopus'))
        if request.form.get('dok_gs') :
            temp_sql.append(request.form.get('dok_gs'))
        if request.form.get('sit_gs') :
            temp_sql.append(request.form.get('sit_gs'))
        if request.form.get('dok_sit_gs') :
            temp_sql.append(request.form.get('dok_sit_gs'))
        if request.form.get('h_i_gs') :
            temp_sql.append(request.form.get('h_i_gs'))
        if request.form.get('g_i_gs') :
            temp_sql.append(request.form.get('g_i_gs'))
        if request.form.get('i10_i_gs') :
            temp_sql.append(request.form.get('i10_i_gs'))
        if request.form.get('dok_wos') :
            temp_sql.append(request.form.get('dok_wos'))
        if request.form.get('sit_wos') :
            temp_sql.append(request.form.get('sit_wos'))
        if request.form.get('dok_sit_wos') :
            temp_sql.append(request.form.get('dok_sit_wos'))
        if request.form.get('h_i_wos') :
            temp_sql.append(request.form.get('h_i_wos'))
        if request.form.get('g_i_wos') :
            temp_sql.append(request.form.get('g_i_wos'))
        if request.form.get('i10_i_wos') :
            temp_sql.append(request.form.get('i10_i_wos'))
        if request.form.get('dok_garuda') :
            temp_sql.append(request.form.get('dok_garuda'))
        if request.form.get('sit_garuda') :
            temp_sql.append(request.form.get('sit_garuda'))
        if request.form.get('dok_sit_garuda') :
            temp_sql.append(request.form.get('dok_sit_garuda'))

        batas = len(temp_sql)-1
        # print('batas : '+str(batas))
        for k,i in enumerate(temp_sql):
            sqlan+=i
            # print(k)
            if k !=batas:
                sqlan+=','

        sqlan+=' FROM dataset'
        print(sqlan)
        cursor = db.cursor()
        sql = "INSERT INTO instruksi (kluster, iterasi, parameter) VALUES (%s,%s,%s)"
        cursor.execute(sql,(klaster,iterasi,sqlan))
        db.commit()
        pesan = 'berhasil masukan instruksi'
        return render_template('pages/instruksi.html',pesan=pesan)
        
@app.route('/hasil_klastering')
def hasil_klastering():
    sql_param = "SELECT parameter FROM instruksi ORDER BY id DESC"
    cursor = db.cursor(dictionary=False)
    cursor.execute(sql_param)
    hasil_param = cursor.fetchall()[0][0]
    db.commit()
    bersih = hasil_param.replace('SELECT ','')
    hasil_akhir = bersih.replace(' FROM dataset','')
    return render_template('pages/hasil_klastering.html',param=hasil_akhir.split(','))

@app.route('/jumlah_klaster')
def jumlah_klaster():
    
    sql_total = "SELECT DISTINCT(cluster) FROM dataset"

    cursor = db.cursor(dictionary=False)
    cursor.execute(sql_total)
    total_cluster = [item[0] for item in cursor.fetchall()]
    db.commit()
    # print(total_cluster)

    jumlah_per_klaster = []
    for i in total_cluster:
        sql_per_klaster = "SELECT COUNT(cluster) FROM dataset WHERE cluster=%s"
        val = (i)
        cursor = db.cursor(dictionary=False)
        cursor.execute(sql_per_klaster,(val,))
        hasil_per_klaster =  cursor.fetchone()
        db.commit()
        jumlah_per_klaster.append(hasil_per_klaster)


    data = {
        'label' : total_cluster,
        'jumlah' : [item[0] for item in jumlah_per_klaster]
    }

    return make_response(jsonify(data),200)

@app.route('/cek_per_cluster/<id>')
def cek_per_cluster(id):
    
    cursor = db.cursor(dictionary=False)
    sql = f"SELECT nama,nidn,cluster FROM dataset WHERE cluster={id}"
    cursor.execute(sql)
    data = cursor.fetchall()
    db.commit()
    return make_response(jsonify(data))

@app.route('/dbi')
def dbi():
    hasil_dbi = session.get('dbi')
    return render_template('pages/dbi.html',data=hasil_dbi)

@app.route('/about')
def about():
    if not session.get('sudah_login'):
        return redirect(url_for('login'))
    return render_template('pages/about.html')

@app.route('/logout')
def logout():
    pesan = 'anda logout'
    session.pop('sudah_login', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login',pesan = pesan))

if __name__ == "__main__":
    app.run(debug=True)
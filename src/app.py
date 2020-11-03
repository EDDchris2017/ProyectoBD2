from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error

#Se leventa en puerto 5000 !!!
app = Flask(__name__)


def getBancos():
    cadquery = "SELECT nombre_banco FROM banco"
    result = conexionBD(cadquery)
    print(result)
    return result

# 19 u 20 anio consulta
# mes -> 1 ...12
def getDatosBanco(banco):
    cadquery = "SELECT YEAR(s.fecha) AS ano, MONTH(s.fecha) AS mes, b.nombre_banco, SUM(saldo) AS saldo, RANK() OVER (PARTITION BY YEAR(s.fecha), MONTH(s.fecha) ORDER BY SUM(saldo) DESC) ranker"
        +"FROM banco b"
        +"JOIN saldo s"
        + "ON b.id_banco = s.id_banco"
        + "WHERE s.tipo = 'A'"
        + "WHERE b.nombre_banco = " + banco + " "
        + "GROUP BY YEAR(s.fecha), MONTH(s.fecha), b.nombre_banco"
    result = conexionBD(cadquery)
    data = []
    for row in result:
        data.insert(row[4])
    return data

def conexionBD(sql_select_Query):
    # Colocar usuarios de la base de datos
    connection = mysql.connector.connect(host='104.154.181.68',database='cuentas',user='root',password='root')
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    connection.close()
    return records

def dataStruct(datosbd):
    #Obtener Bancos de la base de datos
    fechas = ["Jul-2019","Aug-2019","Sep-2019","Oct-2019","Nov-2019","Dic-2019","Jan-2020","Feb-2020","March-2020","Ap-2020","May-2020","Jun-2020","Jul-2020"]
    bancos = getBancos()
    muestra = []
    for banco in bancos:
        #Obtener Ranking de todas las fechas por banco
        muestra.insert(getDatosBanco(banco))
    
        


@app.route('/status')
def verificar():
    return "Servicio Proyecto BD2 activo"

@app.route('/')
def servicio():

    res = conexionBD
    (
        "SELECT YEAR(s.fecha) AS ano, MONTH(s.fecha) AS mes, b.nombre_banco, SUM(saldo) AS saldo, RANK() OVER (PARTITION BY YEAR(s.fecha), MONTH(s.fecha) ORDER BY SUM(saldo) DESC) ranker"
        +"FROM banco b"
        +"JOIN saldo s"
        + "ON b.id_banco = s.id_banco"
        + "WHERE s.tipo = 'A'"
        + "GROUP BY YEAR(s.fecha), MONTH(s.fecha), b.nombre_banco""
    )
    return render_template("home.html", res_1=[10,20,30,40,50],columnas="",rows="")
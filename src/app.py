from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error
import pymysql.cursors
# https://plotly.com/javascript/figure-labels/
#Se leventa en puerto 5000 !!!
app = Flask(__name__)


def getBancos():
    cadquery = "SELECT nombre_banco FROM banco"
    result = conexionBD(cadquery)
    return result

# 19 u 20 anio consulta
# mes -> 1 ...12
def getDatosBanco(banco):
    cadquery = ""
    cadquery += " SELECT * FROM("
    cadquery += " SELECT YEAR(s.fecha) AS ano, MONTH(s.fecha) AS mes, b.nombre_banco, SUM(saldo) AS saldo, RANK() OVER (PARTITION BY YEAR(s.fecha), MONTH(s.fecha) ORDER BY SUM(saldo) DESC) ranker"
    cadquery += " FROM banco b"
    cadquery += " JOIN saldo s"
    cadquery += " ON b.id_banco = s.id_banco"
    cadquery += " WHERE s.tipo = 'A'" 
    cadquery += " GROUP BY YEAR(s.fecha), MONTH(s.fecha), b.nombre_banco) AS temp"
    cadquery += " WHERE temp.nombre_banco = '" + banco + "'"
    result = conexionBD(cadquery)
    data = []
    for row in result:
        data.append(row["ranker"])
    return data

def conexionBD(sql_select_Query):
    result = 0
    # Connect to the database
    connection = pymysql.connect(host='104.154.181.68',
                             user='root',
                             password='root',
                             db='cuentas',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = sql_select_Query
            #sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        connection.close()
    return result
    # Colocar usuarios de la base de datos
    #connection = mysql.connector.connect(host='104.154.181.68',database='cuentas',user='bases2',password='proyecto2')
    #cursor = connection.cursor()
    #cursor.execute(sql_select_Query)
    #records = cursor.fetchall()
    #connection.close()
    #return records

def dataStruct():
    #Obtener Bancos de la base de datos
    fechas = ["Banco","Jul-2019","Aug-2019","Sep-2019","Oct-2019","Nov-2019","Dic-2019","Jan-2020","Feb-2020","March-2020","Ap-2020","May-2020","Jun-2020","Jul-2020"]
    bancos = getBancos()
    muestra = []
    for banco in bancos:
        #Obtener Ranking de todas las fechas por banco
        fila_banco = getDatosBanco(banco['nombre_banco'])
        fila_banco.insert(0,banco['nombre_banco'])
        muestra.append(fila_banco)
    return {'fechas':fechas, 'bancos':muestra}
        


@app.route('/status')
def verificar():
    return "Servicio Proyecto BD2 activo"

@app.route('/')
def servicio():

    #res = conexionBD
    #(
    #    "SELECT YEAR(s.fecha) AS ano, MONTH(s.fecha) AS mes, b.nombre_banco, SUM(saldo) AS saldo, RANK() OVER (PARTITION BY YEAR(s.fecha), MONTH(s.fecha) ORDER BY SUM(saldo) DESC) ranker"
    #    +"FROM banco b"
    #    +"JOIN saldo s"
    #    + "ON b.id_banco = s.id_banco"
    #    + "WHERE s.tipo = 'A'"
    #    + "GROUP BY YEAR(s.fecha), MONTH(s.fecha), b.nombre_banco"
    #)
    datos = dataStruct()
    return render_template("principal.html", columnas=datos["fechas"],rows=datos["bancos"])
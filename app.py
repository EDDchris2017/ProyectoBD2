import plotly.graph_objects as go
from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error

#Se leventa en puerto 5000 !!!
app = Flask(__name__)

# Crear la grafica
# Aqui se crear un Scatter Plot con lineas y puntos
# eje_x -> Numero de las Cuentas
# eje_y -> Numero 
def crearGrafica(eje_x,eje_y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=eje_x, y=eje_y,
                    mode='lines+markers',
                    name='lines+markers'))

def conexionBD(sql_select_Query):
    # Colocar usuarios de la base de datos
    connection = mysql.connector.connect(host='mysql',database='cuentas',user='user1',password='pass')
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    connection.close()
    return records


@app.route('/')
def servicio():
    query_inciso1 = "select * from .... colocar quuery inciso 1"
    res = conexionBD(query_inciso1)
    return render_template("index.html", result = res)
#!/usr/bin/env python
from __future__ import unicode_literals, print_function
from flask import Flask, render_template, json, request, redirect
from flaskext.mysql import MySQL
from pprint import pprint
import random


app = Flask(__name__)
app.secret_key = "super secret key"
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'bucketlist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showIndex')
def showIndex():
    return render_template('index.html')

@app.route('/showjuego')
def showjuego():
    return render_template('juego.html')

@app.route('/showUnjugador')
def showUnjugador():
    return render_template('Unjugador.html')

@app.route('/showUnJugadorResultado')
def showUnJugadorResultado():
    return render_template('UnJugadorResultado.html')

@app.route('/showMultijugador')
def showMultijugador():
    return render_template('Multijugador.html')

@app.route('/showEstadisticas')
def showEstadisticas():
    return render_template('Estadisticas.html')




@app.route('/signUp', methods=['POST', 'GET'])
def signUp():

    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createUser', (_name, _email, _password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/signIn', methods=['POST', 'GET'])
def signIn():
        global _name

        try:
            _name = request.form['inputName']
            _email = request.form['inputEmail']
            _password = request.form['inputPassword']

            # validate the received values
            if _name and _email and _password:

                conn = mysql.connect()
                cursor = conn.cursor()

                result_name = cursor.execute("SELECT * FROM tbl_user WHERE user_name = %s", [_name])
                result_username = cursor.execute("SELECT * FROM tbl_user WHERE user_username = %s", [_email])
                result_password = cursor.execute("SELECT * FROM tbl_user WHERE user_password = %s", [_password])
                cursor.execute("SELECT Victorias,Derrotas,Partidas FROM tbl_user WHERE user_name = %s", [_name])
                victorias = cursor.fetchone()
                cursor.execute("SELECT Derrotas FROM tbl_user WHERE user_name = %s", [_name])
                derrotas = cursor.fetchone()
                cursor.execute("SELECT Partidas FROM tbl_user WHERE user_name = %s", [_name])
                partidas = cursor.fetchone()
                v=victorias
                d=derrotas
                p=partidas
                pprint(v)
                pprint(d)
                pprint(p)



            if result_name+result_username+result_password==3:
                return redirect ("showjuego#", code=302)
            elif result_name == 0:
                error=('Nombre del usuario no existe o es incorrecto !')
                return render_template('FalloLogin.html',MensajeError=error)
            elif result_username==0:
                error=('Correo del usuario no existe o es incorrecto !')
                return render_template('FalloLogin.html',MensajeError=error)
            elif result_password==0:
                error=('Contraseña incorrecta !')
                return render_template('FalloLogin.html',MensajeError=error)
            else:
                error = ('Intentelo de nuevo ninguno de los campos existe !')
                return render_template('FalloLogin.html', MensajeError=error)
        except Exception as e:
            return json.dumps({'error': str(e)})
        finally:
            cursor.close()
            conn.close()

@app.route('/Unjugador', methods=['POST', 'GET'])
def Unjugador():


    try:
        opcion1 = request.form['opcion']
        opcion = ['Piedra', 'Papel', 'Tijera']
        comp = random.choice(opcion)
        conn = mysql.connect()
        cursor = conn.cursor()
        pprint(opcion1)
        pprint(comp)
        pprint(_name)
        if opcion1 == 'Piedra' and comp == 'Piedra':
            mensaje1 = ('***PIEDRA vs PIEDRA***')
            mensaje=('***Empate!***')
            cursor.execute("UPDATE tbl_user SET Partidas = Partidas+1 WHERE user_name = %s", [_name])
            cursor.fetchall()
            conn.commit()
        elif opcion1 == 'Tijera' and comp == 'Tijera':
            mensaje1 = ('***TIJERA vs TIJERA***')
            mensaje = ('***Empate!***')
            cursor.execute("UPDATE tbl_user SET Partidas = Partidas+1 WHERE user_name = %s", [_name])
            cursor.fetchall()
            conn.commit()
        elif opcion1 == 'Papel' and comp == 'Papel':
            mensaje1 = ('***PAPEL vs PAPEL***')
            mensaje = ('***Empate!***')
            cursor.execute("UPDATE tbl_user SET Partidas = Partidas+1 WHERE user_name = %s", [_name])
            cursor.fetchall()
            conn.commit()
        elif opcion1 != comp:
            if opcion1 == 'Piedra' and comp == 'Tijera':
                mensaje1=('***PIEDRA vs TIJERA***')
                mensaje=('***Tu ganas!***')
                cursor.execute("UPDATE tbl_user SET Victorias = Victorias+1,Partidas = Partidas+1 WHERE user_name = %s",[_name])
                cursor.fetchall()
                conn.commit()
            elif opcion1 == 'Tijera' and comp == 'Papel':
                mensaje1=('***TIJERA vs PAPEL***')
                mensaje=('***Tu ganas!***')
                cursor.execute("UPDATE tbl_user SET Victorias = Victorias+1,Partidas = Partidas+1 WHERE user_name = %s",[_name])
                cursor.fetchall()
                conn.commit()
            elif opcion1 == 'Papel' and comp == 'Piedra':
                mensaje1=('***PAPEL vs TIJERA***')
                mensaje=('***Tu ganas!***')
                cursor.execute("UPDATE tbl_user SET Victorias = Victorias+1,Partidas = Partidas+1 WHERE user_name = %s", [_name])
                cursor.fetchall()
                conn.commit()
            elif opcion1 == 'Tijera' and comp == 'Piedra':
                mensaje1 = ('***TIJERA vs PIEDRA***')
                mensaje=('***Tu pierdes.***')
                cursor.execute("UPDATE tbl_user SET Derrotas = Derrotas+1,Partidas = Partidas+1 WHERE user_name = %s",[_name])
                cursor.fetchall()
                conn.commit()
            elif opcion1 == 'Papel' and comp == 'Tijera':
                mensaje1 = ('***PAPEL vs TIJERA***')
                mensaje=('***Tu pierdes.***')
                cursor.execute("UPDATE tbl_user SET Derrotas = Derrotas+1,Partidas = Partidas+1 WHERE user_name = %s",[_name])
                cursor.fetchall()
                conn.commit()
            elif opcion1 == 'Piedra' and comp == 'Papel':
                mensaje1 = ('***PIEDRA vs PAPEL***')
                mensaje=('***Tu pierdes.***')
                cursor.execute("UPDATE tbl_user SET Derrotas = Derrotas+1,Partidas = Partidas+1 WHERE user_name = %s",[_name])
                cursor.fetchall()
                conn.commit()
        pprint(mensaje)
        return render_template('UnJugadorResultado.html', Resultado1=mensaje1, Resultado2=mensaje)


    finally:
        cursor.close()
        conn.close()


@app.route('/Estadisticas', methods=['POST'])
def Estadisticas():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        estadisticas = request.form['opcionestadisticas']
        if estadisticas == 'Unjugador':
            cursor.execute("SELECT Victorias,Derrotas,Partidas FROM tbl_user WHERE user_name = %s", [_name])
            victorias = cursor.fetchone()
            return render_template('EstadisticasJugador.html', Estadisticas=victorias)
        elif estadisticas == 'Multijugador':
            cursor.execute("SELECT VictoriasMultijugador,DerrotasMultijugador,PartidasMultijugador FROM tbl_user WHERE user_name = %s", [_name])
            victorias1 = cursor.fetchone()
            return render_template('EstadisticasMultijugador.html', Estadisticas1=victorias1)
    finally:
        cursor.close()
        conn.close()

@app.route('/Multijugador', methods=['POST', 'GET'])
def Multijugador():

    conn = mysql.connect()
    cursor = conn.cursor()
    opcion1 = request.form['opcion']
    opcioninvitado = request.form['opcioninvitado']
    pprint(opcion1)
    pprint(opcioninvitado)
    if opcion1 == 'Piedra' and opcioninvitado == 'Piedra':
        mensaje1 = ('***PIEDRA vs PIEDRA***')
        mensaje = ('***Empate!***')
        cursor.execute("UPDATE tbl_user SET PartidasMultijugador = PartidasMultijugador+1 WHERE user_name = %s", [_name])
        cursor.fetchall()
        conn.commit()
    elif opcion1 == 'Tijera' and opcioninvitado == 'Tijera':
        mensaje1 = ('***TIJERA vs TIJERA***')
        mensaje = ('***Empate!***')
        cursor.execute("UPDATE tbl_user SET PartidasMultijugador = PartidasMultijugador+1 WHERE user_name = %s",[_name])
        cursor.fetchall()
        conn.commit()
    elif opcion1 == 'Papel' and opcioninvitado == 'Papel':
        mensaje1 = ('***PAPEL vs PAPEL***')
        mensaje = ('***Empate!***')
        cursor.execute("UPDATE tbl_user SET PartidasMultijugador = PartidasMultijugador+1 WHERE user_name = %s",[_name])
        cursor.fetchall()
        conn.commit()
    elif opcion1 != opcioninvitado:
        if opcion1 == 'Piedra' and opcioninvitado == 'Tijera':
            mensaje1 = ('***PIEDRA vs TIJERA***')
            mensaje = ('***Jugador Anfitrion gana!***')
            cursor.execute("UPDATE tbl_user SET VictoriasMultijugador = VictoriasMultijugador+1,PartidasMultijugador = PartidasMultijugador+1 WHERE user_name = %s",[_name])
            cursor.fetchall()
            conn.commit()
        elif opcion1 == 'Tijera' and opcioninvitado == 'Papel':
            mensaje1 = ('***TIJERA vs PAPEL***')
            mensaje = ('***Jugador Anfitrion gana!***')
            cursor.execute("UPDATE tbl_user SET VictoriasMultijugador = VictoriasMultijugador+1,PartidasMultijugador = PartidasMultijugador+1 WHERE user_name = %s",[_name])
            cursor.fetchall()
            conn.commit()
        elif opcion1 == 'Papel' and opcioninvitado == 'Piedra':
            mensaje1 = ('***PAPEL vs TIJERA***')
            mensaje = ('***Jugador Anfitrion gana!***')
            cursor.execute("UPDATE tbl_user SET VictoriasMultijugador = VictoriasMultijugador+1,PartidasMultijugador = PartidasMultijugador+1 WHERE user_name = %s",[_name])
            cursor.fetchall()
            conn.commit()
        elif opcion1 == 'Tijera' and opcioninvitado == 'Piedra':
            mensaje1 = ('***TIJERA vs PIEDRA***')
            mensaje = ('***Jugador Invitado gana!.***')
            cursor.execute("UPDATE tbl_user SET DerrotasMultijugador = DerrotasMultijugador+1,PartidasMultijugador = PartidasMultijugador+1 WHERE user_name = %s",[_name])
            cursor.fetchall()
            conn.commit()
        elif opcion1 == 'Papel' and opcioninvitado == 'Tijera':
            mensaje1 = ('***PAPEL vs TIJERA***')
            mensaje = ('***Jugador Invitado gana!***')
            cursor.execute("UPDATE tbl_user SET DerrotasMultijugador = DerrotasMultijugador+1,PartidasMultijugador = PartidasMultijugador+1 WHERE user_name = %s",[_name])
            cursor.fetchall()
            conn.commit()
        elif opcion1 == 'Piedra' and opcioninvitado == 'Papel':
            mensaje1 = ('***PIEDRA vs PAPEL***')
            mensaje = ('***Jugador Invitado gana!***')
            cursor.execute("UPDATE tbl_user SET DerrotasMultijugador = DerrotasMultijugador+1,PartidasMultijugador = PartidasMultijugador+1 WHERE user_name = %s",[_name])
            cursor.fetchall()
            conn.commit()
    pprint(mensaje)
    return render_template('MultijugadorResultado.html', Resultado1=mensaje1, Resultado2=mensaje)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

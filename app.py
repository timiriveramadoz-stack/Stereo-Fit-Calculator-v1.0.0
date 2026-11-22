
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask import send_from_directory

@app.route('/googlec6f36be820f01405.html')
def google_verification():
    return send_from_directory(
        app.root_path,
        'googlec6f36be820f01405.html'
    )

# Cargar variables del archivo .env
load_dotenv()

# Verificar clave secreta
SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("No se encontró SECRET_KEY en las variables de entorno.")

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["SESSION_PERMANENT"] = False


@app.route("/sw.js")
def service_worker():
    return send_from_directory(
        "static",
        "sw.js",
        mimetype="application/javascript"
    )


@app.route("/", methods=["GET", "POST"])
def inicio():

    if request.method == "POST":

        if "verificar" in request.form:

            Usuario = request.form["usuario"]
            Contraseña = request.form["contrasena"]
            Contraseña_verificacion = request.form["verificacion"]

            if Contraseña == Contraseña_verificacion:
                session["Usuario"] = Usuario
                session["verificado"] = True
                return redirect(url_for("inicio"))

            else:
                return render_template(
                    "index.html",
                    etapa="registro",
                    error="Contraseña incorrecta. Intente nuevamente."
                )

        if "calcular" in request.form:

            if not session.get("verificado") or "Usuario" not in session:
                return redirect(url_for("inicio"))

            try:
                edad = int(request.form["edad"])
                altura = float(request.form["altura"].replace(",", "."))
                peso = float(request.form["peso"].replace(",", "."))

                # Convertir centímetros a metros
                if altura > 3:
                    altura = altura / 100

                # Validar los datos
                if edad <= 0 or altura <= 0 or peso <= 0:
                    raise ValueError

                # Calcular IMC
                IMC = peso / (altura ** 2)

            except (ValueError, ZeroDivisionError):
                return render_template(
                    "index.html",
                    etapa="imc",
                    Usuario=session["Usuario"],
                    error="Ingresá una edad, altura y peso válidos."
                )

            print("PESO:", peso)
            print("ALTURA EN METROS:", altura)
            print("IMC:", IMC)

            if edad < 20:
                clasificacion = "No se puede determinar una categoría sin las curvas de crecimiento correspondientes a tu edad y sexo."

            elif IMC < 18.5:
                clasificacion = "Tu resultado corresponde a la categoría de IMC bajo."

            elif IMC < 25:
                clasificacion = "Tu resultado se encuentra dentro del rango habitual de IMC para adultos."

            elif IMC < 30:
                clasificacion = "Tu resultado corresponde a la categoría de sobrepeso."

            else:
                clasificacion = "Tu resultado corresponde a la categoría de obesidad."

            print("CLASIFICACION:", clasificacion)

            return render_template(
                "index.html",
                etapa="resultado",
                Usuario=session.get("Usuario", "Usuario"),
                IMC=IMC,
                edad=edad,
                clasificacion=clasificacion
            )

    if session.get("verificado"):
        return render_template(
            "index.html",
            etapa="imc",
            Usuario=session["Usuario"]
        )

    return render_template("index.html", etapa="registro")


@app.route("/cerrar_sesion", methods=["POST"])
def cerrar_sesion():
    session.clear()
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False,
        use_reloader=False
    )

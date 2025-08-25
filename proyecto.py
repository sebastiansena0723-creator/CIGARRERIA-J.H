from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

# 📂 Archivo donde se guardará el inventario
ARCHIVO = "inventario.json"

# 🔹 Función para cargar inventario desde el JSON
def cargar_inventario():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    return {}

# 🔹 Función para guardar inventario en el JSON
def guardar_inventario():
    with open(ARCHIVO, "w") as f:
        json.dump(inventario, f, indent=4)

# 📦 Cargar inventario al iniciar
inventario = cargar_inventario()

@app.route("/")
def home():
    return render_template("index.html", inventario=inventario)

@app.route("/agregar", methods=["POST"])
def agregar_producto():
    nombre = request.form["nombre"]
    cantidad = int(request.form["cantidad"])
    precio = float(request.form["precio"])

    if nombre in inventario:
        inventario[nombre]["cantidad"] += cantidad
    else:
        inventario[nombre] = {"cantidad": cantidad, "precio": precio}

    guardar_inventario()  # 🔹 Guardar cambios
    return redirect(url_for("home"))

@app.route("/vender", methods=["POST"])
def vender_producto():
    nombre = request.form["nombre"]
    if nombre in inventario:
        inventario[nombre]["cantidad"] -= 1
        if inventario[nombre]["cantidad"] <= 0:
            del inventario[nombre]
        guardar_inventario()  # 🔹 Guardar cambios
    return redirect(url_for("home"))

@app.route("/eliminar", methods=["POST"])
def eliminar_producto():
    nombre = request.form["nombre"]
    if nombre in inventario:
        del inventario[nombre]
        guardar_inventario()  # 🔹 Guardar cambios
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
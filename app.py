from flask import Flask, render_template, request, abort, redirect, url_for
import json

app = Flask(__name__)

# Cargar el JSON
with open("musica.json", encoding="utf-8") as f:
    datos = json.load(f)

# Preprocesar datos para facilitar búsquedas
def preparar_datos():
    canciones = []
    for artista in datos["artistas"]:
        for album in artista["albumes"]:
            for cancion in album["canciones"]:
                # Creamos un objeto canción con todos los datos relevantes
                cancion_completa = {
                    "id": f"{artista['nombre']}-{album['titulo']}-{cancion['titulo']}".replace(" ", "_").lower(),
                    "titulo": cancion["titulo"],
                    "artista": artista["nombre"],
                    "album": album["titulo"],
                    "genero": album["genero"],
                    "duracion": cancion["duracion"],
                    "rating": cancion.get("rating", 0),
                    "compositores": ", ".join(cancion.get("compositores", [])),
                    "colaboraciones": ", ".join(cancion.get("colaboraciones", [])),
                    "premios": ", ".join(cancion.get("premios", [])),
                    "año": album["año"],
                    "pais": artista["pais"],
                    "productor": album["productor"],
                    "ventas": album["ventas"]
                }
                canciones.append(cancion_completa)
    return canciones

# Preparamos los datos al iniciar
todas_las_canciones = preparar_datos()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inicio")
def inicio():
    return redirect(url_for("buscador"))

@app.route("/canciones", methods=["GET", "POST"])
def buscador():
    # Obtener todos los géneros únicos para el dropdown
    generos = sorted({c["genero"] for c in todas_las_canciones})
    
    # Valores por defecto
    resultados = []
    busqueda = ""
    genero_seleccionado = ""
    
    if request.method == "POST":
        busqueda = request.form.get("nombre", "").lower()
        genero_seleccionado = request.form.get("genero", "")
        
        # Filtrar canciones
        resultados = todas_las_canciones
        if busqueda:
            resultados = [c for c in resultados if busqueda in c["titulo"].lower()]
        if genero_seleccionado:
            resultados = [c for c in resultados if c["genero"] == genero_seleccionado]
    
    return render_template("buscador.html", 
                         canciones=resultados, 
                         busqueda=busqueda,
                         generos=generos,
                         genero_seleccionado=genero_seleccionado)

@app.route("/cancion/<id>")
def detalle(id):
    cancion = next((c for c in todas_las_canciones if c["id"] == id), None)
    if cancion is None:
        abort(404)
    return render_template("detalle.html", cancion=cancion)

if __name__ == "__main__":
    app.run(debug=True)
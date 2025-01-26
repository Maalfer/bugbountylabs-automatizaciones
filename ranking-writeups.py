import requests
from bs4 import BeautifulSoup
from collections import defaultdict

urls = {
    "https://bugbountylabs.com/redirection/": 2,
    "https://bugbountylabs.com/hidden-redirection/": 2,
    "https://bugbountylabs.com/loginn/": 4,
    "https://bugbountylabs.com/moto-pasion/": 4,
    "https://bugbountylabs.com/corsy/": 4,
    "https://bugbountylabs.com/listing/": 2,
    "https://bugbountylabs.com/dogshow/": 4,
    "https://bugbountylabs.com/el-rincon-del-mongo/": 2,
    "https://bugbountylabs.com/forgery/": 2,
    "https://bugbountylabs.com/entity/": 2,
    "https://bugbountylabs.com/escape/": 2,
    "https://bugbountylabs.com/access/": 2,
    "https://bugbountylabs.com/reflection/": 2
}

def obtener_nombres_writeups(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            encabezado = soup.find('h2', class_='elementor-heading-title elementor-size-default', string='WRITE-UPS')

            if encabezado:            
                contenedor = encabezado.find_next('div')
     
                nombres = [span.get_text(strip=True) for span in contenedor.find_all('span', class_='elementor-icon-list-text')]

                return nombres
            else:
                print(f"No se encontró el encabezado 'WRITE-UPS' en {url}.")
                return []
        else:
            print(f"No se pudo acceder a la URL: {url}")
            return []
    except Exception as e:
        print(f"Error al procesar la URL {url}: {e}")
        return []

def calcular_puntuaciones(urls):
    puntuaciones = defaultdict(int)

    for url, valor in urls.items():
        nombres = obtener_nombres_writeups(url)
        for nombre in nombres:
            puntuaciones[nombre] += valor

    puntuaciones_ordenadas = sorted(puntuaciones.items(), key=lambda x: x[1], reverse=True)

    return puntuaciones_ordenadas

# Función para generar el HTML
def generar_html(puntuaciones):
    # Cabecera del HTML original
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ranking De Creadores</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #000;
            padding: 8px;
            text-align: center;
            width: 33.33%; /* Asegura que todas las columnas tengan el mismo tamaño */
        }
        th {
            background-color: #c3317d;
            color: #000000;
        }
        tr:nth-child(even) {
            background-color: black;
            color: white;
        }
        tr:nth-child(odd) {
            background-color: black;
            color: white;
        }
        @media screen and (max-width: 600px) {
            table, thead, tbody, th, td, tr {
                display: block;
            }
            thead tr {
                position: absolute;
                top: -9999px;
                left: -9999px;
            }
            tr {
                margin: 0 0 1rem 0;
                display: flex;
                flex-direction: column;
                border: 1px solid #000;
            }
            td {
                border: none;
                border-bottom: 1px solid #ddd;
                position: relative;
                padding-left: 50%;
                text-align: left;
                background-color: black;
                color: white;
            }
            td:before {
                position: absolute;
                top: 0;
                left: 6px;
                width: 45%;
                padding-right: 10px;
                white-space: nowrap;
                font-weight: bold;
            }
            td:nth-of-type(1):before { content: "CREADOR"; }
            td:nth-of-type(2):before { content: "POSICIÓN"; }
            td:nth-of-type(3):before { content: "PUNTUACION"; }
        }
    </style>
</head>
<body>
    <table>
        <thead>
            <tr>
                <th>CREADOR</th>
                <th>POSICIÓN</th>
                <th>PUNTUACION</th>
            </tr>
        </thead>
        <tbody>
"""

    for idx, (nombre, puntuacion) in enumerate(puntuaciones, start=1):
        html += f"""
            <tr>
                <td>{nombre}</td>
                <td>{idx}</td>
                <td>{puntuacion}</td>
            </tr>
        """

    html += """
        </tbody>
    </table>
</body>
</html>
"""
    return html


if __name__ == '__main__':
    puntuaciones = calcular_puntuaciones(urls)

    html_resultado = generar_html(puntuaciones)

    print(html_resultado)

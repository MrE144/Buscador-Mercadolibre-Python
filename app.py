#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 17:20:21 2026

@author: esteban
"""

import requests
from bs4 import BeautifulSoup
import csv


def exportar_csv(productos, nombre_archivo="productos_mas_baratos.csv"):
    """
    Exporta una lista de productos a un archivo CSV.
    """
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        writer.writerow(["Nombre", "Precio (MXN)", "Link"])

        for p in productos:
            writer.writerow([p["nombre"], p["precio"], p["link"]])


def main():
    """
    Programa principal:
    - Solicita un producto al usuario
    - Busca el producto en Mercado Libre México
    - Extrae nombre, precio y link
    - Muestra los 5 productos más baratos
    - Exporta los resultados a un archivo CSV
    """

    producto = input("Producto a buscar: ")

    # Construcción de la URL de búsqueda
    producto_url = producto.strip().replace(" ", "-").lower()
    url = f"https://listado.mercadolibre.com.mx/{producto_url}"

    # Headers para simular un navegador
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "Gecko/20100101 Firefox/120.0"
        )
    }

    # Petición HTTP
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error al acceder a Mercado Libre.")
        return

    # Parseo del HTML
    soup = BeautifulSoup(response.text, "html.parser")

    productos = []

    # Cada producto está contenido en un <li>
    items = soup.find_all("li")

    for item in items:
        link_tag = item.find("a", href=True)
        precio_tag = item.find("span", class_="andes-money-amount__fraction")
        nombre_tag = item.find("h3")

        # Validar que el elemento tenga la información necesaria
        if not (link_tag and precio_tag and nombre_tag):
            continue

        try:
            precio = int(precio_tag.text.replace(".", "").replace(",", ""))
        except ValueError:
            continue

        producto_info = {
            "nombre": nombre_tag.text.strip(),
            "precio": precio,
            "link": link_tag["href"]
        }

        productos.append(producto_info)

    if not productos:
        print("No se encontraron productos.")
        return

    # Ordenar productos por precio (menor a mayor)
    productos_ordenados = sorted(productos, key=lambda x: x["precio"])

    # Mostrar los 5 más baratos
    print("\nLos 5 productos más baratos encontrados:\n")

    for i, p in enumerate(productos_ordenados[:5], start=1):
        print(f"{i}. {p['nombre']}")
        print(f"   Precio: ${p['precio']}")
        print(f"   Link: {p['link']}\n")

    # Exportar a CSV
    exportar_csv(productos_ordenados[:5])
    print("Archivo CSV generado: productos_mas_baratos.csv")


if __name__ == "__main__":
    main()
else:
    print("Error. Try Again.")

from models import db
from flask import Flask, request, jsonify, render_template

# fonction qui permet formater en json les données des polygones, la classe concernée est définie dans data
def format_geojson(data):
    data_all = []

    for row in data:
        # on crée un dictionnaire contenant uniquement le type et les géométries pour l'instant
        curData = {'type': 'Feature',
                    'geometry': row.converted_geom # cette fonction est définie dans models.py
                    }
        # dans ce dictionnaire, on y rajoute un élément properties vide
        curData['properties'] = {}

        # pour chaque nom de colonne de la table du jeu de données, si la key est différente est différente de geom,
        # on récupère la valeur de la clé et on l'ajoute dans le dictionnaire
        for i in row.__table__.c:
            if i.key != 'geom':
                curData['properties'][i.key] = getattr(row,i.key)
        data_all.append(curData)

    return jsonify(data_all)

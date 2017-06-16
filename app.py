from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import models
from models import db, EspacesVerts, Arrondissements, Ndvi
import simplejson # possibilité d'afficher des données type Decimal
import geoalchemy2.functions as func
import json
import geojson
from sqlalchemy import *
from functions import format_geojson

# on crée un dictionnaire qui contient les différentes routes crées, associées à leur classe definies dans models.py
dictClassData = {
'arr': Arrondissements,
'ndvi': Ndvi,
'esp': EspacesVerts
}

# on crée notre application
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)


# def to_json(func):
#     return jsonify

# cette route, en mettant <obj>, on peut dans le navigateur y mettre la route qu'on veut, définie
# dans le dictionnaire au-dessus, et on récupère les propriétés
@app.route('/<obj>/properties')
def properties(obj):
    # ici on regarde si l'objet rentré existe bien, sinon on lmui donne la valeur none
    dataObj = dictClassData.get(obj, None)
    if not dataObj:
        # dans ce cas, on retourne une erreur (chemin erroné)
        return jsonify('error')
    # ici, la route qu'on a rentré concerne un objet de type classe, on récupère les intitulés des colonnes
    col = dictClassData[obj].__table__.c
    value = []
    for c in col:
        value.append(c.key)
    value.remove('geom')
    print (value)
    # on fait une liste compréhensive pour l'affichage
    # return jsonify([c.key for c in col])
    return jsonify([value])

# on obtient le détail de la géometrie des polygones
@app.route('/<obj>/geometry')
def geometry(obj):
    dataObj = dictClassData.get(obj, None)
    if not dataObj:
        return jsonify('error')
    # on fait une requête pour ne sélectionner que les géométries, en faisant la transfromation en geojson
    query = select([dictClassData[obj].gid.label('gid'), func.ST_AsGeoJSON(func.ST_Transform(dictClassData[obj].geom,4326)).label('geom')]).where(dictClassData[obj].geom!=None)
    dataQuery = db.session.execute(query).fetchall()
    geom_all = []
    for data in dataQuery:
        data = dict(data)
        geom_all.append({
                        'gid': data['gid'],
                        'geometry': data['geom']
                        })
    return jsonify(geom_all)

@app.route('/arr')
def get_data():
    data = Arrondissements.query.all()
    data_all = []
    # print(Arrondissements.toto(1))
    # Arrondissements.tata()

    # # si on fait un filtre dans la navigateur ?gid=1, on récupère cet élément la
    # dataQuery = Arrondissements.query
    # for k in request.args:
    #     print(k)
    #     dataQuery = dataQuery.filter(getattr(Arrondissements, k) == request.args.get(k))

    return format_geojson(data)

@app.route('/esp')
def get_esp():
    # print(dict(request.data))
    data = EspacesVerts.query.all()
    data_all = []
    return format_geojson(data)

@app.route('/ndvi')
def get_ndvi():
    # print(dict(request.data))
    # data = Ndvi.query.filter(Ndvi.geom!=None).all()
    query = select([Ndvi.gid.label('gid'), func.ST_AsGeoJSON(func.ST_Transform(Ndvi.geom,4326)).label('geom')]).where(Ndvi.geom!=None)
    dataQuery = db.session.execute(query).fetchall()
    data_all = []

    for ndvi in dataQuery:
        ndvi = dict(ndvi)
        data_all.append({
                    'type': 'Feature',
                    'properties':{
                            'gid':ndvi['gid'],
                        },
                        'geometry':json.loads(ndvi['geom'])
                        })
    return jsonify(data_all)

if __name__ == '__main__':
    app.run()

from sqlalchemy import Integer, Column, Text, Numeric
from geoalchemy2 import Geometry, Geography
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
import geojson, json
import geoalchemy2.functions as func


db = SQLAlchemy()

# def int(func):
#     def func2(opt):
#         print('is integer??? ')
#         opt = func(opt)
#         return opt+1
#     return func2

# cette classe prend en entrée un objet, on fait hériter cette classe aux autres, la fonction de conversion
# de la géométrie se fera
class DbModelGeom(object):
    @hybrid_property
    def converted_geom(self):
        return geojson.loads(json.dumps(json.loads(db.session.scalar(func.ST_AsGeoJSON(func.ST_Transform(self.geom,4326))))))

class EspacesVerts(db.Model, DbModelGeom):
    __tablename__ = 'espaces_verts_urbains'

    gid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Text)
    code_12 = db.Column(db.Text)
    area_ha = db.Column(db.Numeric)
    geom = db.Column(Geometry(geometry_type='MULTIPOLYGON', srid=32631))

class Arrondissements(db.Model, DbModelGeom):
    __tablename__ = 'arrondissements'

    gid = db.Column(db.Integer, primary_key=True)
    osm_id = db.Column(db.Text)
    name = db.Column(db.Text)
    type = db.Column(db.Text)
    geom = db.Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))
    prixmoy_m2 = db.Column(db.Numeric)

# exemple de décorateur
    # @int
    # def toto(opt):
    #     print('toto')
    #     return opt
    #
    # def tata():
    #     print('tata')
    # @hybrid_property
    # def converted_geom(self):
    #     return geojson.loads(json.dumps(json.loads(db.session.scalar(func.ST_AsGeoJSON(func.ST_Transform(self.geom,4326))))))
    #
    # @converted_geom.setter
    # def converted_geom(self, geom):
    #     print('do something')
        # convert geoJson in geom DB format_geojson
        # self.geom = 'queleque cjhose'

class Ndvi(db.Model):
    __tablename__ = 'ndvi_filtre'

    gid = db.Column(db.Integer, primary_key=True)
    geom = db.Column(Geometry(geometry_type='MULTIPOLYGON', srid=32631))

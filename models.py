from app import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nom = db.Column(db.String(100), nullable = False, unique= True)
    lat = db.Column(db.Float, nullable = False)
    lon = db.Column(db.Float, nullable = False)

    def __str__(self):
        return self.nom
    
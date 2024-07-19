from app import db

class DiseaseStatus(db.Model):
    __tablename__ = "disease_status"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    disease_code = db.Column(db.String(10), nullable=False)
    disease_name = db.Column(db.String(50), nullable=False)
    farm_name = db.Column(db.String(25), nullable=False)
    addr_code = db.Column(db.String(10), nullable=False)
    addr_name = db.Column(db.String(50), nullable=False)
    occur_date = db.Column(db.Date, nullable=False)
    livestock_type = db.Column(db.String(25), nullable=False)
    occur_count = db.Column(db.Integer, nullable=False)
    dgnss_engn = db.Column(db.String(50), nullable=True)
    end_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<DiseaseStatus {self.disease_code} - {self.farm_name}>"
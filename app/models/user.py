from app import db

class DailyChatCount(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.String, primary_key=True)
    chat_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<DailyChatCount {self.user_id}>"
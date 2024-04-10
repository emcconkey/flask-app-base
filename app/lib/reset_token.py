import settings, random, string
db = settings.db()
from datetime import datetime, timedelta, timezone


class ResetToken(db.Model):
    reset_token_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    key = db.Column(db.String(255))
    lifespan = db.Column(db.DateTime)

    def check_lifespan(self):
        return self.lifespan > datetime.now(timezone.utc)

    @staticmethod
    def generate_token(user_id):
        token = ResetToken.query.filter_by(user_id=user_id).first()
        if not token:
            token = ResetToken(user_id=user_id, lifespan=datetime.min)
        if token.lifespan < datetime.utcnow():
            token.key = ResetToken.generate_reset_key()
        token.lifespan = datetime.utcnow() + timedelta(hours=1)
        db.session.add(token)
        db.session.commit()
        return token

    @staticmethod
    def generate_reset_key():
        key = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(32))
        check = ResetToken.query.filter_by(key=key).first()
        if check:
            return ResetToken.generate_reset_key()
        return key

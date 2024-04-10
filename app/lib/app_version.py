import settings
db = settings.db()


class AppVersion(db.Model):
    app_version_id = db.Column(db.Integer, primary_key=True)
    app_version = db.Column(db.String(255))
    os = db.Column(db.String(255))

    def __repr__(self):
        return f'<App Version: {self.app_version}>'

    @staticmethod
    def get_app_version():
        android_version = AppVersion.query.filter_by(os='android').first()
        ios_version = AppVersion.query.filter_by(os='ios').first()
        return {
            'android': android_version.app_version if android_version else 'None',
            'ios': ios_version.app_version if ios_version else 'None'
        }

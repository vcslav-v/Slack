from slack_app_test import db

class finam_income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chanel_id = db.Column(db.Text)
    income_value = db.Column(db.Text)
    income_currency = db.Column(db.Text)
    income_to = db.Column(db.Text)
    comment = db.Column(db.Text)
    income_from = db.Column(db.Text)
    user_id = db.Column(db.Text)
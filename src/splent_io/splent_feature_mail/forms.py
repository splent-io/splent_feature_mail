from flask_wtf import FlaskForm
from wtforms import SubmitField


class SplentFeatureMailForm(FlaskForm):
    submit = SubmitField("Save splent_feature_mail")

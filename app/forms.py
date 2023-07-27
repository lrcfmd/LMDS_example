from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    input_string = StringField("Input strings")
    submit = SubmitField("Calculate")

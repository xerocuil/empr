from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

# FORMS
class GameForm(FlaskForm):
    description = TextAreaField()
    genre_id = IntegerField()
    esrb = StringField(validators=[Length(max=4)])
    title = StringField(validators=[DataRequired('Title required.'), Length(max=128)])
    year = IntegerField(validators=[NumberRange(min=1948, max=9999, message='Year entered is out of sanity range.')])
    submit = SubmitField("Save")
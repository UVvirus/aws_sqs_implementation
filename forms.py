from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import InputRequired,Length


class Inputform(FlaskForm):
    name=StringField("Enter a domain name",validators=[InputRequired(),Length(min=2,max=20)])
    submit=SubmitField("submit")

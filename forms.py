from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Optional

class ItemForm(FlaskForm):
    # image = FileField("Image", validators=[FileRequired()])
    name = StringField("Name", validators=[DataRequired()])
    type = StringField("Type", validators=[DataRequired()])
    brand = StringField("Brand/Creator", validators=[Optional()])
    price = IntegerField("Price", validators=[Optional()])
    character = StringField("Character", validators=[Optional()])
    series = StringField("Series", validators=[Optional()])
    date_acquired = DateField("Date Acquired", validators=[Optional()])
    description = TextAreaField("Description", validators=[DataRequired()])
    # in collection 
    submit = SubmitField("Add Item")
    
class SearchForm(FlaskForm):
    text = StringField("Text", validators=[DataRequired()])
    submit = SubmitField("Search")
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, FloatField
from wtforms.validators import DataRequired, InputRequired

from app.utils.list_images import list_images


class TransformationForm(FlaskForm):
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    color = FloatField('color', validators=[InputRequired()], default=1.0)
    contrast = FloatField('contrast', validators=[InputRequired()], default=1.0)
    brightness = FloatField('brightness', validators=[InputRequired()], default=1.0)
    sharpness = FloatField('sharpness', validators=[InputRequired()], default=1.0)
    submit = SubmitField('Submit')
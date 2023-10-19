from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        validators=[DataRequired(message='Обязательное поле'),
                    Length(max=128)]
    )
    custom_id = URLField(
        validators=[Optional(),
                    Length(max=16)]
    )
    submit = SubmitField('Создать')

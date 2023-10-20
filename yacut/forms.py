from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (ALLOWED_CHARACTERS_REGEX,
                        REQUIRED_FIELD_MESSAGE,
                        MAX_FIELD_LENGTH,
                        MAX_CUSTOM_ID_LENGTH)


class URLForm(FlaskForm):
    original_link = URLField(
        'Оригинальная ссылка',
        validators=[DataRequired(message=REQUIRED_FIELD_MESSAGE),
                    Length(max=MAX_FIELD_LENGTH)]
    )
    custom_id = URLField(
        'Пользовательский идентификатор',
        validators=[Optional(),
                    Length(max=MAX_CUSTOM_ID_LENGTH),
                    Regexp(ALLOWED_CHARACTERS_REGEX)]
    )
    submit = SubmitField('Создать')

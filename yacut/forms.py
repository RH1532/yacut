from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import (ALLOWED_CHARACTERS_REGEX,
                        REQUIRED_FIELD_MESSAGE,
                        MAX_FIELD_LENGTH,
                        MAX_SHORT_LENGTH,
                        ORIGINAL_FORM,
                        SHORT_FORM,
                        CREATE_FORM)


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_FORM,
        validators=[DataRequired(message=REQUIRED_FIELD_MESSAGE),
                    Length(max=MAX_FIELD_LENGTH)]
    )
    custom_id = URLField(
        SHORT_FORM,
        validators=[Optional(),
                    Length(max=MAX_SHORT_LENGTH),
                    Regexp(ALLOWED_CHARACTERS_REGEX)]
    )
    submit = SubmitField(CREATE_FORM)

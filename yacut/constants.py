import string
import re


ALLOWED_CHARACTERS = string.ascii_letters + string.digits
ALLOWED_CHARACTERS_REGEX = re.compile(
    r'^[' + re.escape(ALLOWED_CHARACTERS) + r']+$'
)

MAX_FIELD_LENGTH = 2048
MAX_CUSTOM_LENGTH = 16
SHORT_LENGTH = 6
MAX_CUSTOM_ATTEMPTS = 10

SHORT_REDIRECT_FUNCTION = 'redirect_to_original'
REQUIRED_FIELD_MESSAGE = 'Обязательное поле'
MISSING_REQUEST_BODY = 'Отсутствует тело запроса'
MISSING_URL_FIELD = '"url" является обязательным полем!'
INVALID_SHORT_NAME = 'Указано недопустимое имя для короткой ссылки'
DUPLICATE_SHORT = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_SHORT = 'Указанный id не найден'
TOO_CUSTOM_LENGTH = 'Слишком длинная ссылка'
SHORT_READY_MESSAGE = 'Ваша новая ссылка готова:'
SHORT_CREATION_ERROR = 'Не удалось создать уникальный короткий url'

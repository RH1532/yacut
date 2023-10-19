import string

ALLOWED_CHARACTERS = string.ascii_letters + string.digits

MISSING_REQUEST_BODY = 'Отсутствует тело запроса'
MISSING_URL_FIELD = '"url" является обязательным полем!'
INVALID_SHORT_ID_NAME = 'Указано недопустимое имя для короткой ссылки'
DUPLICATE_SHORT_ID = 'Предложенный вариант короткой ссылки уже существует.'
INVALID_SHORT_ID = 'Указанный id не найден'

### Автор 
- [Ильин Данила](https://github.com/RH1532)
### Техно-стек 
- Flask, Python, Jinja2
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/RH1532/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
###Команды
- `flask db init`: Создание миграций.
- `flask db migrate -m "Initial migration."`: Создание первоначальной миграции.
- `flask db upgrade`: Применение миграции к базе данных.
- `flask run`: Запустить приложение.
### Справка
Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.
Основные возможности проекта:
- генерация коротких ссылок и связь их с исходными длинными ссылками,
- переадресация на исходный адрес при обращении к коротким ссылкам. 
 Пользовательский интерфейс сервиса — одна страница с формой. Эта форма состоит из двух частей:
- обязательное поле для длинной исходной ссылки;
- Необязательного поле для пользовательского варианта короткой ссылки.
Пользовательский вариант короткой ссылки не должен превышать 16 символов. Если пользователь не заполнит поле со своим вариантом короткой ссылки, то сервис сгенерирует её автоматически. 
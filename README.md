### Автор 
- [Ильин Данила](https://github.com/RH1532)
### Техно-стек 
- Flask, Python, Jinja2
```
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
### Команды
- `flask run`: Запустить приложение.
- `flask --help`: Получить доступ к справке Flask.
### Справка
Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.
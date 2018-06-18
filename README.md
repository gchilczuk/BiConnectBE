# BiConnect Backend

> Aplikacja wspierająca towarzystwo biznesowe.

Aplikacja backendowa dostarczająca REST Api do zarządzania spotkaniami Towarzystwa Biznesowego.

Panel użytkownika jest dostarczany przez [BiConnectFE](https://github.com/gchilczuk/BiConnectFE)

### Instrukcja obsługi

Spis endpointów widoczny po uruchomieniu aplikacji pod adresem `localhost:8000/swag`

### Technologie

[Django](https://www.djangoproject.com/) + [Django Rest Framework](http://www.django-rest-framework.org/)

Szczegółowy spis znajduje się w pliku `requirements.txt`

### Build Setup
Aby uruchomić serwer lokalnie 
1. Utwórz virtualne środowisko z Pythonem 3.6.4
2. Zainstaluj w nim zależności `pip install -r requirements.txt`
3. Upewnij się, że jest dostępna baza danych skonfigurowana zgodnie z plikiem settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'devDB',
        'USER': 'devDB',
        'PASSWORD': 'devpass',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

Bazę możesz zainstalować z `https://www.postgresql.org/download/`
lub spróbować uruchomić ją w kontenerze dockera:
```docker run --name biconnect_local_db -e POSTGRES_USER=devDB -e POSTGRES_PASSWORD=devpass --net=host postgres```

4. Uruchom serwer poleceniem:
```python
python manage.py runserver
```
serwer będzie dostępny pod adresem: `localhost:8000`

##### sposób alternatywny - wersja niestabilna
Uruchom cały projekt zgodnie z instrukcją w [BiConnect Docker](https://github.com/gchilczuk/BiConnect)

# BiConnect Backend
### I sposób (manualny)
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

### II sposób (zautomatyzowany) - na Windowsie nie działa
Uruchom cały projekt zgodnie z instrukcją w https://github.com/gchilczuk/BiConnect

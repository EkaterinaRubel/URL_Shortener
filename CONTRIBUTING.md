#####  Инструкции предназначены для операционной системы macOS
### Инициализация рабочего окружения
- Добавить корневую директорию в `PYTHONPATH` (временно): 
    ```
    export PYTHONPATH="$PYTHONPATH:."
    ```
- Установить и активировать poetry.
    ```
    poetry install
    poetry shell
    ```

### Для запуска 
- #### Локально
```
python3 src/app/main.py
```
- #### B Docker
```
docker compose up
```
проверить отклик `curl http://0.0.0.0:8000/healthz/up`
- #### B kubernetes (HELM-Chart)
```
helm install url-shortener helm/url-shortener/
```
uninstall
```
helm uninstall url-shortener
```

### Тестирование
```
pytest src/tests -v
```
#### Для определения тестового покрытия 
```
pytest --cov=src/app src/tests
```
### Linting
```
flake8 src
```

### Сборка образов
- #### Локально
```
docker build -t base_service:1 .
```
- #### Для GitLab
```
docker build -t registry.gitlab.com/ekaterinar/url_shortener:1 .
docker push registry.gitlab.com/ekaterinar/url_shortener:1
```
### Swagger
При наличии UI и активном сервисе - документация доступна по адресу `http://0.0.0.0:8000/docs`

Иначе для получения документации в виде файла - выполнить в консоле
```
curl -k http://0.0.0.0:8000/openapi.json > swagger/openapi.json
```

Открыть в удобочитаемом виде можно на сайте [Swagger UI](https://editor.swagger.io/)
`File -> Clear Editor -> вставить json из swagger/openapi.json`
При необходимости преобразовать в yaml - согласиться.
## URL Shortener
Cервис для сокращения URL, написанный на FastAPI.
Данные хранятся в PostgreSQL.
Автотесты выполнены на pytest, (с примерением unittest.mock, fixture, параметризации). 
Тестовое покрытие 96%.
Для управления миграциями базы данных используется Alembic. 
Настроен gitlab-ci, содержащий стадии линтинга, тестирования и сборки.
Развертывается в Kubernetes с помошью Helm-чарта.
Обеспечено сопровождение сервиса в Kubernetes с помощью Prometheus метрик и трейсинга Jaeger Tracing.

### Технологии
- FastAPI 0.103.1
- PostgreSQL
- Poetry 1.5.1
- Docker, Docker-compose
- Kubernetes, HELM
- CI/CD (linter, testing, build)
- pytest (моки, параметризация, фикстуры) / pytest-cov
- Prometheus
- Jaeger Tracing
- Grafana
- alembic

### Инструкции по развертыванию
[Contributing Guidelines](CONTRIBUTING.md)
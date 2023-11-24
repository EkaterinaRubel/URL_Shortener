## Base service
Cервис для сокращения URL, написанный на FastAPI.
Данные хранятся в памяти сервиса.
Для управления миграциями базы данных используется Alembic. 
Настроен gitlab-ci, содержащий стадии линтинга, тестирования и сборки.
Развертывается в Kubernetes с помошью Helm-чарта.
Обеспечено сопровождение сервиса в Kubernetes с помощью Prometheus метрик и трейсинга Jaeger Tracing.

### Технологии
- FastAPI 0.103.1
- Poetry 1.5.1
- Docker, Docker-compose
- Kubernetes, HELM
- CI/CD (linter, testing, build)
- pytest / pytest-cov
- Prometheus
- Jaeger Tracing
- alembic
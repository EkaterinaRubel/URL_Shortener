## Base service
Добавлен минимальный сервис, содержащий healthz endpoints. 
Настроен gitlab-ci, содержащий стадии линтинга, тестирования, сборки и развертывания в Docker.
Развертывается в Kubernetes с помошью Helm-чарта.
Обеспечено сопровождение сервиса в Kubernetes с помощью Prometheus метрик и трейсинга Jaeger Tracing.

### Технологии
- FastAPI 0.103.1
- Poetry 1.5.1
- Docker, Docker-compose
- Kubernetes, HELM
- CI/CD (linter, testing, build, deploy)
- pytest / pytest-cov
- Prometheus
- Jaeger Tracing
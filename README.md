## Base service
Добавлен минимальный сервис, содержащий healthz endpoints. 
Настроен gitlab-ci, содержащий стадии линтинга, тестирования, сборки и развертывания в Docker.
Развертывается в Kubernetes с помошью Helm-чарта.

### Технологии
- FastAPI 0.103.1
- Poetry 1.5.1
- Docker, Docker-compose
- Kubernetes, HELM
- CI/CD (linter, testing, build, deploy)
- pytest / pytest-cov
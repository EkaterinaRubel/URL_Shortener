# Артефакты релизов
## 0.1.0

## task-1: Added poetry and basic documentations
Добавлен менеджер зависимостей poetry а также базовые инструменты и документация: README.md, CONTRIBUTING.md, CHANGELOG.md, .gitignore, .flake8.

## task-2: Added basic service
Добавлен минимальный сервис, содержащий healthz endpoints. 
CI содержит стадии тестирования, линтинга, сборки и развертывания в Docker.

## task-3: Added Kubernetes, HELM-charts
Сервис развертывается в K8S с помощью HELM-charts.

## task-4: Added Prometheus and Jaeger Tracing
Обеспечено сопровождение сервиса в Kubernetes с помощью Prometheus метрик и трейсинга Jaeger Tracing.

## task-5: Added processing URL
Реализована функциональность сокращения URL и перенаправления на полные URL.

## task-6: Added connection to PostgreSQL
Добавлено подключение к Postgres, ready-проба расширена проверкой доступности базы.
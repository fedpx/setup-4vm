# VM и их роли

| ВМ         | Роль               | ОС               | IP                   |
| ---------- | ------------------ | ---------------- | -------------------- |
| vm-pg      | PostgreSQL 15+     | Ubuntu           | **172.16.254.10/24** |
| vm-backend | Backend (Go)       | Ubuntu           | **172.16.254.20/24** |
| vm-redis   | Redis 7 (в Docker) | CentOS Stream 10 | **172.16.254.30/24** |
| vm-proxy   | Proxy (Flask)      | CentOS Stream 10 | **172.16.254.40/24** |


# Подтверждение работоспособности
Все сервисы запущены на VM c соответсвующими IP - https://share.cleanshot.com/CbKk0rhl
Проверочные запросы `curl -s 'http://172.16.254.40:5000/user?id=6'` с моей хостовой системы к IP vm-proxy - https://share.cleanshot.com/Pjsjf9FB

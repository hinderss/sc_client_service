# 🧠 SC Client Service

**SC Client Service** — микросервис, обеспечивающий взаимодействие с интеллектуальной системой **[Ostis](https://github.com/ostis-apps/ostis-example-app)**. Предоставляет API для авторизации, рекомендаций, навигации и интерпретации биохимических анализов крови.

---

## 🚀 API Endpoints

| Endpoint                     | Описание                                          |
| ---------------------------- | ------------------------------------------------- |
| `POST /auth`                 | Авторизация                                       |
| `POST /reg`                  | Регистрация                                       |
| `POST /nav`                  | Навигационный запрос (например, на карту понятий) |
| `POST /rec`                  | Рекомендации по медицинским вопросам              |
| `POST /blood`                | Общий анализ крови (WBC, RBC, тромбоциты)         |
| `POST /blood_vitamin`        | Витамины в крови                                  |
| `POST /blood_micronutrients` | Микроэлементы (Ca, Mg, Fe)                        |
| `POST /blood_hormones`       | Гормоны (TSH, FSH, LH)                            |
| `POST /diagnosis`            | Предварительная диагностика по симптомам          |

---

## ⚙️ Как это работает

### 🧩 Агенты

Каждое действие обрабатывается отдельным агентом (`auth_agent`, `diagnosis_agent`, и др.), который реализован как Python-класс и вызывается через фабрику агентов (`agent_factory.py`).

### 🔁 Выбор реализаций

В `config.py` описано, какие классы использовать: мок-агенты (`mock`) для тестов или настоящие (`ostis`) для взаимодействия с [Ostis SC-Server](https://github.com/ostis-dev/sc-machine).

```python
AGENTS_TO_LOAD = {
    "auth_agent": "service.agents.mock.OstisAuthAgent",
    ...
}
```

### 📄 Схемы

Для валидации и сериализации используются `marshmallow` схемы (`schemas/input.py`, `schemas/output.py`).

---

## 🔧 Установка

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/your-username/sc_client_service.git
cd sc_client_service
```

### 2. Настройка окружения

Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Конфигурация

Создайте `config.ini` в корне проекта:

```ini
[DEFAULT]
ostis_url = http://localhost:8090 # или ваш SC-Server
```

---

## ▶️ Запуск

```bash
python runner.py
```

Приложение поднимется на `http://localhost:5000`.

---

## 🧪 Пример запроса

```bash
curl -X POST http://localhost:5000/auth \
-H "Content-Type: application/json" \
-d '{"username": "demo", "password": "demo"}'
```

---

## 🗃️ Зависимости (из `requirements.txt`)

```txt
Flask==3.0.3
marshmallow==3.23.1
requests==2.32.3
py-sc-client==0.4.0
Werkzeug==3.0.6
...
```

---

## ✅ Проверка

Микросервис можно использовать совместно с основным Flask-приложением [(медицинская система)](https://github.com/hinderss/medicine-course-project/tree/feature/gpt), настроив в `.env` основной системы переменную `AGENTS_URL=http://localhost:5000`.

# 🛠 Worker App (Симулятор Работяги)

API для автоматизации учета рабочих смен с графиком 2/2 и расчетом зарплаты.

### Что умеет:

- **Авторизация:** Регистрация и вход через JWT (Bearer token).
- **График 2/2:** Автоматическая генерация смен на 2 месяца вперед одной кнопкой.
- **Учет времени:** Возможность "открыть" и "закрыть" смену.
- **Зарплата:** Автоматический расчет заработка на основе почасовой ставки при закрытии смены.
- **Статистика:** Просмотр общего баланса и истории всех смен.

---

### 🚀 Как запустить (Quick Start)

**1. Подготовка окружения:**

```bash
git clone https://github.com/ashen1ne/simulator_rabotyagi.git
cd simulator_rabotyagi
python -m venv .venv
```

**2. Активация и установка:**

- **Windows:** `.venv\Scripts\activate`
- **Linux/macOS:** `source .venv/bin/activate`

<!-- end list -->

```bash
pip install .
```

**3. Запуск сервера:**

```bash
python main.py
```

---

### 📖 Как пользоваться

1.  Перейдите в **Swagger UI**: [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)
2.  Создайте пользователя в `/auth/register`.
3.  Авторизуйтесь в `/auth/login`, скопируйте `access_token` и вставьте его в кнопку **Authorize** (вверху страницы).
4.  Сгенерируйте себе график в `/smeny/generate`.
5.  Пользуйтесь эндпоинтами для открытия/закрытия смен и проверки баланса.

---

### Стек технологий:

- **Python 3.12**, **FastAPI**, **SQLAlchemy 2.0** (Async), **SQLite**, **Pydantic v2**.

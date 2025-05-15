# Установка

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/mkcomru/test_task_xdev_team
   ```

2. Создать виртуальное окружение:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/MacOS
   source venv/bin/activate
   ```

3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустить приложение:
   ```bash
   uvicorn main:app --reload
   ```

5. Перейти в браузере по адресу для просмотра интерактивной документации API:
   ```
   http://127.0.0.1:8000/docs
   ```





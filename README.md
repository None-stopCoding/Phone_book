# Phone_book

Для запуска сервера:

	1. Создать папку venv с виртуальным окружением (Если запускать проект с PyCharm он создаст ее автоматически)

	2. Создать пустую БД Postgres с именем phone

	3. Открыть терминал с проектом и там прописать:
		- pip install -r requirements.txt
		- export FLASK_APP=phone_book.py
		- export DATABASE_URL=postgres://your_user_name_here:your_password_here@localhost/phone
		- flask db init
		- flask db migrate
		- flask db upgrade
		- flask run
	4. Запустить ngrok.exe и написать ngrok http your_port_where_machine_is_running
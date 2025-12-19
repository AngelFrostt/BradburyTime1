# BradburyTime
# команды для быстрого запуска:

cd "C:\Users\error\Desktop\bradbu\BradburyTime1-main"
venv\Scripts\activate
python manage.py runserver


#Полезные команды
# Создание новых миграций при изменении моделей
python manage.py makemigrations

# Применение миграций к базе данных
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# если ошибки с виртуальным окруженеим 
# Ууалите папку venv и создайте заново:
rmdir /s venv
python -m venv venv
venv\Scripts\activate


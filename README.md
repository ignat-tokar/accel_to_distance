# accel_to_distance
ПРЕДНАЗНАЧЕНИЕ ПРИЛОЖЕНИЯ  Приложение accel_to_distance предназначено для превращения осевого перемещения в пространственное.  Для осуществление превращения берутся данные акселерометра, а именно изменения положения по X-Z-осям (в данном случае предусматривается использование android-устройства но при желание файл main.py можно собрать для ios-устройства).  После, путем логических сравнений определяеться направление поворота устройства (вправо или влево) и соответственно увеличивается или уменьшается  Х-координата (уже интерпретируемая как точка в 2D пространстве).  Данные об изменение отправляються на сервер, где их можно считать и использовать уже в своих проектах.  УСТАНОВКА И ИСПОЛЬЗОВАНИЕ  Зайдите в папку 'bin' найдите файл 'clientaccel-0.1-armeabi-v7a-debug.apk' скачайте его на свое android-устройство и запустите (дальше - стандартный процес установки).  После - вернитесь в корневую папку проекта и скачайте на свой компьютер файл 'server.py'. Перейдите в папку со скачанным файлом и откройте ее в терминале.  !!!У вас должен быть установлен python версии 3.х!!!  Введите строку:  *Для Windows python server.py (если не работает попробуйте заменить 'python' на 'py')  *Для Linux python3 server.py  Запуститься серверная программа, которая запросит IP-адрес и номер порта для подключения. После ввода значений, если не было выведено сообщение об ошибке, значит сервер запущен и работает.   Теперь откройте приложений на android-устройстве и введите те же значения для IP-адреса и порта в соответствующие поля. Нажмите кнопку "Начать отправку данных".   Если все поля были заполненны коректно вы увидете в терминале (на компьютере) вывод данных об изменение значения координаты Х, которые можно использовать уже в своих проектах.  Чтобы остановить передачу данных нажмите кнопку "Отключить соеденение" на своем android-устройстве либо зажмите Ctrl+C на компьютере.
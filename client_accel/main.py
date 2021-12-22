# Подключение модулей для создания пользовательского интерфейса
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
# Модуль для работы с автоматическим обновление отправки данных (24 раза в сек)
from kivy.clock import Clock
# Модуль для получения данных от различных датчиков устройства
from plyer import accelerometer
# Модуль для отправки данных на сервер
import socket


# Объект предназначен для превращения осевых координат в пространственных
class XPositionCalculate():

	def __init__(self):
		self.check = True
		self.mass = [[0.0, 0.0], [0.0, 0.0]]
		self.x1 = 0.0
		self.x2 = 0.0
		self.z1 = 0.0
		self.z2 = 0.0

	# Функция задает величину изменения х-координаты
	def changing(self, x1, x2, direction):
		# Необходимо измерить величину отклонения для этого убераеться "-"
		x1 = abs(x1)
		x2 = abs(x2)
		# Создание переменной для отправки
		x = 0.0
		# Сравнение для корректного результата операции вычитания
		if x1 > x2:
			x = x1 - x2
		elif x2 > x1:
			x = x2 - x1			
		# (Ширина устройства*3.14)/40 = 6.0368
		x = 6.0368 * x
		# Если двигаемся вправо х-координату необходимо увеличить, 
		# в другом случае - уменьшить
		if direction:
			return x
		else:
			return -x

	# Функция обнаруживает направление вращения устройства - вправо или влево
	def find_direction(self, x1, x2, z1, z2):
		# Движение может происходить только в двух направлениях (вправо-влево)
		# Каждой из них может происходить в одной из четырех фаз

		# Первая фаза
		if x2 < 0 and z2 > 0:
			if x2 < x1 and z2 < z1:
				# Вправо
				return self.changing(x1,x2, True)
			elif x2 > x1 and z2 > z1:
				# Влево
				return self.changing(x1,x2, False)
		# Вторая фаза
		elif x2 < 0 and z2 < 0:
			if x2 > x1 and z2 < z1:
				# Вправо
				return self.changing(x1,x2, True)
			elif x2 < x1 and z2 > z1:
				# Влево
				return self.changing(x1,x2, False)
		# Третья фаза
		elif x2 > 0 and z2 < 0:
			if x2 > x1 and z2 > z1:
				# Вправо
				return self.changing(x1,x2, True)
			elif x2 < x1 and z2 < z1:
				# Влево
				return self.changing(x1,x2, False)
		# Четвертая фаза
		elif x2 > 0 and z2 > 0:
			if x2 < x1 and z2 > z1:
				# Вправо
				return self.changing(x1,x2,True)
			elif x2 > x1 and z2 < z1:
				# Влево
				return self.changing(x1,x2, False)
		
	# Функция регистрирует данных и передает их для подальшей обработки
	def sign_coor(self, x, z):
		# Промежуточный массивы для последней и предпоследней связки Х-Z
		self.mass.insert(0, self.mass[1])
		self.mass.insert(1, [x,z])
		# Сохрание координат
		self.x1 = self.mass[0][0]
		self.x2 = self.mass[1][0]
		self.z1 = self.mass[0][1]
		self.z2 = self.mass[1][1]
		# Передача координат для дальнейшей обработки
		return self.find_direction(self.x1, self.x2, self.z1, self.z2)


class UI(BoxLayout):#the app ui
	
	def __init__(self, **kwargs):
		super(UI, self).__init__(**kwargs)
		# Установка вертикальной ориентации для виджета
		self.orientation = 'vertical'
		# Стартовая позиция х-координаты
		self.x_pos = 0
		# Создание переменных
		self.sock = None
		self.pos_calculate = XPositionCalculate()
		self.was_started = False
		# Создание виджетов
		self.status_label = Label(text='Статус подключения:\n')
		self.accel_label = Label(text='Показания акселерометра')
		self.ip_addr = TextInput(hint_text='Введите IP-адрес для подключения')
		self.port_addr = TextInput(hint_text='Введите номер порта')
		self.start_button = Button(text='Начать отправку данных')
		self.stop_button = Button(text='Остановить отправку данных')
		# Добавление функций-слушателей для кнопок
		self.start_button.bind(on_press = self.start)
		self.stop_button.bind(on_press = self.stop)
		# Добавление виджетов на лейаут
		self.add_widget(self.status_label)
		self.add_widget(self.accel_label)
		self.add_widget(self.ip_addr)
		self.add_widget(self.port_addr)
		self.add_widget(self.start_button)
		self.add_widget(self.stop_button)
		# Проверка доступности акселерометра
		try:
			accelerometer.enable()
		except:
			self.accel_label.text = "Ну удалось обнаружить акселерометр"
		# Установка запуска функции update 24 раза за секунду
		Clock.schedule_interval(self.update, 1.0/24)

	def update(self, dt):
		txt = ''
		try:
			x = self.pos_calculate.sign_coor(accelerometer.acceleration[0],
				accelerometer.acceleration[2])
			# Проверка: было ли изменено положение устройства по х-координате
			if x:
				self.x_pos += x
			txt = '''Показания акселерометра\n\nX = %.2f
Y = %.2f\nZ = %2.f \n\nПозиция по Х-координате = %.2f''' %(
			accelerometer.acceleration[0],
			accelerometer.acceleration[1],
			accelerometer.acceleration[2],
			self.x_pos)
			# Проверка: была ли нажата кнопка "Начать отправку данных"
			if self.was_started:
				self.send(self.x_pos)
		except Exception as msg:
			txt = '''Не удалось подключиться к акселерометру
Ошибка: {}'''.format(msg)
		self.accel_label.text = txt

	def start(self, touch):
		# Попытка подключения к серверу
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((str(self.ip_addr.text), int(self.port_addr.text)))
			self.status_label.text = 'Подключение установлено'
			self.was_started = True
		except OSError as msg:
			self.status_label.text = '''Подключение не удалось
Ошибка: {}'''.format(msg)
		except Exception as msg:
			self.status_label.text = '''Подключение не удалось
Причина неизвестна...'''

	def send(self, x_pos):
		# Попытка отправки данных на сервер
		try:
			st = str(x_pos)
			self.sock.send(st.encode('utf-8'))
			self.status_label.text = '''Соеденение успешно установлено
Данные отправляются на сервер'''
		except OSError as msg:
			self.status_label.text = '''Отправка не удалась
Ошибка: {}'''.format(msg) 
		except:
			self.status_label.text = '''Отправка не удалась
Причина неизвестна...'''

	def stop(self, touch):
		# Попытка отключения соеденения
		try:
			self.sock.close()
			self.status_label.text = 'Соеденение успешно отключено'
		except OSError as msg:
			self.status_label.text = '''Не удалось отключить соеденение
Ошибка: {}'''.format(msg)
		except:
			self.status_label.text = '''Не удалось отключить соеденение
Причина неизвестна...'''


class Accelerometer(App):
    def build(self):
	    ui = UI()
	    return ui


Accelerometer().run() 
# Модуль для установления соедения с клиентом
import socket


# Функция для обработки принятых данных и выведения их в консоль
def func(data):
    x_pos = data[:9]
    x_pos = float(x_pos)
    x_pos = int(x_pos)
    print("Х-координатa относительно базовой позиции в (мм): " + str(x_pos))


# Установка значений для подключения
HOST = input('Введите IP-адрес: ')
PORT = input('Введите номер порта: ') 
# Создания экземпляра сокета
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Установка прослушивания порта по указанному IP-адресу
s.bind((HOST, int(PORT)))
s.listen(1)
# Подключение и вывод оповещения
conn, addr = s.accept()
print ('Устройство подключено - ' + str(addr))
while True:
    # Получение данных
    data = conn.recv(1024)
    if not data: break
    # Обработка данных
    func(data.decode('utf-8'))
# Закрытие соеденения
conn.close()
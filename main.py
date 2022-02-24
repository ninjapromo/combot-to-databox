import time
import json
import requests
import threading
from databox import Client

def encode_output_data(input_json):
	output_list = []
	for key, value in input_json.items():
		output_list.append({'key': key, 'value': value})

	return output_list

def parse_and_push():
	response = requests.get('https://combot.org/c/-707109232/a/json') 	# получаем данные в от combot
	if response.ok == False:											# проверяем получены ли данные, если нет - выдаем ошибку и заканчиваем выполнение функции
		print(f'Combot data parse error. Status code: {response.status_code}')
		return
	else:
		print(response.status_code)

	json_data = json.loads(response.text) 								# сериализируем данные эти данные
	json_data.popitem() 												# удаляем послейний элемент (time_stamp) из сериализированых данных

	data_to_send = encode_output_data(json_data) 						# "кодируем" данные на отправку
	pushId = client.insert_all(data_to_send) 							# отправляем данные в databox
	print (f"Push id: {pushId}\nTime: {time.time()}") 					# выводим в консоль id и время транзакции

#def main():
#	print(time.ctime())
#	threading.Timer(10, parse_and_push).start()

client = Client()														# инициализируем клиент databox с токеном пользователя
parse_and_push()
#main()



#s = sched.scheduler(time.time, time.sleep)								# инициализируем scheduler
#s.enter(5000, 1, parse_and_push)										# scheduler будет вызывать parse_and_push каждые 5 мин
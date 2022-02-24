import time
import json
import requests
import threading
from os import getenv
from databox import Client
from apscheduler.schedulers.blocking import BlockingScheduler

client = Client()		# инициализируем клиент databox с токеном пользователя
sched = BlockingScheduler()

def encode_output_data(input_json):
	output_list = []
	for key, value in input_json.items():
		output_list.append({'key': key, 'value': value})
	return output_list

@sched.scheduled_job('interval', minutes=int(getenv("DATABOX_UPDATE_INTERVAL")))
def parse_and_push():
	response = requests.get(getenv("COMBOT_LINK"))		# получаем данные в от combot
	if response.ok == False:		# проверяем получены ли данные, если нет - выдаем ошибку и заканчиваем выполнение функции
		print(f'Combot data parse error. Status code: {response.status_code}')
		return

	json_data = json.loads(response.text)		# сериализируем данные эти данные
	json_data.popitem()		# удаляем послейний элемент, time_stamp из сериализированых данных

	data_to_send = encode_output_data(json_data)		# "кодируем" данные на отправку
	pushId = client.insert_all(data_to_send)		# отправляем данные в databox
	print (f"Push id: {pushId}\tTime: {time.time()}")		# выводим в консоль id и время транзакции

if __name__ == "__main__":
	sched.start()
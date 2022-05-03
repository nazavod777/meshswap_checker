# -*- coding: utf8 -*-
from pyuseragents import random as random_useragent
from requests import Session
from msvcrt import getch
from os import system
from ctypes import windll
from urllib3 import disable_warnings
from loguru import logger
from sys import stderr, exit
from json import loads
from multiprocessing.dummy import Pool
from eth_account import Account

class Wrong_Response(BaseException):
	def __init__(self, message):
		self.message = message

disable_warnings()
def clear(): return system('cls')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
windll.kernel32.SetConsoleTitleW('MeshSwap Availability Checker | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n')

threads = int(input('Threads: '))
wallets_data_folder = input('Drop .txt with wallets or private keys: ')

with open(wallets_data_folder, 'r') as file:
	wallets_data = [row.strip() for row in file]

def mainth(wallet_data):
	for _ in range(15):
		try:
			if len(wallet_data) == 42 or len(wallet_data) == 40:
				if wallet_data[:2] != '0x':
					wallet_data = '0x' + wallet_data

				addres_to_send_data = wallet_data[:6].lower()

			else:
				if wallet_data[:2] != '0x':
					wallet_data = f'0x{wallet_data}'

				address = Account.from_key(str(wallet_data)).address
				addres_to_send_data = address[:6].lower()

			session = Session()
			session.headers.update({'user-agent': random_useragent(), 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7'})

			r = session.get(f'https://s.meshswap.fi/claim/{addres_to_send_data}.json')
			
			if not r.ok:
				raise Wrong_Response(r)

			response_json = loads(r.text)

			for current_wallet in response_json:
				if wallet_data.lower() == current_wallet:
					logger.success(f'{wallet_data} | Found')

					with open('founded.txt', 'a') as file:
						file.write(f'{wallet_data}\n')

					return

			logger.error(f'{wallet_data} | Not Found')

			return

		except Wrong_Response:
			logger.error(f'{wallet_data} | Wrong response, status code: {r.status_code}, response text: {r.text}')

		except Exception as error:
			logger.error(f'{wallet_data} | Unexpected error: {str(error)}')

	with open('not_checked.txt', 'a') as file:
		file.write(f'{wallet_data}\n')

if __name__ == '__main__':
	clear()
	pool = Pool(threads)
	pool.map(mainth, wallets_data)

	logger.success('Work completed successfully')
	print('\nPress Any Key To Exit...')
	getch()
	exit()
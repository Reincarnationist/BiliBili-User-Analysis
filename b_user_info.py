from socket import timeout
import threading
import time
import concurrent.futures

import requests
import pymysql
import random

from config import mysql_connection, headers, cookies, proxies

def load_user_agent(fake_ua_file):
	res = []
	with open(fake_ua_file, 'rb') as read_ua:
		for line in read_ua.readlines():
			res.append(line.rstrip())
	return res

fake_ua_list = load_user_agent('fake_user_agent.txt')

print("Finished loading ua list, {} has been loaded.".format(len(fake_ua_list)))

total = 0
lv0_count = 0
lock = threading.Lock()

def get_source(urls):
	global total, lv0_count

	params = {
		"headers": {
						"X-Requested-With": "XMLHttpRequest",
						"User-Agent": random.choice(fake_ua_list),
						'Referer': 'https://space.bilibili.com/' + str(random.randint(10000, 5000000)) + '?from=search&seid=' + str(random.randint(10000, 50000))
					},
		"cookies": cookies,
		"timeout": 10,
		"proxies": proxies,

	}

	# randomly choose to use proxies or not
	basic_info_proxies = {} if random.randint(0, 1) else params["proxies"]
	basic_info = requests.get(
								urls[0], 
								headers=params["headers"], 
								cookies=params["cookies"], 
								timeout=params["timeout"],
								proxies=basic_info_proxies).json()
	time.sleep(random.uniform(0.5, 1))

		
	try:
		basic_info_data = basic_info['data']
		
		if basic_info_data['level'] != 0:

			user_status_proxies = {} if random.randint(0, 1) else params["proxies"]
			user_status = requests.get(
								urls[1], 
								headers=params["headers"], 
								cookies=params["cookies"], 
								timeout=params["timeout"],
								proxies=user_status_proxies).json()
			time.sleep(random.uniform(0.5, 1))


			user_likes_and_views_proxies = {} if random.randint(0, 1) else params["proxies"]
			user_likes_and_views = requests.get(
										urls[2], headers=params["headers"], 
										cookies=params["cookies"], 
										timeout=params["timeout"],
										proxies=user_likes_and_views_proxies).json()
			time.sleep(random.uniform(0.5, 1))


			user_elec_proxies = {} if random.randint(0, 1) else params["proxies"]
			# this api tends to fail a lot
			user_elec = requests.get(
										urls[3], 
										headers=params["headers"], 
										cookies=params["cookies"], 
										timeout=params["timeout"],
										proxies=user_elec_proxies).json()

			user_status_data = user_status['data']
			user_likes_and_views_data = user_likes_and_views['data']
			
			# elec not supported
			if user_elec['code'] != 0:
				user_elec_count = -1
			else:
				user_elec_count = user_elec['data']['total_count']
			
			# live_room could be null
			live_room_status = 0 if not basic_info_data['live_room'] else basic_info_data['live_room']['roomStatus']
			# school could be null
			school_name = '' if not basic_info_data['school'] else basic_info_data['school']['name']
			
			if not basic_info_data['school']:
				basic_info_data['school'] = {'name' : ''}

			res = (
				basic_info_data['mid'], # num
				basic_info_data['name'], # str
				basic_info_data['sex'], # str
				basic_info_data['level'], # num
				basic_info_data['silence'], # num
				basic_info_data['vip']['type'], # num
				live_room_status, # num
				school_name, # str
				user_status_data['following'], # num
				user_status_data['follower'], # num
				user_likes_and_views_data['likes'], # num
				user_likes_and_views_data['archive']['view'], # num
				user_elec_count, # num
			)
			# save to db
			try:
				connection = pymysql.connect(**mysql_connection)
				cursor = connection.cursor()
				stmt = "insert into b_user values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

				cursor.execute(stmt, res)
				connection.commit()
				with lock:
					if total % 100 == 0:
						print(total)
					total += 1
				
			except:
				print('db fail', res)

		else:
			# lv 0 user
			with lock:
				lv0_count += 1
	except:
		print("Error with APIs")
		
		
	
def init_db(connection):
	cursor = connection.cursor()
	cursor.execute(
		"""create table if not exists b_user
				   (mid int primary key,
					name varchar(255),
					sex varchar(2),
					level int,
					silence int,
					vip_type int,
					live_room_status int,
					school_name varchar(255),
					following int,
					follower int,
					likes int,
					archive_view int,
					total_count int)"""
	)
	

def main(max_uid):    
	connection = pymysql.connect(**mysql_connection)
	init_db(connection)
	print('starting main thread')
	
	urls = [[
		'http://api.bilibili.com/x/space/acc/info?mid={}'.format(i),
		'http://api.bilibili.com/x/relation/stat?vmid={}'.format(i),
		'http://api.bilibili.com/x/space/upstat?mid={}'.format(i),
		'http://elec.bilibili.com/api/query.rank.do?mid={}'.format(i),
	] for i in range(10, 20)]
	with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
		executor.map(get_source, urls)

	print("Ending, got {} row of data.".format(total))
	try:
		cursor = connection.cursor()
		cursor.execute(
		"""create table if not exists b_user_lv0
				   (lv0_count int)"""
		)
		stmt = "insert into b_user_lv0 values(%s);"
		cursor.execute(stmt, lv0_count)
		connection.commit()
	except:
		print('Level 0 data failed to write to db')
	connection.close()
	
if __name__ == '__main__':
	# find the maximum uid of all registered user using binary search
	left, right = 1, 5000000000
	
	while left < right:
		middle = left + (right - left) // 2
		if requests.get('http://api.bilibili.com/x/space/acc/info?mid={}'.format(middle), headers=headers).json()['code'] == -404:
			right = middle
		else:
			left = middle + 1
	
	# left - 1 is the max uid
	max_uid = left - 1
	# Note: 1000000000 and 2000000000 are also valid but it's special case

	main(max_uid)
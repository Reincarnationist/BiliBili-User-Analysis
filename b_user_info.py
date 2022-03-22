import threading
import time
import concurrent.futures

import requests
import pymysql

from config import mysql_connection, headers, cookies



total = 0
lv0_count = 0
lock = threading.Lock()

def get_source(urls):
	global total, lv0_count

	
	basic_info = requests.get(urls[0], headers=headers, cookies=cookies, timeout=5).json()
	time.sleep(1)
	user_status = requests.get(urls[1], headers=headers, cookies=cookies, timeout=5).json()
	time.sleep(1)
	user_likes_and_views = requests.get(urls[2], headers=headers, cookies=cookies, timeout=5).json()
	time.sleep(1)
	

	# this api tends to fail a lot
	
	user_elec = requests.get(urls[3], headers=headers, cookies=cookies, timeout=5)
	if user_elec.status_code == 0:
		user_elec = user_elec.json()
	else:
		error = 3
		user_elec = {'data': {'total_count': -1}}

	try:
		basic_info_data = basic_info['data']
		
		if basic_info_data['level'] != 0:
			user_status_data = user_status['data']
			user_likes_and_views_data = user_likes_and_views['data']
			user_elec_data = user_elec['data']

			res = (
				basic_info_data['mid'], # num
				basic_info_data['name'], # str
				basic_info_data['sex'], # str
				basic_info_data['level'], # num
				basic_info_data['silence'], # num
				basic_info_data['vip']['type'], # num
				basic_info_data['live_room']['roomStatus'], # num
				user_status_data['following'], # num
				user_status_data['follower'], # num
				user_likes_and_views_data['likes'], # num
				user_likes_and_views_data['archive']['view'], # num
				user_elec_data['total_count'], # num
			)

			# save to db
			try:
				connection = pymysql.connect(**mysql_connection)
				cursor = connection.cursor()
				stmt = "insert into b_user values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

				cursor.execute(stmt, res)
				print('db success', res)
				connection.commit()
				with lock:
					total += 1
				
			except:
				print('db fail')

		else:
			# lv 0 user
			with lock:
				lv0_count += 1

	except:
		if error != 3:
			print("Error with {}".format(urls[0]))
		pass
		
		
	
def init_db(connection):
	cursor = connection.cursor()
	cursor.execute(
		"""create table if not exists b_user
				   (mid int primary key,
					name text,
					sex text,
					level int,
					silence int,
					vip_type int,
					live_room_status int,
					following int,
					follower int,
					likes int,
					archive_view int,
					total_count int)"""
	)
	


def main():    
	connection = pymysql.connect(**mysql_connection)
	init_db(connection)
	print('starting')
	
	urls = [[
		'http://api.bilibili.com/x/space/acc/info?mid={}'.format(i),
		'http://api.bilibili.com/x/relation/stat?vmid={}'.format(i),
		'http://api.bilibili.com/x/space/upstat?mid={}'.format(i),
		'http://elec.bilibili.com/api/query.rank.do?mid={}'.format(i),
	] for i in range(1,20)]
	with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
		executor.map(get_source, urls)

	print("Ending, got {} row of data.".format(total))
	connection.close()
	
if __name__ == '__main__':
	main()
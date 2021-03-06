'''
program that consumes the scheduled message
and print them on the console
'''
import configs
import requests
import datetime
import re
import time

class MsgScheduler(object):

	def __init__(self):
		self.message_queue = None

	#getter
	def get_message_queue(self):
		return self.message_queue

	#setter
	def set_message_queue(self, messages):
		self.message_queue = messages


	def get_all_messages(self):
		''' get all scheduled messages through api '''
		try:
			res = requests.get(configs.getallurl)
			if res.status_code == 202:
				self.set_message_queue(res.json())
				print("messages fetched successfully!")
				return self.get_message_queue()
		except:
			print("error occured while fetching all messages!")
		return self.message_queue

	def delete_job(self, id):
		try:
			res = requests.delete(configs.delete_url+id)
			if res.status_code == 202:
				print("job deleted successfully!")
		except:
			print("error occured while delete")


	def post_new_job(self, message, scheduled_time):
		''' add a new job to be scheduled through api '''
		data = None
		try:
			data = {}
			data['message_content'] = message
			data['delivery_time'] = scheduled_time
			res = requests.post(configs.post_new_url, json=data)
			if res.status_code == 202:
				print("message posted successfully:")
				data = res.json()
		except Exception as e:
			print(e)
			print("error occured while scheduling a new job!")

		return data

	def print_on_time(self):
			self.get_all_messages()
			job_queue = self.get_message_queue()
			print("scheduler job started! (ctrl+c to exit)")

			while True:
				try:
					current_time = datetime.datetime.now().isoformat()
					for job in job_queue: 
						job_time = str(job['message']['delivery_time'])

						if re.match(job_time, current_time):
							msg = job['message']['message_content']
							print(f"message: {msg} scheduled on {job_time}")

					time.sleep(1)

				except KeyboardInterrupt:
					break

	def addSecs(self, tm, secs):
	    fulldate = datetime.datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second)
	    fulldate = fulldate + datetime.timedelta(seconds=secs)
	    return fulldate.isoformat()

	def load_mock(self):
		print("adding 5 future jobs in 10 seconds interval:")
		current_time = datetime.datetime.now()
		print("current time: "+str(current_time))
		interval = 10
		for i in range(0,5):
			msg = f"this is test data {i}"
			job_time = self.addSecs(current_time, interval)
			print(msg+" "+job_time)
			self.post_new_job(msg, job_time)
			interval = interval+10

		#call scheduler
		self.print_on_time()

		#delete those jobs
		msg_cnt = len(self.get_all_messages())
		for i in range(msg_cnt, msg_cnt-5, -1):
			self.delete_job(f"scheduler{i}")




if __name__ == '__main__':
	scheduler = MsgScheduler()

	while True:
		user_inp = input(''' 
		*** Job Scheduler ***

		1. get messages count
		2. add a new scheduled job
		3. delete by scheduled id
		4. run scheduler
		5. run scheduler(mock data)
		6. exit

		enter choice: ''')

		try:
			choice = int(user_inp)
		except ValueError:
			print('\nPlease enter only integer option!')
			continue

		if choice == 1:
			queue_len = scheduler.get_all_messages()
			print(f"{len(queue_len)} jobs fetched!")

		elif choice == 2:
			msg = ""
			sch_time = ""
			try:
				msg = input("enter message to scheduled: ")
				sch_time = input("on what time ?: ")
			except:
				print("please enter valid inputs!")
				continue

			scheduler.post_new_job(msg, sch_time)

		elif choice == 3:
			try:
				id = input("enter scheduler id: ")
				scheduler.delete_job(id)
				print(f"job deleted: {id}")
			except Exception as e:
				print(e)
				print("enter valid scheduler id")
				continue

		elif choice == 4:
			scheduler.print_on_time()

		elif choice == 5:
			scheduler.load_mock()


		elif choice == 6:
			break

		else:
			print("enter only available options")
			continue


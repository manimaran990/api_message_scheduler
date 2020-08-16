'''
	data access object class.
	to handle all the functionalities
'''
import pymongo
import configs

class MessagesDAO(object):

	def __init__(self, api):
		self.api = api
		client = pymongo.MongoClient(configs.mongohost)
		self.db = client.MessageNoticeDB

	def abortIfMessageDoesNotExist(self, schedulerId):
		if self.db.Messages.count_documents({'scheduler_id': schedulerId}) < 1:
			self.api.abort(404, "message {} doesn't exist".format(schedulerId))

	def get_all_jobs(self):
		cursor = self.db.Messages.find()
		output = []
		for message in cursor:
			output.append({ "scheduler_id": message['scheduler_id'],  
                  "message": { 'message_content': message['message_content'], 'delivery_time': message['delivery_time'] } })
		return output

	def add_job(self, data):
		cursor = self.db.Messages
		scheduler_id = 'scheduler%d' % (cursor.count_documents({}) + 1)
		newDocument = {'scheduler_id': scheduler_id, 'message_content': data['message_content'], 'delivery_time': data['delivery_time']}
		cursor.insert_one(newDocument)
		return {"Accepted": True, "scheduler_id": scheduler_id}

	def delete_job(self, schedulerId):
		self.abortIfMessageDoesNotExist(schedulerId)
		self.db.Messages.delete_many({"scheduler_id" : schedulerId})
		return { "Accepted": True, "scheduler_id": schedulerId }
		
	def get_job(self, schedulerId):
		self.abortIfMessageDoesNotExist(schedulerId)
		output = []
		cursor = self.db.Messages.find({'scheduler_id' : schedulerId})
		for message in cursor:
		    output.append({ 'message_content': message['message_content'], 'delivery_time': message['delivery_time'] })
		return output

'''
   class to contain all the api models
'''
from flask_restplus import Api, Resource, fields, reqparse, inputs

class Models:

	def __init__(self, api):
		self.api = api
		self.models = {}

	def getModels(self):
		message = self.api.model('Message', {
		        'message_content': fields.String(required=True, description='Message Content to be delivered'),
		        'delivery_time': fields.DateTime(required=True, description='Schedule time for message Delivery', dt_format='iso8601')
		        })

		self.models['message'] = message

		messageList = self.api.model('MessageList', {
		    'scheduler_id': fields.String(readonly=True, description='The scheduler unique identifier'),
		    'message': fields.Nested(message, description='Message Content to be delivered')
		})

		self.models['messageList'] = messageList

		returnMessage = self.api.model('ReturnMessage', {
		        'Accepted': fields.Boolean(required=True, description='Return status'),
		        'scheduler_id': fields.String(required=True, description='The scheduler unique identifier')
		})

		self.models['returnMessage'] = returnMessage

		return self.models


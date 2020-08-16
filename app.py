'''
	Simple message notice application integrated with mongoDB
	by: Leema Rose
	date: 15-08-2020
'''

import flask
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restplus import Api, Resource, fields, reqparse, inputs
from werkzeug.middleware.proxy_fix import ProxyFix
from models import Models
from message_dao import MessagesDAO
import pymongo
import datetime

app = flask.Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


api = Api(app, version='1.0', title='Message Scheduler/Notifier',
    description='This api accepts messages from user and schedules it for printing messages on console',
)

ns = api.namespace('api', description='Message Notifier')

#get api models
models = Models(api)
modelDict = models.getModels()

messageList = modelDict['messageList']
returnMessage = modelDict['returnMessage']
message = modelDict['message']

#data access object 
dao = MessagesDAO(api)


@ns.route('/alljobs')
class Alljobs(Resource):
    '''Show a list of all scheduled messages, and lets you POST to schedule a new message'''
    @api.marshal_list_with(messageList)
    def get(self):
        '''List all the jobs scheduled'''
        return dao.get_all_jobs(), 202


@ns.route('/addjob')
class Addjob(Resource):
	''' add a job to the scheduler ''' 
	@api.doc('add a schedule message')
	@api.marshal_with(returnMessage, code=202)
	@api.expect(message)
	def post(self):
		'''add a new job to schedule '''
		return dao.add_job(api.payload), 202 

@ns.route('/delete/<string:schedulerId>')
@api.doc(responses={404: 'Message Not found'}, params={'schedulerId': 'The Message ID'})
class Deletejob(Resource):
	'''to delete a scheduled job'''
	@api.doc(responses={204: 'message deleted'})
	@api.marshal_with(returnMessage, code=202)
	def delete(self, schedulerId):
		'''Delete a message for given schedulerId'''
		return dao.delete_job(schedulerId), 202
     

@ns.route('/get/<string:schedulerId>')
@api.doc(responses={404: 'Message Not found'}, params={'schedulerId': 'The Message ID'})
class Getjob(Resource):
	@api.doc(description="fetch a message by schedulerId")
	@api.marshal_with(message)
	def get(self, schedulerId):
		'''Fetch a given message'''
		return dao.get_job(schedulerId), 202

    
#@ns.route('/runscheduler')
class printMessageOnConsoleOnTime(Resource):
    
    def get(self):
        '''Start a scheduler to print message on time'''
        currentTime = datetime.datetime.now().isoformat()
        cursor = db.Messages.find({'delivery_time' : currentTime})
        for message in cursor:
            print("[{}]: {}".format(message['delivery_time'], message['message_content']))
            
if __name__ == '__main__':
    app.run(debug=True)

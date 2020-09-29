# Defines the text_myself() function that texts a message
# passed to it, as a string

from twilio.rest import Client
import slack
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read('config.ini')

#preset values

cell = config_object['TWILIO']['my_cell_number']
account_sid = config_object['TWILIO']['account_sid']
auth_token = config_object['TWILIO']['auth_token']
my_twilio_number = config_object['TWILIO']['my_twilio_number']
my_cell_number = config_object['TWILIO']['my_cell_number']

slack_token = config_object['SLACK']['slack_token']

print(cell)
print(slack_token)

def text_myself(message):
	twilio_cli = Client(account_sid, auth_token)
	twilio_cli.messages.create(body=message, from_=my_twilio_number, to=my_cell_number)


def slack_to_covid(message):
	client = slack.WebClient(token=slack_token)
	client.chat_postMessage(channel='colorado-covid', text=message)

# slack_to_covid('Testing parser')
# text_myself('Testing text')



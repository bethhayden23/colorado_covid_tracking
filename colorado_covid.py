import requests
import pprint
import datetime
from messaging import *
import os

output_file_name = "covid_tally.csv"
output_file_header = "Date,Total Cases,New Cases"

# Call the API with the url
url = "https://services3.arcgis.com/66aUo8zsujfVXRIT/arcgis/rest/services/colorado_covid19_daily_state_statistics_cumulative/FeatureServer/0/query?where=1%3D1&outFields=Date,Cases&outSR=4326&f=json"
response = requests.get(url)

# make sure it ran successfully
status = response.status_code
print(status)

# # find out what format the content is in
# print(response.headers)

# convert to Python object (dictionary)
data = response.json()
# print(json_data)

# pretty print so I know what I'm looking at
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(data)

# separate out the data so I can work with it
day_data = data['features']

# loop over each dictionary and pull out separate date/case valuess
daily_case_counts = []
for item in day_data:
	one_day = item['attributes']
	daily_case_counts.append(one_day)

today = datetime.date.today()
# Uncomment line below to force the date to a specific day
# today = datetime.datetime.strptime("09/26/2020", "%m/%d/%Y")
today_formatted = today.strftime("%m/%d/%Y")
print(today_formatted)

todays_cases = None
for item in daily_case_counts:
	date = item['Date']
	cases = str(item['Cases'])
	if date == today_formatted:
		print(f'On {date}, the case count is {cases}.')
		todays_cases = cases

if not todays_cases:
	print('Not yet available')
	exit()

print(todays_cases)

one_day = datetime.timedelta(1)
yesterday_date = today - one_day
yesterday_formatted = yesterday_date.strftime("%m/%d/%Y")

for item in daily_case_counts:
	item_date = item['Date']
	cases = str(item['Cases'])
	if item_date == yesterday_formatted:
		print(f'Yesterday, the case count is {cases}.')
		yesterdays_cases = cases

new_cases = int(todays_cases) - int(yesterdays_cases)
print(f"The number of new cases in Colorado today is {new_cases}.")

slack_to_covid(f"The number of new cases in Colorado today is {new_cases}.")

output_record = f"{today_formatted},{todays_cases},{new_cases}"
print(output_record)

# create a boolean flag to track whether we are creating a new file or not
file_exists = True 

# output file size
try:
	file_stats = os.stat(output_file_name)
	print(file_stats)
	print(f'File Size in Bytes is {file_stats.st_size}')
	print(f'File Size in MegaBytes is {file_stats.st_size / (1024 * 1024)}')
# tell us it's creating a new file if no file is found
except FileNotFoundError as e:
	print(f'Creating a new file - {output_file_name}')
	file_exists = False


# Open the file = 'with' command means Python will close the file for us
# Write a header (if new file)and today's data to a file  
# Write today's data
# Python will close the file for us

# with open(output_file_name, "a") as output_file:
# 	if not file_exists:
# 		output_file.write(f"{output_file_header}\n")

# 	output_file.write(f"{output_record}\n")


from pymongo import MongoClient
import json, datetime

client = MongoClient("mongodb://dheeraj:Testing123@ds031601.mongolab.com:31601/vaccinfo")
# client = MongoClient()

db = client['vaccinfo']
schedule = db['schedule']
users = db['users']

# Return all the vaccines with week range for each
#@return: list of dictionary
def getVaccines(week):
	result = []
	query = {"week_range.s": {"$lte": week}, "week_range.e": {"$gte": week}}
	projection = {"vaccines": 1, "week_range": 1, "_id": 0}
	cursor = schedule.find(query, projection)
	for doc in cursor:
		start_week = doc["week_range"]["s"]

		end_week = doc["week_range"]["e"]

		vaccines = doc["vaccines"]
		for vaccine in vaccines:
			vaccine = json.dumps(vaccine)
			result_entry = {"vaccine": vaccine, "start_week": start_week, "end_week": end_week}
			result.append(result_entry)
	return (result)

# It registers new user with phone number & date of birth
def register(phone, dob):
	#mydob = datetime.datetime.strptime('22081991', '%d%m%Y')
	data = {"phone": phone, "dob": dob}
	if not userExist(phone):
		users.insert(data)

#Check if user Exist or not
def userExist(phone):
	if users.find({"phone": phone}).count():
		return True
	else:
		return False

#returns date of birth of the registered mobile number
#@return: date
def getInfo(phone):
	query = {"phone": phone}
	projection = {"dob": 1, "_id": 0}
	cursor = users.find_one(query, projection) #@TODO : Check for more than one entry
	if cursor and cursor["dob"]:
		dob = datetime.datetime.strptime(cursor["dob"], '%d%m%Y')
		return str(cursor["dob"])
	return False

if __name__ == '__main__':
	pass
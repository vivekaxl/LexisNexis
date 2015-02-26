from flask import Flask, request
from datetime import datetime
from server import database
import math, json, os
app = Flask(__name__, static_folder='client', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

''' check user info & return vaccines details if user exists'''
@app.route('/isRegistered', methods=["GET"])
def isRegistered():
	phone = request.args.get('mob')
	result = {}
	registration = database.getInfo(phone)
	if registration:
		result["isReg"] = True
		# result["details"] = getVaccineInfo(dob) # @param : DOB
	else:
		result["isReg"] = False
	return str(json.dumps(result["isReg"]))

@app.route('/register', methods=["GET"])
def register():
	mob = request.args.get('mob')
	dob = request.args.get('dob')
	database.register(mob, dob)

	result_str = ""
	if dob:
		vaccines = getVaccineInfo(dob) # @param : DOB
		result_str = buildString(vaccines)
	return str(result_str)

@app.route('/getVaccines', methods=["GET"])
def getVaccines():
	phone = request.args.get('mob')
	dob = database.getInfo(phone)
	result_str = ""
	if dob:
		vaccines = getVaccineInfo(dob) # @param : DOB
		result_str = buildString(vaccines)
	return result_str

def buildString(arr):
	res = ""
	for vaccine in arr:
		print vaccine
		name = vaccine["vaccine"]
		res = res + name + " is due from " + str(vaccine["start_week"]) + " to " + str(vaccine["end_week"]) + " AND "
	return res

''' Returns next Vaccination Details '''
def getVaccineInfo(dob):
	noOfWeeks = calcWeeks(dob)
	return database.getVaccines(noOfWeeks)

def calcWeeks(strBirthDate):
    date = datetime.strptime(strBirthDate, '%d%m%Y')
    today = date.today()
    delta = (today - date)
    week = int(math.floor(delta.days / 7.0))
    return week

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.debug = True
	app.run(host='0.0.0.0', port = port)


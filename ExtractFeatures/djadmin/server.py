from flask import Flask, request
from datetime import datetime
from server import database
import math, json
app = Flask(__name__, static_folder='client', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

''' check user info & return vaccines details if user exists'''
@app.route('/isRegistered/<phone>')
def isRegistered(phone):
	result = {}
	registration = database.getInfo(phone)
	if registration:
		result["isReg"] = True
		dob = registration
		result["details"] = getVaccineInfo(dob) # @param : DOB
	else:
		result["isReg"] = False
	return str(json.dumps(result))

@app.route('/register', methods=["GET"])
def register():
	mob = request.args.get('mob')
	dob = request.args.get('dob')
	database.register(mob, dob)
	return str(getVaccineInfo(dob))

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

# @app.route('/getNextVaccinationInfo/<mobileNo>')
# def getNextVaccinationInfo(mobileNo):
#     a,d = getDueDate(mobileNo)
#     #int_birthDate = 01012015
#     #str_birthTime = str('01012015')
#     #date = calculateWeeks(str_birthTime)
#     return 'Vaccination' + a + 'due on ' + d + 'for MobileNumber: ' + mobileNo


# def register():
#     pass

# def getInfantInfo():
#     raise NotImplementedError

# def calculateWeeks(str_birthDate):
#     '''Expected format is DDMMYYYY'''
#     #int_birthDate = 01012015
#     #date = datetime(year = int_birthDate[4:8], month = int_birthDate[2:4], day = int_birthDate[0:2])
#     date = datetime.strptime(str_birthDate, '%d%m%Y') 
#     return date
    
# '''DB Fetch methods here'''
# def getDueDate(mobileNo):
# 	dueDate = database.getInfo(mobileNo) # Format - %d%m%Y
# 	return dueDate

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



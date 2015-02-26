# import stackless
import MySQLdb
import xlrd
import datetime
from datetime import date
from datetime import timedelta
import time

db = MySQLdb.connect("127.0.0.1","root","server","qpcm" )
cursor = db.cursor()


today = date.today()
flag = str(today).replace('-','')
counter = 0

cursor.execute("SELECT id from qpcmms_organization where lower(name)='QP'")
for row in cursor.fetchall():
	organization_id = row[0]

def familyData():
	# copies the FAMILY data from excel sheet to database
	# workbook = xlrd.open_workbook('C:/Users/Anipr/Downloads/qpcm/qpcmms/Qpfam.xlsx')
	workbook = xlrd.open_workbook('Qpfam.xlsx')
	sheet = workbook.sheet_by_index(0)
	num_rows = sheet.nrows - 1
	num_cells = sheet.ncols - 1
	curr_row = 0
	counter = 0

	while curr_row < num_rows:
		counter = counter+1
		curr_row += 1
	 	row = sheet.row(curr_row)

	 	CLUB_CODE = sheet.cell_value(curr_row, 0)
	 	PERSONNEL_NUMBER = sheet.cell_value(curr_row, 1)
	 	DEPENDENT_FIRST_NAME = sheet.cell_value(curr_row, 2)
	 	DEPENDENT_FAMILY_NAME = sheet.cell_value(curr_row, 3)
	 	DEPENDENT_TYPE = sheet.cell_value(curr_row, 4)
	 	DEPENDENT_DOB = sheet.cell_value(curr_row, 5)
	 	DEPENDENT_SEQUENCE = sheet.cell_value(curr_row, 6)
	 	DEPENDENT_DOB = DEPENDENT_DOB.split('-')

		date = DEPENDENT_DOB[0]
		month = DEPENDENT_DOB[1]
		year = int(DEPENDENT_DOB[2])
		year_to_concat = DEPENDENT_DOB[2]

		if (year>50):
			year = '19'+ year_to_concat
		elif(year<=50 and year>=00):
			year = '20'+ year_to_concat

		months = {
			 	'JAN': '01',
			 	'FEB': '02',
			 	'MAR': '03',
			 	'APR': '04',
			 	'MAY': '05',
			 	'JUN': '06',
			 	'JUL': '07',
			 	'AUG': '08',
			 	'SEP': '09',
			 	'OCT': '10',
			 	'NOV': '11',
			 	'DEC': '12'
			 	}

		if month in months:
			month = months[month]

		DEPENDENT_DOB = year + '-' + month + '-' + date

	 	query = "INSERT INTO slave_excel_copy (f_club_code, f_member_uid, f_dependent_first_name, f_dependent_family_name, f_relationship, f_dob, f_dependent_sequence, update_flag, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, '0', NOW())"
	  	print "Inserting: ", (DEPENDENT_FIRST_NAME)
	  	cursor.execute(query, (CLUB_CODE, PERSONNEL_NUMBER, DEPENDENT_FIRST_NAME, DEPENDENT_FAMILY_NAME, DEPENDENT_TYPE, DEPENDENT_DOB, DEPENDENT_SEQUENCE))

	db.commit()
	print 'Now of data entered: ', counter


def memberData():
	# copies the MEMBER data from excel sheet to database
	# workbook = xlrd.open_workbook('C:/Users/Anipr/Downloads/qpcm/qpcmms/Qpdata.xlsx')
	workbook = xlrd.open_workbook('data.xlsx')
	sheet = workbook.sheet_by_index(0)
	num_rows = sheet.nrows - 1
	num_cells = sheet.ncols - 1
	curr_row = 0
	counter = 0
	while curr_row < num_rows:
		counter = counter+1
		curr_row += 1
	 	row = sheet.row(curr_row)

	 	CLUB_CODE = sheet.cell_value(curr_row, 0)
	 	PERSONNEL_NUMBER = sheet.cell_value(curr_row, 1)
	 	FAMILY_NAME = sheet.cell_value(curr_row, 2)
	 	FIRST_NAME_1 = sheet.cell_value(curr_row, 3)
	 	FIRST_NAME_2 = sheet.cell_value(curr_row, 4)
	 	FIRST_NAME_3= sheet.cell_value(curr_row, 5)
	 	INITIALS = sheet.cell_value(curr_row, 6)
	 	ARABIC_NAME = sheet.cell_value(curr_row, 7)
	 	GENDER = sheet.cell_value(curr_row, 8)
	 	MARTIAL_STATUS = sheet.cell_value(curr_row, 9)
	 	NATIONALITY = sheet.cell_value(curr_row, 10)
	 	DEPARTMENT = sheet.cell_value(curr_row, 11)
	 	WORK_LOCATION = sheet.cell_value(curr_row, 12)
	 	OFFICE_PHONE = sheet.cell_value(curr_row, 13)
	 	OFFICE_FAX = sheet.cell_value(curr_row, 14)
	 	PERSONNEL_LEVEL = sheet.cell_value(curr_row, 15)
	 	POS_DESC = sheet.cell_value(curr_row, 16)
	 	CONT_TYPE = sheet.cell_value(curr_row, 17)
	 	CONT_TERM_REASON = sheet.cell_value(curr_row, 18)
	 	CONT_EXPIRY_DATE = sheet.cell_value(curr_row, 19)
	 	NUM_DEPENDENTS = sheet.cell_value(curr_row, 20)
	 	ACTIVE_STATUS = sheet.cell_value(curr_row, 21)
	 	EXTRACT_RUN_DATE = sheet.cell_value(curr_row, 22)

	 	query = "INSERT INTO slave_excel_copy (m_club_code,  m_name , m_member_uid, m_first_name_1, m_first_name_2, m_first_name_3, m_initials, m_arabic_name, m_gender, m_maritalstatus, m_nationality, m_department, m_worklocation, m_mobileno, m_office_fax_no, m_membership_category, m_pos_desc, m_cont_type, m_cont_term_reason, m_cont_expiry_date, m_number_of_dependents, m_active_status, m_extract_run_date, update_flag, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending', %s, '0', NOW())"
	  	print "Inserting: ", (FIRST_NAME_1)
	  	cursor.execute(query, (CLUB_CODE, FAMILY_NAME, PERSONNEL_NUMBER,  FIRST_NAME_1, FIRST_NAME_2, FIRST_NAME_3, INITIALS, ARABIC_NAME, GENDER, MARTIAL_STATUS, NATIONALITY, DEPARTMENT, WORK_LOCATION, OFFICE_PHONE, OFFICE_FAX, PERSONNEL_LEVEL, POS_DESC, CONT_TYPE, CONT_TERM_REASON, CONT_EXPIRY_DATE, NUM_DEPENDENTS,  EXTRACT_RUN_DATE))

	db.commit()
	print 'Now of data entered: ', counter

def countFamilyMembers():
	#selects the member_id in slave_excel_copy
	#selects the family details of the selected member_id
	#Update/insert some table

	counter = 0
	#sql = 'SELECT member_uid from qpcmms_member WHERE member_uid IS NOT NULL'
	cursor.execute("SELECT member_uid from qpcmms_member WHERE member_uid IS NOT NULL")
	for row in cursor.fetchall():
		counter = counter + 1
		print "*******"
		member_id = row[0]
		#sql = "SELECT id_slave_excel, f_member_uid from slave_excel_copy WHERE f_member_uid=%s AND f_member_uid IS NOT NULL", (member_id)
		cursor.execute("SELECT id_slave_excel, f_member_uid from slave_excel_copy WHERE f_member_uid=%s AND f_member_uid IS NOT NULL", [member_id])
		flag = 0
		for row in cursor.fetchall():
			flag = flag + 1
			# type(member_id)
			family_flag = member_id + long(flag)
			id_slave_excel = row[0]
			print "Family Flag: ", family_flag
			print id_slave_excel
			sql = "UPDATE qpcm.slave_excel_copy SET flag=%s WHERE id_slave_excel=%s",(family_flag, id_slave_excel)
			cursor.execute(*sql)


	print 'Counter: ', counter
	db.commit()



def compareWithView():
	sql = "SELECT m_member_uid from slave_excel_copy WHERE m_member_uid IS NOT NULL"
	cursor.execute(sql)
	for row in cursor.fetchall():
		member_id_in_db = row[10] #m_member_uid

	query = "SELECT f_member_uid from slave_db_view"
	cursor.execute(query)
	for data in cursor.fetchall():
		print data[0]

def slaveToMasterMember():
	#copies member-data from slave_excel_copy table to qpcmms_member table!
    sql = "SELECT * from slave_excel_copy WHERE m_member_uid IS NOT NULL"
    cursor.execute(sql)
    for row in cursor.fetchall():
    	member_id = row[10]
    	name = row[9]
    	first_name_1 = row[11]
    	first_name_2 = row[12]
    	first_name_3 = row[13]
    	initials = row[14]
    	gender = row[16]
    	maritalstatus = row[17]
    	nationality = row[18]
    	department = row[19]
    	worklocation = row[20]
    	mobileno = row[21]
    	office_fax_no = row[22]
    	membership_category = row[23]
    	pos_desc = row[24]
    	cont_type = row[25]
    	cont_term_reason = row[26]
    	cont_expiry_date = row[27]
    	number_of_dependents = row[28]
    	status = row[29]
    	extract_run_date = row[30]
    	qpuser_id = 1
    	clubs_allowed = '[<club: Jinan Recreation Club>, <club: Al-Shareen Recreation Club>, <club: Alghazal Club>]'

    	print gender, member_id
        query = "INSERT INTO qpcmms_member (name , member_uid, first_name_1, first_name_2, first_name_3, initials, gender, maritalstatus, nationality, department, worklocation, mobileno, office_fax_no, membership_category, pos_desc, cont_type, cont_term_reason, cont_expiry_date, No_of_dependents, status, organization_id, extract_run_date, qpuser_id, clubsallowed, datetime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"
        cursor.execute(query, (name, member_id, first_name_1, first_name_2, first_name_3, initials, gender, maritalstatus, nationality, department, worklocation, mobileno, office_fax_no, membership_category, pos_desc, cont_type, cont_term_reason, cont_expiry_date, number_of_dependents, status, organization_id, extract_run_date, qpuser_id, clubs_allowed))

    db.commit()


def newDataInMember():
	#insert new  member from slave table to family table. It checks for the update_flag in slave table, if the update_flag is 0 then this member goes into member table.

	sql = "SELECT * from qpcmms_member WHERE update_flag=0 AND flag IS NOT NULL AND m_member_uid IS NOT NULL"
	cursor.execute(sql)
	for row in cursor.fetchall():
		member_id = row[2]
		id_slave_excel = row[0]
		club_code = row[1]
		dependent_first_name = row[3]
		dependent_family_name = row[4]
		relationship = row[5]
		date_of_birth = row[6]
		dependent_sequence = row[7]
		flag = row[31]
		print "member id: ", member_id, "with flag: ", row[31], "status is: ", row[32]

		sql_id = "SELECT * FROM qpcmms_member WHERE member_uid=%s", (member_id)
		print sql_id
		cursor.execute(*sql_id)
		for data in cursor.fetchall():
			id = data[0]

			sql_to_insert = "INSERT INTO `qpcmms_family` (member_id, dapendent_first_name1, dependent_family_name, dependent_sequence, relationship, dob, status, family_flag, time_flag) VALUES (%s, %s, %s, %s, %s, %s,'Active', %s, CURDATE())"
			cursor.execute(*sql_to_insert)


def copyFamilyDataFromSlaveToMaster():
	counter = 0


	check_sql = cursor.execute("SELECT count(*) from qpcmms_family")
	num_of_rows_family  = cursor.fetchone()[0]
	

	last_id_sql = cursor.execute("SELECT MAX(id) from qpcmms_family")
	last_id = cursor.fetchone()[0]
	if last_id is None:
		last_id = 0
	

	if(num_of_rows_family == 0):
		sql_for_id = "SELECT id, member_uid FROM qpcmms_member"
		cursor.execute(sql_for_id)
		for data in cursor.fetchall():
			#fetch db id and member id from qpcmms_member, db_id is the primary key
			id = data[0]
			member_id = data[1]

			#sql = "SELECT * from slave_excel_copy WHERE f_member_uid=%s", (member_id)
			cursor.execute("SELECT * from slave_excel_copy WHERE f_member_uid=%s", [member_id])
			for row in cursor.fetchall():
				id_slave_excel = row[0]
				member_id = row[2]
				club_code = row[1]
				dependent_first_name = row[3]
				dependent_family_name = row[4]
				relationship = row[5]
				date_of_birth = row[6]
				dependent_sequence = row[7]
				flag = row[31]
				# print dependent_first_name
				# print "checking for: ", member_id
				last_id += 1

				#create the family_uid
				last_uid = str(member_id) + '000' + str(last_id)
				print last_uid
			# print family_flag
				print "num_row: ", num_of_rows_family
				some_sql_statement = "INSERT INTO `qpcmms_family` (member_id, dapendent_first_name1, dependent_family_name, dependent_sequence, family_uid, relationship, dob, status, family_flag, time_flag) VALUES (%s, %s, %s, %s, %s, %s, %s,'Active', %s, CURDATE())"
				cursor.execute(some_sql_statement, (id, dependent_first_name,dependent_family_name, dependent_sequence, last_uid,relationship, date_of_birth, flag))
				print "Inserting: ", member_id
				

				sql_slave_update = "UPDATE `slave_excel_copy` SET `update_flag`=%s WHERE `f_member_uid`=%s AND `flag`=%s", ('1', member_id, flag)
				cursor.execute(*sql_slave_update)
				print "Updating: ", member_id, "with flag id: ", flag



		db.commit()


	# elif(num_of_rows_family != 0):
	# 	sql = "SELECT * from slave_excel_copy WHERE f_member_uid IS NOT NULL"
	# 	cursor.execute(sql)
	# 	for row in cursor.fetchall():
	# 		id_slave_excel = row[0]
	# 		member_id = row[2]
	# 		club_code = row[1]
	# 		dependent_first_name = row[3]
	# 		dependent_family_name = row[4]
	# 		relationship = row[5]
	# 		date_of_birth = row[6]
	# 		dependent_sequence = row[7]
	# 		flag = row[31]
	# 		print "checking for: ", member_id


	# 		print "num_row_not_zero: ", num_of_rows_family
	# 		some_sql_statement = "SELECT * from qpcmms_family WHERE member_id=%s and family_flag=%s", (member_id, flag)
	# 		cursor.execute(*some_sql_statement)
	# 		for some_data in cursor.fetchall():
	# 			member_id_in_master = some_data[17]
	# 			family_flag_in_master = some_data[18]

	# 			print "ID in master: ", member_id_in_master

	# 			#update the qpcmms_family table with new data
	# 			sql_to_update = "UPDATE qpcmms_family SET dapendent_first_name1=%s, dependent_family_name=%s, dependent_sequence=%s, relationship=%s, dob=%s WHERE member_id=%s AND family_flag=%s", (dependent_first_name, dependent_family_name, dependent_sequence, relationship, date_of_birth,  member_id, flag)

	# 			#update the slave table with a flag, so that you know which member_id and family_flag has been updated in the master table
	# 			sql_slave_update = "UPDATE slave_excel_copy SET update_flag=1 WHERE m_member_uid=%s AND flag=%s", (member_id, flag)
	# 			cursor.execute(*sql_slave_update)
		
	# 		#insert the NEW family members with update_flag=0
	# 		another_sql_statement = "SELECT * FROM slave_excel_copy WHERE update_flag=0"
	# 		cursor.execute(another_sql_statement)
	# 		for newly_added_data in cursor.fetchall():
	# 			print "Member id of new data: ", newly_added_data[10]
	# 			print "Family flag: ", newly_added_data[31]

	# 			some_sql_statement = "INSERT INTO qpcmms_family (member_id, dapendent_first_name1, dependent_family_name, dependent_sequence, relationship, dob, family_flag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
	# 			cursor.execute(some_sql_statement, (member_id, dependent_first_name, dependent_family_name, dependent_sequence, relationship, date_of_birth, flag))

		








		#check whether a member_id from slave table is there in master table or not, if not there then push the data else discard it
		# print "num: ", num_of_rows_family
		# if(num_of_rows_family == 0):
		# 	query = "INSERT INTO qpcmms_family (member_id, dapendent_first_name1, dependent_family_name, dependent_sequence, relationship, dob, family_flag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
		# 	cursor.execute(query, (member_id, dependent_first_name, dependent_family_name, dependent_sequence, relationship, date_of_birth, flag))
		# 	print "Inserting: ", member_id
		# #there might be some error, will figure it out and I have to integrate the update thing as well
		# elif(num_of_rows_family != 0):
		# 	query = "SELECT member_id from qpcmms_family WHERE member_id=%s", (member_id)
		# 	cursor.execute(*query)
		# 	for data in cursor.fetchall():
		# 		print "Member ID from qpcmms_family: ", data[0]
			# 	print "data: ", data[0]
			# print "num: ", num_row
			# sql = "UPDATE qpcm.slave_excel_copy SET flag=%s WHERE id_slave_excel=%s",(family_flag, id_slave_excel)
			# cursor.execute(*sql)


	print 'Counter: ', counter
	db.commit()

def newDataInFamily():
	#insert new family member from slave table to family table. It checks for the update_flag in slave table, if the update_flag is 0 then this member goes into family table.

	sql = "SELECT * from slave_excel_copy WHERE update_flag=0 AND flag IS NOT NULL AND f_member_uid IS NOT NULL"
	cursor.execute(sql)
	for row in cursor.fetchall():
		member_id = row[2]
		id_slave_excel = row[0]
		club_code = row[1]
		dependent_first_name = row[3]
		dependent_family_name = row[4]
		relationship = row[5]
		date_of_birth = row[6]
		dependent_sequence = row[7]
		flag = row[31]
		print "member id: ", member_id, "with flag: ", row[31], "status is: ", row[32]

		sql_id = "SELECT * FROM qpcmms_member WHERE member_uid=%s", (member_id)
		print sql_id
		cursor.execute(*sql_id)
		for data in cursor.fetchall():
			id = data[0]

			sql_to_insert = "INSERT INTO `qpcmms_family` (member_id, dapendent_first_name1, dependent_family_name, dependent_sequence, relationship, dob, status, family_flag, time_flag) VALUES (%s, %s, %s, %s, %s, %s,'Active', %s, CURDATE())"
			cursor.execute(*sql_to_insert)

def oldDataInFamilyTable():
	#(deactivates the status of a family member)/(deletes a family member from dbin) whose data is not present in the new excel sheet
	sql = "SELECT * FROM qpcmms_family WHERE time_flag < CURDATE()"
	cursor.execute(sql)

	for row in cursor.fetchall():
		family_flag_to_deactivate = row[18]
		sql_deactivate = "UPDATE qpcmms_family SET status='InActive' WHERE family_flag=%s", (family_flag_to_deactivate)
		cursor.execute(*sql_deactivate)
		print family_flag_to_deactivate
		

	db.commit()



check_sql = cursor.execute("SELECT COUNT(*) from qpcmms_member")
num_of_row_qpcmms_member = cursor.fetchone()[0]

check_sql = cursor.execute("SELECT COUNT(*) from slave_excel_copy WHERE m_member_uid IS NOT NULL")
num_of_row_slave_excel_copy = cursor.fetchone()[0]

#if ((num_of_row_qpcmms_member == 0) && (num_of_row_slave_excel_copy == 0)):
 #	memberData()
 #	slaveToMasterMember()
# 	print "hello"



#TODO:
# check for the first id while copying to member table to avoid redundancy
#check for family_table to update copyFamilyData...

# memberData()
# familyData()
# countFamilyMembers()
# slaveToMasterMember()
copyFamilyDataFromSlaveToMaster()
#familyDatabaseCopy()
#compareWithView()
#newDataInFamily()
#oldDataInFamilyTable()
db.close()
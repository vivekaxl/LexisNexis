import xlrd
import MySQLdb

# Open the workbook and define the worksheet
book = xlrd.open_workbook("Qpfam.xlsx")
sheet = book.sheet_by_name("Qpfam")

# Establish a MySQL connection
database = MySQLdb.connect (host="localhost", user = "root", passwd = "server", db = "qpcm")

# Get the cursor, which is used to traverse the database, line by line
cursor = database.cursor()

# Create the INSERT INTO sql query


# Create a For loop to iterate through each row in the XLS file, starting at row 2 to skip the headers
for r in range(1, sheet.nrows):
      CLUB_CODE          = str(sheet.cell(r,0).value)
      PERSONNEL_NUMBER  = str(sheet.cell(r,1).value)
      DEPENDENT_FIRST_NAME = str(sheet.cell(r,2).value)
      DEPENDENT_FAMILY_NAME = str(sheet.cell(r,3).value)
      DEPENDENT_TYPE = str(sheet.cell(r,4).value)
      DEPENDENT_DOB = str(sheet.cell(r,5).value)
      DEPENDENT_SEQUENCE = str(sheet.cell(r,6).value)
      values = (CLUB_CODE, PERSONNEL_NUMBER, DEPENDENT_FIRST_NAME, DEPENDENT_FAMILY_NAME, DEPENDENT_TYPE, DEPENDENT_DOB, DEPENDENT_SEQUENCE)
      query = "INSERT INTO slave_excel_copy (f_member_uid, f_dependent_first_name, f_dependent_family_name, f_relationship, f_dependent_sequence) VALUES (%s, %s, %s, %s, %s)"%(PERSONNEL_NUMBER, DEPENDENT_FIRST_NAME, DEPENDENT_FAMILY_NAME, DEPENDENT_TYPE,  DEPENDENT_SEQUENCE)

      # Assign values from each row
      # Execute sql Query
      print query
      print "Inserting: ", (DEPENDENT_FIRST_NAME)
      cursor.execute(query)

# Close the cursor
cursor.close()

# Commit the transaction
database.commit()

# Close the database connection
database.close()

# Print results
print ""
print "All Done! Congrats."
print ""
columns = str(sheet.ncols)
rows = str(sheet.nrows)
print "Task Finished."

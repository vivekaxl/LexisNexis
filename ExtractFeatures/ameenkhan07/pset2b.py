#The following variables contain values as described below:
#balance - the outstanding balance on the credit card
#annualInterestRate - annual interest rate as a decimal

balance = 3329
annualInterestRate = 0.2

minimumMonthlyPayment = 10.0
monthlyInterestRate=(annualInterestRate) / 12.0

while True:
	bal=balance
	for i in range(1,13):
		monthlyUnpaidBalance = (bal) - (minimumMonthlyPayment)
		bal = (monthlyUnpaidBalance) + (monthlyInterestRate * monthlyUnpaidBalance)
	if(bal>0):
		minimumMonthlyPayment+=10
	else:
		break

print("Lowest Payment:"+str(minimumMonthlyPayment))
balance = 999999
annualInterestRate = 0.18
raw_input("Enter some some")
monthlyInterestRate = (annualInterestRate) / 12.0

lowerBound = balance / 12
upperBound = (balance * (1 + monthlyInterestRate)*12)/ 12.0
bal=balance

while bal>.02:
	bal=balance
	minimumMonthlyPayment=(lowerBound+upperBound)/2
	for i in range(1,13):
		monthlyUnpaidBalance=(bal)-(minimumMonthlyPayment)
		bal=(monthlyUnpaidBalance)+(monthlyInterestRate * monthlyUnpaidBalance)
	if balance>0:
		lowerBound=minimumMonthlyPayment
	else:
		upperBound=minimumMonthlyPayment

print("Lowest Payment:"+str( round(minimumMonthlyPayment,2) ) )
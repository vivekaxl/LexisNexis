balance = 4213
annualInterestRate = 0.2
monthlyPaymentRate = 0.04
total_paid=0.0
for i in range(1,13):
	monthlyInterestRate =(annualInterestRate)/12.0
	minimumMonthlyPayment = (monthlyPaymentRate*balance)
	monthlyUnpaidBalance = (balance - minimumMonthlyPayment)
	balance = monthlyUnpaidBalance + (monthlyInterestRate *monthlyUnpaidBalance) 

	print("Month:"+str(i) )
	print("Minimum monthly payment:"+str(round(minimumMonthlyPayment,2)))
	print("Remaining balance:"+str(round(balance,2)))
	total_paid +=minimumMonthlyPayment

print("Total Paid:"+str(round(total_paid,2)))
print("Remaining Balance"+str(round(balance,2)))

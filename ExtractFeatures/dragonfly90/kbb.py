import mechanize
br=mechanize.Browser()
br.open('http://www.kbb.com/whats-my-car-worth/')
#br.select_form(predicate=lambda(form): 'yearid' in form.action)
#br['yearid']=2001
#br['manufacturername']=Honda
#br['modelname']=Accord
#br['mileage']=54000
#response=br.submit()
#content=response.read()
#print content
#response=br.open('http://www.edmunds.com/')
for form in br.forms():
    print '%r %r %s' %(form.name,form.attrs.get('id'),form.action)
    for control in form.controls:
        print ' ', control.type,control.name,repr(control.value)

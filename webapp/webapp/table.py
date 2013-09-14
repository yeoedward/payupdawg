from django.db import models
from models import Receipt

#create receipt (5)
#add receipts to table
#show name, category/ies, price, 



table = []
table.append(Receipt(name="1", price="5.00", user="Niki"))
table.append(Receipt(name="2", price="2.00", user='Marisa'))

for x in xrange(0,2):
    print("You owe " + table[x].user + " $" + table[x].price)





# DatabaseDataGenerator

# https://pypi.org/project/DatabaseDataGenerator

## Generates large amounts of fake data for testing purposes

## Currently only supports postgresql & sqlite3!

---

Example of use can be found in main.py

Generators can be found in Generators.py

The majority of generators are wrappers of [Faker](https://faker.readthedocs.io/en/master/index.html)

---

## Another example

```py
from DataGenerator import *
from DataGenerator.Generators import *
from DataGenerator.Table import *
from DataGenerator.Column import *
# Currently I don't know how to handle imports any better

# Initialize database where insertion replaces rows which already exist (with same pk)
db = Databases.PostgreSQLDB(override=True)
db.connect(user="demo", password="demo", ip="127.0.0.1", port="5432", dbName="demo")

# Create a table object which will signify the existance of that table in the database
# In other words, when queries are generated these are the tables that are inserted to
some_table = Table("some_table_name")
# INSERT INTO some_table_name VALUES ...

# A database can have multiple tables and they will all be added rows simultaneously though this is untested yet
db.setTable(some_table)

# Adding columns to a table can either be done in batch (like below) or one by one
# Columns have a name and a generator, they can also be the primary key (the pk comes into play when override is enabled and rows will be overriden by removing the row by the PK column)
some_table.addColumns([
	Column("id", SerialGenerator(1), True),
	Column("some_data", RandomStringGenerator()),
])
# Example of adding one column
some_table.addColumn(Column("some_other_data", RandomIntegerGenerator(1e3, 1e6)))

# From here calling db.insertRow() will insert a single row, call it multiple times to insert mutliple rows
for i in range(100):
	db.insertRow()

# Can also be used to insert 200 rows to some_table
db.insertRows(some_table, 200)
```

---

`db.wipeTable(Table)` can be used for dropping all entries in a table, see main.py for example

---

## Available generators

With example output

```py
RandomStringGenerator(length=10, 
                      hasLowercase=True, 
                      hasUppercase=False,
                      hasDigits=False)
# RandomStringGenerator(24, True, True, False)                      
# CgR9MmJqbdIGmhB8tixhqetC
# 6QahKKKYKJwIfmhTYksARQK8
# KvG3YT8qU0nIqTngv4FFX8l0

RandomIntegerGenerator(min, max)
# RandomIntegerGenerator(1e2, 1e6)
# 850992
# 319942
# 568911

SerialGenerator(start=0, step=1)
# SerialGenerator()
# 0
# 1
# 2

SetGenerator(chSet, destructive=False)
# for destructive=True entries are removed from the set as they are picked
# SetGenerator({'a', 'b', 12, 43, "testing"})
# 12
# b
# a

FakeFirstNameGenerator()
# FakeFirstNameGenerator()
# Kimberly
# Kathleen
# Ryan

FakeLastNameGenerator()
# FakeLastNameGenerator()
# Horne
# Barry
# Cantu

FakeNameGenerator()
# FakeNameGenerator()
# Julian Bryant
# Jerry King
# Debbie Hubbard

FakeCityGenerator()
# FakeCityGenerator()
# West Sarahfurt
# Susanside
# Robertmouth

FakeCountryGenerator()
# FakeCountryGenerator()
# Bulgaria
# American Samoa
# France

FakeStreetGenerator()
# FakeStreetGenerator()
# Ferguson Fords
# Thomas Summit
# Jones Walks

FakeEmailGenerator()
# FakeEmailGenerator()
# david56@example.net
# kaufmangrace@example.com
# lisaschmidt@example.com

FakeIPv4Generator()
# FakeIPv4Generator()
# 100.239.243.174
# 212.240.225.211
# 22.42.176.240

FakeIPv6Generator()
# FakeIPv6Generator()
# b2ce:dcd2:83de:657:310a:3279:95f4:91db
# 6532:eec7:d615:7bf5:814c:3be9:9a65:606e
# be69:81ab:9d91:5896:7413:451c:24ac:a95b

FakeMacGenerator()
# FakeMacGenerator()
# 6f:6c:d4:44:0d:89
# 73:6e:6e:c8:0a:cf
# 3e:e6:83:34:43:69

FakeUriGenerator()
# FakeUriGenerator()
# http://www.smith.org/tag/home/
# https://www.gutierrez-calhoun.org/about.htm
# https://www.vincent-jennings.com/list/main/app/home.php

FakeUrlGenerator()
# FakeUrlGenerator()
# http://williams.com/
# https://waters.com/
# https://www.williams.com/

FakeUsernameGenerator()
# FakeUsernameGenerator()
# prussell
# evanmartinez
# huntbrandi

FakeCreditCardNumberGenerator()
# FakeCreditCardNumberGenerator()
# 4591224799613
# 4396095491829044
# 3520959742328224

FakeDateGenerator()
# FakeDateGenerator()
# 1996-05-08
# 1983-04-23
# 1984-06-12

FakeCurrentDecadeDateGenerator()
# FakeCurrentDecadeDateGenerator()
# 2021-04-12
# 2020-11-02
# 2020-04-11

FakeCurrentMonthDateGenerator()
# FakeCurrentMonthDateGenerator()
# 2022-01-16
# 2022-01-04
# 2022-01-17

FakeCurrentYearDateGenerator()
# FakeCurrentYearDateGenerator()
# 2022-01-06
# 2022-01-08
# 2022-01-04

FakeVehicleModelGenerator()
# FakeVehicleModelGenerator()
# Express 1500 Passenger
# Explorer Sport Trac
# Santa Fe Sport

FakeVehicleMakeGenerator()
# FakeVehicleMakeGenerator()
# Chevrolet
# Ram
# Lexus

FakeLicensePlateGenerator()
# FakeLicensePlateGenerator()
# FF1 5232
# XU2 X0Q
# PC 66274
```
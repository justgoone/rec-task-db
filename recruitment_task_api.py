import requests
import json
import argparse
import sqlite3
from datetime import date
import collections

today = date.today()

def count_days(personDob, today):
    checkDate = date(today.year, personDob.month, personDob.day)
    daysUntilBday = (checkDate - today).days
    if (daysUntilBday < 0):
        if (personDob.month == 2 and personDob.day == 29):
            #exception of a person being born on 29th of February
            #asked via email, was left with free choice between 28.02 and 01.03, chose the 28th
            checkDate = date(today.year + 1, personDob.month, personDob.day - 1)
            daysUntilBday = (checkDate - today).days
            return daysUntilBday
        else:
            checkDate = date(today.year + 1, personDob.month, personDob.day)
            daysUntilBday = (checkDate - today).days
    return daysUntilBday

def add_days_until_bday(listOfPeople):
    for person in listOfPeople['results']:
        dob = person['dob']['date'].split('T')[0].split('-')
        personDayOfBirth = date(int(dob[0]), int(dob[1]), int(dob[2]))
        daysUntilBirthday = count_days(personDayOfBirth, today)
        person['dob']['daysUntilBirthday'] = daysUntilBirthday

def transform_phone_numbers_to_digits_only(listOfPeople):
    for person in listOfPeople['results']:
        cellNumber = person['cell']
        phoneNumber = person['phone']
        cellNumber = ''.join(num for num in cellNumber if num.isdigit())
        phoneNumber = ''.join(num for num in phoneNumber if num.isdigit())
        person['cell'] = cellNumber
        person['phone'] = phoneNumber

def remove_pictures_from_file(listOfPeople):
    for person in listOfPeople['results']:
        del person['picture']

def transform_data(numberOdPeople):
    peopleList = requests.get('https://randomuser.me/api/?results='+numberOdPeople)
    allData = peopleList.json()
        
    add_days_until_bday(allData)
    transform_phone_numbers_to_digits_only(allData)
    remove_pictures_from_file(allData)

    return allData

def create_database():
    dbConnection = sqlite3.connect('people.db')
    cursor = dbConnection.cursor()
    cursor.execute("""
    CREATE TABLE user (
        gender str, 
        name_title str, 
        name_first str, 
        name_last str, 
        location_street_number int, 
        location_street_name str, 
        location_city str, 
        location_state str, 
        location_country str, 
        location_postcode str, 
        location_coordinates_latitude str, 
        location_coordinates_longitude str, 
        location_timezone_offset str, 
        location_timezone_description str, 
        email str, 
        login_uuid str, 
        login_username str, 
        login_password str, 
        login_salt str, 
        login_md5 str, 
        login_sha1 str, 
        login_sha256 str, 
        dob_date str, 
        dob_age int, 
        dob_daysUntilBirthday int, 
        registered_date str, 
        registered_age int, 
        phone str, 
        cell str, 
        id_name str, 
        id_value str, 
        nat str
    );
    """)

    dbConnection.commit()
    dbConnection.close()

def upload_data_to_base(data):
    for people in data['results']:
        values = []
        for firstLayer in people:
            if(type(people[firstLayer]) == dict):
                for secondLayer in people[firstLayer]:
                    if(type(people[firstLayer][secondLayer]) == dict):
                        for thirdLayer in people[firstLayer][secondLayer]:
                            values.append(people[firstLayer][secondLayer][thirdLayer])
                    else:
                        values.append(people[firstLayer][secondLayer])
            else:
                values.append(people[firstLayer])
        try:
            dbConnection = sqlite3.connect('people.db')
            cursor = dbConnection.cursor()
            cursor.execute("""INSERT INTO user(gender, 
            name_title, 
            name_first, 
            name_last, 
            location_street_number, 
            location_street_name, 
            location_city, 
            location_state, 
            location_country, 
            location_postcode, 
            location_coordinates_latitude, 
            location_coordinates_longitude, 
            location_timezone_offset, 
            location_timezone_description, 
            email, 
            login_uuid, 
            login_username, 
            login_password, 
            login_salt, 
            login_md5, 
            login_sha1, 
            login_sha256, 
            dob_date, 
            dob_age, 
            dob_daysUntilBirthday, 
            registered_date, 
            registered_age, 
            phone, 
            cell, 
            id_name, 
            id_value, 
            nat) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", values)
            dbConnection.commit()
            dbConnection.close()
        except sqlite3.OperationalError:
            create_database()
            dbConnection = sqlite3.connect('people.db')
            cursor = dbConnection.cursor()
            cursor.execute("""INSERT INTO user(gender, 
            name_title, 
            name_first, 
            name_last, 
            location_street_number, 
            location_street_name, 
            location_city, 
            location_state, 
            location_country, 
            location_postcode, 
            location_coordinates_latitude, 
            location_coordinates_longitude, 
            location_timezone_offset, 
            location_timezone_description, 
            email, 
            login_uuid, 
            login_username, 
            login_password, 
            login_salt, 
            login_md5, 
            login_sha1, 
            login_sha256, 
            dob_date, 
            dob_age, 
            dob_daysUntilBirthday, 
            registered_date, 
            registered_age, 
            phone, 
            cell, 
            id_name, 
            id_value, 
            nat) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", values)
            dbConnection.commit()
            dbConnection.close()

def male_to_female_percentage():
    dbConnection = sqlite3.connect('people.db')
    cursor = dbConnection.cursor()
    cursor.execute("SELECT COUNT (gender) FROM user WHERE gender='male'")
    maleAmount = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT (gender) FROM user WHERE gender='female'")
    femaleAmount = cursor.fetchone()[0]
    totalAmount = maleAmount + femaleAmount
    print('Percentage of males:', maleAmount/totalAmount*100, '% \nPercentage of females:', femaleAmount/totalAmount*100, '%')

def average_age(who):
    dbConnection = sqlite3.connect('people.db')
    cursor = dbConnection.cursor()
    if (who == 'm'):
        cursor.execute("SELECT AVG(dob_age) FROM user WHERE gender='male'")
        print('Average age of males:', int(cursor.fetchone()[0]))
    if (who == 'f'):
        cursor.execute("SELECT AVG(dob_age) FROM user WHERE gender='female'")
        print('Average age of females:', int(cursor.fetchone()[0]))
    if (who == 'a'):
        cursor.execute("SELECT AVG(dob_age) FROM user")
        print('Average age:', int(cursor.fetchone()[0]))

def most_popular_cities(howMany):
    dbConnection = sqlite3.connect('people.db')
    cursor = dbConnection.cursor()
    cursor.execute("SELECT location_city FROM user GROUP BY location_city ORDER BY COUNT(*) DESC")
    listOfCities = cursor.fetchmany(howMany)
    for city in listOfCities:
        print(city[0])

def most_popular_passwords(howMany = 5):
    dbConnection = sqlite3.connect('people.db')
    cursor = dbConnection.cursor()
    cursor.execute("SELECT login_password, COUNT(*) FROM user GROUP BY location_city ORDER BY COUNT(*) DESC")
    listOfPasswords = cursor.fetchmany(howMany)
    for password in listOfPasswords:
        print('Password:', password[0], '| Amount used:', password[1])

def password_security_rating(password):
    score = 0
    password = str(password)
    for letter in password:
        if(letter.isnumeric()):
            score += 1
            break
    for letter in password:
        if(letter.isupper()):
            score += 2
            break
    for letter in password:
        if(letter.islower()):
            score += 1
            break
    for letter in password:
        if(not(letter.isalnum())):
            score += 3
            break
    if(len(password) >= 8):
        score += 5
    return score

def most_secure_password():
    dbConnection = sqlite3.connect('people.db')
    cursor = dbConnection.cursor()
    cursor.execute("SELECT login_password FROM user")
    listOfPasswords = cursor.fetchall()
    topPasswordScore = 0
    for password in listOfPasswords:
        checkPasswordScore = password_security_rating(password[0])
        if(topPasswordScore < checkPasswordScore):
            topPassword = password[0]
            topPasswordScore = checkPasswordScore
    print('Password:', topPassword, '| Score:', topPasswordScore)

def born_between(startDate, endDate):
    dbConnection = sqlite3.connect('people.db')
    cursor = dbConnection.cursor()
    dateSelectionQuery = "SELECT * FROM user WHERE dob_date BETWEEN '"+startDate+"T00:00:00.000Z' AND '"+endDate+"T23:59:59.999Z'"
    cursor.execute(dateSelectionQuery)
    print(cursor.fetchall())

parser = argparse.ArgumentParser()
parser.add_argument('-create', '--boot-up',nargs='?', const='1000', help='create database from file or upload new data to database if it already exists. DEFAULT = 1000 entries')
parser.add_argument('-password-list', '--list-of-most-popular-passwords',nargs='?', const=5, help='display most common passwords in database. DEFAULT = 5', type=int)
parser.add_argument('-mtfp', '--male-to-female-percentage', nargs='?', const=1, help='display male-to-female ratio')
parser.add_argument('-avg-age', '--average-age', nargs='?', const='a', help='display average age of people in database (a - all (DEFAULT) | m - male | f - female')
parser.add_argument('-pop-cities','--most-popular-cities', nargs='?', const=5, help='display most popular cities in database. DEFAULT = 5', type=int)
parser.add_argument('-max-sec-passwd','--most-secure-password', nargs='?', const=1, help='display most secure password in database.', type=int)
parser.add_argument('-born', '--born-between', nargs='*', help='display all people born between two dates [YYYY-MM-DD]')
args = parser.parse_args()
if args.boot_up:
    upload_data_to_base(transform_data(args.boot_up))
if args.list_of_most_popular_passwords:
    most_popular_passwords(args.list_of_most_popular_passwords)
if args.male_to_female_percentage:
    male_to_female_percentage()
if args.average_age:
    average_age(args.average_age)
if args.most_popular_cities:
    most_popular_cities(args.most_popular_cities)
if args.born_between:
    born_between(args.born_between[0], args.born_between[1])
if args.most_secure_password:
    most_secure_password()
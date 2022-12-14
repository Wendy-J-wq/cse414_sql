from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime
from random import randint


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    """
    TODO: Part 1
    """
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    # strong password
    upper = False
    lower = False
    numbers = False
    special = False
    letter = False
    for a in password:
        if a.isalpha():
            letter = True
        if a.isupper():
            upper = True
        if a.islower():
            lower = True
        if a.isnumeric():
            numbers = True
        if a == "!" or a == "@" or a == "#" or a == "?":
            special = True
    # print error message
    if len(password) < 8:
        print("Use at least 8 characters in password.")
    if not (upper and lower):
        print("The strong password needs to contain mixture of both uppercase and lowercase letters.")
    if not numbers or not letter:
        print("The strong password needs a mixture of letters and numbers.")
    if not special:
        print("The strong password should include sepcial characters.")
    if len(password) >= 8 and upper and lower and letter and special and numbers:
        pass
    else:
        print("Please reset password!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the patient
    patient = Patient(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    # print if create parient successful
    print("Created user {}".format(username))


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    # strong password
    upper = False
    lower = False
    numbers = False
    special = False
    letter = False

    for a in password:
        if a.isalpha():
            letter = True
        if a.isupper():
            upper = True
        if a.islower():
            lower = True
        if a.isnumeric():
            numbers = True
        if a == "!" or a == "@" or a == "#" or a == "?":
            special = True
    # print error message
    if len(password) < 8:
        print("Use at least 8 characters in password.")
    if not upper or not lower:
        print("The strong password needs to contain mixture of both uppercase and lowercase letters.")
    if not numbers or not letter:
        print("The strong password needs a mixture of letters and numbers.")
    if not special:
        print("The strong password should include sepcial characters.")
    if len(password) >= 8 and upper and lower and letter and special and numbers:
        pass
    else:
        print("Please reset password!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    """
    TODO: Part 1
    """
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_patient = patient



def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    """
    TODO: Part 2
    """
    # check number of input
    if len(tokens) != 2:
        print("Please try again!")
        return

    # check login
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first!")
        return

    date = tokens[1]

    # connect to server
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    # select information from tables
    vacc = "SELECT Username, Name, Doses FROM Availabilities, Vaccines WHERE Time = %s ORDER BY Username"
    try:
        cursor.execute(vacc, date)

        # print available appointments
        for row in cursor:
            caregiver_name = row['Username']
            vname = row['Name']
            vnum = row['Doses']
            avail_caregiveers = "caregiver_name:" + caregiver_name
            available_vac = "vaccine_name:" + vname + " " + "Num of Vacine:" + str(vnum)
            print(avail_caregiveers)
            print(available_vac)
        print("Successfully Searched!")
    # error message
    except pymssql.Error:
        print("Please try again!")
        print("Error occurred.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Please try again!")
        print("Error occurred.")
        print("Error:", e)
    finally:
        cm.close_connection()

def reserve(tokens):
    """
    TODO: Part 2
    """
    # reserve <date> <vaccine>
    # check length of tokens
    if len(tokens) != 3:
        print("Please try again!")
        return

    # check login
    global current_caregiver
    global current_patient
    if current_caregiver is not None:
        print("Please login as a patient!")
    elif current_patient is None:
        print("Please login first!")
        return

    date = tokens[1]
    vaccine = tokens[2]
    # check valid vaccine name
    if vaccine is None:
        print("Vaccine name not specified.")
        print("Please try again!")

    # connect to the server
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    # select information from tables
    selecttime = "SELECT Username, Name, Doses FROM Availabilities, Vaccines WHERE Time = %s ORDER BY Username"
    selectvac = "SELECT * FROM Vaccines WHERE Name = %s"
    reserve_ID = "SELECT ID FROM Appointments WHERE ID = %d"
    notavailable = "DELETE FROM Availabilities WHERE Time = %s AND Username = %s"
    vupdate = "UPDATE Vaccines SET Doses = %s WHERE Name = %s"

    # set random id number
    id = randint(10000,99999)

    try:
        cursor = conn.cursor(as_dict=True)
        # check id number uniqueness
        while cursor.execute(reserve_ID, id):
            id = random.randint(10000,99999)
        conn.commit()
        # execute selection
        cursor.execute(selecttime, date)
        caregivers = cursor.fetchall()
        if len(caregivers) == 0:
            print("No Caregiver is available!")
            return

        add_reservation = "INSERT INTO Appointments VALUES (%s,%d,%s,%s,%s)"
        selectcaregiver = caregivers[0]['Username']

        cursor = conn.cursor(as_dict=True)
        cursor.execute(selectvac, vaccine)
        for row in cursor:
            doses_update = row['Doses']
            if doses_update <= 0:
                print("Not enough available doses!")
                print("Please check other doses.")
                return
            doses_update = doses_update - 1

        cursor = conn.cursor(as_dict=True)
        cursor.execute(add_reservation,
                        (date, id, vaccine, selectcaregiver, current_patient.username))
        conn.commit()

        cursor = conn.cursor(as_dict=True)
        cursor.execute(vupdate, (doses_update, vaccine))
        conn.commit()

        cursor = conn.cursor(as_dict=True)
        cursor.execute(notavailable, (date, selectcaregiver))
        conn.commit()
        # print results of Reservation
        print("Appointment ID: " + str(id) +", Caregiver username:"+ selectcaregiver)

    except pymssql.Error as e:
            print("Please try again!")
            print("Db-Error:", e)
            quit()
    except Exception as e:
            print("Please try again!")
            print("Error:", e)
            return

def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    """
    TODO: Extra Credit
    """
    pass


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    '''
    TODO: Part 2
    '''

    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login as a caregiver first!")
        return

    if len(tokens) != 1:
        print("Please try again!")
        return

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    if current_caregiver != None:
        try:
            username = current_caregiver.get_username()
            print("Current longin user:" + username)
            statement = "SELECT * FROM Appointments WHERE cname = %s ORDER BY ID"
            cursor.execute(statement, username)
            #conn.commit()
            # check whether have the apppointment already
            if statement is None:
                print("You do not have appointment yet.")
            for row in cursor:
                id = row['ID']
                vname = row['vname']
                date = row['Time']
                pname = row['pname']
                print("Appointment ID:" + str(id) + " vaccine name:" + vname + " date:" + str(date) + " patient name: " + pname)
        except pymssql.Error as e:
            print("Please try again!")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
            return

    if current_patient != None:
        try:
            username = current_patient.get_username()
            print("Current longin user:" + username)
            statement = "SELECT * FROM Appointments WHERE pname = %s ORDER BY ID"
            cursor.execute(statement, username)
            #conn.commit()
            # check whether have the apppointment already
            if statement is None:
                print("You do not have appointment yet.")
            for row in cursor:
                id = row['ID']
                vname = row['vname']
                date = row['Time']
                cname = row['cname']
                print("Appointment ID:" + str(id) + " vaccine name:" + vname + " date:" + str(date) + " caregiver name: " + cname)
        except pymssql.Error as e:
            print("Please try again!")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Please try again!")
            print("Error:", e)
            return



def logout(tokens):
    """
    TODO: Part 2
    """
    global current_caregiver
    global current_patient
    if len(tokens) != 1:
        print("Please try again!")
        return
    if current_caregiver is None and current_patient is None:
        print("Please login first!")
    else:
        current_patient = None
        current_caregiver = None
        print("Successfully logged out!")
        return

def start():
    stop = False
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> Quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        tokens = response.split(" ")
        fname = tokens[0].lower()
        if fname != "create_patient" and fname != "create_patient" and fname != "login_patient" and fname != "login_caregiver":
            tokens = response.lower().split()
        else:
            tokens[0] = fname

        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == cancel:
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()

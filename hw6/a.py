from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''

current_patient = None

current_caregiver = None


def create_patient(tokens):
    """
    TODO: Part 1 (Extra credit not yet completed)
    """
    # check 1: the length for tokens need to be exactly 3 to include all
    # information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user. Try again.")
        return

    username = tokens[1]
    password = tokens[2]

    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # check 3: check if the passcode is safe
    # This part is for extra credit, will be edited in the future when
    # turning in part2

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
    # print this statement if patient created successful
    print("Created user: ", username)


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include
    # all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user. Try again.")
        return 

    username = tokens[1]
    password = tokens[2]

    # check 2: check if the username has been taken already, ask users to 
    # try again if the username is taken
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # Extra credit for checking safe passcode(not yet completed)

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
    print("Created user: ", username)


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "select * from Caregivers where Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username) 
        # returns false if the cursor is not before the first record or
        # if there are no rows in the ResultSet.
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

def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "select * fromm Patients where Username = %s"
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
    TODO: Part 1 (Forgot to paste this part from Python envrionment)
    """
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.") 
        return

    # check 2: the length for tokens need to be exactly 3
    # to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed. Try again!")
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
    # search for the schedule of the current caregiver
    if current_patient == current_caregiver:
        print("Please log in first.")
        return
    if len(tokens) != 2:
        print("Please enter the right information.")
        return

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    try:
        # First, parse the date, retrieve availability information, and then get all vaccines and their num of doses
        date_whole = tokens[1].split("-")
        month = int(date_whole[0])
        day = int(date_whole[1])
        year = int(date_whole[2])
        d = datetime.datetime(year, month, day)

        get_available_dates = "SELECT Time, Username FROM Availabilities WHERE Time = %s ORDER BY Username"
        get_vaccines = "SELECT Name, Doses FROM Vaccines"

        # Query all the rows of both availabilities and vaccines
        cursor.execute(get_available_dates, d)
        schedule_rows = cursor.fetchall()
        cursor.execute(get_vaccines)
        vaccine_rows = cursor.fetchall()

        if len(schedule_rows) == 0:  # No appointments avaiable this day
            print("There are no appointments available on", tokens[1])
            return

    except pymssql.Error:
        print("Retrieving dates failed; try again")
        return
    except ValueError:
        print("Please enter a valid date")
        return
    except Exception:
        print("Error occurred when checking availability; try again")
        return
    finally:
        cm.close_connection()


def reserve(tokens):
    """
    TODO: Part 2
    """
    # check 1: check valid arguments / login requirements
    if current_patient == current_caregiver:
        print("Please login first before reserving an appointment")
    if current_patient is None:
        print("Please login as a patient to reserve an appointment")
    if len(tokens) != 3:
        print("Failed to reserve appointment; wrong arguments")

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)
    try:
        # check 2: Parse the date and attempt to retrieve date, caregiver, and vaccine name from the database
        date_whole = tokens[1].split("-")
        month = int(date_whole[0])
        day = int(date_whole[1])
        year = int(date_whole[2])
        d = datetime.datetime(year, month, day)
        find_available_dates = "SELECT TOP 1 Time, Username FROM Availabilities WHERE Time = %s ORDER BY Username"
        cursor.execute(find_available_dates, d)
        dates = cursor.fetchall()
        if len(dates) == 0:
            print("There are no caregivers available for this date")
            return
        assigned_caregiver = dates[0]["Username"]
        assigned_date = dates[0]["Time"]
        vaccine_name = tokens[2]
        vaccine = Vaccine(vaccine_name, available_doses=None).get()

        # Check3: see if vaccine is valid and if it is remove 1 from the supply
        if vaccine is None:
            print("Our caregivers do not have this vaccine. Try again inputting a valid vaccine from this list:")
            cursor.execute("SELECT Name FROM Vaccines")
            for row in cursor:
                print(row["Name"])
            return
        if vaccine.available_doses == 0:
            print("There are not enough doses left. Try another vaccine brand.")
            return
        vaccine.decrease_available_doses(1)

        # Check 4: Add appointment to appointment database. ID is just 1 + the highest id number
        add_appointment = "INSERT INTO Appointments VALUES (%d, %s, %s, %s, %s)"
        temp_cursor = conn.cursor()
        temp_cursor.execute("SELECT MAX(a_id) FROM Appointments")
        highest_row = temp_cursor.fetchone()[0]
        if highest_row is None:
            cursor.execute(add_appointment, (1
                                             , assigned_date, current_patient.username, assigned_caregiver,
                                             vaccine_name))
        else:
            cursor.execute(add_appointment, (highest_row + 1
                                             , assigned_date, current_patient.username, assigned_caregiver,
                                             vaccine_name))

        # Check 5: Drop that caregiver's availability from the availability database
        drop_availability = "DELETE FROM Availabilities WHERE Time = %s AND Username = %s"
        cursor.execute(drop_availability, (d, assigned_caregiver))

        conn.commit()

        # Check 6: Output information about the appointment if successfully added
        print("Success! Below is information on your appointment:")
        print("-----------------------")
        get_appointment = "SELECT a_id, date, c_username, vaccine_name FROM appointments WHERE p_username = %s AND c_username = %s AND date = %s"
        cursor.execute(get_appointment, (current_patient.username, assigned_caregiver, assigned_date))
        print("{: >10}\t{: >10}\t{: >10}\t{: >10}".format("Appointment ID", "Date", "Caregiver", "Vaccine"))
        for row in cursor:
            print("{: >10}\t{: >10}\t{: >10}\t{: >10}".format(row["a_id"], str(row["date"]), row["c_username"],
                                                              row["vaccine_name"]))

    except pymssql.Error as e:
        print("Error trying to create appointment; try again")
        print("DBError:", e)
        return
    except ValueError as e:
        print("Invalid date format; try again")
        print("Error:", e)
        return
    except Exception as e:
        print("Error occurred when creating an appointment; try again")
        print("Error:", e)
        return
    finally:
        cm.close_connection()


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
    if current_patient == current_caregiver:
        print("Please login first!")
        return
    if len(tokens) != 2:
        print("Failed to cancel appointment; wrong arguments given")
        return
    try:
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor(as_dict=True)
        cancel_id = tokens[1]

        # Check 1: check that the user's desired appointment id is actually in their own appointments
        get_appointment = "SELECT a_id, date, p_username, c_username, vaccine_name FROM Appointments WHERE a_id = %d"
        cursor.execute(get_appointment, cancel_id)
        appointment = cursor.fetchone()
        valid_appointment = False
        if current_patient is not None:
            if appointment['p_username'] == current_patient.username:
                valid_appointment = True
            else:
                print("Could not find appointment with id:", cancel_id)
        elif current_caregiver is not None:
            if appointment['c_username'] == current_caregiver.username:
                valid_appointment = True
            else:
                print("Could not find appointment with id:", cancel_id)

        # If valid appointment id, then delete that appointment while replenishing the respective vaccine supply (+1)
        if valid_appointment:
            delete_appointment = "DELETE FROM Appointments WHERE a_id = %d"
            vaccine = Vaccine(appointment["vaccine_name"], None).get()
            vaccine.increase_available_doses(1)  # Need this to replenish 1 more vaccine if cancel is successful
            cursor.execute(delete_appointment, cancel_id)
            conn.commit()
            print("Appointment successfully cancelled.")
            if current_patient is not None:  # If a patient canceled that appointment, add the availability back to caregiver
                appointment_date = appointment['date']
                caregiver = appointment['c_username']
                cursor.execute("INSERT INTO Availabilities VALUES (%d, %d)", (appointment_date, caregiver))
                conn.commit()
        else:
            print("Could not find appointment with id:", cancel_id)
    except pymssql.Error as e:
        print("Failed to retrieve appointment information")
        print("DBError:", e)
    except Exception as e:
        print("Could not find appointment with id:", cancel_id)
    finally:
        cm.close_connection()


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
    if current_patient == current_caregiver:
        print("Please log in.")
        return

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    if current_caregiver is not None:
        try:
            # Try to access the appointmenets for the patient and print it
            sql_query = "select * from Appointments where Caregiver_name = %s
                                  order by ID"
	  username = current_caregiver.get_username()
            print("Current longin user:" + username)
            cursor.execute(sql_query, username)
            # check whether have the apppointment already
            if len(sql_query) == 0:
                print("You do not have appointments scheduled.")
            for row in cursor:
                id = row['ID']
                vname = row['vname']
                date = row['Time']
                pname = row['pname']
                print("Appointment ID:" + str(id) + " vaccine name:" + \
	          vname + " date:" + str(date) + " patient name: " + pname)


def logout(tokens):
    """
    TODO: Part 2
    """
    global current_patient
    global current_caregiver
    try:
        # All this checks is that either a patient or a caregiver is logged in to logout
        if current_patient != current_caregiver:
            current_patient = None
            current_caregiver = None
            print("Successfully logged out!")
            base_menu()
        else:
            print("Please login first!")
    except Exception as e:
        print("Failed to logout!")
        print("Error:", e)
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

        response = response.lower()
        tokens = response.split(" ")
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

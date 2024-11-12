# Open Source MySQL Shell
# https://gist.github.com/longhirar/44e805c203f74fd5b6b2364a10daccd0

import getpass
import mysql.connector

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

db = mysql.connector.connect(
    host = input("Host: "),
    port = input("Port: "),
    user = input("User: "),
    password = getpass.getpass("Password: "),
    database = input("Database: ")
)

shouldExit = False

while not shouldExit:
    print(bcolors.OKCYAN, end="")
    raw_command = input("$ ")
    print(bcolors.ENDC, end="")

    if (raw_command == ""):
        continue
    if (raw_command[0] == "/"):
        command = raw_command.split(' ')
        if (command[0] == "/exit" or command[0] == "/bye"):
            shouldExit = True
            continue
        elif (command[0] == "/help" or command[0] == "/?"):
            print(bcolors.OKGREEN, end="")
            print("Longhi Simple MySQL Shell")
            print("Help")
            print("")
            print(" /exit or /bye    - closes session")
            print(" /help or /?      - shows this menu")
            print(" /file <filename> - runs all commands inside file")
            print("")
            print("Type out SQL commands to run. All result will show below.")
            print(bcolors.ENDC, end="")
            continue
        elif (command[0] == "/file"):
            try:
                with open(command[1], 'r') as sqlfile:
                    sql_code = sqlfile.read()
            except Exception as err:
                print(bcolors.FAIL, end="")
                print(f"Failed to send file: {err}")
                print(bcolors.ENDC, end="")
                continue
        else:
            print(bcolors.OKGREEN, end="")
            print("Unknown command. See help with /help")
            print(bcolors.ENDC, end="")
            continue
    else:
        sql_code = raw_command

    cursor = db.cursor()
    try:
        cursor.execute(sql_code, multi=True)
        for value in cursor:
            print(value)
    except Exception as err:
        print(bcolors.FAIL, end="")
        print(f"Error: {err}")
        print(bcolors.ENDC, end="")
    finally:
        cursor.close()
        db.commit()


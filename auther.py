# Imports
import os
import time
import json
import hashlib
import keyboard
import threading
from pysqlcipher3 import dbapi2 as sqlite
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pathlib import Path
from pwinput import pwinput

# Text
choices = '''[1] Add New Key
[2] View Auth Key(s)
[3] Remove Existing Key
[4] Exit
'''
welcome = '''Welcome To Auth v2! A New Generation Of Two Factor Authentication!
To Get Started, Get A Public Key And A Private Key And Import Them!

'''

# Functions

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def checkKeyboard():
    global inViewKeys
    while inViewKeys:
        if keyboard.is_pressed('enter'):
            global exitchoice
            exitchoice = True
            inViewKeys = False
            input('')

def process_row(rows):
    clear_console()
    for row in rows:
        pubkey = row[2]
        privkey = row[1]
        f = Fernet(privkey)
        tokenstr = json.loads(split_string(f.decrypt(pubkey)))
        tkey = f.decrypt(pubkey).decode('utf-8') + '|' + str(round(time.time() / 10) * 10)
        hashed_key = hashlib.sha256(tkey.encode('utf-8')).hexdigest()
        print(f'\n ID: {row[0]} \n Public Key: {row[2]} \n Auth Key: {hashed_key}\n')
    print('Press Enter To Return To Main Menu...')

def is_password_correct(db_path, password):
    try:
        con = sqlite.connect(db_path)
        con.execute("PRAGMA key = '%s'" % password)
        con.execute("SELECT count(*) FROM sqlite_master")  # Attempt a simple query
        return True
    except sqlite.DatabaseError:
        return False

def write_data(conn, private, public):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Vault (private, public) VALUES (?, ?)", (private, public))
    conn.commit()

def read_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Vault")
    rows = cursor.fetchall()
    return rows

def split_string(input_string):
    # Split the input string using the '.' separator
    split_list = input_string.split(b'|')

    # Extract the individual elements from the split list
    username = split_list[0].decode('utf-8')
    email = split_list[1].decode('utf-8')
    password = split_list[2].decode('utf-8')
    time = float(split_list[3].decode('utf-8'))

    # Create a dictionary with the individual elements
    data_dict = {
        "username": username,
        "email": email,
        "password": password,
        "time": time
    }

    # Convert the dictionary to a JSON object and return it
    return json.dumps(data_dict)

# Main
def main(firsttime):
    clear_console()
    choice = ''
    global exitchoice
    exitchoice = False
    if firsttime:
        print(welcome)
        main(False)
    else:
        choice = input(choices)
        if choice == '1':
            pubkey = bytes(input('Enter Public Key: '), 'utf-8')
            privkey = bytes(pwinput('Enter Private Key: '), 'utf-8')
            if not pubkey or privkey:
                print('Exit Setup.')
                time.sleep(1)
                main(False)
            f = Fernet(privkey)
            tokenstr = json.loads(split_string(f.decrypt(pubkey)))
            if (time.time() - tokenstr['time'] < 60):
                tkey = f.decrypt(pubkey).decode('utf-8') + '|' + str(round(time.time() / 10) * 10)
                hashed_key = hashlib.sha256(tkey.encode('utf-8')).hexdigest()
                write_data(conn, privkey, pubkey)
                clear_console()
                print('Key: ' + hashed_key)
            else:
                print('Token Expired! Generate A New One!')
            main(False)
        elif choice == '2':
            global inViewKeys
            inViewKeys = True
            rows = read_data(conn)
            if not rows:
                print('No Keys To Display, Going Back!')
                time.sleep(1)
                main(False)
                return
            keyboardListen = threading.Thread(target=checkKeyboard)
            keyboardListen.start()
            thread = threading.Thread(target=process_row, args=(rows,))
            thread.start()
            while True:
                thread = threading.Thread(target=process_row, args=(rows,))
                thread.start()
                time.sleep(1)
                if exitchoice:
                    break
            main(False)
        elif choice == '3':
            clear_console()
            cur = conn.cursor()
            cur.execute("SELECT id, public FROM Vault")
            rows = cur.fetchall()
            if not rows:
                print('Nothing to delete, Going Back!')
                time.sleep(1)
                main(False)
                return
            print('ID, Public Key')
            for row in rows:
                print(row)
            delchoice = input('Enter Key ID To Remove (0 to cancel): ')
            cur.execute(f'DELETE FROM Vault WHERE ID = {delchoice}')
            if cur.rowcount == 0:
                print("No Keys deleted")
            else:
                print(f"{cur.rowcount} Key deleted")
                conn.commit()
            time.sleep(1)
            main(False)
        elif choice == '4':
            print('Exiting... Bye!')
            conn.close()
        else:
            print('Invalid Choice.')
            time.sleep(0.5)
            main(False)

            
            
# Init
def entry():
    global path 
    global password
    global conn
    path = Path('./vault/')
    if not path.exists():
        os.makedirs(path)
        password = pwinput('Create A New Password: ')
        conn = sqlite.connect(str(path / 'vault.sqlite'))
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA key='{password}'")
        cursor.execute('''
            CREATE TABLE Vault(
                id INTEGER PRIMARY KEY,
                private TEXT,
                public TEXT)
        ''')
        conn.commit()
        main(True)
    else:
        password = pwinput('Enter Password: ')
        if is_password_correct(str(path / 'vault.sqlite'), password):
            conn = sqlite.connect(str(path / 'vault.sqlite'))
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA key='{password}'")
            main(False)
        else:
            print('Incorrect Password!')
            entry()

    


# End 
if __name__ == "__main__":
    entry()

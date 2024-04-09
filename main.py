# Julefrokost tilmeldnings hjemmeside/app
# KEA Programmering Eksamens projekt
# Tjek for modules: flask, sqlite3, requests, zipfile, io, shutil
# For at køre programmet, skal du installere de nødvendige modules ovenfor
from flask import Flask, render_template, request, redirect, session
import sqlite3

# Flask app
# __name__ er navnet på modulet
# Flask er en klasse
# app er en instans af klassen Flask
app = Flask(__name__)
app.secret_key = 'dit_hemmelige_nøgle'

# Middleware til autentificering
@app.before_request
def authenticate():
    # Brug brugernavn og password til at autentificere
    brugernavn = "sekretær"
    password = "kea2024"

    # Hvis brugeren ikke er logget ind, bliver de sendt til login siden
    if request.endpoint != 'login' and not session.get('brugernavn') == brugernavn and not session.get('password') == password:
        return redirect('/login')

# Database connection
# Jeg har valgt at bruge en in-memory database, da det er nemmere at teste og debugge
# check_same_thread=False er nødvendig, da SQLite ikke er thread-safe
# thread-safe betyder at flere tråde kan tilgå databasen samtidig, hvilket SQLite ikke kan
# conn = sqlite3.connect(':memory:', check_same_thread=False)

# Hvis du vil gemme data i en fil, kan du bruge følgende linje i stedet for linje 16
# Dette opretter en fil kaldet julefrokost.db i samme mappe som main.py
conn = sqlite3.connect('julefrokost.db', check_same_thread=False)

# Cursor objekt bruges til at udføre SQL kommandoer
c = conn.cursor()

# Create table if not exists betyder at tabellen kun oprettes, hvis den ikke allerede eksisterer
# Data som skal gemmes: navn, email, telefon, betalingsmetode, betalingsstatus = boolean
c.execute('''CREATE TABLE IF NOT EXISTS participants
                (name text, email text, phone text, payment_method text, payment_status boolean)''')

# Show_participants function
# Henter alle deltagere fra databasen
def show_participants():
    c.execute("SELECT * FROM participants")
    return c.fetchall()

# Indsætter deltagere i databasen
# Tjekker om email og telefon nummer allerede eksisterer i databasen
# Hvis email eller telefon nummer allerede eksisterer i databasen, returneres en besked
# Dette kunne laves smartere ved at håndtere det i sql med constraints men det er uden for scope af dette projekt
def insert_into_db(name, email, phone, payment_method, payment_status):
    # Tjekker om email og telefon nummer allerede eksisterer i databasen
    check_email = c.execute("SELECT email FROM participants WHERE email = ?", (email,))
    # fetchone() henter en række fra databasen og returnerer den som en tuple, hvis der ikke er nogen rækker, returneres None
    # Hvis email allerede eksisterer i databasen, returneres en besked
    if check_email.fetchone() is not None:
        print("Email already exists in the database")
        return ""
    
    # Tjekker om telefon nummer allerede eksisterer i databasen
    check_phone = c.execute("SELECT phone FROM participants WHERE phone = ?", (phone,))
    # Hvis telefon nummer allerede eksisterer i databasen, returneres en besked
    if check_phone.fetchone() is not None:
        print("Phone number already exists in the database")
        return ""
    
    # Indsætter deltagere i databasen
    # For at vi ikke har sql injection, bruger vi ? i stedet for at sætte variabler direkte ind i sql kommandoen
    # Dette anvender tuple unpacking, hvor variablerne bliver sat ind i sql kommandoen i den rækkefølge de er i tuplen
    # Det er også muligt at bruge dictionary unpack, her er et eksemple: 
    # c.execute("INSERT INTO participants VALUES (:name, :email........)", {'name': name, 'email': email........})
    c.execute("INSERT INTO participants VALUES (?, ?, ?, ?, ?)", (name, email, phone, payment_method, payment_status))
    conn.commit()

# Sorter deltager listen efter navn
# key=lambda x: x[0] = sortere efter første element i listen
def sort_list_participants(participants, sort = ""):
    if sort == 'not_paid':
        participants_t = c.execute("SELECT * FROM participants WHERE payment_status = 0")
    elif sort == 'paid':
        participants_t = c.execute("SELECT * FROM participants WHERE payment_status = 1")
    else:
        participants_t = c.execute("SELECT * FROM participants")

    return sorted(participants_t, key=lambda x: x[0])

# Test data for at fylde databasen
def import_test_users():
    # Test data for at fylde databasen pakket ind i en liste, hvor hvert element er en tuple
    test_users = [
        ("John Doe", "john@example.com", "12345678", "MobilePay", 1),
        ("Jane Smith", "jane@example.com", "87654321", "Bank transfer", 0),
        ("Alice Johnson", "alice@example.com", "98765432", "Credit card", 1),
        ("Bob Anderson", "bob@example.com", "54321678", "PayPal", 0),
        ("Eve Wilson", "eve@example.com", "23456789", "Venmo", 1),
        ("Grace Lee", "grace@example.com", "34567890", "Cash", 0),
        ("Michael Brown", "michael@example.com", "98765432", "Bank transfer", 1),
        ("Sarah Johnson", "sarah@example.com", "45678901", "Credit card", 0),
        ("David Smith", "david@example.com", "10987654", "PayPal", 1),
        ("Olivia Wilson", "olivia@example.com", "56789012", "Venmo", 0),
        ("James Lee", "james@example.com", "21098765", "Cash", 1),
        ("Emma Brown", "emma@example.com", "65432109", "Bank transfer", 0),
        ("William Anderson", "william@example.com", "89012345", "MobilePay", 1),
        ("Sophia Doe", "sophia@example.com", "43210987", "Credit card", 0),
        ("Alexander Johnson", "alexander@example.com", "76543210", "PayPal", 1),
        ("Mia Smith", "mia@example.com", "90123456", "Venmo", 0),
        ("Benjamin Wilson", "benjamin@example.com", "32109876", "Cash", 1)
    ]

    # For hver bruger i test_users listen, indsættes brugeren i databasen
    for user in test_users:
        # * betyder at vi unpacker tuplen, så vi får hver værdi i tuplen som et argument
        insert_into_db(*user)

def all_stats():
    # Get all participants
    participants = show_participants()
    # Get total number of participants
    total_participants = len(participants)
    # Get total number of participants that have paid
    total_paid = len([participant for participant in participants if participant[4] == 1])
    # Get total number of participants that have not paid
    total_not_paid = len([participant for participant in participants if participant[4] == 0])

    return {
        "total_participants": total_participants,
        "total_paid": total_paid,
        "total_not_paid": total_not_paid,
    }

# __________Routing__________
# Login side til autentificering af sekretæren.
@app.route('/login', methods=['GET'])
def login():

    # Store brugernavn og password i session, så vi kan tjekke om brugeren er logget ind den får username og kode fra url via GET request
    # Dette kunne være lavet mere sikkert ved at bruge POST request og form data i stedet for GET request og url parametre
    session['brugernavn'] = request.args.get('username')
    session['password'] = request.args.get('password')

    # Hvis brugernavn og password er korrekt, bliver brugeren sendt til forsiden
    if session['brugernavn'] == "sekretær" and session['password'] == "kea2024":
        return redirect('/')

    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('brugernavn', None)
    session.pop('password', None)
    return redirect('/login')

# @app.route('/'), definerer en route til /, som er hjemmesiden
# def index(): returnerer index.html og bliver kørt når nogen går til hjemmesiden
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/tilmeld'), definerer en route via /tilmeld
# def tilmeld(): returnerer tilmeldings-formularen og bliver kørt når nogen går til /tilmeld
# Her kan folk skrive sig op til julefrokosten.
@app.route('/tilmeld')
def tilmeld():
    # Reroute til tilmeldings-formularen
    return render_template('tilmeldings-formular.html')

# POST request til /tilmeld, når brugeren har udfyldt tilmeldings-formularen og trykket på tilmeld knappen
# kaldes tilmeld_post() funktionen som håndterer POST requesten og tilføjer brugeren til databasen, hvis brugeren ikke allerede eksisterer.
@app.route('/tilmeld', methods=['POST'])
def tilmeld_post():
    # Henter data fra formularen
    name = request.form['navn']
    email = request.form['email']
    phone = request.form['telefon']
    payment_method = request.form['betalings-metode']
    payment_status = 0
    # Indsætter brugeren i databasen
    insert_into_db(name, email, phone, payment_method, payment_status)
    # Reroute tilbage til tilmeldings-formularen med en besked om at tilmeldingen er gennemført
    return render_template('tilmeldings-formular.html', message="Tak for din tilmelding")

# GET request til /deltagere, når brugeren går til /deltagere
# kaldes deltagere() funktionen som håndterer GET requesten og viser en liste over alle deltagere
@app.route('/deltagere', methods=['GET'])
def deltagere():
    stats = all_stats()
    args = request.args
    sort = args.get('sort', '')
    sort = sort.lower()
    if sort == 'not_paid':
        participants = sort_list_participants(show_participants(), sort)
    elif sort == 'paid':
        participants = sort_list_participants(show_participants(), sort)
    else:
        participants = sort_list_participants(show_participants())      

    return render_template('print.html', participants=participants, stats=stats)

@app.route('/betal/<email>', methods=['GET', 'POST'])
def betal(email):
    c.execute("SELECT payment_status FROM participants WHERE email = ?", (email,))
    payment_status = c.fetchone()[0]
    if payment_status == 1:
        c.execute("UPDATE participants SET payment_status = 0 WHERE email = ?", (email,))
        conn.commit()
    elif payment_status == 0:
        c.execute("UPDATE participants SET payment_status = 1 WHERE email = ?", (email,))
        conn.commit()

    return redirect("/deltagere", code=302)

@app.route('/slet/<email>', methods=['GET', 'POST'])
def slet(email):
    c.execute("SELECT payment_status FROM participants WHERE email = ?", (email,))
    payment_status = c.fetchone()[0]
    if payment_status == 1:
        c.execute("UPDATE participants SET payment_status = 0 WHERE email = ?", (email,))
        conn.commit()
    elif payment_status == 0:
        c.execute("DELETE FROM participants WHERE email = ?", (email,))
        conn.commit()

    return redirect("/deltagere", code=302)

def check_for_templates():
    # Tjek om templates mappen eksisterer
    # Hvis den ikke gør det skal vi oprette den, samt hente index.html/print.html/tilmeldings-formular.html
    # Fra github repository
    import os
    if not os.path.exists('templates'):
        os.makedirs('templates')
    else:
        print("Templates folder already exists")

    # Check om vi mangler en af de tre templates
    # Hvis vi mangler en af de tre templates, henter vi dem fra github repository
    if not os.path.exists('templates/index.html') or not os.path.exists('templates/print.html') or not os.path.exists('templates/tilmeldings-formular.html') or not os.path.exists('templates/login.html'):
        import requests
        import zipfile
        import io

        url = "https://github.com/SixtenDK/kea-julefrokost/archive/refs/heads/main.zip"
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
    
        import shutil
        shutil.move('kea-julefrokost-main/templates/index.html', './templates/')
        shutil.move('kea-julefrokost-main/templates/print.html', './templates/')
        shutil.move('kea-julefrokost-main/templates/tilmeldings-formular.html', './templates/')
        shutil.move('kea-julefrokost-main/templates/login.html', './templates/')
        # Fjern kea-julefrokost-main mappen
        shutil.rmtree('kea-julefrokost-main')


# Hvis main.py bliver kørt, vil __name__ være __main__ og koden vil blive kørt
# Hvis main.py bliver importeret i et andet script, vil __name__ være navnet på modulet og koden vil ikke blive kørt
if __name__ == '__main__':
    # First time run
    # Insert some data into the database
    if c.execute("SELECT * FROM participants").fetchone() is None:
        import_test_users()

    check_for_templates()

    # Kører appen på port 9080 og host
    app.run(debug=True,port=9080,host='0.0.0.0')
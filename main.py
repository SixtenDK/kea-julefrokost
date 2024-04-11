# Julefrokost tilmeldnings hjemmeside/app
# KEA Programmering Eksamens projekt
# Tjek for modules: flask, requests
# For at køre programmet, skal du installere de nødvendige modules ovenfor
from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt

# Baggrundsopgave (Hvis vi vil have en baggrundsopgave, der kører i baggrunden, mens vores app kører)
# from threading import Thread
# Opretter og starter en tråd, der kører baggrundsopgaven
# def baggrundsopgave():
#     while True:
#         print("Baggrundsopgave")
#         time.sleep(5)
#         # Her kan vi indsætte vores baggrundsopgave
#         # F.eks. tjekke om der er nogen der har betalt og sende en påmindelse
#         # Dette kunne også gøres med en cronjob eller en scheduler
# thread = Thread(target=baggrundsopgave)
# thread.start()

# Flask app
# __name__ er navnet på modulet
# Flask er en klasse
# app er en instans af klassen Flask
app = Flask(__name__)

# Denne secret key bruges til at signere session cookien, dette sikre i mod angreb som session fixation
# Dette er en meget simpel secret key, i produktion skal denne være meget længere og mere kompleks
app.secret_key = 'EnSuperHemmeligNøgle'

# Opret en hashet adgangskode for sekretæren
# Bemærk: Dette trin skal kun gøres én gang, og derefter skal du gemme den hashede adgangskode et sikkert sted
sekretaer_password = "kea2024".encode('utf-8')
# bcrypt er en krypterings algoritme, der bruges til at hashe adgangskoder
# gensalt() genererer et salt, som bruges til at gøre hashet mere sikker
# hashpw() hasher adgangskoden med saltet
hashed_password = bcrypt.hashpw(sekretaer_password, bcrypt.gensalt(12))

# Middleware til autentificering
# Før hver request, tjekker vi om brugeren er logget ind
# Hvis brugeren ikke er logget ind, bliver de sendt til login siden
@app.before_request
def authenticate():
    # Brugernavn og hashet password for sekretæren
    brugernavn = "sekretær"
    # Antag, at denne hashede adgangskode er gemt et sikkert sted, fx i en database eller en miljøvariabel
    stored_hashed_password = hashed_password

    # Hvis brugeren ikke er logget ind, bliver de sendt til login siden
    if request.endpoint != 'login':
        session_password = session.get('password', '').encode('utf-8')
        if not session.get('brugernavn') == brugernavn or not bcrypt.checkpw(session_password, stored_hashed_password):
            return redirect('/login')

# Database connection
# sqlite3 er en indbygget database i python
# connect() metoden opretter en forbindelse til en database
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
        ("Karl Jensen", "karl@example.com", "12523678", "mobilepay", 1),
        ("John Doe", "john@example.com", "12345678", "mobilepay", 1),
        ("Jane Smith", "jane@example.com", "87654321", "mobilepay", 0),
        ("Alice Johnson", "alice@example.com", "98765432", "kontant", 1),
        ("Bob Anderson", "bob@example.com", "54321678", "kontant", 0),
        ("Eve Wilson", "eve@example.com", "23456789", "kontant", 1),
        ("Grace Lee", "grace@example.com", "34567890", "mobilepay", 0),
        ("Michael Brown", "michael@example.com", "98765432", "mobilepay", 1),
        ("Sarah Johnson", "sarah@example.com", "45678901", "mobilepay", 0),
        ("David Smith", "david@example.com", "10987654", "kontant", 1),
        ("Olivia Wilson", "olivia@example.com", "56789012", "kontant", 0),
        ("James Lee", "james@example.com", "21098765", "kontant", 1),
        ("Emma Brown", "emma@example.com", "65432109", "mobilepay", 0),
        ("William Anderson", "william@example.com", "89012345", "MobilePay", 1),
        ("Sophia Doe", "sophia@example.com", "43210987", "mobilepay", 0),
        ("Alexander Johnson", "alexander@example.com", "76543210", "kontant", 1),
        ("Mia Smith", "mia@example.com", "90123456", "kontant", 0),
        ("Benjamin Wilson", "benjamin@example.com", "32109876", "kontant", 1)
    ]

    # For hver bruger i test_users listen, indsættes brugeren i databasen
    for user in test_users:
        # * betyder at vi unpacker tuplen, så vi får hver værdi i tuplen som et argument
        insert_into_db(*user) # Example på unpacking: insert_into_db("Karl Jensen", "........")......

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
    # Gem brugernavn og password i session, så vi kan tjekke om brugeren er logget ind den får username og kode fra url via GET request
    # Dette kunne være lavet mere sikkert ved at bruge POST request og form data i stedet for GET request og url parametre
    session['brugernavn'] = request.args.get('username')
    session['password'] = request.args.get('password')

    stored_hashed_password = hashed_password
    if session.get('password') is not None:
        session_password = session.get('password', '').encode('utf-8')

    # Hvis brugernavn og password er korrekt, bliver brugeren sendt til forsiden
    if session['brugernavn'] == "sekretær" and bcrypt.checkpw(session_password, stored_hashed_password):
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
    # Stats viser nogle ekstra informationer om deltagelse
    stats = all_stats()
    # Henter GET parametre
    args = request.args
    # Hvis der er en sort parameter, sorteres listen efter denne parameter
    sort = args.get('sort', '')
    sort = sort.lower()
    # Hvis sort parameteren er not_paid, sorteres listen efter deltagere der ikke har betalt
    if sort == 'not_paid':
        participants = sort_list_participants(show_participants(), sort)
    # Hvis sort parameteren er paid, sorteres listen efter deltagere der har betalt
    elif sort == 'paid':
        participants = sort_list_participants(show_participants(), sort)
    # Hvis sort parameteren er tom, vises alle deltagere
    else:
        participants = sort_list_participants(show_participants())      
    
    # Viser listen over deltagere
    return render_template('print.html', participants=participants, stats=stats)

# Betal deltager
@app.route('/betal/<email>', methods=['GET', 'POST'])
def betal(email):
    # Henter betalingsstatusen for brugeren
    c.execute("SELECT payment_status FROM participants WHERE email = ?", (email,))
    payment_status = c.fetchone()[0]
    # Hvis betalingsstatusen er 1, sættes den til 0
    if payment_status == 1:
        c.execute("UPDATE participants SET payment_status = 0 WHERE email = ?", (email,))
        conn.commit()
    # Hvis betalingsstatusen er 0, sættes den til 1
    elif payment_status == 0:
        c.execute("UPDATE participants SET payment_status = 1 WHERE email = ?", (email,))
        conn.commit()
    # Reroute tilbage til deltagere siden
    return redirect("/deltagere", code=302)

# Slet deltager
@app.route('/slet/<email>', methods=['GET', 'POST'])
def slet(email):
    # Henter betalingsstatusen for brugeren
    c.execute("SELECT payment_status FROM participants WHERE email = ?", (email,))
    payment_status = c.fetchone()[0]
    # Hvis betalingsstatusen er 1, sættes den til 0
    if payment_status == 1:
        c.execute("UPDATE participants SET payment_status = 0 WHERE email = ?", (email,))
        conn.commit()
    # Hvis betalingsstatusen er 0, slettes brugeren fra databasen
    elif payment_status == 0:
        c.execute("DELETE FROM participants WHERE email = ?", (email,))
        conn.commit()
    # Reroute tilbage til deltagere siden
    return redirect("/deltagere", code=302)

# Check for templates, hvis de ikke eksisterer, hentes de fra github repository
# Dette sørger for at scriptet her er det eneste der skal køres for at få appen til at køre
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

        # Hent github repository som zip fil
        url = "https://github.com/SixtenDK/kea-julefrokost/archive/refs/heads/main.zip"
        # Hent zip filen
        r = requests.get(url)
        # Åbn zip filen
        z = zipfile.ZipFile(io.BytesIO(r.content))
        # Extract zip filen
        z.extractall()

        # Shutil er et modul til at håndtere filer og mapper
        import shutil
        # Brug shutil til at flytte filerne fra kea-julefrokost-main mappen til templates mappen
        shutil.move('kea-julefrokost-main/templates/index.html', './templates/')
        shutil.move('kea-julefrokost-main/templates/print.html', './templates/')
        shutil.move('kea-julefrokost-main/templates/tilmeldings-formular.html', './templates/')
        shutil.move('kea-julefrokost-main/templates/login.html', './templates/')
        # Fjern kea-julefrokost-main mappen
        shutil.rmtree('kea-julefrokost-main')

# Betalingssystem
# @app.route('/mobilepay/<phone>', methods=['GET'])
# def mobilepay(phone):
#     return render_template('mobilepay.html', phone=phone)

# @app.route('/mobilepay/<phone>', methods=['POST'])
# def mobilepay_post(phone):
#     c.execute("UPDATE participants SET payment_status = 1 WHERE phone = ?", (phone,))
#     conn.commit()
#     return redirect('/deltagere')

# Hvis main.py bliver kørt, vil __name__ være __main__ og koden vil blive kørt
# Hvis main.py bliver importeret i et andet script, vil __name__ være navnet på modulet og koden vil ikke blive kørt
if __name__ == '__main__':
    # First time run
    # Insert some data into the database
    if c.execute("SELECT * FROM participants").fetchone() is None:
        import_test_users()

    # Check for templates
    check_for_templates()

    # Kører appen på port 9080 og host
    app.run(debug=True,port=9080,host='0.0.0.0')
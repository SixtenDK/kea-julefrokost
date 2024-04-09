from flask import Flask, render_template, request, redirect
import sqlite3

class Participants:
    def __init__(self):
        # Flask app
        self.app = Flask(__name__)

        # Database connection
        self.conn = sqlite3.connect('julefrokost.db', check_same_thread=False)
        self.c = self.conn.cursor()

        # Create table
        self.c.execute('''CREATE TABLE IF NOT EXISTS participants
                        (name text, email text, phone text, payment_method text, payment_status boolean)''')

    def show_participants(self):
        self.c.execute("SELECT * FROM participants")
        return self.c.fetchall()

    def wait_for_payment(self, email):
        payment_status = self.c.execute("SELECT payment_status FROM participants WHERE email = ?", (email,))
        while True:
            if payment_status == 1:
                self.c.execute("UPDATE participants SET payment_status = 1 WHERE email = ?", (email,))
                self.conn.commit()
                break

    def insert_into_db(self, name, email, phone, payment_method, payment_status):
        self.c.execute("INSERT INTO participants VALUES (?, ?, ?, ?, ?)", (name, email, phone, payment_method, payment_status))
        self.conn.commit()

    def sort_list_participants(self, sort=""):
        if sort == 'not_paid':
            participants_t = self.c.execute("SELECT * FROM participants WHERE payment_status = 0")
        elif sort == 'paid':
            participants_t = self.c.execute("SELECT * FROM participants WHERE payment_status = 1")
        else:
            participants_t = self.c.execute("SELECT * FROM participants")

        return sorted(participants_t, key=lambda x: x[0])

    def index(self):
        return render_template('index.html')

    def tilmeld(self):
        return render_template('tilmeldings-formular.html')

    def tilmeld_post(self):
        name = request.form['navn']
        email = request.form['email']
        phone = request.form['telefon']
        payment_method = request.form['betalings-metode']
        payment_status = 0
        self.insert_into_db(name, email, phone, payment_method, payment_status)
        return render_template('tilmeldings-formular.html', message="Tak for din tilmelding")

    def deltagere(self):
        args = request.args
        sort = args.get('sort', '')
        sort = sort.lower()
        if sort == 'not_paid':
            participants = self.sort_list_participants(sort)
        elif sort == 'paid':
            participants = self.sort_list_participants(sort)
        else:
            participants = self.sort_list_participants()

        return render_template('print.html', participants=participants)

    def betal(self, email):
        self.c.execute("SELECT payment_status FROM participants WHERE email = ?", (email,))
        payment_status = self.c.fetchone()[0]
        if payment_status == 1:
            self.c.execute("UPDATE participants SET payment_status = 0 WHERE email = ?", (email,))
            self.conn.commit()
        elif payment_status == 0:
            self.c.execute("UPDATE participants SET payment_status = 1 WHERE email = ?", (email,))
            self.conn.commit()

        return redirect("/deltagere", code=302)

    # def import_test_users(self):
    #     test_users = [
    #         ("John Doe", "john@example.com", "12345678", "MobilePay", 1),
    #         ("Jane Smith", "jane@example.com", "87654321", "Bank transfer", 0),
    #         ("Alice Johnson", "alice@example.com", "98765432", "Credit card", 1),
    #         ("Bob Anderson", "bob@example.com", "54321678", "PayPal", 0),
    #         ("Eve Wilson", "eve@example.com", "23456789", "Venmo", 1),
    #         ("Grace Lee", "grace@example.com", "34567890", "Cash", 0),
    #         ("Michael Brown", "michael@example.com", "98765432", "Bank transfer", 1),
    #         ("Sarah Johnson", "sarah@example.com", "45678901", "Credit card", 0),
    #         ("David Smith", "david@example.com", "10987654", "PayPal", 1),
    #         ("Olivia Wilson", "olivia@example.com", "56789012", "Venmo", 0),
    #         ("James Lee", "james@example.com", "21098765", "Cash", 1),
    #         ("Emma Brown", "emma@example.com", "65432109", "Bank transfer", 0),
    #         ("William Anderson", "william@example.com", "89012345", "MobilePay", 1),
    #         ("Sophia Doe", "sophia@example.com", "43210987", "Credit card", 0),
    #         ("Alexander Johnson", "alexander@example.com", "76543210", "PayPal", 1),
    #         ("Mia Smith", "mia@example.com", "90123456", "Venmo", 0),
    #         ("Benjamin Wilson", "benjamin@example.com", "32109876", "Cash", 1)
    #     ]
    #     for user in test_users:
    #         self.insert_into_db(*user)

participants = Participants()

@participants.app.route('/')
def index():
    return participants.index()

@participants.app.route('/tilmeld')
def tilmeld():
    return participants.tilmeld()

@participants.app.route('/tilmeld', methods=['POST'])
def tilmeld_post():
    return participants.tilmeld_post()

@participants.app.route('/deltagere', methods=['GET'])
def deltagere():
    return participants.deltagere()

@participants.app.route('/betal/<email>', methods=['GET', 'POST'])
def betal(email):
    return participants.betal(email)

if __name__ == '__main__':
    participants.app.run(debug=True, port=9080, host='0.0.0.0')


    # Her har vi en klasse stats, som indeholder information om antal deltagere, antal deltagere som har betalt, antal deltagere som ikke har betalt
# Ved instansiering af klassen, hentes alle deltagere fra databasen, deltagerne som har betalt og deltagerne som ikke har betalt
# Der få metoder i klassen, da det er en simpel klasse, som kun indeholder information, dette kunne også være en dictionary
class stats:
    def __init__(self):
        # Hent alle deltagerne fra databasen
        # Bruger show_participants funktionen til at hente alle deltagerne fra databasen
        self.participants = show_participants()

        # Hent alle deltagerne fra databasen som har betalt
        self.participants_paid = c.execute("SELECT * FROM participants WHERE payment_status = 1").fetchall()

        # Hent alle deltagerne fra databasen som ikke har betalt
        self.participants_not_paid = c.execute("SELECT * FROM participants WHERE payment_status = 0").fetchall()

        # Beregn antal deltagere, antal deltagere som har betalt, antal deltagere som ikke har betalt
        self.total_participants = len(self.participants)

        # Beregn antal deltagere som har betalt
        self.total_participants_paid = len(self.participants_paid)

        # Beregn antal deltagere som ikke har betalt
        self.total_participants_not_paid = len(self.participants_not_paid)

        # Beregn procentdelen af deltagere som har betalt og ikke har betalt
        self.total_participants_paid_percentage = self.total_participants_paid / self.total_participants * 100

        # Beregn procentdelen af deltagere som ikke har betalt
        self.total_participants_not_paid_percentage = self.total_participants_not_paid / self.total_participants * 100

    def all_stats_dict(self):
        return {
            'total_participants': self.total_participants,
            'total_participants_paid': self.total_participants_paid,
            'total_participants_not_paid': self.total_participants_not_paid,
            'total_participants_paid_percentage': self.total_participants_paid_percentage,
            'total_participants_not_paid_percentage': self.total_participants_not_paid_percentage
        }
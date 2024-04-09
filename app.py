from flask import Flask, request, session

app = Flask(__name__)
app.secret_key = 'dit_hemmelige_nøgle'

def auth(f):
    # Brug brugernavn og password til at autentificere
    brugernavn = "sekretær"
    password = "kea2024"

    def auth_function(*args, **kwargs):
        # Hvis brugernavn og password er gemt i sessionen og er korrekt, kører vi funktionen
        if 'brugernavn' in session and 'password' in session:
            if session['brugernavn'] == brugernavn and session['password'] == password:
                return f(*args, **kwargs)
        # Hvis brugernavn og password ikke er gemt i sessionen, eller er forkert, beder vi om autentificering
        return "Du har ikke adgang til denne side", 401

    return auth_function

# Login-endpunkt til at gemme brugernavn og adgangskode i sessionen
@app.route('/login')
def login():
    session['brugernavn'] = request.args.get('brugernavn')
    session['password'] = request.args.get('password')
    return "Du er logget ind"

# Beskyttede ruter, hvor autentificering kræves
@app.route('/sekretær')
@auth
def sekretær():
    return "Velkommen sekretær"

@app.route('/direktør')
@auth
def direktør():
    return "Velkommen direktør"

if __name__ == "__main__":
    app.run(debug=True)

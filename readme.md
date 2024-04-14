# Kea programmering

## Usage

```bash
python3 main.py
```

Ved kørsel af programmet, starter der en webserver op på port 9080.\
Denne webserver kan du tilgå via dette link http://localhost:9080 eller http://ip:9080
## Brugeroplysninger
Username: sekretær\
Password: kea2024

## Opgave1: Tilmelding til julefrokost
Du er af en forening blevet bedt om at lave et system\
hvor foreningssekretæren skal kunne indtaste tilmeldinger til den årlige julefrokost.
## Minimumskravfrabrugerperspektiv:
### En bruger skal kunne indtaste stamdata for en tilmelding herunder: 
- Navn
- Har deltageren betalt? 

### Brugeren skal kunne danne et overblik over tilmeldte vha. følgende funktioner:
- Print navn på tilmeldte, der ikke har betalt.
- Print navn på tilmeldte, der har betalt.
- Print alle tilmeldte. 

## Kort beskrivelse af programmet
Dette program er bygget så vores sekrætær kan tilmelde folk til julefrokost.\
nemt og hurtigt kan se hvem der har betalt og hvem der ikke har betalt.\
Sekrætæren kan også se en liste over alle tilmeldingerne. både for dem der har betalt og dem der ikke har betalt.
Her kan hun slette eller ændre betaling status.

## Motivation for valg af opgaven
Jeg har valgt at lave en webapplikation til tilmelding til en julefrokost, fordi det er en simpel og overskuelig opgave, som jeg kan løse med Flask. Jeg har valgt at bruge Flask, fordi det er et letvægtsframework, som er nemt at bruge og udvide. Jeg har valgt at lave en webapplikation, fordi det er en god måde at øve mig i at arbejde med Flask og webudvikling.

## Teknisk beskrivelse af programmet
Programmet er bygget med Flask, som er et microframework til Python. Flask er designet til at være let at bruge og udvide, og det er derfor et godt valg til små og mellemstore projekter. Flask er en del af Pallets-projekterne, som er en samling af små og lette værktøjer til at udvikle webapplikationer i Python.

Programmet består af en fil og en mappe templates med nogle html templates:
- main.py: Flask applikationen
- templates/index.html: Forsiden med valg mulighederne
- templates/login.html: Login siden
- templates/print.html: deltagere listen
- templates/tilmeldings-formular.html: tilmeldingsformular siden

Programmet har en simpel brugergrænseflade, hvor brugeren kan indtaste stamdata for en tilmelding til en julefrokost. Brugeren kan indtaste navn og om deltageren har betalt. Programmet giver brugeren mulighed for at danne et overblik over tilmeldingerne ved at printe navnene på de tilmeldte, der ikke har betalt, navnene på de tilmeldte, der har betalt, og alle tilmeldingerne.

Programmet gemmer tilmeldingerne i en SQLite database, som er en letvægtsdatabase, der er nem at bruge og udvide. SQLite er en del af Python standardbiblioteket, og det er derfor nemt at bruge i Flask applikationer.

### Teknologier
- Flask
- Python
- HTML
- CSS
- JavaScript
- sqlite3

## Forslag til mulige forbedringer
- Brugeren skal kunne redigere en tilmelding.
- Brugeren skal kunne søge efter en tilmelding.
- Brugeren skal kunne eksportere tilmeldingerne til en CSV-fil.
- Brugeren skal kunne importere tilmeldingerne fra en CSV-fil.
- Brugeren skal kunne oprette en bruger.
- Brugeren skal kunne ændre sin adgangskode.

## Literatur liste
- https://flask.palletsprojects.com/en/3.0.x/
- https://www.w3schools.com/

## Forfatter
- [Sixten Nexø Grahn]()

## License
[MIT](https://choosealicense.com/licenses/mit/)

```
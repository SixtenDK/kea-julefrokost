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

## Opbygning af min applikation
Jeg har valgt at følge opgaven, så man i min applikation kan indtaste navn\
Her er der blevet lavet lidt om på betalingsmetoden, hvor man kan vælge mobilepay/kontant.

Der så lavet en oversigt hvor i at man kan ændre betalingsstatus, og slette brugere.
Der også mulighed for at se andre oplysninger.

## Literatur liste
- https://flask.palletsprojects.com/en/3.0.x/
- https://www.w3schools.com/
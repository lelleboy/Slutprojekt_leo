import json
import datetime


session = {"användarnamn": None}

def träningslogg():
    pass

def kalori_beräkning(aktivitet, tid_i_min):
    aktiviteter = [
        {"aktivitet": "löpning",      "met": {"låg": 7.0,  "medel": 8.3,  "hög": 11.0}},
        {"aktivitet": "cykling",      "met": {"låg": 4.5,  "medel": 6.8,  "hög": 10.0}},
        {"aktivitet": "simning",      "met": {"låg": 6.0,  "medel": 7.0,  "hög": 9.5}},
        {"aktivitet": "promenad",     "met": {"låg": 2.8,  "medel": 3.5,  "hög": 4.3}},
        {"aktivitet": "styrketräning","met": {"låg": 3.5,  "medel": 5.0,  "hög": 6.0}},
        {"aktivitet": "yoga",         "met": {"låg": 2.0,  "medel": 2.5,  "hög": 3.0}},
        {"aktivitet": "aerobics",     "met": {"låg": 6.5,  "medel": 7.3,  "hög": 8.5}},
        {"aktivitet": "dans",         "met": {"låg": 3.5,  "medel": 5.0,  "hög": 7.5}},
        {"aktivitet": "roddmaskin",   "met": {"låg": 5.5,  "medel": 7.0,  "hög": 8.5}},
        {"aktivitet": "vandring",     "met": {"låg": 5.0,  "medel": 6.0,  "hög": 7.0}},
        {"aktivitet": "samlag",       "met": {"låg": 3.0,  "medel": 5.0,  "hög": 5.8}},
    ]

    def hitta_met(aktivitet):
        aktivitet = aktivitet.lower()
        for a in aktiviteter:
            if aktivitet == a["aktivitet"].lower():
                return a["met"]
        print("Din aktivitet hittades inte.")
        return None

    def beräkna_kalorier(aktivitet, tid_i_min):
        användare = session["användarnamn"]
        filnamn = f"{användare}.json"
        with open(filnamn, "r", encoding="utf-8") as file:
            data = json.load(file)

        kön    = data["kön"]
        vikt   = data["vikt"]
        ålder  = data["ålder"]
        längd  = data["längd"]

        met = hitta_met(aktivitet)
        if met is None:
            return 0

        if kön.lower() == "man":
            bmr = 66.47 + (13.75 * vikt) + (5.003 * längd) - (6.755 * ålder)
        elif kön.lower() == "kvinna":
            bmr = 655.1 + (9.563 * vikt) + (1.850 * längd) - (4.676 * ålder)
        else:
            raise ValueError("Kön måste vara 'man' eller 'kvinna'.")

        kalorier = (bmr / 1440) * met["medel"] * tid_i_min
        return round(kalorier, 2)

    return beräkna_kalorier(aktivitet, tid_i_min)

def lägg_till_träning():
    användare = session["användarnamn"]
    filnamn = f"{användare}.json"

    try:
        with open(filnamn, "r", encoding="utf-8") as file:
            data = json.load(file)

        aktivitet  = input("Aktivitet: ").strip()
        tid_i_min  = float(input("Tid i minuter: "))
        datum      = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        kalorier = kalori_beräkning(aktivitet, tid_i_min)

        nytt_pass = {
            "datum":      datum,
            "aktivitet":  aktivitet,
            "tid_i_min":  tid_i_min,
            "kalorier":   kalorier
        }

        if "träning" not in data:
            data["träning"] = []
        data["träning"].append(nytt_pass)

        with open(filnamn, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print("Träningspass sparat!")

    except Exception as e:
        print("Något gick fel:", e)

def lägg_till_konto():
    print("Skapa nytt konto")
    användarnamn = input("Välj ett användarnamn: ").lower()
    namn         = input("Ange ditt riktiga namn: ")
    kön          = input("Ange biologiska kön (man eller kvinna): ").lower()
    ålder        = int(input("Ange ålder: "))
    längd        = float(input("Ange längd i (cm): "))
    vikt         = float(input("Ange vikt i (kg): "))

    användare = {
        "användarnamn": användarnamn,
        "namn":         namn,
        "kön":          kön,
        "ålder":        ålder,
        "längd":        längd,
        "vikt":         vikt
    }

    filnamn = f"{användarnamn}.json"
    with open(filnamn, "w", encoding="utf-8") as fil:
        json.dump(användare, fil, ensure_ascii=False, indent=4)

    print(f"Ditt konto '{användarnamn}' har sparats!")

def logga_in():
    användarnamn = input("Användarnamn: ").lower().strip()
    filnamn = f"{användarnamn}.json"
    try:
        with open(filnamn, "r", encoding="utf-8") as file:
            json.load(file)
        session["användarnamn"] = användarnamn
        print(f"Inloggad som '{användarnamn}'!")
    except FileNotFoundError:
        print("Kontot hittades inte.")


while True:
    if session["användarnamn"] is None:
        print("\n=== Välkommen ===")
        print("1. Logga in")
        print("2. Skapa konto")
        print("3. Avsluta")
        val = input("Välj: ").strip()

        if val == "1":
            logga_in()
        elif val == "2":
            lägg_till_konto()
        elif val == "3":
            print("Hej då!")
            break
        else:
            print("Ogiltigt val, försök igen.")

    else:
        print(f"\n=== Inloggad som '{session['användarnamn']}' ===")
        print("1. Lägg till träning")
        print("2. Logga ut")
        print("3. Avsluta")
        val = input("Välj: ").strip()

        if val == "1":
            lägg_till_träning()
        elif val == "2":
            session["användarnamn"] = None
            print("Utloggad.")
        elif val == "3":
            print("Hej då!")
            break
        else:
            print("Ogiltigt val, försök igen.")
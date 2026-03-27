import json


def träningslogg():
    
    pass


def kalori_beräkning():
    aktiviteter = [
    {"aktivitet": "löpning", "met": 8.3},
    {"aktivitet": "cykling", "met": 6.8},
    {"aktivitet": "simning", "met": 7.0},
    {"aktivitet": "promenad", "met": 3.5},
    {"aktivitet": "styrketräning", "met": 6.0},
    {"aktivitet": "yoga", "met": 2.5},
    {"aktivitet": "aerobics", "met": 7.3},
    {"aktivitet": "dans", "met": 5.0},
    {"aktivitet": "roddmaskin", "met": 7.0},
    {"aktivitet": "vandring", "met": 6.0},
    {"aktivitet": "samlag","met":5.0}
]

# returnerar met värdet 
    def hitta_met(aktivitet):
        aktivitet = aktivitet.lower()
        for a in aktiviteter:
            if aktivitet == a["aktivitet"].lower():
                return a["met"]
        print("Din aktivitet hittades inte.")
        return None

    # beräknar kalorier
    def beräkna_kalorier(aktivitet, tid_i_min):
        användare = session.användarnamn
        filnamn = f"{användare}.json"
        with open(filnamn, "r", encoding="utf-8") as file:
            data = json.load(file)

        kön = data["kön"]
        vikt = data["vikt"]
        ålder = data["ålder"]
        längd = data["längd"]

        met = hitta_met(aktivitet)
        if met is None:
            return 0

        if kön.lower() == "man":
            bmr = 66.47 + (13.75 * vikt) + (5.003 * längd) - (6.755 * ålder)
        elif kön.lower() == "kvinna":
            bmr = 655.1 + (9.563 * vikt) + (1.850 * längd) - (4.676 * ålder)
        else:
            raise ValueError("Kön måste vara 'man' eller 'kvinna'.")

        kalorier = (bmr / 1440) * met * tid_i_min
        return round(kalorier, 2)
    
def session():
    användarnamn = None
    

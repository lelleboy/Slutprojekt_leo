import customtkinter as ctk
from tkcalendar import Calendar
import json
import datetime
import os
import glob

# Sätter dark mode
ctk.set_appearance_mode("dark")

# Färger
BG_COLOR = "#0B1120"
CARD_COLOR = "#1F2937"
ACCENT_COLOR = "#3B82F6"
DOT_COLOR = "#EF4444"
TEXT_SECONDARY = "#9CA3AF"
ERROR_COLOR = "#F87171"

# Fönsterstorlek
WIDTH = 360
HEIGHT = 500

# Skapar appen
app = ctk.CTk()

# Sätter storlek
app.geometry(f"{WIDTH}x{HEIGHT}")

# Titel på appen
app.title("Fitness App")

# Bakgrundsfärg
app.configure(fg_color=BG_COLOR)

# Går ej att ändra storlek
app.resizable(False, False)

# Kollar om input är decimaltal
def check_float(P):

    # Tillåter tom ruta
    if P == "" or P == ".":
        return True

    try:
        float(P)
        return True

    except ValueError:
        return False

# Kollar om input är heltal
def check_int(P):

    # Tillåter tom ruta
    if P == "":
        return True

    try:
        int(P)
        return True

    except ValueError:
        return False

# Registrerar validering
v_float_reg = app.register(check_float)
v_int_reg = app.register(check_int)

# Sparar inloggad användare
session = {"username": None}

# Lista med aktiviteter
ACTIVITIES = [
    {"activity": "Running", "met": {"low": 6.0, "medium": 8.3, "high": 12.0}},
    {"activity": "Cycling", "met": {"low": 4.0, "medium": 7.0, "high": 10.5}},
    {"activity": "Swimming", "met": {"low": 5.0, "medium": 7.0, "high": 10.0}},
]

# Tar bort widgets
def clear():

    # Loopar igenom widgets
    for w in main_frame.winfo_children():

        # Tar bort widget
        w.destroy()

# Laddar användardata
def load_user():

    # Hämtar användarnamn
    name = session["username"]

    # Standarddata
    default_user = {
        "username": name,
        "gender": "male",
        "age": 30,
        "height": 170,
        "weight": 70,
        "workouts": [],
        "weight_history": []
    }

    # Returnerar standard om ingen användare finns
    if not name:
        return default_user

    try:

        # Kollar om fil finns
        if not os.path.exists(f"{name}.json"):
            return default_user

        # Öppnar JSON-fil
        with open(f"{name}.json", "r", encoding="utf-8") as f:

            # Returnerar data
            return json.load(f)

    except:
        return default_user

# Sparar användardata
def save_user(data):

    # Hämtar användarnamn
    name = session["username"]

    # Kollar om användare finns
    if name:

        try:

            # Sparar till JSON-fil
            with open(f"{name}.json", "w", encoding="utf-8") as f:

                # Skriver data
                json.dump(data, f, indent=4, ensure_ascii=False)

        except:
            pass

# Räknar kalorier
def calculate_calories(activity, intensity, minutes):

    # Hämtar användare
    user = load_user()

    try:

        # Hämtar vikt
        weight = float(user.get("weight", 70))

        # Hämtar ålder
        age = int(user.get("age", 30))

        # Hämtar längd
        height = float(user.get("height", 170))

        # Hämtar kön
        gender = user.get("gender", "male")

        # Standard MET-värde
        met = 5.0

        # Loopar igenom aktiviteter
        for a in ACTIVITIES:

            # Matchar aktivitet
            if a["activity"].lower() == activity.lower():

                # Hämtar MET-värde
                met = a["met"].get(intensity, 5.0)

        # Räknar BMR för män
        if gender == "male":
            bmr = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)

        # Räknar BMR för kvinnor
        else:
            bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)

        # Returnerar kalorier
        return round((bmr / 1440) * met * float(minutes), 1)

    except:
        return 0.0

# Skapar navbar
def navbar():

    # Skapar navbar
    nav = ctk.CTkFrame(main_frame, height=65, fg_color="#111827", corner_radius=0)

    # Placerar navbar
    nav.pack(side="bottom", fill="x")

    # Lista med knappar
    buttons = [
        ("🏠", "Home", dashboard),
        ("➕", "New", add_workout),
        ("📅", "Calendar", calendar_page),
        ("👤", "History", history_page),
        ("🚪", "Logout", logout),
    ]

    # Loopar igenom knappar
    for icon, text, cmd in buttons:

        # Skapar knapp-frame
        btn = ctk.CTkFrame(nav, fg_color="transparent", corner_radius=6, cursor="hand2")

        # Placerar knapp
        btn.pack(side="left", expand=True, pady=4, padx=1)

        # Visar ikon
        i_lbl = ctk.CTkLabel(btn, text=icon, font=("Arial", 16), text_color="white")
        i_lbl.pack()

        # Visar text
        t_lbl = ctk.CTkLabel(btn, text=text, font=("Arial", 9), text_color=TEXT_SECONDARY)
        t_lbl.pack()

        # Klickfunktion
        btn.bind("<Button-1>", lambda e, c=cmd: c())
        i_lbl.bind("<Button-1>", lambda e, c=cmd: c())
        t_lbl.bind("<Button-1>", lambda e, c=cmd: c())

# Skapar kort
def create_card(parent, title):

    # Skapar frame
    card = ctk.CTkFrame(parent, fg_color=CARD_COLOR, corner_radius=12)

    # Placerar kort
    card.pack(fill="x", padx=15, pady=5)

    # Titel
    label = ctk.CTkLabel(card, text=title, font=("Arial", 11, "bold"), text_color=TEXT_SECONDARY)

    # Placerar titel
    label.pack(anchor="w", padx=12, pady=(8, 2))

    return card

# Visar startsida
def start_page():

    # Rensar sidan
    clear()

    # Titel
    ctk.CTkLabel(
        main_frame,
        text="FITNESS",
        font=("Impact", 42),
        text_color=ACCENT_COLOR
    ).pack(pady=(60, 20))

    # Login-knapp
    ctk.CTkButton(
        main_frame,
        text="Login",
        fg_color=ACCENT_COLOR,
        command=login_page
    ).pack(pady=10, padx=40, fill="x")

    # Skapa konto-knapp
    ctk.CTkButton(
        main_frame,
        text="Create Account",
        fg_color=CARD_COLOR,
        command=register_page
    ).pack(pady=10, padx=40, fill="x")

# Login-sida
def login_page():

    # Rensar sidan
    clear()

    # Titel
    ctk.CTkLabel(main_frame, text="Login", font=("Arial", 22, "bold")).pack(pady=20)

    # Inputfält
    e = ctk.CTkEntry(main_frame, placeholder_text="Username")
    e.pack(padx=40, fill="x")

    # Loginfunktion
    def go():

        # Hämtar användarnamn
        val = e.get().strip().lower()

        # Kollar om tomt
        if not val:
            return

        # Sparar användare
        session["username"] = val

        # Går till dashboard
        dashboard()

    # Login-knapp
    ctk.CTkButton(
        main_frame,
        text="Go",
        fg_color=ACCENT_COLOR,
        command=go
    ).pack(pady=10, padx=40, fill="x")

# Dashboard
def dashboard():

    # Rensar sidan
    clear()

    # Hämtar användare
    user = load_user()

    # Hälsning
    ctk.CTkLabel(
        main_frame,
        text=f"Hello {user.get('username', '')}",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    # Skapar progress-kort
    card = create_card(main_frame, "Progress")

    # Hämtar workouts
    workouts = user.get("workouts", [])

    # Räknar kalorier
    tc = sum(float(w.get("calories", 0)) for w in workouts)

    # Räknar minuter
    tm = sum(float(w.get("time_in_min", 0)) for w in workouts)

    # Visar kalorier
    ctk.CTkLabel(
        card,
        text=f"{tc:.0f} kcal",
        font=("Arial", 28, "bold")
    ).pack(anchor="w", padx=12)

    # Visar minuter
    ctk.CTkLabel(
        card,
        text=f"{tm:.0f} total minutes",
        text_color=TEXT_SECONDARY
    ).pack(anchor="w", padx=12)

    # Visar navbar
    navbar()

# Sida för att lägga till workout
def add_workout():

    # Rensar sidan
    clear()

    # Titel
    ctk.CTkLabel(
        main_frame,
        text="Log Workout",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    # Input för minuter
    m_entry = ctk.CTkEntry(main_frame, placeholder_text="Minutes")
    m_entry.pack(padx=30, fill="x", pady=5)

    # Variabel för aktivitet
    act_v = ctk.StringVar(value="Running")

    # Dropdown för aktiviteter
    ctk.CTkOptionMenu(
        main_frame,
        values=[a["activity"] for a in ACTIVITIES],
        variable=act_v
    ).pack(padx=30, fill="x", pady=5)

    # Sparfunktion
    def save():

        # Hämtar användare
        user = load_user()

        try:
            m = float(m_entry.get())

        except:
            return

        # Sparar workout
        user["workouts"].append({
            "activity": act_v.get(),
            "time_in_min": m,
            "calories": calculate_calories(act_v.get(), "medium", m),
            "date": datetime.datetime.now().strftime("%Y-%m-%d")
        })

        # Sparar användare
        save_user(user)

        # Till dashboard
        dashboard()

    # Sparaknapp
    ctk.CTkButton(
        main_frame,
        text="Save Workout",
        fg_color=ACCENT_COLOR,
        command=save
    ).pack(pady=10, padx=30, fill="x")

    # Navbar
    navbar()

# Kalender-sida
def calendar_page():

    # Rensar sidan
    clear()

    # Titel
    ctk.CTkLabel(main_frame, text="Calendar", font=("Arial", 18, "bold")).pack(pady=10)

    try:

        # Skapar kalender
        cal = Calendar(main_frame)

        # Visar kalender
        cal.pack(pady=10)

    except:
        pass

    # Navbar
    navbar()

# Historik-sida
def history_page():

    # Rensar sidan
    clear()

    # Titel
    ctk.CTkLabel(main_frame, text="History", font=("Arial", 18, "bold")).pack(pady=10)

    # Scrollbar
    scroll = ctk.CTkScrollableFrame(main_frame)

    # Placerar scrollbar
    scroll.pack(fill="both", expand=True, padx=10)

    # Hämtar workouts
    workouts = load_user().get("workouts", [])

    # Loopar igenom workouts
    for w in workouts:

        # Visar workout
        ctk.CTkLabel(
            scroll,
            text=f"{w['date']} - {w['activity']} - {w['time_in_min']} min"
        ).pack(anchor="w", pady=3)

    # Navbar
    navbar()

# Registreringssida
def register_page():

    # Rensar sidan
    clear()

    # Titel
    ctk.CTkLabel(main_frame, text="Create Account", font=("Arial", 22, "bold")).pack(pady=20)

    # Inputfält
    user_entry = ctk.CTkEntry(main_frame, placeholder_text="Username")
    user_entry.pack(padx=40, fill="x", pady=5)

    # Skapa konto
    def create():

        # Hämtar namn
        u = user_entry.get().strip().lower()

        # Kollar om tomt
        if not u:
            return

        # Sparar användare
        session["username"] = u

        # Skapar användardata
        data = {
            "username": u,
            "gender": "male",
            "age": 20,
            "height": 170,
            "weight": 70,
            "workouts": [],
            "weight_history": []
        }

        # Sparar användare
        save_user(data)

        # Går till dashboard
        dashboard()

    # Create-knapp
    ctk.CTkButton(
        main_frame,
        text="Create",
        fg_color=ACCENT_COLOR,
        command=create
    ).pack(pady=10, padx=40, fill="x")

# Loggar ut användaren
def logout():

    # Tar bort användare
    session["username"] = None

    # Visar startsida
    start_page()

# Skapar huvudframe
main_frame = ctk.CTkFrame(app, fg_color=BG_COLOR, corner_radius=0)

# Placerar huvudframe
main_frame.pack(fill="both", expand=True)

# Startar startsidan
start_page()

# Startar appen
app.mainloop()


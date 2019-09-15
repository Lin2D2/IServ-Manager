from datetime import datetime, date

weekdays = {
    1: "Montag",
    2: "Dienstag",
    3: "Mittwoch",
    4: "Donnerstag",
    5: "Freitag",
    6: "Samstag",
    7: "Sonntag"
}

def date_and_day():
    day = weekdays[datetime.today().isoweekday()]
    date_today = date.today().strftime("%d.%m.%Y")
    return date_today + " " + day

import PySimpleGUI as sg
from bs4 import BeautifulSoup
import requests

def get_stock_data(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, "html.parser")
    soppan = soup.find("tbody")
    rader = soppan.find_all("tr")
    stock_data = []
    for rad in rader:
        info = rad.find_all("td")
        namn = info[0].find("a", href=True).text.strip()
        kurs = info[1].text.strip()
        procent = info[3].text.strip()
        stock_data.append([namn, kurs, procent])
    return stock_data

def find_daily_winner(data):
    max_percent = -float('inf')
    winner = None
    for stock in data:
        percent_str = stock[2].replace("%", "").replace(",", ".")
        percent = float(percent_str)
        if percent > max_percent:
            max_percent = percent
            winner = stock
    return winner

def find_daily_loser(data):
    min_percent = float('inf')
    loser = None
    for stock in data:
        percent_str = stock[2].replace("%", "").replace(",", ".")
        percent = float(percent_str)
        if percent < min_percent:
            min_percent = percent
            loser = stock
    return loser

# Skapa layout för appen
layout = [
    [sg.Text("Välj en Lista:", font=("Helvetica", 15)), sg.Button("Large Cap", size=(14, 1), key="-LARGE_CAP-"), sg.Button("Small Cap", size=(14, 1), key="-SMALL_CAP-")],
    [sg.Frame("Dagens vinnare:", [
        [sg.Text("", size=(40, 1), key="-WINNER_FRAME-", relief=sg.RELIEF_SUNKEN, font=("Helvetica", 12))]
    ], border_width=1)],
    [sg.Frame("Dagens förlorare:", [
        [sg.Text("", size=(40, 1), key="-LOSER_FRAME-", relief=sg.RELIEF_SUNKEN, font=("Helvetica", 12))]
    ], border_width=1)],
    [sg.Table(values=[], headings=["Namn", "Kurs", "Förändring"], display_row_numbers=False,
              auto_size_columns=False, num_rows=25, key="-TABLE-", col_widths=[15, 10, 15])],
    [sg.Button("Uppdatera (live)", size=(34, 1)), sg.Button("Avsluta", size=(10, 1))]
]

# Skapa fönster
window = sg.Window("AddeKvat-Aktie-App", layout, finalize=True)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Avsluta"):
        break
    elif event in ("-LARGE_CAP-", "-SMALL_CAP-"):
        if event == "-LARGE_CAP-":
            url = "https://www.di.se/bors/large-cap/"
            window.TKroot.title("AddeKvat-Aktie-App - Large Cap")
        else:
            url = "https://www.di.se/bors/small-cap/"
            window.TKroot.title("AddeKvat-Aktie-App - Small Cap")

        data = get_stock_data(url)
        window["-TABLE-"].update(values=data)

        # Hitta dagens vinnare och förlorare för respektive börs och visa i fönstret
        winner = find_daily_winner(data)
        loser = find_daily_loser(data)
        if winner:
            window["-WINNER_FRAME-"].update(f" {winner[0]} ({winner[2]})")
        else:
            window["-WINNER_FRAME-"].update("Dagens vinnare:")

        if loser:
            window["-LOSER_FRAME-"].update(f" {loser[0]} ({loser[2]})")
        else:
            window["-LOSER_FRAME-"].update("Dagens förlorare:")

    elif event == "Uppdatera (live)":
        # Uppdatera aktieinformationen
        if "url" in locals():
            data = get_stock_data(url)
            window["-TABLE-"].update(values=data)

            # Hitta dagens vinnare och förlorare för respektive börs och visa i fönstret
            winner = find_daily_winner(data)
            loser = find_daily_loser(data)
            if winner:
                window["-WINNER_FRAME-"].update(f" {winner[0]} ({winner[2]})")
            else:
                window["-WINNER_FRAME-"].update("Dagens vinnare:")

            if loser:
                window["-LOSER_FRAME-"].update(f" {loser[0]} ({loser[2]})")
            else:
                window["-LOSER_FRAME-"].update("Dagens förlorare:")

# Stäng fönstret
window.close()

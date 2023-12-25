import requests
from bs4 import BeautifulSoup

class Squadra:
    def __init__(self, nome, punti=0, elo=1500):
        self.nome = nome
        self.elo = elo
        self.punti = punti


def selezione():
    print("")
    print("\n***MENU SCELTE***")
    print("1: elenco partite, risultati e aggiornamento elo")
    print("2: classifica estrapolata")
    print("3: tabellone elo")
    print("4: confronta % vittoria")
    scelta = int(input("\npregasi scegliere cosa fare: "))
    if scelta == 1:
        estrapola_serieb()
    elif scelta == 2:
        tabella_classifica()
    elif scelta == 3:
        tabella_elo()
    elif scelta == 4:
        stime_squadre()
    else:
        print("Scelta non valida")
        selezione()


def calcola_elo(punteggio_1, punteggio_2, k=20):
    esperienza_1 = 1 / (1 + 10**((punteggio_2 - punteggio_1) / 400))
    esperienza_2 = 1 / (1 + 10**((punteggio_1 - punteggio_2) / 400))

    nuovo_elo_1 = punteggio_1 + k * (1 - esperienza_1)
    nuovo_elo_2 = punteggio_2 + k * (0 - esperienza_2)

    return round(nuovo_elo_1), round(nuovo_elo_2)


def calcola_percentuali_vittoria(squadra1_elo, squadra2_elo, k=20):
    esperienza_1 = 1 / (1 + 10**((squadra2_elo - squadra1_elo) / 400))
    esperienza_2 = 1 / (1 + 10**((squadra1_elo - squadra2_elo) / 400))

    prob_vittoria_squadra1 = esperienza_1
    prob_vittoria_squadra2 = esperienza_2
    prob_pareggio = 1 - prob_vittoria_squadra1 - prob_vittoria_squadra2

    return prob_vittoria_squadra1, prob_vittoria_squadra2, prob_pareggio


def estrapola_serieb():
    url_base = "https://www.legab.it/seriebkt/calendario"
    num_giornate = int(input("Scegli il numero di giornata: ")) # Modifica il numero di giornate desiderato
    global squadre
    squadre = {}

    for giornata in range(1, num_giornate + 1):
        url_giornata = f"{url_base}/2023-2024/stagione-regolare/{giornata}"
        response = requests.get(url_giornata)
        soup = BeautifulSoup(response.text, 'html.parser')

        partite = soup.find_all("div", class_="giornata-partita relative")
        for partita in partite:
            squadre_blocchi = partita.find_all("div", class_="club p-0")

            if len(squadre_blocchi) == 2:
                squadra1_nome = squadre_blocchi[0].find("span", class_="sigla").text.strip()
                squadra2_nome = squadre_blocchi[1].find("span", class_="sigla").text.strip()

                if squadra1_nome not in squadre:
                    squadre[squadra1_nome] = Squadra(squadra1_nome)

                if squadra2_nome not in squadre:
                    squadre[squadra2_nome] = Squadra(squadra2_nome)

                punteggi_blocchi = partita.find_all("span", class_="gol")
                if len(punteggi_blocchi) == 2:
                    gol1, gol2 = map(int, [punteggi_blocchi[0].text.strip(), punteggi_blocchi[1].text.strip()])

                    # Qui puoi gestire i risultati della partita e calcolare i punteggi Elo come hai fatto prima
                    if gol1 > gol2:
                        squadre[squadra1_nome].punti += 3
                        squadre[squadra1_nome].elo, squadre[squadra2_nome].elo = calcola_elo(squadre[squadra1_nome].elo, squadre[squadra2_nome].elo)
                    elif gol1 < gol2:
                        squadre[squadra2_nome].punti += 3
                        squadre[squadra2_nome].elo, squadre[squadra1_nome].elo = calcola_elo(squadre[squadra2_nome].elo, squadre[squadra1_nome].elo)
                    else:
                        squadre[squadra1_nome].punti += 1
                        squadre[squadra2_nome].punti += 1
                        squadre[squadra1_nome].elo, squadre[squadra2_nome].elo = calcola_elo(squadre[squadra1_nome].elo, squadre[squadra2_nome].elo, k=10)

                    print(f"Giornata {giornata}: {squadra1_nome} {gol1}-{gol2} {squadra2_nome}")
                    print(f"Punteggio Elo: {squadra1_nome}: {squadre[squadra1_nome].elo}, {squadra2_nome}: {squadre[squadra2_nome].elo}\n")
    selezione()


def tabella_classifica():
    print("Classifica fino a dove estrapolato: ")
    for squadra in sorted(squadre.values(), key=lambda x: x.punti, reverse=True):
        print(f"{squadra.nome}: {squadra.punti}")
    selezione()    


def tabella_elo():
    print("Riassunto Punteggi Elo:")
    for squadra in sorted(squadre.values(), key=lambda x: x.elo, reverse=True):
        print(f"{squadra.nome}: {squadra.elo}")
    selezione()



def stime_squadre():
    squadra1_nome = input("Inserisci il nome della prima squadra: ")
    squadra2_nome = input("Inserisci il nome della seconda squadra: ")

    if squadra1_nome not in squadre or squadra2_nome not in squadre:
        print("Squadra non trovata. Assicurati di aver inserito i nomi corretti.")
    else:
        squadra1_elo = squadre[squadra1_nome].elo
        squadra2_elo = squadre[squadra2_nome].elo

        prob_vittoria_squadra1, prob_vittoria_squadra2, prob_pareggio = calcola_percentuali_vittoria(squadra1_elo, squadra2_elo)

        print(f"Probabilità di vittoria per {squadra1_nome}: {prob_vittoria_squadra1 * 100:.2f}%")
        print(f"Probabilità di vittoria per {squadra2_nome}: {prob_vittoria_squadra2 * 100:.2f}%")
        print(f"Probabilità di pareggio: {prob_pareggio * 100:.2f}%")    
    selezione()



#--------------------------------------
print("BENVENUTO NEL CALCOLATORE SERIE B (di Andrea Gobbetti)!")
selezione()





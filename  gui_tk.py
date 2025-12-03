#Tkinter-GUI
import random
import tkinter as tk

#Importerar spelmotorn (main.py) för att återanvända funktionerna
import main as motor
from rum import Rum
from speltillstand import Speltillstand

#Klass för att använda grafik
class WhumpusGUI:

    def __init__(self, huvudfonster, kartfil, andel_hal, andel_fladder,
                 sannolikhet_norm, antal_pilar, svarighetsgrad):
        #Sparar "inställningar" som instansvariabler
        self.huvudfonster = huvudfonster
        self.kartfil = kartfil
        self.andel_hal = andel_hal
        self.andel_fladder = andel_fladder
        self.sannolikhet_norm = sannolikhet_norm
        self.antal_pilar_start = antal_pilar
        self.svarighetsgrad = svarighetsgrad
        self.slumpgenerator = random.Random() #slumpgenerator

        #Flagga för att stänga av knappar efter vinst/förlust
        self.game_over = False

        #Titel
        huvudfonster.title("Whumpus (Tkinter)")

        #Textfönster
        self.textlogg = tk.Text(huvudfonster, height=10, width=60, state="disabled")
        self.textlogg.pack(padx=6, pady=6)

        #Knappar för förflyttning
        ram_riktningar = tk.Frame(huvudfonster)
        ram_riktningar.pack()
        for knapptext in ("N", "O", "S", "V"):
            tk.Button(
                ram_riktningar,
                text=knapptext,
                width=6,
                command=lambda riktning=knapptext: self.tryck_flytta(riktning) #Varje knapp anropar metoden tryck_flytta()
            ).pack(side="left", padx=3)

        #Rad för att skjuta: en Entry där man skriver tre bokstäver (t.ex. "NOS")
        ram_skjutning = tk.Frame(huvudfonster)
        ram_skjutning.pack(pady=6)
        tk.Label(ram_skjutning, text="Skjut (t.ex. NOS):").pack(side="left")
        self.inmatning_skjut = tk.Entry(ram_skjutning, width=8)
        self.inmatning_skjut.pack(side="left", padx=4)
        tk.Button(ram_skjutning, text="Skjut pil", command=self.tryck_skjut).pack(side="left") #knapp som anropar tryck_skjut()

        #Spelarstatus (ex grannar och hur många pilar som finns kvar)
        self.etikett_status = tk.Label(huvudfonster, text="", anchor="w", justify="left")
        self.etikett_status.pack(padx=6, pady=4, fill="x")

        self.starta_nytt_spel()

   
    #Startar nytt spel: läser karta, placerar faror, skapar speltillstånd
    def starta_nytt_spel(self):
        #Läser in kartan
        self.rum_lista = motor.las_karta_fran_fil(self.kartfil)
        if self.rum_lista is None:
            self.skriv_till_logg("Gick inte att läsa kartan.")
            self.game_over = True
            return

        #Välj spelarens startrum
        self.spelarens_rum = self.slumpgenerator.choice(range(len(self.rum_lista)))

        #Slumpar faror enligt dina parametrar (undvik spelarens start)
        wumpus_rum = motor.slumpa_faror(
            self.rum_lista, self.slumpgenerator,
            self.andel_hal, self.andel_fladder,
            forbjudna_start={self.spelarens_rum}
        )

        if wumpus_rum is None:
            self.skriv_till_logg("Placering av faror misslyckades.")
            self.game_over = True
            return

        #Skapar speltillstånds-objekt (antal pilar & svårighetsgrad)
        self.speltillstand = Speltillstand(
            spelarens_rum=self.spelarens_rum,
            wumpus_rum=wumpus_rum,
            antal_pilar=self.antal_pilar_start,
            svarighetsgrad=self.svarighetsgrad
        )

        #Skriver ut välkomstinfo och uppdaterar statusytan
        self.skriv_till_logg("Spelet börjar!")
        self.skriv_till_logg(f"Spelaren startar i rum: {self.speltillstand.spelarens_rum}")
        self.skriv_till_logg(f"Wumpus startar i rum: {self.speltillstand.wumpus_rum}\n")
        self.uppdatera_statusrad()

   #Skriver en rad i textloggens slut
    def skriv_till_logg(self, text):
        self.textlogg.config(state="normal")
        self.textlogg.insert("end", text + "\n")
        self.textlogg.see("end")
        self.textlogg.config(state="disabled")

    #Uppdaterar statustexten
    def uppdatera_statusrad(self):
        if self.game_over:
            return

        grannar_dict = self.rum_lista[self.speltillstand.spelarens_rum].hamta_grannar()
        har_hal = any(self.rum_lista[r].fara == Rum.FARA_HAL for r in grannar_dict.values())
        har_wumpus = any(self.rum_lista[r].fara == Rum.FARA_WUMPUS for r in grannar_dict.values())
        har_fladdermoss = any(self.rum_lista[r].fara == Rum.FARA_FLADDERMUS for r in grannar_dict.values())

        statusrader = []
        if har_fladdermoss:
            statusrader.append("Du hör fladdermöss!")
        if har_wumpus:
            statusrader.append("Du känner lukten av Wumpus!")
        if har_hal:
            statusrader.append("Du känner vinddrag!")

        statusrader.append(
            f"Härifrån kan man komma till följande rum: "
            f"{grannar_dict['N']} {grannar_dict['O']} {grannar_dict['S']} {grannar_dict['V']}"
        )
        statusrader.append(f"Pilar kvar: {self.speltillstand.antal_pilar}")

        self.etikett_status.config(text="\n".join(statusrader))

    #Avsluta med skriva ett meddelande och GAME OVER och blockera knapptryck
    def avsluta_med_meddelande(self, meddelande):
        self.skriv_till_logg(meddelande)
        self.skriv_till_logg("GAME OVER")
        self.game_over = True

   #Förflyttning (anropar flytta_spelare)
    def tryck_flytta(self, riktning):
        
        if self.game_over:
            return

        nytt_rum, utfall = motor.flytta_spelare(
            self.rum_lista, self.speltillstand.spelarens_rum, riktning
        )
        self.speltillstand.spelarens_rum = nytt_rum

        if utfall == "DOD_HAL":
            self.avsluta_med_meddelande("Du klev just ner i ett bottenlöst hål.")
            return
        if utfall == "DOD_WUMPUS":
            self.avsluta_med_meddelande("Du gick in i Wumpus rum och blev uppäten.")
            return
        if utfall == "FLADDERMUS":
            #Teleportera till tomt rum (enligt din main.py)
            nytt_rum_teleport = motor.teleportera_vid_fladdermoss(self.rum_lista, self.slumpgenerator)
            if nytt_rum_teleport is not None:
                self.skriv_till_logg("Du känner fladdermusvingar mot kinden och lyfts uppåt.")
                self.skriv_till_logg(f"Efter en kort flygtur släpper fladdermössen ner dig i rum {nytt_rum_teleport}.")
                self.speltillstand.spelarens_rum = nytt_rum_teleport

        #Låt Wumpus röra sig enligt svårighetsgrad/sannolikhet
        mote_wumpus = motor.wumpus_ror_sig(
            self.rum_lista, self.speltillstand, self.sannolikhet_norm, self.slumpgenerator
        )
        if mote_wumpus == "SPELARE_UPPATEN":
            self.avsluta_med_meddelande("Wumpus vandrade in i ditt rum - du blev uppäten.")
            return

        self.uppdatera_statusrad()

    #Skjuter, läser tre riktningar från inmatningsrutan, kallar på funktionen skjut_pil() från main()
    def tryck_skjut(self):
        
        if self.game_over:
            return

        text_inmatning = self.inmatning_skjut.get().strip().upper().replace(" ", "")
        riktningar_lista = [bokstav for bokstav in text_inmatning if bokstav in ("N", "O", "S", "V")][:3]
        if len(riktningar_lista) < 3:
            self.skriv_till_logg("Ange tre riktningar (t.ex. NOS).")
            return

        resultat = motor.skjut_pil(self.rum_lista, self.speltillstand.spelarens_rum, riktningar_lista)
        if resultat == "TRAFF":
            self.skriv_till_logg("Du dödade Wumpus! Du vinner!")
            self.game_over = True
            return
        elif resultat == "SJALVTRAFF":
            self.avsluta_med_meddelande("Aj! Pilen kom tillbaka - självträff. Du dör.")
            return
        else:
            self.speltillstand.minska_pilar()
            self.skriv_till_logg(f"Miss. Pilar kvar: {self.speltillstand.antal_pilar}")
            if not self.speltillstand.har_pilar_kvar():
                self.avsluta_med_meddelande("Pilarna är slut. Du förlorar!")
                return

        #Efter miss: Wumpus kan röra på sig
        mote_wumpus = motor.wumpus_ror_sig(
            self.rum_lista, self.speltillstand, self.sannolikhet_norm, self.slumpgenerator
        )
        if mote_wumpus == "SPELARE_UPPATEN":
            self.avsluta_med_meddelande("Wumpus vandrade in i ditt rum - du blev uppäten.")
            return

        self.uppdatera_statusrad()

#Metod för att välja svårighetsgrad
def valj_svarighetsgrad(huvudfonster, standard="NORMAL"):
    
    resultat = {"val": standard}

    dialog = tk.Toplevel(huvudfonster)
    dialog.title("Svårighetsgrad")
    dialog.resizable(False, False)

    tk.Label(dialog, text="Skriv LÄTT, NORMAL eller SVÅR (L/N/S går också).").pack(
        padx=12, pady=(12, 6), anchor="w"
    )
    #Låt spelaren mata in 
    inmatning = tk.Entry(dialog, width=20)
    inmatning.insert(0, standard)
    inmatning.pack(padx=12, pady=(0, 6))
    feletikett = tk.Label(dialog, text="", fg="red")
    feletikett.pack(padx=12, pady=(0, 10), anchor="w")

    #Metod för att skriva in 
    def forsok_stanga():
        text = inmatning.get().strip().upper()
        if text == "":
            resultat["val"] = standard
            dialog.destroy()
            return
        if text in ("LÄTT", "L"):
            resultat["val"] = "LÄTT"
        elif text in ("NORMAL", "N"):
            resultat["val"] = "NORMAL"
        elif text in ("SVÅR", "S"):
            resultat["val"] = "SVÅR"
        else:
            feletikett.config(text="Ogiltigt. Skriv LÄTT, NORMAL eller SVÅR.")
            inmatning.focus_set()
            return
        dialog.destroy()

    

    knapprad = tk.Frame(dialog)
    knapprad.pack(pady=(0, 12))
    tk.Button(knapprad, text="OK", command=forsok_stanga).pack(side="left", padx=6)

    inmatning.bind("<Return>", lambda e: forsok_stanga())

    #pop-up-dialog som måste stängas innan spelet fortsätter
    dialog.transient(huvudfonster)
    dialog.grab_set()
    inmatning.focus_set()
    huvudfonster.wait_window(dialog)

    return resultat["val"]

        


def main():
    #Startar huvudfönster
    huvudfonster = tk.Tk()

    #Fråga svårighetsgrad 
    vald_svarighetsgrad = valj_svarighetsgrad(huvudfonster, standard="NORMAL")

    #Sätt Wumpus-rörelsesannolikhet för NORMAL-läget
    if vald_svarighetsgrad == "LÄTT":
        sannolikhet_norm = 0.0
    elif vald_svarighetsgrad == "SVÅR":
        sannolikhet_norm = 1.0
    else:  #"NORMAL"
        sannolikhet_norm = 0.30

    #Skapa GUI-applikationen med valda parametrar
    app = WhumpusGUI(
        huvudfonster,
        kartfil="karta.txt",
        andel_hal=0.20,
        andel_fladder=0.30,
        sannolikhet_norm=sannolikhet_norm,
        antal_pilar=5,
        svarighetsgrad=vald_svarighetsgrad
    )

    #Kör Tkinter-loop
    huvudfonster.mainloop()




if __name__ == "__main__":
    main()

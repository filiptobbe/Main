#Skapar klassen "Rum" som representerar ett rum i kartan
class Rum:
    #Klasskonstanter
    GILTIGA_RIKTNINGAR = ("N", "O", "S", "V")
    FARA_TOM = "TOM"
    FARA_HAL = "HAL"
    FARA_FLADDERMUS = "FLADDERMUS"
    FARA_WUMPUS = "WUMPUS"
    TILLATNA_FAROR = {FARA_TOM, FARA_HAL, FARA_FLADDERMUS, FARA_WUMPUS}

    #Skapar instansvariablerna
    def __init__(self, rumsnummer, norr, oster, soder, vaster, fara=None):
        self.rumsnummer = rumsnummer
        self.norr = norr
        self.oster = oster
        self.soder = soder
        self.vaster = vaster

        #Sätter faran om den är tillåten, annars blir rummet tomt
        if fara in Rum.TILLATNA_FAROR:
            self.fara = fara
        else:
            self.fara = Rum.FARA_TOM

    #Metod som hämtar rumsnumret i riktningen användaren anger
    #Returnerar rumsnumret eller None om riktningen är ogiltig
    def hamta_granne(self, riktning):
        riktning = str(riktning).upper().strip()
        if riktning == "N":
            return self.norr
        elif riktning == "O":
            return self.oster
        elif riktning == "S":
            return self.soder
        elif riktning == "V":
            return self.vaster
        else:
            return None

    #Metod som returnerar en dictionary med alla grannar {'N': nrum, 'O': orum, 'S': srum, 'V': vrum}
    def hamta_grannar(self):
        return {"N": self.norr, "O": self.oster, "S": self.soder, "V": self.vaster}

    #Metod som placerar en fara i rummet (den valideras)
    #Returnerar True om det gick bra, annars False
    def satt_fara(self, ny_fara):
        if ny_fara in Rum.TILLATNA_FAROR:
            self.fara = ny_fara
            return True
        else:
            return False

    #Metod som returnerar True om rummet är tomt, alltså saknar faror
    def ar_tomt(self):
        return self.fara == Rum.FARA_TOM

    #Metod som returnerar True om rummet har just den faran
    def har_fara(self, faratyp):
        return self.fara == faratyp

    #Output
    def __str__(self):
        return (f"Rum {self.rumsnummer}: N={self.norr} O={self.oster} "
                f"S={self.soder} V={self.vaster} Fara={self.fara}")

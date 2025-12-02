#Gammal kod från main
#Importerar konstanter från rum och inställningar
"""
from rum import Rum, FARA_TOM, FARA_HAL, FARA_FLADDERMUS, FARA_WUMPUS, GILTIGA_RIKTNINGAR
from installningar import (
    KARTFIL, AVGRANSARE_STANDARD,
    ANTAL_STARTPILAR, ANDEL_HAL_STANDARD, ANDEL_FLADDERMUS_STANDARD,
    SVARIGHET_LATT, SVARIGHET_NORMAL, SVARIGHET_SVAR,
    SANNOLIKHET_WUMPUS_GAR_NORMAL,
)"""


#Definierar konstanter som används i klassen Rum
GILTIGA_RIKTNINGAR = ("N", "O", "S", "V")
FARA_TOM = "TOM"
FARA_HAL = "HAL"
FARA_FLADDERMUS = "FLADDERMUS"
FARA_WUMPUS = "WUMPUS"
TILLATNA_FAROR = {FARA_TOM, FARA_HAL, FARA_FLADDERMUS, FARA_WUMPUS}

#Skapar klassen "Rum" som representerar ett rum i kartan
class Rum:

    #Skapar instansvariablerna
    def __init__(self, rumsnummer: int, norr: int, oster: int, soder: int, vaster: int,
                 fara: str = FARA_TOM):
        #Felhantering: typkontroll för int-värden
        for namn, varde in [("rumsnummer", rumsnummer), ("norr", norr),
                        ("oster", oster), ("soder", soder), ("vaster", vaster)]:
            if not isinstance(varde, int):
                raise TypeError(f"{namn} ska vara int, inte {type(varde).__name__}")

        self.rumsnummer = rumsnummer
        self.norr = norr
        self.oster = oster
        self.soder = soder
        self.vaster = vaster

        if fara not in TILLATNA_FAROR:
            raise ValueError(f"Ogiltig fara '{fara}' i rum {rumsnummer}.")
        self.fara = fara

    #Skapar metoder

    #Metod som hämtar rumsnumret i riktingen användaren anger
    def hamta_granne(self, riktning: str) -> int:
        #Felhantering: typkontroll för riktning
        if not isinstance(riktning, str):
            raise TypeError("riktning ska vara en sträng: 'N', 'O', 'S' eller 'V'.")

        riktning = riktning.upper().strip()
        
        #Felhantering: validerar rikting
        if riktning not in GILTIGA_RIKTNINGAR:
            raise ValueError(f"Ogiltig riktning '{riktning}'. Tillåtna: {GILTIGA_RIKTNINGAR}")
        return {
            "N": self.norr,
            "O": self.oster,
            "S": self.soder,
            "V": self.vaster,
        }[riktning]

    #Metod som retunerar en dictonary med alla grannar {'N': nrum, 'O': orum, 'S': srum, 'V': vrum}
    def hamta_grannar(self) -> dict:
        return {
            "N": self.norr,
            "O": self.oster,
            "S": self.soder,
            "V": self.vaster,
        }

    #Metod som placerar en fara i rummet (den valideras)
    def satt_fara(self, ny_fara: str) -> None:
        if ny_fara not in TILLATNA_FAROR:
            raise ValueError(f"Ogiltig fara '{ny_fara}'. Tillåtna: {TILLATNA_FAROR}")
        self.fara = ny_fara

    #Metod som retunerar "True" om rummet är tomt, alltså saknar faror
    def ar_tomt(self) -> bool:
        return self.fara == FARA_TOM

    #Metod som returnerar "True" om rummet har just den faran
    def har_fara(self, faratyp: str) -> bool:
        return self.fara == faratyp

    #Output
    def __str__(self) -> str:
        return (f"Rum {self.rumsnummer}: N={self.norr} O={self.oster} "
                f"S={self.soder} V={self.vaster} Fara={self.fara}")


#Testar klasserna
rum = Rum(1, 2, 3, 4, 5, FARA_HAL)
print(rum)
print(rum.hamta_granne("N"))
#print(rum.hamta_granne("X"))  # Ger False och skriver ut fel
print(rum.satt_fara("FLADDERMUS"))
print(rum)
#print(rum.satt_fara("LAVA"))  # Ger False och skriver ut fel

"""
Representerar speltillståndet i Wumpus-spelet

Parametrar (till __init__):
    spelarens_rum (int): Rummet där spelaren befinner sig i början av spelet.
    wumpus_rum (int): Rummet där Wumpus befinner sig i början av spelet.
    antal_pilar (int): Antalet pilar spelaren har tillgängliga.
    svarighetsgrad (str | int): Anger spelets svårighetsgrad (t.ex. "lätt", "medel", "svår" eller motsvarande kod).

Attribut:
    spelarens_rum (int): Håller nuvarande rum där spelaren befinner sig.
    wumpus_rum (int): Håller nuvarande rum där Wumpus befinner sig.
    antal_pilar (int): Håller nuvarande antal pilar spelaren har kvar.
    svarighetsgrad (str | int): Spelets svårighetsgrad.

Klassen används för att lagra och uppdatera spelets tillstånd.
    """
class Speltillstand:

    #Skapar instansvariablerna
    def __init__(self, spelarens_rum, wumpus_rum, antal_pilar, svarighetsgrad):
        self.spelarens_rum = spelarens_rum
        self.wumpus_rum = wumpus_rum
        self.antal_pilar = antal_pilar
        self.svarighetsgrad = svarighetsgrad

    #Metod som uppdaterar var någonstans Wumpus är
    #Tar bort gammal markering och sätter ny i rum_lista
    def uppdatera_wumpus_plats(self, rum_lista, nytt_rum):
        from rum import Rum
        #Ta bort gammal plats
        gammalt_rum = self.wumpus_rum
        if rum_lista[gammalt_rum].fara == Rum.FARA_WUMPUS:
            rum_lista[gammalt_rum].fara = Rum.FARA_TOM
        #Sätt ny plats
        self.wumpus_rum = nytt_rum
        rum_lista[nytt_rum].fara = Rum.FARA_WUMPUS

    #Metod som minskar antalet pilar med 1
    #Returnerar True om en pil fanns att ta bort, annars False
    def minska_pilar(self):
        if self.antal_pilar > 0:
            self.antal_pilar -= 1
            return True
        return False

    #Metod som returnerar True om spelaren har pilar kvar
    def har_pilar_kvar(self):
        return self.antal_pilar > 0

    #Output
    def __str__(self):
        return ("Spelare i rum " + str(self.spelarens_rum) +
                ", Wumpus i rum " + str(self.wumpus_rum) +
                ", Pilar: " + str(self.antal_pilar) +
                ", Svårighetsgrad: " + str(self.svarighetsgrad))

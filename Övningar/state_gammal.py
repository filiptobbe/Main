from dataclasses import dataclass, field
import random

#Importerar konstanter från spelinställningarna
from settings import ANTAL_STARTPILAR, SVARIGHET_NORMAL

#En klass för speltillståndet som upptaterar
@dataclass
class Speltillstand:
    spelarens_rum: int
    wumpus_rum: int
    antal_pilar: int = ANTAL_STARTPILAR
    svarighetsgrad: str = SVARIGHET_NORMAL # Gör variabel?
    slumpgenerator: random.Random = field(default_factory=random.Random)

    #Metod som uppdaterar var någonstans Wumpus befinner sig 
    def uppdatera_wumpus_plats(self, rum_lista, nytt_rum: int) -> None:
        
        from rum import FARA_WUMPUS, FARA_TOM
        #Ta bort gammal plats
        gammalt_rum = self.wumpus_rum
        if rum_lista[gammalt_rum].fara == FARA_WUMPUS:
            rum_lista[gammalt_rum].fara = FARA_TOM
        #Sätt ny plats
        self.wumpus_rum = nytt_rum
        rum_lista[nytt_rum].fara = FARA_WUMPUS

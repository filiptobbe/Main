#Spelinställningar
class Installningar:
    def __init__(self,
                 kartfil="karta.txt",
                 avgransare=';',
                 antal_startpilar=5,
                 andel_hal=0.20,
                 andel_fladdermus=0.30,
                 svarighet_default="NORMAL",
                 sannolikhet_wumpus_gar_normal=0.30):
        self.kartfil = kartfil
        self.avgransare = avgransare
        self.antal_startpilar = antal_startpilar
        self.andel_hal = andel_hal
        self.andel_fladdermus = andel_fladdermus
        self.svarighet_default = svarighet_default
        self.sannolikhet_wumpus_gar_normal = sannolikhet_wumpus_gar_normal

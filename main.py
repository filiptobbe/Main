#Importerar klasser och random
import random
from rum import Rum
from speltillstand import Speltillstand

#Inläsning och validering

#Läser filen
def las_karta_fran_fil(filnamn):
    rum_lista = []
    try:
        with open(filnamn, encoding="utf-8") as fil:
            #Dela upp varje rad i fyra delar för varje väderstreck
            for rumsnummer, rad in enumerate(fil):
                rad = rad.strip()
                if rad == "" or rad.startswith("#"):
                    continue
                delar = rad.split(";")

                #Gör om till integers och lägger in i vår lista med rum
                norr, oster, soder, vaster = map(int, delar)
                rum_lista.append(Rum(rumsnummer, norr, oster, soder, vaster))

    except FileNotFoundError:
        print("Hittar inte filen:", filnamn)
        return None

    #Validera grannar
    antal_rum = len(rum_lista)
    for rum in rum_lista:
        for granne in (rum.norr, rum.oster, rum.soder, rum.vaster):
            if granne < 0 or granne >= antal_rum:
                print("Ogiltigt grannrum", granne, "i rum", rum.rumsnummer)
                return None
    return rum_lista

#Hjälpfunktion - Kontrollerar om grannrummen innehåller en viss fara
def har_granne_fara(rum_lista, rumsnummer, fara):
    rum = rum_lista[rumsnummer]
    for granne in rum.hamta_grannar().values():
        if 0 <= granne < len(rum_lista) and rum_lista[granne].fara == fara:
            return True
    return False


#Slump och placering

#Slumpa ut rum (av de tomma rummen)
def slumpa_tomt_rum(rum_lista, slumpgenerator, forbjudna=frozenset()):
    mojliga_rum = []
    #Slumpar ut alla tomma rum (ej Whumpus/fladdermöss/hål)
    for index, rum in enumerate(rum_lista):
        if rum.fara == Rum.FARA_TOM and index not in forbjudna:
            mojliga_rum.append(index)
    
    return slumpgenerator.choice(mojliga_rum)

#Slumpar ut faror i rum och returnerar var de hamnar utan att krocka. Undviker spelarens startrum
def slumpa_faror(rum_lista, slumpgenerator, andel_hal, andel_fladdermus, forbjudna_start=frozenset()):
    #Nollställ
    for rum in rum_lista:
        rum.fara = Rum.FARA_TOM

    antal_rum = len(rum_lista)
    antal_hal = int(andel_hal * antal_rum)
    antal_fladder = int(andel_fladdermus * antal_rum)

    forbjudna = set(forbjudna_start)
    hal_rum = set()
    fladdermus_rum = set()

    #Wumpus
    wumpus_rum = slumpa_tomt_rum(rum_lista, slumpgenerator, forbjudna)
    #Placerar ut Wumpus (kollar först att det går)
    if wumpus_rum is None:
        print("Kunde inte placera Wumpus.")
        return None
    forbjudna.add(wumpus_rum)
    rum_lista[wumpus_rum].fara = Rum.FARA_WUMPUS

    #Hål
    for i in range(antal_hal):
        valt = slumpa_tomt_rum(rum_lista, slumpgenerator, forbjudna)
        if valt is None:
            print("Kunde inte placera fler avgrundshål.")
            break
        hal_rum.add(valt)
        forbjudna.add(valt)
        rum_lista[valt].fara = Rum.FARA_HAL

    #Fladdermöss
    for i in range(antal_fladder):
        valt = slumpa_tomt_rum(rum_lista, slumpgenerator, forbjudna)
        if valt is None:
            print("Kunde inte placera fler fladdermöss.")
            break
        fladdermus_rum.add(valt)
        forbjudna.add(valt)
        rum_lista[valt].fara = Rum.FARA_FLADDERMUS

    return wumpus_rum


#Visning

#Skriver ut grannar
def visa_grannar(rum_lista, rumsnummer):
    granne = rum_lista[rumsnummer].hamta_grannar()
    print("Härifrån kan man komma till följande rum:", granne["N"], granne["O"], granne["S"], granne["V"])

#Kontrollerar om grannrummen innehåller faror och "varnar"
def visa_sinnen(rum_lista, rumsnummer):
    har_hal = har_granne_fara(rum_lista, rumsnummer, Rum.FARA_HAL)
    har_wumpus = har_granne_fara(rum_lista, rumsnummer, Rum.FARA_WUMPUS)
    har_fladdermus = har_granne_fara(rum_lista, rumsnummer, Rum.FARA_FLADDERMUS)

    if har_fladdermus:
        print("Du hör fladdermöss!")
    if har_wumpus:
        print("Du känner lukten av Wumpus!")
    if har_hal:
        print("Du känner vinddrag!")


#Inmatning (felkontroll)

#Giltigt val: (F/S) för val av förflyttning eller skjuta
def ar_giltig_handling(text):
    return isinstance(text, str) and text.strip().upper() in ("F", "S")

#Giltigt val av riktning
def ar_giltig_riktning(text):
    return isinstance(text, str) and text.strip().upper() in Rum.GILTIGA_RIKTNINGAR

#Användaren matar in vad den vill göra (skjuta eller förflytta sig)
def fraga_handling():
    while True:
        svar = input("Vill du förflytta dig eller skjuta (F/S)? ").strip().upper()
        if ar_giltig_handling(svar):
            return svar
        print("Ogiltigt val. Skriv F eller S.")

#Frågar användaren om riktning, och validerar att det fungerar
def fraga_riktning(rum_lista, rumsnummer):
    while True:
        svar = input("Vilken riktning (N, O, S, V)? ").strip().upper()
        if not ar_giltig_riktning(svar):
            print("Ogiltig riktning. Skriv N, O, S eller V.")
            continue
        granne = rum_lista[rumsnummer].hamta_granne(svar)
        if granne is None:
            print("Den riktningen går inte från det här rummet. Försök igen.")
            continue
        return svar

#Inmatning riktning på pilarna
def fraga_tre_riktningar(rum_lista, rumsnummer):
    riktningar = []
    for i in range(3):
        etikett = ["första", "andra", "tredje"][i]
        while True:
            svar = input("Pilen lämnar " + etikett + " rummet. Vilken riktning (N, O, S, V)? ").strip().upper()
            if not ar_giltig_riktning(svar):
                print("Ogiltig riktning. Skriv N, O, S eller V.")
                continue
            granne = rum_lista[rumsnummer].hamta_granne(svar)
            if granne is None:
                print("Den riktningen går inte från det här rummet. Försök igen.")
                continue
            riktningar.append(svar)
            #Uppdaterar nuvarande rum till grannrummet, så att nästa steg valideras från rätt position
            rumsnummer = granne
            break
    return riktningar

#Inmatning välj svårighetsgrad
def valj_svarighetsgrad(standard):
    tillatna = ("LÄTT", "NORMAL", "SVÅR")
    while True:
        svar = input("Välj svårighetsgrad (LÄTT/NORMAL/SVÅR) [Enter för " + standard + "]: ").strip().upper()
        if svar == "":
            return standard
        if svar in tillatna:
            return svar
        print("Ogiltigt val. Skriv LÄTT, NORMAL eller SVÅR (eller bara Enter).")


#Funktioner för spellogiken

#Spelaren förflyttas 
def flytta_spelare(rum_lista, spelarens_rum, riktning):
    granne = rum_lista[spelarens_rum].hamta_granne(riktning)
    if granne is None:
        print("Ogiltig riktning. Försök igen.")
        return spelarens_rum, "OK"

    nytt_rum = granne
    fara = rum_lista[nytt_rum].fara

    #Kollar efter faror och retunerar rätt "tillstånd"
    if fara == Rum.FARA_WUMPUS:
        return nytt_rum, "DOD_WUMPUS"
    elif fara == Rum.FARA_HAL:
        return nytt_rum, "DOD_HAL"
    elif fara == Rum.FARA_FLADDERMUS:
        return nytt_rum, "FLADDERMUS"
    else:
        return nytt_rum, "OK"

#Funktion för förflyttning när du kliver in i ett rum med fladdermöss
def teleportera_vid_fladdermoss(rum_lista, slumpgenerator):
    nytt = slumpa_tomt_rum(rum_lista, slumpgenerator)
    if nytt is None:
        print("Fladdermössen hittar inget tomt rum att släppa dig i.")
        return None
    print("Du känner fladdermusvingar mot kinden och lyfts uppåt")
    print("Efter en kort flygtur släpper fladdermössen ner dig i rum", nytt)
    return nytt

#Skjuter pilarna (3 st)
def skjut_pil(rum_lista, start_rum, riktningar):
    nuvarande = start_rum
    etiketter = ["första", "andra", "tredje"]

    for i in range(3):
        print("Pilen lämnar", etiketter[i], "rummet.")
        if i >= len(riktningar):
            print("Ingen riktning angavs - pilen missar.")
            return "MISS"

        riktning = str(riktningar[i]).strip().upper()
        granne = rum_lista[nuvarande].hamta_granne(riktning)
        if granne is None:
            print("Ogiltig riktningssekvens - pilen missar.")
            return "MISS"

        nuvarande = granne

        #Träffar Wumpus när som helst -> vinst direkt
        if rum_lista[nuvarande].fara == Rum.FARA_WUMPUS:
            return "TRAFF"

    #Självträff kollas först efter tre steg
    if nuvarande == start_rum:
        return "SJALVTRAFF"

    return "MISS"


#Whumpus rörelse

#Avgör om rummen intill är tomma
def tomma_grannar(rum_lista, rumsnummer):
    resultat = []
    lista_grannar = rum_lista[rumsnummer].hamta_grannar()
    for kod, granne in lista_grannar.items():
        if 0 <= granne < len(rum_lista) and rum_lista[granne].fara == Rum.FARA_TOM:
            resultat.append(granne)
    return resultat

#Slumpa en tom granne 
def slumpa_tomt_granne(rum_lista, rumsnummer, slumpgenerator):
    kandidater = tomma_grannar(rum_lista, rumsnummer)
    if not kandidater:
        return rumsnummer  #står still om inga tomma grannar
    return slumpgenerator.choice(kandidater)


def wumpus_ror_sig(rum_lista, spel, sannolikhet_wumpus_gar_normal, slumpgenerator):
    nu = spel.wumpus_rum
    spelarrum = spel.spelarens_rum

    #Mängder av grannar för Wumpus respektive spelaren
    w_grannar = set(rum_lista[nu].hamta_grannar().values())
    s_grannar = set(rum_lista[spelarrum].hamta_grannar().values())

    #Logik för olika svårighetsgrader
    if spel.svarighetsgrad == "LÄTT":
        nytt = nu  #står still

    elif spel.svarighetsgrad == "NORMAL":
        #Gå ibland (enligt sannolikhet), annars stå still
        if slumpgenerator.random() >= sannolikhet_wumpus_gar_normal:
            nytt = nu
        else:
            #1) Om spelaren är granne, gå in i spelarens rum
            if spelarrum in w_grannar:
                nytt = spelarrum
            else:
                #2) Försök ta ett steg mot spelaren: granne som också är granne till spelaren och är TOM
                mot_kandidater = [g for g in w_grannar if g in s_grannar and rum_lista[g].fara == Rum.FARA_TOM]
                if mot_kandidater:
                    nytt = slumpgenerator.choice(mot_kandidater)
                else:
                    #3) Annars valfri TOM granne
                    nytt = slumpa_tomt_granne(rum_lista, nu, slumpgenerator)



    else:  #"SVÅR" - rör sig varje tur
        if spelarrum in w_grannar:
            nytt = spelarrum
        else:
            mot_kandidater = [g for g in w_grannar if g in s_grannar and rum_lista[g].fara == Rum.FARA_TOM]
            nytt = slumpgenerator.choice(mot_kandidater) if mot_kandidater else slumpa_tomt_granne(rum_lista, nu, slumpgenerator)


    #Uppdatera plats (markerar rummen korrekt)
    spel.uppdatera_wumpus_plats(rum_lista, nytt)

    if spel.wumpus_rum == spel.spelarens_rum:
        return "SPELARE_UPPATEN"
    return None


#Huvudspelet

def main():
    #Spelinställningar
    andel_hal = 0.20
    andel_fladdermus = 0.30
    svarighet_default = "NORMAL"
    sannolikhet_wumpus_gar_normal = 0.30

    slump = random.Random()

    #Läs karta
    rum_lista = las_karta_fran_fil("karta.txt")
    if rum_lista is None:
        return
    print("Antal rum i kartan:", len(rum_lista))

    #Välj spelarens start bland tomma rum (alla är tomma nu)
    spelarens_rum = slump.choice(list(range(len(rum_lista))))

    #Slumpa faror - undvik spelarens start
    wumpus_rum = slumpa_faror(
    rum_lista, slump, andel_hal, andel_fladdermus, forbjudna_start={spelarens_rum}
    )

    if wumpus_rum is None:
        return

    #Fråga och sätt svårighetsgrad
    svarighetsgrad = valj_svarighetsgrad(svarighet_default)

    #Sätt antal pilar och skapa speltillstånd
    spel = Speltillstand(
        spelarens_rum=spelarens_rum,
        wumpus_rum=wumpus_rum,
        antal_pilar=5,
        svarighetsgrad=svarighetsgrad
    )

    print("\nSpelet börjar!")
    print("Spelaren startar i rum:", spel.spelarens_rum)
    print("Wumpus startar i rum:", spel.wumpus_rum)
    print()

    #Spelloop
    while True:
        #Visa sinnen
        visa_sinnen(rum_lista, spel.spelarens_rum)

        #Visa grannar
        visa_grannar(rum_lista, spel.spelarens_rum)

        #Slut om pilarna tagit slut
        if not spel.har_pilar_kvar():
            print("Pilarna är slut. Du förlorar!")
            break

        #Fråga vad användaren vill göra
        handling = fraga_handling()

        if handling == "F":
            #Förflyttning
            riktning = fraga_riktning(rum_lista, spel.spelarens_rum)
            nytt_rum, utfall = flytta_spelare(rum_lista, spel.spelarens_rum, riktning)

            spel.spelarens_rum = nytt_rum

            #Se vad som händer med spelaren
            if utfall == "DOD_HAL":
                print("Du klev just ner i ett bottenlöst hål.")
                print("Game Over!")
                break
            elif utfall == "DOD_WUMPUS":
                print("Du gick in i Wumpus rum och blev uppäten.")
                print("Game Over!")
                break

            #Om fladdermöss i rummet, teleporterar spelaren till nytt rum (ett tomt rum)
            elif utfall == "FLADDERMUS":
                tele = teleportera_vid_fladdermoss(rum_lista, slump)
                if tele is not None:
                    spel.spelarens_rum = tele

        #Annars om spelaren vill skjuta
        else:
            #Fråga riktning och se var pilen hamnar
            riktningar = fraga_tre_riktningar(rum_lista, spel.spelarens_rum)
            resultat = skjut_pil(rum_lista, start_rum=spel.spelarens_rum, riktningar=riktningar)
            
            #Om användaren träffar
            if resultat == "TRAFF":
                print("Du dödade Wumpus! Du vinner!")
                break

            #Om självträff
            elif resultat == "SJALVTRAFF":
                print("Aj! Pilen kom tillbaka - självträff. Du dör.")
                print("Game Over!")
                break
            #Annars miss
            else:
                spel.minska_pilar()
                print("Miss. Pilar kvar:", spel.antal_pilar)

        #Wumpus rör sig enligt svårighetsgrad
        mote = wumpus_ror_sig(rum_lista, spel, sannolikhet_wumpus_gar_normal, slump)
        if mote == "SPELARE_UPPATEN":
            print("Wumpus vandrade in i ditt rum - du blev uppäten.")
            print("Game Over!")
            break

    #Avslut
    print("\nTack för att du spelade!")

if __name__ == "__main__":
    main()

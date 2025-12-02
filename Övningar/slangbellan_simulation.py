import random

def simulate_slangbella(n_games=100000, p_hit=0.4, price=20, prize=100):
    """
    n_games : antal simulerade spel
    p_hit   : sannolikhet att träffa med ett skott
    price   : kostnad per spel
    prize   : vinst om du klarar spelet (minst 2 träffar)
    """
    wins = 0
    net_sum = 0.0

    # loopar över spel
    for i in range(n_games):
        hits = 0  # antal träffar i spel i

        # 3 skott per spel
        for j in range(3):
            u = random.random()          # slumptal i [0,1)
            if u < p_hit:                # träff med sannolikhet p_hit
                hits += 1

        # kolla om spelet blev vinst eller förlust
        if hits >= 2:
            wins += 1
            net_sum += (prize - price)
        else:
            net_sum -= price

    # uppskattad sannolikhet att vinna
    p_win = wins / n_games

    # förväntat netto per spel
    expected_net = net_sum / n_games

    return p_win, expected_net


if __name__ == "__main__":
    # Ändra dessa efter dina riktiga data från Gröna Lund
    p_hit = 0.3       # ex: träffar / skott du faktiskt skjutit
    n_games = 10
    price = 40        # verkligt pris per spel --> Skriv in
    prize = 100       # verklig vinst --> Skriv in 

    p_win, expected_net = simulate_slangbella(n_games, p_hit, price, prize)

    print(f"Antal simuleringar: {n_games}")
    print(f"Träff-sannolikhet p: {p_hit}")
    print(f"Uppskattad sannolikhet att vinna: {p_win:.4f}")
    print(f"Förväntat netto per spel: {expected_net:.2f} kr")

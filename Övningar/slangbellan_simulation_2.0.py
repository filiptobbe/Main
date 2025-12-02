import random

def simulate_slangbella(n_games, p_hit=0.3, price=40, prize=100):
    wins = 0
    net_sum = 0.0

    for i in range(n_games):
        hits = 0

        # 3 skott per spel
        for j in range(3):
            u = random.random()  # slumptal i [0,1)
            if u < p_hit:
                hits += 1

        # vinst om minst 2 träffar
        if hits >= 2:
            wins += 1
            net_sum += (prize - price)
        else:
            net_sum -= price

    p_win = wins / n_games
    expected_net = net_sum / n_games
    return p_win, expected_net


if __name__ == "__main__":
    p_hit = 0.3       # ändra till din uppmätta sannolikhet
    price = 40        # verkligt pris
    prize = 100       # uppskattat värde på vinsten

    for n_games in [1, 10, 100, 1000, 100000]:
        p_win, expected_net = simulate_slangbella(n_games, p_hit, price, prize)
        print(f"Antal simuleringar: {n_games}")
        print(f"Uppskattad sannolikhet att vinna: {p_win:.4f}")
        print(f"Genomsnittligt netto per spel: {expected_net:.2f} kr")
        print("-" * 40)

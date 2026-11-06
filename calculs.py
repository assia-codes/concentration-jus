def calculer(m0=1000, x0=0.10, residus=20, mR=100, xR=0.40,
             Cp=3.8, T2=20, T3=80, x4=0.40, lambda_v=2300,
             T4=80, T5=25):
    # 1. Filtration
    m1 = m0 - residus
    x1 = m0 * x0 / m1

    # 2. Mélange
    m2 = m1 + mR
    x2 = (m1 * x1 + mR * xR) / m2

    # 3. Chauffage
    Q3 = m2 * Cp * (T3 - T2) / 3600

    # 4. Évaporation
    m4 = m2 * x2 / x4
    mv = m2 - m4
    Q4 = mv * lambda_v / 3600

    # 5. Refroidissement
    Q5 = m4 * Cp * (T4 - T5) / 3600

    # Vérification du bilan global
    erreur = (m0 + mR) - (residus + mv + m4)

    return {
        "m1": m1, "x1": x1 * 100,
        "m2": m2, "x2": x2 * 100,
        "Q3": Q3, "m4": m4, "mv": mv,
        "Q4": Q4, "Q5": Q5, "erreur": erreur,
    }


if __name__ == "__main__":
    for nom, valeur in calculer().items():
        print(nom, ":", round(valeur, 2))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import numpy as np
import os

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def afficher_prix_ligne_par_ligne(url_produit):
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # garder visible pour que JS charge bien

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url_produit)

        # Attendre que la table-body soit présente
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.table-body"))
        )

        # Récupération du nom et extension FR
        try:
            h1_element = driver.find_element(By.CSS_SELECTOR, "div.page-title-container h1")
            span_element = h1_element.find_element(By.TAG_NAME, "span")

            # Nom FR → texte avant le span
            nom_fr = h1_element.text.replace(span_element.text, "").strip()

            # Extension FR → nettoyer "- Cartes -" ou variantes
            extension_fr = re.sub(r'\s*-\s*Cartes\s*-?\s*', '', span_element.text).strip()

            # Affichage avec couleur et style ANSI
            print(f"\nNom de la carte : \033[1;32m{nom_fr}\033[0m")      # vert + gras
            print(f"Extension : \033[3;33m{extension_fr}\033[0m")        # jaune + italique
        except:
            print("\nNom ou extension indisponible")

        # Récupération des prix
        lignes = driver.find_elements(By.CSS_SELECTOR, "div.table-body > div[id^='articleRow']")
        if not lignes:
            print("Aucune offre trouvée sur cette page.")
            return

        prix_list = []
        print("\n🔥 Prix des offres FR :\n")
        for i, ligne in enumerate(lignes, start=1):
            try:
                prix_text = ligne.find_element(By.CSS_SELECTOR, "div.col-offer.col-auto").text.strip()
                prix_text = re.sub(r"[^\d,]", "", prix_text).replace(",", ".")
                prix = float(prix_text)
                prix_list.append(prix)
                print(f"{i:2d}. {prix:.2f} €")
            except:
                continue

        if prix_list:
            moyenne = sum(prix_list) / len(prix_list)
            print(f"\n⭐ Moyenne des offres FR : {moyenne:.2f} €")

            # Prix conseillé (20-80 percentile pour éviter extrêmes)
            bas, haut = np.percentile(prix_list, [20, 80])
            prix_conseilles = [p for p in prix_list if bas <= p <= haut]
            if prix_conseilles:
                prix_recommande = sum(prix_conseilles) / len(prix_conseilles)
                print(f"💰 Prix conseillé : {prix_recommande:.2f} € (hors extrêmes)")
            else:
                print("💰 Prix conseillé : impossible de calculer (tous les prix sont extrêmes)")
        else:
            print("Aucun prix valide trouvé.")

    finally:
        driver.quit()


def menu():
    while True:
        clear_terminal()
        print("\n🎴================================🎴")
        print("         \033[1;36mCARDMARKET SCRAPER\033[0m")
        print("🎴================================🎴\n")
        print("1️⃣  🔍  Chercher une carte par URL")
        print("2️⃣  🚪  Quitter\n")
        print("🎴================================🎴")

        choix = input("👉 Choisissez une option (1-2) : ").strip()

        if choix == "1":
            url = input("\n🔗 Entrez l'URL de la page produit : ").strip()
            afficher_prix_ligne_par_ligne(url)
            input("\n🔁 Appuyez sur Entrée pour revenir au menu...")
        elif choix == "2":
            print("\n👋 Merci d'avoir utilisé le scraper, à bientôt !")
            break
        else:
            print("\n⚠️  Option invalide, veuillez réessayer.\n")


if __name__ == "__main__":
    menu()


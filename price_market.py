from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from collections import Counter
import re
import numpy as np
import os
import time

# ------------------------------------------ PARSING INPUT - REGEX ------------------------------------------ #

def url_valide(url: str) -> bool:
    # Vérifie que l’URL ne contient pas de "?" ou "&"
    pattern = r"^https:\/\/www\.cardmarket\.com\/[a-z]{2}\/Magic\/Products\/Singles\/[A-Za-z0-9\-\_\/]+$"
    return re.match(pattern, url) is not None

# ------------------------------------------ CLEAR TERMINAL ------------------------------------------ #

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

# ------------------------------------------ WEB PAGE MANAGEMENT ------------------------------------------ #

def close_cookie_banner(driver):
    """Ferme les bandeaux cookies les plus courants (FR/EN)."""
    try:
        candidates = [
            (By.ID, "onetrust-accept-btn-handler"),
            (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"),
            (By.XPATH, "//button[contains(., 'Tout accepter') or contains(., 'Accepter') or contains(., 'Accept all') or contains(., 'Accept')]"),
        ]
        for by, sel in candidates:
            elems = driver.find_elements(by, sel)
            if elems:
                driver.execute_script("arguments[0].click();", elems[0])
                time.sleep(0.5)
                break
    except Exception:
        pass

# ------------------------------------------ LOADING PART ------------------------------------------ #

def load_all_offers(driver, max_cycles=40):
    """
    Scroll jusqu'en bas et clique sur 'Show more results' tant que possible.
    """
    last_count = 0
    stagnant = 0
    for _ in range(max_cycles):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.7)

        # Tente de cliquer sur le bouton si visible
        try:
            btn = driver.find_element(By.ID, "loadMoreButton")
            style = (btn.get_attribute("style") or "").lower()
            disabled = btn.get_attribute("disabled")
            if ("display: none" not in style) and (disabled is None):
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(0.9)
        except Exception:
            pass

        # Compte les lignes actuellement chargées
        try:
            rows = driver.find_elements(By.CSS_SELECTOR, "div.table-body > div[id^='articleRow']")
            cur = len(rows)
        except StaleElementReferenceException:
            time.sleep(0.3)
            rows = driver.find_elements(By.CSS_SELECTOR, "div.table-body > div[id^='articleRow']")
            cur = len(rows)

        if cur > last_count:
            last_count = cur
            stagnant = 0
        else:
            stagnant += 1
            if stagnant >= 3:  # plus de nouveaux résultats après 3 cycles
                break
    return last_count

# ------------------------------------------ EXTRACTION NAME + EXTENSION ------------------------------------------ #

def get_data_cards(driver):
    try:
        h1_element = driver.find_element(By.CSS_SELECTOR, "div.page-title-container h1")
        span_element = h1_element.find_element(By.TAG_NAME, "span")

        nom = h1_element.text.replace(span_element.text, "").strip()
        extension = re.sub(r'\s*-\s*Cartes\s*-?\s*', '', span_element.text).strip()

        print(f"\nNom de la carte : \033[1;32m{nom}\033[0m")      # vert + gras
        print(f"Extension : \033[3;33m{extension}\033[0m")        # jaune + italique
    except:
        print("\nNom ou extension indisponible")

# ------------------------------------------ EXTRACTION PRICES + QUALITY ------------------------------------------ #

def get_prices(driver, language) -> list:
    lignes = driver.find_elements(By.CSS_SELECTOR, "div.table-body > div[id^='articleRow']")
    if not lignes:
        print("Aucune offre trouvée sur cette page.")
        return []

    prix_list = []
    qualite_list = []

    print(f"\n🔥 🔹 Prix des offres {language} 🔹 🔥\n")
    for i, ligne in enumerate(lignes, start=1):
        try:
            badge = ligne.find_element(By.CSS_SELECTOR, "div.product-attributes a.article-condition span.badge").text.strip()
            prix_text = ligne.find_element(By.CSS_SELECTOR, "div.col-offer.col-auto").text.strip()
            prix_text = re.sub(r"[^\d,]", "", prix_text).replace(",", ".")
            prix = float(prix_text)

            prix_list.append(prix)
            qualite_list.append(badge)

            # Affichage ligne par ligne avec qualité
            print(f"{i:2d}. {prix:.2f} € - {badge}")
        except:
            continue
    print(f"\n📊 Total d'offres récupérées : {len(prix_list)}\n")
    return prix_list

# ------------------------------------------ STATISTICS PART ------------------------------------------ #

def statistics(prix_list):
    print("===================================")
    print("📊 STATISTIQUES DES OFFRES")
    print("===================================\n")

    # Moyenne simple
    moyenne = sum(prix_list) / len(prix_list)
    print(f"⭐ Moyenne simple : {moyenne:.2f} €")
    print("   (Moyenne de tous les prix, sans pondération ni exclusion)\n")

    # Prix 'réel' = mode
    compte = Counter(prix_list)
    prix_reel = compte.most_common(1)[0][0]
    print(f"💠 Prix 'réel' (mode) : {prix_reel:.2f} €")
    print("   (Prix le plus fréquent parmi les offres)\n")

    # Prix conseillé - IQR
    q1, q3 = np.percentile(prix_list, [25, 75])
    iqr = q3 - q1
    prix_filtre = [p for p in prix_list if q1 - 1.5*iqr <= p <= q3 + 1.5*iqr]
    prix_conseille = np.mean(prix_filtre)
    print(f"💰 Prix conseillé (hors extrêmes, IQR) : {prix_conseille:.2f} €")
    print("   (Exclut les prix trop bas ou trop élevés pour refléter le marché)\n")

    print(f"📊 Nombre total d’offres analysées : {len(prix_list)}")
    print("===================================\n")

# ------------------------------------------ MAIN PROGRAM ------------------------------------------ #

def scraper(url_produit, lang):
    language = ""
    if lang == "1":
        language = "FR"
    elif lang == "2":
        language = "EN"
    elif lang == "3":
        language = "DE"

    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url_produit)
        close_cookie_banner(driver)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.table-body"))
        )

        # Charger toutes les offres
        load_all_offers(driver)

        # Récupération du nom et extension
        get_data_cards(driver)

        # Récupération des prix
        prix_list = get_prices(driver, language)

        if prix_list:
            statistics(prix_list)
        else:
            print("Aucun prix valide trouvé.")

    finally:
        driver.quit()

# ------------------------------------------ MENU PRINCIPAL ------------------------------------------ #

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
            print("\n🔗 Merci de saisir l'URL du produit SANS filtre (pas de '?language=2' etc.)")
            print("   Exemple attendu : https://www.cardmarket.com/fr/Magic/Products/Singles/The-Lord-of-the-Rings-Tales-of-Middle-earth/Nazgul\n")
            url = input("👉 Entrez l'URL du produit : ").strip()

            if not url_valide(url):
                print("\n⚠️  L’URL contient des filtres ou n’est pas valide !")
                input("🔁 Appuyez sur Entrée pour réessayer...")
                continue

            print("\n🌐 Choisissez la langue des offres :")
            print("   1️⃣  🇫🇷  Français")
            print("   2️⃣  🇬🇧  Anglais")
            print("   3️⃣  🇩🇪  Allemand")
            lang = input("\n👉 Entrez le numéro de la langue : ").strip()

            if lang == "1":
                url += "?language=2"
            elif lang == "2":
                url += "?language=1"
            elif lang == "3":
                url += "?language=3"
            else:
                print("\n⚠️ Langue invalide, utilisation par défaut : Français 🇫🇷")
                url += "?language=2"

            scraper(url, lang)
            input("\n🔁 Appuyez sur Entrée pour revenir au menu...")
        elif choix == "2":
            print("\n👋 Merci d'avoir utilisé le scraper, à bientôt !")
            break
        else:
            print("\n⚠️  Option invalide, veuillez réessayer.\n")

# ------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    menu()

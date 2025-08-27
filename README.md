# 🎴 CardMarket Scraper

Un petit outil en **Python** permettant de récupérer automatiquement les prix des cartes Magic: The Gathering sur [CardMarket](https://www.cardmarket.com/).  
Il utilise **Selenium** et **BeautifulSoup** pour extraire les offres en français et calcule un prix conseillé.

---

## ✨ Fonctionnalités

- 🔍 Recherche de cartes directement à partir de l'URL CardMarket  
- 📊 Extraction des offres disponibles (langue FR)  
- 💰 Calcul du prix moyen et du prix conseillé (hors extrêmes)  
- 🎨 Interface console simple et colorée avec menu interactif  

---

## 📦 Installation

Clone le projet et installe les dépendances nécessaires :  

```bash
git clone https://github.com/ton-pseudo/cardmarket-scraper.git
cd cardmarket-scraper
pip install -r requirements.txt
```

---

## ▶️ Utilisation

Lance le programme avec Python :  

```bash
python3 price_market.py
```

Puis navigue dans le menu :  

```
🎴================================🎴
         CARDMARKET SCRAPER
🎴================================🎴

1️⃣  Rechercher une carte par URL
2️⃣  Quitter
```

---

## 📸 Exemple de sortie

```
Nom de la carte : Anneau de Bilbo (V.1)
Extension : Le Seigneur des Anneaux : chroniques de la Terre du Milieu: Extras

🔥 Prix des offres FR :

 1. 4.00 €
 2. 4.70 €
 3. 5.00 €
 4. 5.30 €
 ...

⭐ Moyenne des offres FR : 5.47 €
💰 Prix conseillé : 5.28 € (hors extrêmes)
```

---

## ⚡️ Roadmap

- [ ] Ajout d’une recherche par **nom de carte** directement  
- [ ] Export des données en **CSV/Excel**  
- [ ] Support d’autres langues (EN, DE, etc.)  
- [ ] Mode "batch" pour scrapper plusieurs cartes  

---

## 🛠️ Technologies

- Python 3.10+  
- [Selenium](https://selenium.dev/)  
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

---

## 📜 Licence

Projet sous licence MIT – libre à vous de l'utiliser et de le modifier 🚀

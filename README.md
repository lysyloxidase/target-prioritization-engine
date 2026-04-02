# 🧬 Target Prioritization Engine

Target Prioritization Engine to narzędzie służące do systematycznej identyfikacji i wyliczania rankingów dla potencjalnych celów terapeutycznych (genów/białek) i leków w kontekście obranej choroby. 

Narzędzie buduje autorski, zbiorowy **Priority Score** używając trzech mocnych źródeł danych zewnętrznych:
1. **Open Targets Platform**: asocjacje celów i twarde dowody z bazy OpenTargets GraphQL API.
2. **Europe PMC**: skanowanie literatury medycznej (występowanie ko-cytowań genu i choroby).
3. **NCBI GEO**: wykrywanie silnych sygnałów w metadanych eksperymentów z platform (jak RNA-Seq czy mikromacierze).

Dla wygody i interaktywności aplikacja wyposażona jest w w pełni funkcjonalny, responsywny **Dashboard** (napisany w oparciu o framework Streamlit).

---

## 🌟 Funkcjonalności (Features)

- **Automatyczna Agregacja** – podajesz kod choroby, a skrypty wykonują odpowiednią serię zapytań HTTP/GraphQL gromadząc na żywo najświeższą wiedzę.
- **Explainability (Karty Dowodowe)** – system nie jest "czarną skrzynką" – każdy wygenerowany procent jest wyjaśniony przez transparentne karty oceniające siłę każdego z trzech czynników.
- **Decision-Ready Report** – wyciąga w ułamek minuty setki danych i pozwala wyeksportować ranking 50 topowych celów terapeutycznych w zgrabnym pliku `.csv`.

## 🚀 Szybki Start (Instalacja i Uruchomienie)

Aplikacja wymaga interpretera języka **Python** na Twoim komputerze.

1. **Sklonuj repozytorium na swój dysk:**
   ```bash
   git clone https://github.com/TWOJA_NAZWA/target-prioritization-engine.git
   cd target-prioritization-engine
   ```

2. **Zbuduj i uruchom wirtualne środowisko (zalecane):**
   ```bash
   python -m venv venv
   
   # Windows:
   .\venv\Scripts\activate
   
   # Linux / macOS:
   source venv/bin/activate
   ```

3. **Zainstaluj wymagane pakiety:**
   ```bash
   pip install streamlit pandas requests matplotlib
   ```

4. **Włącz interfejs graficzny Dashboardu:**
   ```bash
   streamlit run dashboard/app.py
   ```
   Aplikacja załaduje serwer i wygeneruje aktywny odnośnik `http://localhost:8501`, który automatycznie włączy się w przeglądarce!

---

## 📂 Struktura Projektu

```text
target-prioritization-engine/
│
├── dashboard/
│   └── app.py               # Główny Front-End
│
├── data_fetchers/
│   ├── epmc_client.py       # Moduł ekstrakcji tekstu (Europe PMC API)
│   ├── geo_client.py        # Moduł identyfikacji profilowania (NCBI GEO)
│   └── opentargets.py       # Klient bazowy asocjacji (Open Targets GraphQL)
│
├── engine/
│   └── ranker.py            # Model punktacyjny min-max scaling
│
└── README.md                # Dokumentacja
```

## 📝 Użycie

W systemie korzystamy z identyfikatorów **EFO** (Experimental Factor Ontology). W Panelu Bocznym aplikacji należy wkleić dowolny wspierany ID choroby, by uruchomić skanowanie.  
*Przykładowo:*
- Astma (Asthma) = `EFO_0000676`
- Choroba Alzheimera (Alzheimer's disease) = `EFO_0000249`
- Rak piersi (Breast Carcinoma) = `EFO_0000305`

---
*Powered by: Open Targets, Europe PMC, NCBI E-utilities.*

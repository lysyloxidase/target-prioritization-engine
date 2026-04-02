# 🧬 Target Prioritization Engine

Target Prioritization Engine is an open-source tool designed for the systematic identification and prioritization of potential therapeutic targets (genes/proteins) for a selected disease.

The tool calculates a comprehensive **Priority Score** by integrating three powerful external data sources:
1. **Open Targets Platform**: Target-disease associations and hard evidence fetched via the Open Targets GraphQL API.
2. **Europe PMC**: Medical literature scanning (co-citation frequency of a gene and a disease).
3. **NCBI GEO**: Detection of strong expression signals in experimental metadata (e.g., RNA-Seq or microarrays).

For ease of use and interactivity, the application features a fully functional, responsive **Dashboard** built with the Streamlit framework.

---

## 🌟 Features

- **Automated Data Aggregation** – Input a disease code, and the scripts execute a series of HTTP/GraphQL queries to gather the latest biomedical knowledge in real time.
- **Explainability (Evidence Cards)** – The system is not a black box! Every percentage point of the score is explained through visual cards detailing the strength of each of the three underlying factors.
- **Decision-Ready Report** – Extracts thousands of data points in seconds and exports a ranked list of the top therapeutic targets in a convenient `.csv` format.

## 🚀 Quick Start (Installation & Execution)

The application requires **Python** to be installed on your system.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/target-prioritization-engine.git
   cd target-prioritization-engine
   ```

2. **Set up and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Windows:
   .\venv\Scripts\activate
   
   # Linux / macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install streamlit pandas requests matplotlib
   ```

4. **Run the Dashboard GUI:**
   ```bash
   streamlit run dashboard/app.py
   ```
   The application will start a local server and generate an active link (`http://localhost:8501`), which will automatically open in your browser!

---

## 📂 Project Structure

```text
target-prioritization-engine/
│
├── dashboard/
│   └── app.py               # Main Front-End Dashboard
│
├── data_fetchers/
│   ├── epmc_client.py       # Text extraction module (Europe PMC API)
│   ├── geo_client.py        # Profiling identification module (NCBI GEO)
│   └── opentargets.py       # Core associations client (Open Targets GraphQL)
│
├── engine/
│   └── ranker.py            # Scoring model using min-max scaling
│
└── README.md                # Documentation
```

## 📝 Usage

The system uses **EFO** (Experimental Factor Ontology) identifiers. In the application's sidebar, paste any supported disease ID to start the scan.
*Examples:*
- Asthma = `EFO_0000676`
- Alzheimer's disease = `EFO_0000249`
- Breast Carcinoma = `EFO_0000305`

---
*Powered by: Open Targets, Europe PMC, NCBI E-utilities.*

import sys
import os
import streamlit as st
import pandas as pd

# Umożliwia imporotwanie modułów gdy odpalamy apkę bezpośrednio z dashboard/app.py
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from engine.ranker import run_ranking

# Konfiguracja UI
st.set_page_config(
    page_title="Target Prioritization Engine",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Target Prioritization Engine")
st.markdown("""
Aplikacja agreguje dowody z **Open Targets**, literatury (**Europe PMC**) oraz poziomów ekspresji (**NCBI GEO**). 
Wyznacza ogólny *Priority Score* dla celów terapeutycznych wybranej choroby.
""")

st.sidebar.header("Ustawienia Analizy")
efo_id = st.sidebar.text_input("Podaj Open Targets EFO ID:", value="EFO_0000676")
st.sidebar.caption("Przykłady: EFO_0000676 (Asthma), EFO_0000249 (Alzheimer's disease)")

top_n = st.sidebar.slider("Liczba celów do analizy (API limit):", min_value=5, max_value=50, value=15)

if st.sidebar.button("Uruchom Silnik 🚀"):
    with st.spinner(f"Pobieranie i agregacja danych z wielu baz dla chorby: {efo_id}... (To może potrwać dłuższą chwilę)"):
        try:
            df = run_ranking(efo_id, limit=top_n)
            
            if df.empty:
                st.error("Nie znaleziono wyników dla zadanego EFO ID.")
            else:
                st.success("Dane załadowane i przeliczone pomyślnie!")
                
                # Warstwa 1: DataFrame (Ranking główny)
                st.subheader("🏆 Tabela Rankingowa")
                
                # Wyświetlamy schludnie
                display_cols = ['symbol', 'name', 'priority_score', 'ot_norm', 'epmc_norm', 'geo_norm', 'epmc_hits_raw']
                st.dataframe(
                    df[display_cols].style.background_gradient(cmap='viridis', subset=['priority_score']),
                    use_container_width=True
                )
                
                st.divider()
                
                # Warstwa 2: Evidence Cards (Explainability)
                st.subheader("🔬 Karta Dowodów (Evidence Cards)")
                st.markdown("Poniżej znajdziesz dowody składowe, pokazujące dlaczego dany target znalazł się tak wysoko.")
                
                cols = st.columns(3)
                for index, row in df.head(6).iterrows(): # Wyświetlamy max. pierwszych 6 jako karty
                    col = cols[index % 3]
                    with col:
                        # Karta wizualna
                        score_proc = int(row['priority_score'] * 100)
                        st.markdown(f"### {row['symbol']}")
                        st.markdown(f"**{row['name']}**")
                        st.progress(row['priority_score'], text=f"Priority Score: {score_proc}%")
                        
                        st.write("---")
                        st.write(f"🧬 **Open Targets Score**: `{row['ot_norm']:.3f}`")
                        st.write(f"📚 **Literatura (EPMC)**: `{row['epmc_hits_raw']}` wystąpień *(norm: {row['epmc_norm']:.2f})*")
                        st.write(f"📊 **Ekspresja (GEO)**: `{row['geo_hits_raw']}` datasetów *(norm: {row['geo_norm']:.2f})*")
                        st.write("")
                        
                # Funkcjonalność eksportu "decision-ready report"
                st.divider()
                st.subheader("📥 Eksport Wyników")
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Pobierz pełny raport CSV",
                    data=csv,
                    file_name=f'ranking_targets_{efo_id}.csv',
                    mime='text/csv',
                )
                
        except Exception as e:
            st.error(f"Wystąpił nieoczekiwany błąd: {e}")
else:
    st.info("👈 Wpisz EFO ID i kliknij 'Uruchom Silnik', aby zbadać cele terapeutyczne.")

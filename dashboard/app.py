import sys
import os
import streamlit as st
import pandas as pd

# Allow importing modules when running directly from dashboard/app.py
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from engine.ranker import run_ranking

# UI Configuration
st.set_page_config(
    page_title="Target Prioritization Engine",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Target Prioritization Engine")
st.markdown("""
This application aggregates evidence from **Open Targets**, literature (**Europe PMC**), and expression levels (**NCBI GEO**). 
It calculates an overall *Priority Score* for therapeutic targets related to a selected disease.
""")

st.sidebar.header("Analysis Settings")
efo_id = st.sidebar.text_input("Enter Open Targets EFO ID:", value="EFO_0000676")
st.sidebar.caption("Examples: EFO_0000676 (Asthma), EFO_0000249 (Alzheimer's disease)")

top_n = st.sidebar.slider("Number of targets to analyze (API limit):", min_value=5, max_value=50, value=15)

if st.sidebar.button("Run Engine 🚀"):
    with st.spinner(f"Fetching and aggregating data from multiple databases for disease: {efo_id}... (This might take a moment)"):
        try:
            df = run_ranking(efo_id, limit=top_n)
            
            if df.empty:
                st.error("No results found for the provided EFO ID.")
            else:
                st.success("Data successfully loaded and processed!")
                
                # Layer 1: DataFrame (Main Ranking)
                st.subheader("🏆 Ranking Table")
                
                # Neatly display the table
                display_cols = ['symbol', 'name', 'priority_score', 'ot_norm', 'epmc_norm', 'geo_norm', 'epmc_hits_raw']
                st.dataframe(
                    df[display_cols].style.background_gradient(cmap='viridis', subset=['priority_score']),
                    use_container_width=True
                )
                
                st.divider()
                
                # Layer 2: Evidence Cards (Explainability)
                st.subheader("🔬 Evidence Cards")
                st.markdown("Below you will find the constituent evidence explaining why a given target ranked so high.")
                
                cols = st.columns(3)
                for index, row in df.head(6).iterrows(): # Display max 6 cards
                    col = cols[index % 3]
                    with col:
                        # Visual card
                        score_proc = int(row['priority_score'] * 100)
                        st.markdown(f"### {row['symbol']}")
                        st.markdown(f"**{row['name']}**")
                        st.progress(row['priority_score'], text=f"Priority Score: {score_proc}%")
                        
                        st.write("---")
                        st.write(f"🧬 **Open Targets Score**: `{row['ot_norm']:.3f}`")
                        st.write(f"📚 **Literature (EPMC)**: `{row['epmc_hits_raw']}` hits *(norm: {row['epmc_norm']:.2f})*")
                        st.write(f"📊 **Expression (GEO)**: `{row['geo_hits_raw']}` datasets *(norm: {row['geo_norm']:.2f})*")
                        st.write("")
                        
                # Export functionality "decision-ready report"
                st.divider()
                st.subheader("📥 Export Results")
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download full CSV report",
                    data=csv,
                    file_name=f'ranking_targets_{efo_id}.csv',
                    mime='text/csv',
                )
                
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
else:
    st.info("👈 Enter an EFO ID and click 'Run Engine' to explore therapeutic targets.")

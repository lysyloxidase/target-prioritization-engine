import sys
import os
import pandas as pd

# Dodajemy głowny folder do ścieżki dla bezpośrednich testów
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_fetchers.opentargets import get_disease_targets
from data_fetchers.epmc_client import get_epmc_hit_count
from data_fetchers.geo_client import get_geo_expression_count

def run_ranking(efo_id: str, limit: int = 15):
    """
    Krok 1: Pobiera top N celów terapii z Open Targets.
    Krok 2: Dla każdego celu iteracyjnie wykonuje odpytanie EPMC oraz GEO.
    Krok 3: Normalizuje dane (Min-Max scaler).
    Krok 4: Wyrzuca pandas.DataFrame - wynik finalnego "Priority Score".
    """
    print(f"Pobieram asocjacje Open Targets dla {efo_id} ...")
    ot_data = get_disease_targets(efo_id, limit=limit)
    
    if not ot_data:
        return pd.DataFrame()
        
    disease_name = ot_data[0]['disease_name']
    
    # Krok 2: Zbieramy dowody z zewnętrznych API
    for ix, record in enumerate(ot_data):
        symbol = record['symbol']
        print(f"Będę pobierał sygnały dla [{ix+1}/{len(ot_data)}] {symbol}...")
        
        epmc_hits = get_epmc_hit_count(disease_name, symbol)
        geo_hits = get_geo_expression_count(disease_name, symbol)
        
        record['epmc_hits_raw'] = epmc_hits
        record['geo_hits_raw'] = geo_hits
        
    df = pd.DataFrame(ot_data)
    
    # Krok 3: Normalizacja i Scoring
    
    # Funkcja do Min-Max scalling jeśli max > min
    def min_max_scale(series):
        if series.max() == series.min():
            return [0.5] * len(series) # wszystko równe, daje środek 0.5
        return (series - series.min()) / (series.max() - series.min())

    df['epmc_norm'] = min_max_scale(df['epmc_hits_raw'])
    df['geo_norm'] = min_max_scale(df['geo_hits_raw'])
    # Open Targets zwraca wartości [0-1] standardowo, używamy ich bezpośrednio.
    df['ot_norm'] = df['ot_score']
    
    # Wagi do Priority Score (Wzorowane np. na dominacji OpenTargets)
    W_OT = 0.5
    W_EPMC = 0.25
    W_GEO = 0.25
    
    df['priority_score'] = (
        (df['ot_norm'] * W_OT) +
        (df['epmc_norm'] * W_EPMC) +
        (df['geo_norm'] * W_GEO)
    )
    
    # Sortowane po najwyższym
    df = df.sort_values(by='priority_score', ascending=False).reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    test_df = run_ranking("EFO_0000676", limit=3)
    if not test_df.empty:
        print("\nTOP 3 TARGETS:")
        print(test_df[['symbol', 'priority_score', 'ot_score', 'epmc_norm', 'geo_norm']])

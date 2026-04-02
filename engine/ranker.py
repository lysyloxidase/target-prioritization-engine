import sys
import os
import pandas as pd

# Add root folder to path for direct testing
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_fetchers.opentargets import get_disease_targets
from data_fetchers.epmc_client import get_epmc_hit_count
from data_fetchers.geo_client import get_geo_expression_count

def run_ranking(efo_id: str, limit: int = 15):
    """
    Step 1: Fetch top N therapeutic targets from Open Targets.
    Step 2: Iterate over each target to fetch EPMC and GEO data.
    Step 3: Normalize the data (Min-Max scaler).
    Step 4: Return pandas.DataFrame with the final "Priority Score".
    """
    print(f"Fetching Open Targets associations for {efo_id} ...")
    ot_data = get_disease_targets(efo_id, limit=limit)
    
    if not ot_data:
        return pd.DataFrame()
        
    disease_name = ot_data[0]['disease_name']
    
    # Step 2: Gather evidence from external APIs
    for ix, record in enumerate(ot_data):
        symbol = record['symbol']
        print(f"Fetching signals for [{ix+1}/{len(ot_data)}] {symbol}...")
        
        epmc_hits = get_epmc_hit_count(disease_name, symbol)
        geo_hits = get_geo_expression_count(disease_name, symbol)
        
        record['epmc_hits_raw'] = epmc_hits
        record['geo_hits_raw'] = geo_hits
        
    df = pd.DataFrame(ot_data)
    
    # Step 3: Normalization and Scoring
    
    # Function for Min-Max scaling
    def min_max_scale(series):
        if series.max() == series.min():
            return [0.5] * len(series) # all equal, default to 0.5 middle
        return (series - series.min()) / (series.max() - series.min())

    df['epmc_norm'] = min_max_scale(df['epmc_hits_raw'])
    df['geo_norm'] = min_max_scale(df['geo_hits_raw'])
    # Open Targets returns values [0-1] by default, use them directly.
    df['ot_norm'] = df['ot_score']
    
    # Weights for the Priority Score (Giving dominance to OpenTargets API)
    W_OT = 0.5
    W_EPMC = 0.25
    W_GEO = 0.25
    
    df['priority_score'] = (
        (df['ot_norm'] * W_OT) +
        (df['epmc_norm'] * W_EPMC) +
        (df['geo_norm'] * W_GEO)
    )
    
    # Sort by highest score
    df = df.sort_values(by='priority_score', ascending=False).reset_index(drop=True)
    
    return df

if __name__ == "__main__":
    test_df = run_ranking("EFO_0000676", limit=3)
    if not test_df.empty:
        print("\nTOP 3 TARGETS:")
        print(test_df[['symbol', 'priority_score', 'ot_score', 'epmc_norm', 'geo_norm']])

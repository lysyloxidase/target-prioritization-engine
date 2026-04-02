import requests

NCBI_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

def get_geo_expression_count(disease_name: str, target_symbol: str) -> int:
    """
    Checks how many experimental datasets in GEO (Gene Expression Omnibus)
    mention both the disease and the specific gene simultaneously in their metadata,
    which serves as a proxy for expression signal strength at this stage.
    """
    query = f'"{disease_name}"[All Fields] AND "{target_symbol}"[All Fields]'
    params = {
        "db": "gds", # GEO Datasets database
        "term": query,
        "retmode": "json"
    }
    
    try:
        res = requests.get(NCBI_ESEARCH_URL, params=params)
        if res.status_code == 200:
            data = res.json()
            return int(data.get("esearchresult", {}).get("count", 0))
        return 0
    except Exception as e:
        print(f"Error fetching from NCBI GEO: {e}")
        return 0

if __name__ == "__main__":
    count = get_geo_expression_count("Asthma", "IL4")
    print(f"Found {count} GEO datasets for Asthma + IL4")

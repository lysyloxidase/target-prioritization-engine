import requests

EPMC_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

def get_epmc_hit_count(disease_name: str, target_symbol: str) -> int:
    """
    Kwerenduje Europe PMC, żeby sprawdzić liczbę publikacji wspominających
    jednocześnie zadaną chorobę i cel terapeutyczny.
    """
    query = f'"{disease_name}" AND ("{target_symbol}")'
    params = {
        "query": query,
        "format": "json",
        "resultType": "lite",
        "pageSize": 1 # zależy nam tylko na hitCount
    }
    
    try:
        res = requests.get(EPMC_URL, params=params)
        if res.status_code == 200:
            data = res.json()
            return data.get("hitCount", 0)
        return 0
    except Exception as e:
        print(f"Error uderzając do Europe PMC: {e}")
        return 0

if __name__ == "__main__":
    count = get_epmc_hit_count("Asthma", "IL4")
    print(f"Znaleziono {count} abstraktów dla Asthma + IL4")

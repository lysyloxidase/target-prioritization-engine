import requests
from typing import List, Dict, Any

OPENTARGETS_API_URL = "https://api.platform.opentargets.org/api/v4/graphql"

def get_disease_targets(efo_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetches targets associated with a disease from Open Targets via GraphQL.
    Returns the top `limit` targets based on overall association score.
    """
    query = """
    query diseaseTargets($efoId: String!, $size: Int!) {
      disease(efoId: $efoId) {
        id
        name
        associatedTargets(page: {index: 0, size: $size}) {
          rows {
            target {
              id
              approvedSymbol
              approvedName
            }
            score
          }
        }
      }
    }
    """
    
    variables = {
        "efoId": efo_id,
        "size": limit
    }
    
    response = requests.post(
        OPENTARGETS_API_URL, 
        json={"query": query, "variables": variables}
    )
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and "disease" in data["data"] and data["data"]["disease"]:
            disease_name = data["data"]["disease"]["name"]
            rows = data["data"]["disease"]["associatedTargets"]["rows"]
            
            targets = []
            for row in rows:
                targets.append({
                    "disease_efo": efo_id,
                    "disease_name": disease_name,
                    "target_id": row["target"]["id"],
                    "symbol": row["target"]["approvedSymbol"],
                    "name": row["target"]["approvedName"],
                    "ot_score": row["score"]
                })
            return targets
        else:
            print(f"No disease found for EFO ID: {efo_id}")
            return []
    else:
        print(f"Error fetching Open Targets data: {response.status_code}")
        return []

if __name__ == "__main__":
    # Test
    targets = get_disease_targets("EFO_0000676", 5) # Asthma
    print(f"Found {len(targets)} targets for Asthma:")
    for t in targets:
        print(f"{t['symbol']}: {t['ot_score']}")

import requests
from langchain_core.tools import tool


@tool
def get_country_info(country_name: str = None) -> dict:
    """Get information about countries for travel planning.

    Args:
        country_name: Name of country to look up (optional - returns list of countries if not specified)

    Returns:
        Country data including capital, region, currencies, languages, population
    """
    try:
        url = "https://restcountries.com/v3.1/all"
        params = {
            "fields": "name,capital,region,subregion,currencies,languages,population,flags"
        }
        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            return {"found": False, "error": f"API returned {response.status_code}"}

        countries = response.json()

        if country_name:
            country_name_lower = country_name.lower()
            for c in countries:
                if country_name_lower in c.get("name", {}).get("common", "").lower():
                    return {
                        "found": True,
                        "data": {
                            "name": c.get("name", {}).get("common"),
                            "official_name": c.get("name", {}).get("official"),
                            "capital": c.get("capital", []),
                            "region": c.get("region"),
                            "subregion": c.get("subregion"),
                            "population": c.get("population"),
                            "currencies": c.get("currencies"),
                            "languages": c.get("languages"),
                            "flag": c.get("flags", {}).get("emoji"),
                        },
                    }
            return {
                "found": False,
                "data": None,
                "message": f"Country '{country_name}' not found",
            }

        return {
            "found": True,
            "data": [
                {
                    "name": c.get("name", {}).get("common"),
                    "region": c.get("region"),
                    "capital": c.get("capital", []),
                }
                for c in countries[:20]
            ],
            "message": "First 20 countries. Specify a country name for details.",
        }
    except Exception as e:
        return {"found": False, "error": str(e)}

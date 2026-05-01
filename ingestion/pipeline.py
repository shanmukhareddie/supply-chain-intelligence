from ingestion.sources.fred import fetch_fred_data
from ingestion.load.postgres import save_to_db

commodity_codes = [
    "DCOILBRENTEU",    # Oil
    "DHHNGSP",         # Natural Gas
    "PWHEAMTUSDM",     # Wheat
    "PCOALAUUSDM",     # Coal
    "NASDAQQGLDI",     # Gold
]

for code in commodity_codes:

    data= fetch_fred_data(code)      # fetch data for this code
    save_to_db(data,"commodities_prices") # save to database
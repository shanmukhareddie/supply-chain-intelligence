from ingestion.db_connection import get_engine

def save_to_db(df, table_name):
    engine = get_engine()
    df.to_sql(
        name=table_name,   # which table — "commodities_prices"
        con=engine,  # the database connection (the pipe)
        if_exists="append",# don't delete existing data, just add new rows
        index=False        # our DataFrame index (0,1,2,3..) is not a real column, don't save it
    )
    print(f"Saved {len(df)} rows to {table_name}")
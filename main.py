from dispatcher import dispatch_and_map
from validator import enforce_types
from api_retriever import fetch_from_openalex


def run_advanced_etl(query):
    # 1. EXTRACT: Fetch from OpenAlex API
    print(f"Starting Advanced ETL for: '{query}'")
    raw_df = fetch_from_openalex(query)

    if raw_df.empty:
        print("No data found.")
        return

    # 2. TRANSFORM: Dispatch & Map
    # Note: We specify 'openalex' as the source
    df = dispatch_and_map(raw_df, 'openalex')

    # 3. TRANSFORM: Enforce Types
    df = enforce_types(df)

    # 4. LOAD: Export
    output_path = "advanced_standardized_data.csv"
    df.to_csv(output_path, sep=';', index=False)
    print(f"Pipeline complete! File saved: {output_path}")
    print("First 5 rows:")
    print(df.head())  # Preview the normalized result
    print("\nAll column names in the final DataFrame:")
    print(df.columns.tolist())

# To run it, uncomment the line below:
run_advanced_etl("machine learning")
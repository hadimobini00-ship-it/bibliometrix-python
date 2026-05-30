import pandas as pd


def enforce_types(df):
    # 1. Ensure TC is integer
    if 'TC' in df.columns:
        df['TC'] = pd.to_numeric(df['TC'], errors='coerce').fillna(0).astype(int)

    # 2. Ensure PY is integer (publication year)
    if 'PY' in df.columns:
        df['PY'] = pd.to_numeric(df['PY'], errors='coerce').fillna(0).astype(int)

    # 3. Ensure multi-value fields are lists, preserve existing lists
    list_columns = ['AU', 'AF', 'C1', 'CR', 'DE', 'ID']
    for col in list_columns:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: x if isinstance(x, list) else (x.split(';') if isinstance(x, str) else []))

    # 4. Compute SR if needed (your existing SR code here)
    # ... (keep your SR calculation code)

    return df
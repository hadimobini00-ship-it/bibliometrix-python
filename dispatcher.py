from mapping import FIELD_MAPPINGS
import ast

def extract_authors(row):
    """Extract list of author names from authorships column."""
    authorships = row.get('authorships')
    if isinstance(authorships, str):
        try:
            authorships = ast.literal_eval(authorships)
        except:
            return []
    if not isinstance(authorships, list):
        return []
    authors = []
    for auth in authorships:
        if isinstance(auth, dict):
            author_info = auth.get('author')
            if isinstance(author_info, dict):
                name = author_info.get('display_name')
                if name:
                    authors.append(name)
    return authors

def extract_cited_references(row):
    """Extract list of cited reference IDs from referenced_works column."""
    refs = row.get('referenced_works')
    if isinstance(refs, str):
        try:
            refs = ast.literal_eval(refs)
        except:
            return []
    if not isinstance(refs, list):
        return []
    return refs

def extract_source(row):
    """Extract source/journal name from primary_location."""
    primary_location = row.get('primary_location')
    if isinstance(primary_location, str):
        try:
            primary_location = ast.literal_eval(primary_location)
        except:
            return ''
    if not isinstance(primary_location, dict):
        return ''
    source = primary_location.get('source', {})
    if isinstance(source, dict):
        return source.get('display_name', '')
    return ''

def extract_keywords(row):
    """Extract list of keyword strings from keywords column."""
    keywords = row.get('keywords')
    if isinstance(keywords, str):
        try:
            keywords = ast.literal_eval(keywords)
        except:
            return []
    if not isinstance(keywords, list):
        return []
    result = []
    for kw in keywords:
        if isinstance(kw, dict):
            name = kw.get('display_name')
            if name:
                result.append(name)
    return result

def extract_concepts(row):
    """Extract list of concept display names from concepts column."""
    concepts = row.get('concepts')
    if isinstance(concepts, str):
        try:
            concepts = ast.literal_eval(concepts)
        except:
            return []
    if not isinstance(concepts, list):
        return []
    result = []
    for cpt in concepts:
        if isinstance(cpt, dict):
            name = cpt.get('display_name')
            if name:
                result.append(name)
    return result

def extract_affiliations(row):
    """Extract list of affiliation names from authorships column."""
    authorships = row.get('authorships')
    if isinstance(authorships, str):
        try:
            authorships = ast.literal_eval(authorships)
        except:
            return []
    if not isinstance(authorships, list):
        return []
    affiliations = set()
    for auth in authorships:
        if not isinstance(auth, dict):
            continue
        institutions = auth.get('institutions', [])
        for inst in institutions:
            if isinstance(inst, dict):
                name = inst.get('display_name')
                if name:
                    affiliations.add(name)
    return list(affiliations)

def extract_abstract(row):
    """Reconstruct abstract from abstract_inverted_index dict."""
    inverted = row.get('abstract_inverted_index')
    if isinstance(inverted, str):
        try:
            inverted = ast.literal_eval(inverted)
        except:
            return ''
    if not isinstance(inverted, dict):
        return ''
    max_pos = 0
    for positions in inverted.values():
        if positions:
            max_pos = max(max_pos, max(positions))
    words = [''] * (max_pos + 1)
    for word, positions in inverted.items():
        for pos in positions:
            words[pos] = word
    return ' '.join(words).strip()

def dispatch_and_map(df, source_name):
    if source_name not in FIELD_MAPPINGS:
        raise ValueError(f"Source '{source_name}' not supported. Check mapping.py.")

    mapping = FIELD_MAPPINGS[source_name]

    # Extract authors if needed (AU)
    if 'AU' in mapping and mapping['AU'] == 'authorships':
        print("Extracting authors...")
        df['AU'] = df.apply(extract_authors, axis=1)

    # Extract cited references if needed (CR)
    if 'CR' in mapping and mapping['CR'] == 'referenced_works':
        print("Extracting cited references...")
        df['CR'] = df.apply(extract_cited_references, axis=1)

    # Extract source if needed (SO)
    if 'SO' in mapping and mapping['SO'] == 'primary_location.source.display_name':
        print("Extracting source...")
        df['SO'] = df.apply(extract_source, axis=1)

    # Extract keywords if needed (DE)
    if 'DE' in mapping and mapping['DE'] == 'keywords':
        print("Extracting keywords...")
        df['DE'] = df.apply(extract_keywords, axis=1)

    # Extract concepts if needed (ID)
    if 'ID' in mapping and mapping['ID'] == 'concepts':
        print("Extracting concepts...")
        df['ID'] = df.apply(extract_concepts, axis=1)

    # Extract affiliations if needed (C1)
    if 'C1' in mapping and mapping['C1'] == 'authorships':
        print("Extracting affiliations...")
        df['C1'] = df.apply(extract_affiliations, axis=1)

    # Extract abstract if needed (AB)
    if 'AB' in mapping and mapping['AB'] == 'abstract_inverted_index':
        print("Extracting abstract...")
        df['AB'] = df.apply(extract_abstract, axis=1)

    # Rename columns (skip the ones we already created)
    rename_dict = {}
    for target, source in mapping.items():
        if target in ['AU', 'CR', 'SO', 'DE', 'ID', 'C1', 'AB']:
            continue  # already handled
        if source in df.columns:
            rename_dict[source] = target

    df = df.rename(columns=rename_dict)

    # Keep only the required WoS columns (as per exam Table 4.2)
    required_columns = [
        'UT', 'DI', 'PMID', 'TI', 'SO', 'JI', 'PY', 'DT', 'LA', 'TC',
        'AU', 'AF', 'C1', 'RP', 'CR', 'DE', 'ID', 'AB', 'VL', 'IS', 'BP', 'EP', 'SR'
    ]
    # Keep only columns that actually exist in the DataFrame
    existing_cols = [col for col in required_columns if col in df.columns]
    df = df[existing_cols]

    return df
"""Build the multi-source corpus from individual public datasets.

Each source CSV is loaded, normalized to a common schema, tagged with its
provenance (`source`) so the bias audit can compare single- vs. multi-source,
deduplicated, then concatenated. Place raw CSVs in data/raw/ (see data/README.md).
"""
import pandas as pd

COMMON_SCHEMA = ["sender", "receiver", "date", "subject", "body", "urls", "label", "source"]


def load_source(path: str, source_name: str) -> pd.DataFrame:
    """Load one source CSV and coerce it to the common schema."""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    for col in COMMON_SCHEMA:
        if col not in df.columns:
            df[col] = None
    df["source"] = source_name
    return df[COMMON_SCHEMA]


def merge(sources: dict) -> pd.DataFrame:
    """sources = {source_name: csv_path}. Returns a deduplicated merged frame."""
    frames = [load_source(p, name) for name, p in sources.items()]
    df = pd.concat(frames, ignore_index=True)
    df = df.dropna(subset=["body"]).drop_duplicates(subset=["subject", "body"])
    return df.reset_index(drop=True)

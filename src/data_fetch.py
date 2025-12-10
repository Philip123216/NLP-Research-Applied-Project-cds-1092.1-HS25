import requests
import pandas as pd
from typing import List, Dict

import config


def fetch_hf_rows() -> List[Dict]:
    """
    Holt Zeilen vom HF datasets-server.
    Erwartet Spalten: question, context1, context2, ...
    """
    config.OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows: List[Dict] = []
    offset = 0

    print("== Lade Dataset von Hugging Face...")

    while True:
        remaining = None
        if config.HF_MAX_ROWS is not None:
            remaining = config.HF_MAX_ROWS - len(rows)
            if remaining <= 0:
                break

        length = config.HF_BATCH_SIZE
        if remaining is not None:
            length = min(length, remaining)

        params = {
            "dataset": config.HF_DATASET,
            "config": config.HF_CONFIG,
            "split": config.HF_SPLIT,
            "offset": offset,
            "length": length,
        }

        resp = requests.get(config.HF_ROWS_URL, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        batch = data.get("rows", [])
        if not batch:
            break

        for item in batch:
            rows.append(item["row"])

        print(f"  -> geholt: {len(batch)} rows (gesamt: {len(rows)})")

        if len(batch) < length:
            break

        offset += length

    print(f"== Fertig: {len(rows)} Instanzen geladen.")
    return rows


def build_pairs_df(rows: List[Dict]) -> pd.DataFrame:
    """
    Baut ein DataFrame  mit den relevanten Spalten:
      id          = question_ID
      question    = Frage
      text_a      = context1
      text_b      = context2
    plus etwas Meta.
    """
    df_raw = pd.DataFrame(rows)

    df_pairs = pd.DataFrame({
        "id": df_raw["question_ID"],
        "question": df_raw["question"],
        "text_a": df_raw["context1"],   # wird später als Kontext 1 ins LLM gefüttert
        "text_b": df_raw["context2"],   # wird als Kontext 2 ins LLM gefüttert
        "contradict_type": df_raw.get("contradictType"),
        "same_passage": df_raw.get("samepassage"),
    })

    df_pairs.to_csv(config.PAIRS_CSV, index=False, encoding="utf-8")
    print(f"== Pairs CSV gespeichert unter: {config.PAIRS_CSV.resolve()}")

    return df_pairs

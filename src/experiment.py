import time
import pandas as pd
from typing import Dict, Any

import config
from llm_client import query_ollama


def run_experiment(df_pairs: pd.DataFrame) -> pd.DataFrame:
    results: list[Dict[str, Any]] = []
    n = len(df_pairs)

    print(f"== Starte LLM-Evaluation über {n} Instanzen mit Modell '{config.MODEL_NAME}'")

    for idx, row in df_pairs.iterrows():
        row_id = row["id"]
        question = str(row.get("question", ""))
        text_a = str(row["text_a"])
        text_b = str(row["text_b"])

        print(f"[{idx+1}/{n}] Frage Modell für ID={row_id} ...", end="", flush=True)

        llm_out = None
        error = None

        try:
            llm_out = query_ollama(question, text_a, text_b)
            print(" OK")
        except Exception as e:
            error = str(e)
            print(" FEHLER:", error)

        result_row: Dict[str, Any] = {
            "id": row_id,
            "question": question,
            "text_a": text_a,
            "text_b": text_b,
            "contradict_type": row.get("contradict_type"),
            "same_passage": row.get("same_passage"),
            "model_name": config.MODEL_NAME,
            "error": error,
        }

        if llm_out is not None:
            result_row.update({
                "llm_contradiction": llm_out.get("contradiction"),
                "llm_explanation": llm_out.get("explanation"),
                "llm_can_decide_truth": llm_out.get("can_decide_truth"),
                "llm_chosen_side": llm_out.get("chosen_side"),
                "llm_choice_reason": llm_out.get("choice_reason"),
            })
        else:
            result_row.update({
                "llm_contradiction": None,
                "llm_explanation": None,
                "llm_can_decide_truth": None,
                "llm_chosen_side": None,
                "llm_choice_reason": None,
            })

        results.append(result_row)
        time.sleep(0.2)

    df_res = pd.DataFrame(results)
    df_res.to_csv(config.RESULTS_CSV, index=False, encoding="utf-8")
    df_res.to_json(
        config.RESULTS_JSONL,
        orient="records",
        lines=True,
        force_ascii=False
    )

    print(f"== Ergebnisse gespeichert als CSV:   {config.RESULTS_CSV.resolve()}")
    print(f"== Ergebnisse gespeichert als JSONL: {config.RESULTS_JSONL.resolve()}")

    return df_res

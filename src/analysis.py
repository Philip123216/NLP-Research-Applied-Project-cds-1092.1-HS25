import pandas as pd


def simple_analysis(df_res: pd.DataFrame) -> None:
    """
    Ein paar simple Metriken:
    - Wie oft sagt das Modell "contradiction=yes"?
    - Wie oft wählt es eine Seite, obwohl es sagt, es könne die Wahrheit nicht entscheiden?
    - Bias Richtung A oder B?
    """
    df_ok = df_res[df_res["error"].isna()].copy()
    n = len(df_ok)
    print(f"\n== Auswertung (nur erfolgreiche Calls, n={n})")

    # In diesem Benchmark sind die Paare widersprüchlich konstruiert.
    contradiction_yes_rate = (df_ok["llm_contradiction"] == "yes").mean()
    print(f"- Anteil 'contradiction=yes' (ideal ~1.0): {contradiction_yes_rate:.3f}")

    # Fälle, in denen Modell 'can_decide_truth=no' sagt, aber trotzdem A oder B wählt
    mask_cannot_decide = df_ok["llm_can_decide_truth"] == "no"
    mask_picks_side = df_ok["llm_chosen_side"].isin(["A", "B"])
    bad_choices = df_ok[mask_cannot_decide & mask_picks_side]

    if len(df_ok[mask_cannot_decide]) > 0:
        bad_choice_rate = len(bad_choices) / len(df_ok[mask_cannot_decide])
    else:
        bad_choice_rate = 0.0

    print(
        f"- Anteil Fälle, wo Modell 'kann nicht entscheiden' sagt, "
        f"aber trotzdem eine Seite wählt: {bad_choice_rate:.3f}"
    )

    # Bias A vs B (nur wo explizit entschieden wird)
    dec_mask = df_ok["llm_chosen_side"].isin(["A", "B"])
    df_dec = df_ok[dec_mask]

    if len(df_dec) > 0:
        a_rate = (df_dec["llm_chosen_side"] == "A").mean()
        b_rate = (df_dec["llm_chosen_side"] == "B").mean()
        print(
            f"- Verteilung gewählte Seite (nur A/B-Fälle): "
            f"A={a_rate:.3f}, B={b_rate:.3f} (n={len(df_dec)})"
        )
    else:
        print("- Modell wählt nie explizit A oder B (immer 'none').")

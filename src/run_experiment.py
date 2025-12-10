from data_fetch import fetch_hf_rows, build_pairs_df
from experiment import run_experiment
from analysis import simple_analysis


def main():
    rows = fetch_hf_rows()
    df_pairs = build_pairs_df(rows)
    df_res = run_experiment(df_pairs)
    simple_analysis(df_res)


if __name__ == "__main__":
    main()

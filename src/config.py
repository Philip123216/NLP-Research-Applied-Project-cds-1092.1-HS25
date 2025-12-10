from pathlib import Path

# Projektwurzel = Ordner "NLP_LLM"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data-Ordner auf derselben Ebene wie src
DATA_DIR = PROJECT_ROOT / "data"

# Unterordner für dieses Experiment
OUT_DIR = DATA_DIR / "wikicontradict_out"

# HF Dataset Config
HF_ROWS_URL = "https://datasets-server.huggingface.co/rows"
HF_DATASET = "ibm-research/Wikipedia_contradict_benchmark"
HF_CONFIG = "default"
HF_SPLIT = "train"
HF_BATCH_SIZE = 100
HF_MAX_ROWS = 256  # oder None, wenn du alles willst

# Ollama Confi
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:3b"  # oder z.B. "qwen2.5:7b" können wir auch etwas rumtesten

# Output-Dateien IM data/wikicontradict_out/
PAIRS_CSV = OUT_DIR / "wikicontradict_pairs.csv"
RESULTS_CSV = OUT_DIR / "wikicontradict_llm_results.csv"
RESULTS_JSONL = OUT_DIR / "wikicontradict_llm_results.jsonl"

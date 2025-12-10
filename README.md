# Wikipedia Contradiction Experiment (Ollama)

Dieses Projekt evaluiert die Fähigkeit von LLMs (via Ollama), logische Widersprüche in Textpaaren aus dem [WikiContradict Dataset](https://huggingface.co/datasets/wiki_contradict) zu erkennen.

## Voraussetzungen

* **Python 3.8+**
* **Ollama** installiert und laufend ([ollama.com](https://ollama.com/))

## Installation

1. **Repository klonen** (falls zutreffend) oder in den Projektordner wechseln.

2. **Virtuelle Umgebung erstellen und aktivieren:**

   Powershell:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   Bash/Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Abhängigkeiten installieren:**

   ```bash
   pip install -r requirements.txt
   ```
   (Alternativ: `pip install requests pandas`)

4. **Ollama Modell herunterladen:**

   Standardmäßig wird `llama3.2:3b` verwendet (konfigurierbar in `src/config.py`).
   
   ```bash
   ollama pull llama3.2:3b
   ```

## Nutzung

1. **Ollama Server starten:**
   Starten Sie Ollama in einem separaten Terminal und lassen Sie es laufen:
   ```bash
   ollama serve
   ```

2. **Experiment ausführen:**
   Führen Sie das Hauptskript aus, um Daten zu laden, das Modell zu befragen und Ergebnisse zu speichern.
   ```bash
   python src/run_experiment.py
   ```

   Das Skript wird:
   * Das Dataset von Hugging Face laden.
   * Paare in `data/wikicontradict_out/wikicontradict_pairs.csv` speichern.
   * Das LLM für jedes Paar befragen.
   * Ergebnisse in `data/wikicontradict_out/` speichern (CSV und JSONL).
   * Eine kurze Analyse auf der Konsole ausgeben.

## Projektstruktur

* **`src/config.py`**: Zentrale Einstellungen (Modellname, Pfade, Dataset-Infos).
* **`src/data_fetch.py`**: Lädt Daten von HuggingFace API und erstellt den Datensatz.
* **`src/prompts.py`**: Enthält System-Prompts, User-Prompt-Templates und das JSON-Schema für strukturierte Antworten.
* **`src/llm_client.py`**: Client für die Kommunikation mit der Ollama API.
* **`src/experiment.py`**: Führt die Evaluation über alle Instanzen durch.
* **`src/analysis.py`**: Berechnet einfache Metriken (Widerspruchsrate, Entscheidungsverhalten).
* **`src/run_experiment.py`**: Hauptprogramm, das alle Schritte verbindet.


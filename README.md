# BankAssist Triage

BankAssist Triage is a local AI engineering project for fine-tuning a small language model to produce structured banking ticket triage decisions.

The project is currently at the dataset preprocessing stage. It uses `PolyAI/banking77`, filters the current nine selected intents, derives readable intent names from the dataset `ClassLabel` metadata, and enriches every record with deterministic business routing fields.

## Current Dataset Step

Run preprocessing from the project root with:

```bash
conda run -n bankassist env PYTHONPATH=src python -m bankassist.data.preprocess
```

This saves the enriched Hugging Face `DatasetDict` to:

```text
data/processed/business-labelled-v1
```

Each enriched record keeps the original integer label:

```json
{
  "text": "I can't use my card because it is not working.",
  "label": 14,
  "intent": "card_not_working",
  "priority": "medium",
  "route": "card_support",
  "requires_human_review": false
}
```

The next project step is to convert enriched records into `System` / `User` / `Assistant` instruction-following conversations. Tokenization should start only after that conversion.

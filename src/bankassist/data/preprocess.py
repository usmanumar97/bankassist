"""Preprocessing for the BankAssist Triage dataset.

This module keeps the first preprocessing step explicit:

1. Load BANKING77.
2. Keep only the selected Version 1 intents.
3. Convert the integer label into the readable intent name.
4. Attach deterministic business triage fields.

The original integer ``label`` is intentionally preserved for traceability.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datasets import DatasetDict


BANKING77_DATASET_NAME = "PolyAI/banking77"
BANKING77_REVISION = "refs/pr/7"

SELECTED_INTENTS: tuple[str, ...] = (
    "lost_or_stolen_card",
    "compromised_card",
    "card_payment_not_recognised",
    "cash_withdrawal_not_recognised",
    "wrong_amount_of_cash_received",
    "transfer_not_received_by_recipient",
    "declined_card_payment",
    "card_not_working",
    "change_pin",
)

BUSINESS_RULES: dict[str, dict[str, str | bool]] = {
    "lost_or_stolen_card": {
        "priority": "critical",
        "route": "card_security",
        "requires_human_review": True,
    },
    "compromised_card": {
        "priority": "critical",
        "route": "fraud_team",
        "requires_human_review": True,
    },
    "card_payment_not_recognised": {
        "priority": "critical",
        "route": "fraud_team",
        "requires_human_review": True,
    },
    "cash_withdrawal_not_recognised": {
        "priority": "critical",
        "route": "fraud_team",
        "requires_human_review": True,
    },
    "wrong_amount_of_cash_received": {
        "priority": "high",
        "route": "atm_disputes",
        "requires_human_review": True,
    },
    "transfer_not_received_by_recipient": {
        "priority": "high",
        "route": "transfers_team",
        "requires_human_review": True,
    },
    "declined_card_payment": {
        "priority": "medium",
        "route": "card_support",
        "requires_human_review": False,
    },
    "card_not_working": {
        "priority": "medium",
        "route": "card_support",
        "requires_human_review": False,
    },
    "change_pin": {
        "priority": "low",
        "route": "self_service",
        "requires_human_review": False,
    },
}


def validate_business_rules(
    selected_intents: tuple[str, ...] = SELECTED_INTENTS,
    business_rules: dict[str, dict[str, str | bool]] = BUSINESS_RULES,
) -> None:
    """Ensure every selected intent has exactly one business-rule entry."""

    selected = set(selected_intents)
    rule_intents = set(business_rules)

    missing_rules = selected - rule_intents
    extra_rules = rule_intents - selected

    if missing_rules:
        missing = ", ".join(sorted(missing_rules))
        raise ValueError(f"Missing business rules for selected intents: {missing}")

    if extra_rules:
        extra = ", ".join(sorted(extra_rules))
        raise ValueError(f"Business rules contain unsupported intents: {extra}")


def label_names_from_dataset(dataset: DatasetDict) -> list[str]:
    """Return the readable ClassLabel names from the training split."""

    label_feature = dataset["train"].features["label"]

    if not hasattr(label_feature, "names"):
        raise TypeError("Expected dataset['train'].features['label'] to be a ClassLabel.")

    return list(label_feature.names)


def selected_label_ids(label_names: list[str], selected_intents: tuple[str, ...]) -> set[int]:
    """Convert selected intent names into their BANKING77 integer label IDs."""

    name_to_id = {name: index for index, name in enumerate(label_names)}
    missing_intents = [intent for intent in selected_intents if intent not in name_to_id]

    if missing_intents:
        missing = ", ".join(missing_intents)
        raise ValueError(f"Selected intents not found in dataset metadata: {missing}")

    return {name_to_id[intent] for intent in selected_intents}


def enrich_record(example: dict[str, Any], label_names: list[str]) -> dict[str, Any]:
    """Add intent and business triage fields to one dataset record."""

    intent = label_names[example["label"]]
    rules = BUSINESS_RULES[intent]

    return {
        "intent": intent,
        "priority": rules["priority"],
        "route": rules["route"],
        "requires_human_review": rules["requires_human_review"],
    }


def build_enriched_dataset(dataset: DatasetDict) -> DatasetDict:
    """Filter BANKING77 and enrich every remaining record."""

    validate_business_rules()

    label_names = label_names_from_dataset(dataset)
    allowed_label_ids = selected_label_ids(label_names, SELECTED_INTENTS)

    filtered_dataset = dataset.filter(lambda example: example["label"] in allowed_label_ids)

    return filtered_dataset.map(lambda example: enrich_record(example, label_names))


def load_banking77_dataset(
    dataset_name: str = BANKING77_DATASET_NAME,
    revision: str = BANKING77_REVISION,
) -> DatasetDict:
    """Load BANKING77 from Hugging Face."""

    from datasets import load_dataset

    return load_dataset(dataset_name, revision=revision)


def save_dataset(dataset: DatasetDict, output_dir: Path) -> None:
    """Persist the enriched dataset in Hugging Face's native on-disk format."""

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    dataset.save_to_disk(str(output_dir))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the business-labelled Version 1 BankAssist dataset."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed/business-labelled-v1"),
        help="Directory where the enriched Hugging Face DatasetDict will be saved.",
    )
    parser.add_argument(
        "--dataset-name",
        default=BANKING77_DATASET_NAME,
        help="Hugging Face dataset name to load.",
    )
    parser.add_argument(
        "--revision",
        default=BANKING77_REVISION,
        help="Dataset revision to load.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_dataset = load_banking77_dataset(
        dataset_name=args.dataset_name,
        revision=args.revision,
    )
    enriched_dataset = build_enriched_dataset(raw_dataset)
    save_dataset(enriched_dataset, args.output_dir)

    print(enriched_dataset)
    print(f"Saved enriched dataset to {args.output_dir}")


if __name__ == "__main__":
    main()

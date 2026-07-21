import pytest

from bankassist.data.preprocess import (
    BUSINESS_RULES,
    SELECTED_INTENTS,
    enrich_record,
    selected_label_ids,
    validate_business_rules,
)


def test_business_rules_match_selected_intents() -> None:
    validate_business_rules()


def test_selected_label_ids_uses_classlabel_order() -> None:
    label_names = [
        "activate_my_card",
        "lost_or_stolen_card",
        "change_pin",
        "cash_withdrawal_not_recognised",
    ]

    selected = ("lost_or_stolen_card", "change_pin")

    assert selected_label_ids(label_names, selected) == {1, 2}


def test_selected_label_ids_fails_for_missing_intent() -> None:
    with pytest.raises(ValueError, match="Selected intents not found"):
        selected_label_ids(["lost_or_stolen_card"], ("change_pin",))


def test_enrich_record_preserves_business_mapping_without_mutating_label() -> None:
    label_names = ["lost_or_stolen_card", "change_pin"]
    example = {"text": "My card was stolen.", "label": 0}

    enriched_fields = enrich_record(example, label_names)

    assert example == {"text": "My card was stolen.", "label": 0}
    assert enriched_fields == {
        "intent": "lost_or_stolen_card",
        "priority": "critical",
        "route": "card_security",
        "requires_human_review": True,
    }


def test_every_selected_intent_has_expected_output_fields() -> None:
    for intent in SELECTED_INTENTS:
        assert set(BUSINESS_RULES[intent]) == {
            "priority",
            "route",
            "requires_human_review",
        }

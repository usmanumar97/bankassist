# BANKING77 Dataset Notes

## 1. Document purpose

This document records the research, inspection, cleaning decisions, risks, and final preparation choices made for the BANKING77 dataset.

It should answer:

- what the dataset contains
- why it was selected
- which categories are being used
- how the data is distributed
- whether the data contains quality problems
- whether an `out_of_scope` category will be added in a later version
- how training, validation, and test data will be created
- what limitations may affect the final evaluation

This document will be updated during:

- dataset exploration
- dataset cleaning
- dataset splitting
- model evaluation
- error analysis

---

## 2. Dataset identity

### Dataset name

`PolyAI/banking77`

### Domain

Banking customer support and intent classification.

### Language

English.

### Task type

Intent classification from short customer-support messages.

### Original number of intents

77 banking-related intent categories.

### Original data fields

The dataset is expected to contain:

- `text`: the customer-support message
- `label`: the intent category

The actual field names and label representation must be confirmed during dataset exploration.

### Current inspection status

Inspected locally in `notebooks/01_dataset_exploration.ipynb`.

Confirmed:

- the dataset contains `train` and `test` splits
- records contain `text` and integer `label` fields
- the `label` feature contains ClassLabel metadata with readable intent names
- the current selected-intent filter has been explored in the notebook

---

## 3. Why this dataset was selected

BANKING77 was selected because it matches the project’s business problem closely.

The project requires a model that can understand short banking-support messages and classify them into operational categories.

The dataset is suitable because it contains:

- realistic banking-support questions
- labelled customer intents
- several closely related categories
- short natural-language messages
- enough examples to support supervised fine-tuning
- an existing train and test structure
- examples that resemble support tickets or chatbot messages

The dataset also creates realistic classification challenges.

For example, the model must distinguish between:

- a lost card
- a compromised card
- an unrecognised card payment
- an unrecognised cash withdrawal

These categories are related but require different business actions.

---

## 4. How the dataset relates to the project

The original dataset provides:

- a customer message
- an intent label

The original dataset does not provide:

- priority
- routing destination
- human-review requirement
- structured JSON output

The project will add these business fields using predefined routing rules.

The transformation will conceptually be:

Customer message  
→ Original intent  
→ Business priority  
→ Support route  
→ Human-review decision  
→ Structured training output

Example:

### Original dataset example

```text
Customer message:
I withdrew £100 but only received £50.

Intent:
wrong_amount_of_cash_received


```

### Project training target

```json
{
  "intent": "wrong_amount_of_cash_received",
  "priority": "high",
  "route": "atm_disputes",
  "requires_human_review": true
}
```

---

## 5. Selected supported intents

Version 1 of BankAssist Triage will directly support the following nine BANKING77 intents:

1. `lost_or_stolen_card`
2. `compromised_card`
3. `card_payment_not_recognised`
4. `cash_withdrawal_not_recognised`
5. `wrong_amount_of_cash_received`
6. `transfer_not_received_by_recipient`
7. `declined_card_payment`
8. `card_not_working`
9. `change_pin`

---

## 6. Reason for selecting these intents

The selected intents provide a mixture of:

- security-related requests
- fraud-related requests
- card-support requests
- ATM disputes
- transfer problems
- low-risk self-service requests

They also provide different levels of classification difficulty.

### Closely related security categories

The following categories may be difficult to distinguish:

- `lost_or_stolen_card`
- `compromised_card`
- `card_payment_not_recognised`
- `cash_withdrawal_not_recognised`

### Related card-support categories

The following categories may overlap:

- `declined_card_payment`
- `card_not_working`

### Transaction-related categories

The following categories involve delayed, missing, or incorrect transactions:

- `wrong_amount_of_cash_received`
- `transfer_not_received_by_recipient`

These selected categories will help determine whether the model understands the meaning of a message rather than relying only on obvious keywords.

---

## 7. Business label mapping

The project will attach the following business rules to each intent:

| Intent | Priority | Route | Human review |
|---|---|---|---|
| `lost_or_stolen_card` | critical | `card_security` | true |
| `compromised_card` | critical | `fraud_team` | true |
| `card_payment_not_recognised` | critical | `fraud_team` | true |
| `cash_withdrawal_not_recognised` | critical | `fraud_team` | true |
| `wrong_amount_of_cash_received` | high | `atm_disputes` | true |
| `transfer_not_received_by_recipient` | high | `transfers_team` | true |
| `declined_card_payment` | medium | `card_support` | false |
| `card_not_working` | medium | `card_support` | false |
| `change_pin` | low | `self_service` | false |

These mappings are simulated business rules created for this project.

They do not represent the real operational policies of a particular bank.

---

## 8. Out-of-scope construction strategy

Out-of-scope handling is deferred for the current preprocessing pass.

The active Version 1 dataset uses only the nine selected BANKING77 intents listed above. A future version may add `out_of_scope`, but that should be designed as a separate dataset version so baseline, SFT training, and evaluation remain comparable.

### Why random unrelated messages are insufficient

Messages such as:

```text
What is the weather today?
```

would make out-of-scope detection too easy.

The more realistic problem is distinguishing between:

```text
A supported banking request
```

and:

```text
A valid but unsupported banking request
```

---

## 9. Original dataset splits

BANKING77 is expected to provide official:

- training data
- test data

The exact split names and record counts must be confirmed during local dataset exploration.

### Planned use

The official training split will be divided into:

- a project training set
- a project validation set

The official test split will remain untouched for final evaluation.

The planned structure is:

```text
Official training split
├── Project training set
└── Project validation set

Official test split
└── Final project test set
```

### Important rule

The final test set must not be repeatedly used while:

- changing prompts
- selecting hyperparameters
- selecting model checkpoints
- modifying business mappings
- adjusting generation settings
- changing the dataset preparation process

Repeatedly using the test set during development would make the final evaluation less reliable.

---

## 10. Planned validation split

The current plan is:

- 85% of the selected official training examples for training
- 15% of the selected official training examples for validation
- selected official test examples for final testing

The training and validation split should be stratified by intent.

Stratification means that each category should maintain approximately the same proportion in both the training and validation sets.

The exact counts will be recorded after the dataset is inspected.

---

## 11. Class distribution

The current selected-intent dataset was created by running:

```text
conda run -n bankassist env PYTHONPATH=src python -m bankassist.data.preprocess
```

The enriched dataset was saved locally to:

```text
data/processed/business-labelled-v1
```

### Selected intent counts

| Intent | Official train count | Official test count | Total |
|---|---:|---:|---:|
| `lost_or_stolen_card` | 82 | 40 | 122 |
| `compromised_card` | 86 | 40 | 126 |
| `card_payment_not_recognised` | 168 | 40 | 208 |
| `cash_withdrawal_not_recognised` | 160 | 40 | 200 |
| `wrong_amount_of_cash_received` | 180 | 40 | 220 |
| `transfer_not_received_by_recipient` | 171 | 40 | 211 |
| `declined_card_payment` | 153 | 40 | 193 |
| `card_not_working` | 112 | 40 | 152 |
| `change_pin` | 122 | 40 | 162 |

### Questions to answer

- Are the selected classes balanced?
- Which intent has the most examples?
- Which intent has the fewest examples?
- Is resampling necessary?

### Current findings

The official test split is balanced for the nine selected intents, with 40 examples per intent.

The selected official training subset is moderately imbalanced. `wrong_amount_of_cash_received` has the most training examples with 180, while `lost_or_stolen_card` has the fewest with 82. This does not need to be fixed before enrichment, but it should be considered during train/validation splitting and evaluation.

---

## 12. Missing-value inspection

The following checks must be performed:

- missing customer messages
- empty strings
- whitespace-only messages
- missing labels
- invalid label IDs
- unexpected data types

### Results

| Check | Result |
|---|---|
| Missing text values | Pending |
| Empty messages | Pending |
| Whitespace-only messages | Pending |
| Missing labels | Pending |
| Invalid labels | Pending |
| Unexpected data types | Pending |

### Final decision

Pending dataset exploration.

---

## 13. Duplicate inspection

The dataset must be checked for:

- exact duplicate messages inside the training split
- exact duplicate messages inside the test split
- identical messages appearing in both training and test sets
- duplicate messages with different labels
- messages differing only by capitalisation
- messages differing only by surrounding whitespace

### Why duplicates matter

If the same message appears in both training and testing, the model may memorise the expected answer.

This could make the evaluation look stronger than the model’s actual ability to generalise to unseen messages.

### Results

| Duplicate type | Count |
|---|---:|
| Exact duplicates in training | Pending |
| Exact duplicates in test | Pending |
| Exact train-test overlap | Pending |
| Duplicates with conflicting labels | Pending |
| Case-insensitive duplicates | Pending |

### Final decision

Pending dataset exploration.

---

## 14. Near-duplicate inspection

Exact duplicate checks are not enough.

Messages may contain almost identical wording.

For example:

```text
My card payment was declined.
```

and:

```text
Why was my card payment declined?
```

These are not exact duplicates, but they are extremely similar.

The following should be investigated:

- repeated sentence templates
- small spelling variations
- punctuation-only differences
- singular and plural variations
- messages with only one word changed
- paraphrases appearing across different splits

### Risk

Near-duplicate leakage may cause the final test score to measure memorisation instead of genuine generalisation.

### Planned approach

The initial exploration should identify:

- common repeated phrases
- suspiciously similar messages
- similarities between training and test examples
- examples that may require manual inspection

More advanced semantic duplicate detection may be considered later if necessary.

### Findings

Pending dataset exploration.

---

## 15. Message-length analysis

The dataset should be analysed using:

- character count
- word count
- token count during the later tokenisation phase

### Statistics to record

| Statistic | Characters | Words |
|---|---:|---:|
| Minimum | Pending | Pending |
| Maximum | Pending | Pending |
| Mean | Pending | Pending |
| Median | Pending | Pending |
| 95th percentile | Pending | Pending |

### Questions to answer

- Are most messages only one sentence?
- Are any messages unusually long?
- Are some messages only one or two words long?
- Do very short messages create ambiguity?
- What sequence length is likely to be sufficient later?

### Findings

Pending dataset exploration.

---

## 16. Text-quality inspection

The dataset should be manually checked for:

- spelling errors
- grammatical errors
- informal language
- abbreviations
- missing punctuation
- unclear wording
- incomplete questions
- repeated templates
- unusual characters
- personally identifiable information

### Expected cleaning position

Spelling and grammatical errors should generally not be automatically corrected.

Real customer messages often contain:

- informal language
- typing mistakes
- incomplete sentences
- missing punctuation

Cleaning these messages too heavily could make the dataset less representative of real customer-support traffic.

### Findings

Pending dataset exploration.

---

## 17. Ambiguous examples

Some customer messages may reasonably fit more than one intent.

Potentially difficult distinctions include the following.

### Lost card versus compromised card

```text
I think someone has access to my card.
```

This does not clearly state whether the physical card is missing.

### Compromised card versus unrecognised payment

```text
Someone may have used my card.
```

It may be unclear whether an actual payment has already appeared.

### Card not working versus declined card payment

```text
My card keeps failing.
```

It may not explain whether the issue is a specific declined payment or a more general card problem.

### Refund not received versus transfer not received

Some messages may refer to missing money without clearly identifying the transaction type.

### Manual-review table

| Customer message | Dataset label | Possible alternative | Notes |
|---|---|---|---|
| Pending | Pending | Pending | Pending |

### Findings

Pending manual inspection.

---

## 18. Label-quality inspection

The following questions should be investigated:

- Do examples consistently match their assigned intent?
- Are any examples obviously mislabelled?
- Are category definitions sufficiently clear?
- Are some labels too similar to separate reliably?
- Do some messages require external context?
- Are some intents identifiable only through one keyword?
- Are the same phrases used for different labels?

### Findings

Pending dataset exploration.

---

## 19. Data leakage risks

Potential data leakage risks include the following.

### Exact message leakage

The same message may appear in both training and test data.

### Near-duplicate leakage

Very similar messages may appear across different dataset splits.

### Template leakage

Repeated sentence structures may make classification artificially easy.

### Label-word leakage

Some customer messages may explicitly contain a category-specific phrase that makes the answer obvious.

### Pretraining contamination

The base model may already have encountered BANKING77 or copies of the dataset during its original training.

This cannot be fully verified for a public pretrained model.

### Development leakage

Repeatedly examining and optimising against the final test set can contaminate the evaluation.

### Planned controls

- preserve the official test split
- avoid tuning based on final test performance
- check for exact train-test duplicates
- inspect near-duplicate examples
- use a separate validation set during development
- document any suspected contamination
- compare the fine-tuned model with the untouched base model

---

## 20. Personally identifiable information

The dataset should be inspected for information such as:

- real names
- account numbers
- card numbers
- telephone numbers
- email addresses
- physical addresses
- transaction references

### Findings

Pending dataset exploration.

### Planned action

Any genuine sensitive information discovered should be removed or anonymised before model training.

---

## 21. Dataset licence

The dataset licence must be confirmed using the official dataset source.

The following information must be recorded:

- licence name
- attribution requirements
- whether modification is permitted
- whether redistribution is permitted
- whether commercial use is permitted
- required dataset citation

### Confirmed licence

Pending verification from the official dataset documentation.

### Required attribution

Pending verification.

---

## 22. Dataset limitations

Expected limitations include:

- English-language data only
- short, single-message inputs
- no previous conversation history
- no customer account context
- no live transaction data
- no bank-specific policies
- no reliable customer demographic information
- limited representation of long or complex complaints
- possible ambiguity between similar intents
- possible duplicate or near-duplicate examples
- simulated business-routing labels
- unknown overlap with the base model’s original training data

These limitations must be considered when interpreting final model performance.

---

## 23. Dataset bias considerations

The dataset may not represent:

- every English dialect
- every spelling style
- all levels of English proficiency
- multilingual banking customers
- elderly or vulnerable customers
- extremely complex financial disputes
- customers using speech-to-text
- long-form complaints
- customers with accessibility requirements

A high score on BANKING77 will not prove that the model performs equally well on real-world banking traffic.

---

## 24. Cleaning policy

The default cleaning policy will be conservative.

### Permitted cleaning

- remove empty records
- remove exact duplicates when justified
- normalise accidental leading and trailing whitespace
- validate labels
- remove or anonymise genuine sensitive information
- correct technical formatting problems

### Cleaning to avoid

- rewriting customer messages
- correcting every spelling mistake
- converting informal language into formal language
- removing meaningful punctuation
- simplifying difficult examples
- changing labels without documented evidence
- deleting ambiguous examples only to improve evaluation scores

The goal is to preserve realistic customer language.

---

## 25. Dataset versioning

Every prepared dataset should have an identifiable version.

Suggested versions include:

```text
raw-v1
selected-intents-v1
business-labelled-v1
split-v1
instruction-formatted-v1
```

For every version, record:

- creation date
- source dataset version
- selected categories
- filtering rules
- duplicate-handling rules
- out-of-scope sampling rules
- split seed
- record counts
- file locations

This will help ensure that experiments can be reproduced.

---

## 26. Reproducibility decisions

The following decisions must be fixed and documented before creating the final data splits:

- random seed
- selected intent list
- excluded intent list
- out-of-scope source categories
- number of out-of-scope examples
- validation percentage
- stratification method
- duplicate-handling method
- final output schema

### Current decisions

| Decision | Value |
|---|---|
| Supported intents | 9 |
| Additional project intent | None in current preprocessing pass |
| Validation percentage | 15% of selected official training data |
| Final test source | Official BANKING77 test split |
| Random seed | Pending |
| Out-of-scope sample size | Deferred |
| Out-of-scope source strategy | Deferred |
| Duplicate policy | Pending inspection |

---

## 27. Dataset exploration deliverables

Phase 2 should produce:

- dataset structure summary
- list of all original intent names
- selected category counts
- excluded category counts
- class-distribution chart
- sample messages from every selected intent
- missing-value report
- exact-duplicate report
- initial near-duplicate findings
- message-length statistics
- ambiguous-example table
- licence confirmation
- final out-of-scope construction decision

Generated charts should be stored in:

```text
reports/figures/
```

Generated numerical summaries should be stored in:

```text
reports/metrics/
```

---

## 28. Final dataset decisions

This section will be completed at the end of the dataset exploration and preparation phases.

### Final selected intents

Confirmed as the nine intents listed in Section 5.

### Final out-of-scope source categories

Deferred.

### Final class sizes

Current enriched dataset size:

- train: 1,234 records
- test: 360 records
- total: 1,594 records

### Final duplicate policy

Pending inspection.

### Final validation split

Pending creation.

### Final test split

Created from the official BANKING77 test split for the nine selected intents.

### Final cleaning rules

Pending inspection.

### Final dataset limitations

Pending completed audit.

---

## 29. Current status

### Phase 0 — Environment and repository setup

Status: Completed

### Phase 1 — Project scope and research design

Status: Completed

### Phase 2 — Dataset exploration

Status: In progress

BANKING77 has been inspected enough to confirm schema, label metadata, selected intents, filtering logic, and class counts.

The preprocessing pipeline now filters the selected intents, derives readable intent names from ClassLabel metadata, adds business-rule fields, preserves the original integer label, and saves the enriched dataset to `data/processed/business-labelled-v1`.

Deeper quality checks, including duplicate review, message-length analysis, and ambiguous-example review, remain pending.

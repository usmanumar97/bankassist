# BankAssist Triage — Experiment Log

## 1. Document purpose

This document records every meaningful experiment performed during the BankAssist Triage project.

The experiment log exists to make the project:

- reproducible
- organised
- comparable
- auditable
- easier to debug
- easier to explain in a portfolio or interview

Each experiment should record:

- what was tested
- why it was tested
- what data was used
- what model was used
- which settings were used
- what results were obtained
- what problems occurred
- what was learned
- what decision was made next

This document should be updated immediately after every experiment.

---

## 2. What counts as an experiment

An experiment is any controlled test that helps answer a project question.

Examples include:

- evaluating the untouched base model
- comparing two prompt formats
- testing JSON output reliability
- measuring inference speed
- testing different LoRA configurations
- comparing training epochs
- comparing learning rates
- evaluating different checkpoints
- testing different dataset versions
- measuring the effect of class balancing
- testing out-of-scope detection
- comparing the base and fine-tuned models

Routine actions are not necessarily experiments.

Examples of routine actions include:

- creating directories
- installing a package
- renaming a file
- formatting Markdown
- committing documentation

However, environment changes that affect results should still be documented.

---

## 3. Experiment naming convention

Every experiment will use a unique identifier.

Format:

```text
EXP-XXX
```

Examples:

```text
EXP-001
EXP-002
EXP-003
```

The numbers should increase sequentially.

Experiment folders and generated files may use a more descriptive format:

```text
EXP-001-base-model-baseline
EXP-002-prompt-format-comparison
EXP-003-lora-first-run
```

---

## 4. Dataset version naming

Every experiment must identify the exact dataset version used.

Planned dataset versions include:

```text
raw-v1
selected-intents-v1
business-labelled-v1
split-v1
instruction-formatted-v1
```

An experiment must not simply say:

```text
BANKING77 dataset
```

It should say something more precise, such as:

```text
instruction-formatted-v1
```

The dataset version should identify:

- selected categories
- filtering rules
- duplicate policy
- out-of-scope construction
- train-validation-test split
- random seed

---

## 5. Model version naming

The model used in every experiment must be recorded precisely.

Examples:

```text
Qwen/Qwen3-0.6B
Qwen/Qwen3-0.6B + LoRA adapter EXP-003
Qwen/Qwen3-0.6B + LoRA adapter EXP-006 checkpoint-500
```

Do not record the model only as:

```text
Qwen
```

The exact model and adapter must be identifiable.

---

## 6. Experiment status values

Every experiment should have one of the following statuses:

| Status | Meaning |
|---|---|
| `planned` | Designed but not started |
| `running` | Currently executing |
| `completed` | Finished successfully |
| `failed` | Could not complete because of an error |
| `stopped` | Intentionally stopped before completion |
| `invalid` | Completed, but the results cannot be trusted |
| `superseded` | Replaced by a better or corrected experiment |

A failed experiment should remain in the log.

Failed experiments often contain useful information.

---

## 7. Experiment summary table

Update this table whenever a new experiment is created.

| Experiment | Name | Phase | Status | Primary result | Decision |
|---|---|---|---|---|---|
| `EXP-001` | Base-model baseline | Phase 3 | Planned | Pending | Pending |
| `EXP-002` | Initial LoRA fine-tuning | Phase 6 | Planned | Pending | Pending |

More experiments will be added as the project progresses.

---

# Experiment records

---

## EXP-001 — Base-model baseline

### General information

| Field | Value |
|---|---|
| Experiment ID | `EXP-001` |
| Experiment name | Base-model baseline |
| Project phase | Phase 3 — Base-model baseline |
| Status | Planned |
| Date started | Pending |
| Date completed | Pending |
| Researcher | Osman Janjua |
| Git commit | Pending |

### Objective

Measure how well the untouched `Qwen/Qwen3-0.6B` model performs on the BankAssist Triage task before fine-tuning.

This experiment will establish the baseline against which the fine-tuned model will be compared.

### Research question

How accurately can the original Qwen3-0.6B model classify and route banking-support messages using prompting alone?

### Hypothesis

The base model is expected to understand many customer messages, but it may:

- confuse closely related banking intents
- produce inconsistent JSON
- use unsupported intent names
- assign incorrect priorities
- assign incorrect routes
- add unwanted explanations
- perform poorly on out-of-scope messages

Fine-tuning is expected to improve consistency and classification performance.

### Independent variable

The untouched base model using the project prompt and output schema.

### Dependent variables

The following results will be measured:

- intent accuracy
- macro-F1
- per-class precision
- per-class recall
- critical-case recall
- out-of-scope recall
- priority accuracy
- route accuracy
- human-review accuracy
- JSON validity rate
- inference latency

### Controlled conditions

The following should remain fixed when comparing the base and fine-tuned models:

- test dataset
- system instruction
- supported intent list
- output schema
- generation settings
- evaluation logic
- hardware environment

### Dataset

| Field | Value |
|---|---|
| Source dataset | `PolyAI/banking77` |
| Dataset version | Pending |
| Split used | Validation or baseline evaluation split |
| Number of records | Pending |
| Supported categories | 10 plus `out_of_scope` |
| Random seed | Pending |

The official final test set should not be used repeatedly during baseline development.

### Model

| Field | Value |
|---|---|
| Base model | `Qwen/Qwen3-0.6B` |
| Model type | Post-trained causal language model |
| Fine-tuned | No |
| Adapter | None |
| Quantisation | Pending |
| Device | Pending |

### Prompt configuration

| Field | Value |
|---|---|
| Prompt version | Pending |
| Thinking mode | Disabled |
| Output format | JSON |
| Temperature | Pending |
| Maximum generated tokens | Pending |
| Sampling enabled | Pending |

### Expected output format

```json
{
  "intent": "wrong_amount_of_cash_received",
  "priority": "high",
  "route": "atm_disputes",
  "requires_human_review": true
}
```

### Hardware

| Field | Value |
|---|---|
| Computer | Osman’s MacBook Pro |
| Processor architecture | Pending |
| Chip | Pending |
| Memory | Pending |
| Accelerator | Pending |

### Software environment

| Field | Value |
|---|---|
| Operating system | macOS |
| Python | 3.11.15 |
| Conda environment | `bankassist` |
| PyTorch version | Pending |
| Transformers version | Pending |
| Datasets version | Pending |
| PEFT version | Not applicable |
| TRL version | Not applicable |

### Results

| Metric | Result |
|---|---:|
| Intent accuracy | Pending |
| Macro-F1 | Pending |
| Critical-case recall | Pending |
| Out-of-scope recall | Pending |
| Priority accuracy | Pending |
| Route accuracy | Pending |
| Human-review accuracy | Pending |
| JSON validity | Pending |
| Mean inference latency | Pending |

### Per-class results

| Intent | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| `lost_or_stolen_card` | Pending | Pending | Pending | Pending |
| `compromised_card` | Pending | Pending | Pending | Pending |
| `card_payment_not_recognised` | Pending | Pending | Pending | Pending |
| `cash_withdrawal_not_recognised` | Pending | Pending | Pending | Pending |
| `wrong_amount_of_cash_received` | Pending | Pending | Pending | Pending |
| `transfer_not_received_by_recipient` | Pending | Pending | Pending | Pending |
| `refund_not_showing_up` | Pending | Pending | Pending | Pending |
| `declined_card_payment` | Pending | Pending | Pending | Pending |
| `card_not_working` | Pending | Pending | Pending | Pending |
| `change_pin` | Pending | Pending | Pending | Pending |
| `out_of_scope` | Pending | Pending | Pending | Pending |

### Observations

Pending experiment.

Record observations such as:

- common intent confusions
- invalid JSON patterns
- additional unwanted text
- inconsistent capitalisation
- unsupported output values
- missed critical cases
- unusual response delays

### Errors and failures

Pending experiment.

Record:

- technical errors
- model-loading errors
- memory errors
- JSON parsing errors
- interrupted runs
- invalid evaluation records

### Artifacts

| Artifact | Location |
|---|---|
| Raw predictions | Pending |
| Metrics | `reports/metrics/` |
| Confusion matrix | `reports/figures/` |
| Error analysis | `reports/error_analysis/` |
| Prompt configuration | Pending |

### Conclusion

Pending experiment.

### Decision

Pending experiment.

### Next action

Complete dataset exploration and preparation before running the baseline evaluation.

---

## EXP-002 — Initial LoRA fine-tuning

### General information

| Field | Value |
|---|---|
| Experiment ID | `EXP-002` |
| Experiment name | Initial LoRA fine-tuning |
| Project phase | Phase 6 — LoRA fine-tuning |
| Status | Planned |
| Date started | Pending |
| Date completed | Pending |
| Researcher | Osman Janjua |
| Git commit | Pending |

### Objective

Perform the first supervised fine-tuning experiment using LoRA on `Qwen/Qwen3-0.6B`.

The purpose is to determine whether the model can learn the project’s supported intents, business rules, and structured JSON output.

### Research question

Does supervised fine-tuning with LoRA improve BankAssist Triage performance compared with the untouched base-model baseline?

### Hypothesis

The LoRA fine-tuned model is expected to:

- improve intent macro-F1
- improve critical-case recall
- improve JSON validity
- produce only permitted output values
- apply the business-routing rules more consistently
- improve out-of-scope detection

### Dataset

| Field | Value |
|---|---|
| Source dataset | `PolyAI/banking77` |
| Dataset version | Pending |
| Training split | Pending |
| Validation split | Pending |
| Number of training records | Pending |
| Number of validation records | Pending |
| Random seed | Pending |

### Model

| Field | Value |
|---|---|
| Base model | `Qwen/Qwen3-0.6B` |
| Training technique | Supervised fine-tuning |
| Parameter-efficient method | LoRA |
| Quantisation | Pending |
| Device | Pending |

### LoRA configuration

| Parameter | Value |
|---|---|
| Rank | Pending |
| Alpha | Pending |
| Dropout | Pending |
| Target modules | Pending |
| Bias configuration | Pending |
| Trainable parameter count | Pending |
| Trainable parameter percentage | Pending |

### Training configuration

| Parameter | Value |
|---|---|
| Epochs | Pending |
| Learning rate | Pending |
| Training batch size | Pending |
| Evaluation batch size | Pending |
| Gradient accumulation | Pending |
| Effective batch size | Pending |
| Maximum sequence length | Pending |
| Optimiser | Pending |
| Weight decay | Pending |
| Warm-up ratio or steps | Pending |
| Learning-rate scheduler | Pending |
| Evaluation frequency | Pending |
| Checkpoint frequency | Pending |
| Early stopping | Pending |
| Mixed precision | Pending |
| Random seed | Pending |

### Training results

| Metric | Result |
|---|---:|
| Initial training loss | Pending |
| Final training loss | Pending |
| Best validation loss | Pending |
| Final validation loss | Pending |
| Best checkpoint | Pending |
| Total training time | Pending |
| Maximum memory usage | Pending |

### Final evaluation results

| Metric | Base model | Fine-tuned model | Difference |
|---|---:|---:|---:|
| Intent accuracy | Pending | Pending | Pending |
| Macro-F1 | Pending | Pending | Pending |
| Critical-case recall | Pending | Pending | Pending |
| Out-of-scope recall | Pending | Pending | Pending |
| Priority accuracy | Pending | Pending | Pending |
| Route accuracy | Pending | Pending | Pending |
| Human-review accuracy | Pending | Pending | Pending |
| JSON validity | Pending | Pending | Pending |
| Mean inference latency | Pending | Pending | Pending |

### Observations

Pending experiment.

Record observations such as:

- whether training and validation loss decreased
- whether overfitting appeared
- which intents improved
- which intents remained difficult
- whether JSON output became consistent
- whether the model learned the business mappings
- whether new failure patterns appeared

### Errors and failures

Pending experiment.

### Artifacts

| Artifact | Location |
|---|---|
| LoRA adapter | `models/adapters/` |
| Checkpoints | `models/checkpoints/` |
| Training metrics | `reports/metrics/` |
| Evaluation metrics | `reports/metrics/` |
| Confusion matrix | `reports/figures/` |
| Error-analysis report | `reports/error_analysis/` |
| Training configuration | `configs/` |

### Conclusion

Pending experiment.

### Decision

Pending experiment.

### Next action

Pending experiment results.

---

# Blank experiment template

Copy this section whenever a new experiment is created.

---

## EXP-XXX — Experiment name

### General information

| Field | Value |
|---|---|
| Experiment ID | `EXP-XXX` |
| Experiment name | Pending |
| Project phase | Pending |
| Status | Planned |
| Date started | Pending |
| Date completed | Pending |
| Researcher | Osman Janjua |
| Git commit | Pending |

### Objective

Describe exactly what this experiment is trying to determine.

### Research question

State the specific question being investigated.

### Hypothesis

State the expected result and why it is expected.

### Reason for running this experiment

Explain why the experiment is necessary and what previous finding led to it.

### Independent variable

Describe what is intentionally being changed.

### Dependent variables

Describe what will be measured.

### Controlled conditions

List everything that must remain unchanged for a fair comparison.

### Dataset

| Field | Value |
|---|---|
| Source dataset | Pending |
| Dataset version | Pending |
| Split used | Pending |
| Number of records | Pending |
| Random seed | Pending |

### Model

| Field | Value |
|---|---|
| Base model | Pending |
| Adapter | Pending |
| Checkpoint | Pending |
| Quantisation | Pending |
| Device | Pending |

### Prompt configuration

| Field | Value |
|---|---|
| Prompt version | Pending |
| Output schema version | Pending |
| Temperature | Pending |
| Maximum generated tokens | Pending |
| Sampling enabled | Pending |

### Training configuration

Complete this section only for training experiments.

| Parameter | Value |
|---|---|
| Training technique | Pending |
| Epochs | Pending |
| Learning rate | Pending |
| Batch size | Pending |
| Gradient accumulation | Pending |
| Effective batch size | Pending |
| Maximum sequence length | Pending |
| Optimiser | Pending |
| Scheduler | Pending |
| Warm-up | Pending |
| Weight decay | Pending |
| Random seed | Pending |

### LoRA configuration

Complete this section only for LoRA experiments.

| Parameter | Value |
|---|---|
| Rank | Pending |
| Alpha | Pending |
| Dropout | Pending |
| Target modules | Pending |
| Trainable parameters | Pending |
| Trainable parameter percentage | Pending |

### Hardware

| Field | Value |
|---|---|
| Computer | Pending |
| Processor or chip | Pending |
| Memory | Pending |
| Accelerator | Pending |

### Software environment

| Field | Value |
|---|---|
| Operating system | Pending |
| Python version | Pending |
| PyTorch version | Pending |
| Transformers version | Pending |
| Datasets version | Pending |
| PEFT version | Pending |
| TRL version | Pending |

### Results

| Metric | Result |
|---|---:|
| Intent accuracy | Pending |
| Macro-F1 | Pending |
| Critical-case recall | Pending |
| Out-of-scope recall | Pending |
| Priority accuracy | Pending |
| Route accuracy | Pending |
| Human-review accuracy | Pending |
| JSON validity | Pending |
| Mean inference latency | Pending |

### Comparison with previous experiment

| Metric | Previous experiment | Current experiment | Difference |
|---|---:|---:|---:|
| Intent accuracy | Pending | Pending | Pending |
| Macro-F1 | Pending | Pending | Pending |
| Critical-case recall | Pending | Pending | Pending |
| JSON validity | Pending | Pending | Pending |

### Observations

Record factual observations from the experiment.

Examples:

- training loss decreased consistently
- validation loss increased after the second epoch
- the model confused two related categories
- JSON output became more reliable
- inference became slower
- one class had significantly lower recall

### Errors and unexpected behaviour

Record:

- technical errors
- memory problems
- invalid outputs
- interrupted training
- configuration mistakes
- unreliable measurements
- data leakage concerns

### Error analysis

| Input message | Expected intent | Predicted intent | Error type | Notes |
|---|---|---|---|---|
| Pending | Pending | Pending | Pending | Pending |

### Artifacts

| Artifact | Location |
|---|---|
| Configuration | Pending |
| Predictions | Pending |
| Metrics | Pending |
| Model or adapter | Pending |
| Checkpoint | Pending |
| Figures | Pending |
| Error-analysis report | Pending |

### Conclusion

Summarise what the experiment demonstrated.

### Decision

Record the decision made from the results.

Possible decisions include:

- keep this configuration
- reject this configuration
- repeat with corrected data
- reduce the learning rate
- increase training examples
- stop training earlier
- investigate one weak intent
- compare another prompt
- use a different checkpoint

### Next action

State the exact next experiment or project task.

---

## Experiment logging rules

1. Never overwrite or delete an unsuccessful experiment.
2. Give every experiment a unique ID.
3. Record the exact dataset version.
4. Record the exact model and adapter.
5. Change one major variable at a time where possible.
6. Use the validation set for development decisions.
7. Preserve the final test set for final evaluation.
8. Record random seeds.
9. Record package versions.
10. Save generated metrics and artifacts.
11. Explain why an experiment was accepted or rejected.
12. Mark unreliable experiments as `invalid`.
13. Record failures immediately rather than relying on memory.
14. Link experiment results to the relevant Git commit.
15. Do not report only the best result while hiding weaker runs.

---

## Current project status

### Phase 0 — Environment and repository setup

Status: Completed

### Phase 1 — Project scope and research design

Status: Completed

### Phase 2 — Dataset exploration

Status: Not started

### Experiments completed

None.

### Next planned experiment

`EXP-001 — Base-model baseline`

This experiment will be performed only after the required dataset has been explored and prepared.
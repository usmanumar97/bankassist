# BankAssist Triage — Project Scope

## 1. Project description

BankAssist Triage is a local small-language-model project designed to automate the initial triage of banking customer-support messages.

The system will receive a short customer message, identify the type of banking issue, determine its urgency, assign it to the appropriate support team, and indicate whether the case requires human review.

The model will run locally and will be fine-tuned for this specific business task.

The purpose of the project is not to build a complete banking chatbot. Version 1 focuses only on understanding, classifying, prioritising, and routing customer-support requests.

---

## 2. Business problem

Digital banks and financial-support teams receive large numbers of customer messages every day.

Before a support agent can respond, each message must be:

1. Read and understood.
2. Categorised by issue.
3. Assigned a priority.
4. Routed to the correct team.
5. Escalated when fraud or account security may be involved.

This process is repetitive and can be inconsistent when performed manually.

Incorrect triage can result in:

- delayed responses
- tickets being sent to the wrong department
- urgent fraud cases not being recognised quickly
- inconsistent priority decisions
- unnecessary work for customer-support agents

The business needs a system that can support the first stage of ticket handling.

---

## 3. Problem statement

The project aims to determine whether a locally running small language model can be fine-tuned to reliably classify and route banking customer-support messages.

The model must convert a customer message into a structured business decision containing:

- the customer’s intent
- the priority of the issue
- the team responsible for handling it
- whether human review is required

The fine-tuned model will be compared with the original, non-fine-tuned model to measure whether supervised fine-tuning provides a meaningful improvement.

---

## 4. Research question

Can supervised fine-tuning with LoRA improve the ability of a 0.6-billion-parameter language model to classify and route banking customer-support messages compared with prompting the original model?

---

## 5. Proposed solution

The proposed solution is a small language model fine-tuned on labelled banking customer-support messages.

The system will follow this flow:

```text
Customer message
→ Small language model
→ Structured triage decision
→ Human support agent or ticket-management system
```

The model will assist with decision-making, but it will not perform real banking actions.

---

## 6. Target users

The primary users are:

- banking customer-support agents
- support-team supervisors
- automated ticket-management systems
- fraud and security triage teams

The direct user of Version 1 is not necessarily the bank customer.

The model produces a recommendation that can be reviewed by a human or consumed by another business system.

---

## 7. Model input

The model will receive one short English-language banking support message.

Example:

> I withdrew £100, but the cash machine only gave me £50.

Version 1 will not receive:

- customer account details
- transaction history
- previous conversation messages
- customer identity
- uploaded documents
- live banking data
- company policy documents

---

## 8. Model output

The model will return structured JSON containing four fields:

```json
{
  "intent": "wrong_amount_of_cash_received",
  "priority": "high",
  "route": "atm_disputes",
  "requires_human_review": true
}
```

### Intent

The category that best represents the customer’s request.

### Priority

The urgency of the request.

Allowed values:

- `low`
- `medium`
- `high`
- `critical`

### Route

The support team or process responsible for handling the request.

### Requires human review

A Boolean value indicating whether an employee must review the case.

Allowed values:

- `true`
- `false`

---

## 9. Supported intents

Version 1 will support the following nine banking intents:

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

## 10. Business routing rules

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

These rules are simulated project assumptions.

They do not represent the real operational policies of a specific bank.

---

## 11. Selected dataset

The selected dataset is:

```text
PolyAI/banking77
```

BANKING77 contains short English-language banking customer-support messages labelled by intent.

The original dataset contains 77 banking intents.

For the current Version 1 preprocessing pass:

- nine original intents will be directly supported
- the official test split will be preserved for final evaluation
- part of the official training split will be used for validation

The dataset will eventually be divided into:

- training data
- validation data
- final test data

---

## 12. Selected base model

The selected model is:

```text
Qwen/Qwen3-0.6B
```

The post-trained version will be used.

Reasons for selecting it include:

- it is small enough for local experimentation
- it already understands instructions
- it supports conversational formatting
- it is compatible with Hugging Face tools
- it can be fine-tuned using LoRA
- experiments can be repeated without very expensive hardware

The model will be used in non-thinking mode because the task is structured classification rather than complex reasoning.

---

## 13. Selected fine-tuning technique

The selected technique is:

```text
Supervised Fine-Tuning with Low-Rank Adaptation
```

Abbreviation:

```text
SFT with LoRA
```

Supervised fine-tuning will teach the model using examples containing:

- a system instruction
- a customer message
- the expected structured JSON output

LoRA will train a relatively small set of adapter parameters while keeping the original model weights frozen.

This reduces:

- memory requirements
- training time
- storage requirements
- the cost of repeating experiments

---

## 14. Training-example structure

Each training example will conceptually contain three roles.

### System instruction

The system instruction will define:

- the task
- the permitted intents
- the permitted priority values
- the permitted routes
- the required JSON schema
- the rule that no explanation should be added

### User message

Example:

```text
Someone used my card and I do not recognise the purchase.
```

### Expected assistant output

```json
{
  "intent": "card_payment_not_recognised",
  "priority": "critical",
  "route": "fraud_team",
  "requires_human_review": true
}
```

---

## 15. Baseline strategy

Before fine-tuning, the original Qwen3-0.6B model will be evaluated on the same task.

The baseline model and fine-tuned model will use the same:

- system instruction
- intent list
- output schema
- test messages
- thinking-mode setting
- generation settings
- evaluation logic
- evaluation metrics

The comparison will answer:

> Did fine-tuning improve the model compared with prompting the original model?

Without a baseline, a strong final score would not prove that fine-tuning was useful.

---

## 16. Evaluation metrics

The model will not be evaluated using accuracy alone.

The following metrics will be measured:

- intent accuracy
- macro-F1 score
- precision for each intent
- recall for each intent
- F1-score for each intent
- critical-case recall
- out-of-scope recall
- priority accuracy
- route accuracy
- human-review accuracy
- JSON validity rate
- confusion matrix
- local inference latency

### Primary metric

The primary metric will be:

```text
Macro-F1
```

Macro-F1 gives equal importance to every intent, even when class sizes differ.

### Safety-related metric

Critical-case recall will also be treated as important.

This measures how many genuine fraud and security cases are correctly identified as critical.

---

## 17. Success criteria

The initial targets are:

| Metric | Target |
|---|---:|
| Intent accuracy | 85% or higher |
| Macro-F1 | 0.82 or higher |
| Critical-case recall | 95% or higher |
| JSON validity | 99% or higher |
| Priority accuracy | 90% or higher |
| Route accuracy | 90% or higher |
| Out-of-scope recall | 80% or higher |
| Macro-F1 improvement over baseline | At least 10 percentage points |

These are experimental targets rather than guaranteed results.

A result below the targets may still be useful if the causes are properly investigated and documented.

---

## 18. Project boundaries

Version 1 will include:

- English-language messages
- one customer message at a time
- nine supported banking intents
- structured JSON output
- local model inference
- supervised fine-tuning
- LoRA adapters
- comparison with the original model
- human-reviewed decisions

Version 1 will not include:

- real customer accounts
- transaction data
- payment processing
- card freezing
- refund execution
- financial advice
- customer identity verification
- customer-facing response generation
- multi-turn conversations
- RAG
- vector databases
- knowledge graphs
- agents
- external tool calling
- multilingual support
- autonomous business decisions

---

## 19. Model safety rules

The model must not:

- claim that it accessed a customer account
- claim that a transaction was verified
- claim that a card was frozen
- promise that a refund will be issued
- ask for a full card number
- ask for a PIN
- ask for a password
- provide financial or investment advice
- invent banking policies
- produce unsupported intent names
- produce unsupported routes
- make final fraud decisions

Out-of-scope or uncertain requests should be routed to human review.

---

## 20. Ethical and operational limitations

The system is an experimental support tool and not a production banking system.

Important limitations include:

- the dataset contains short messages
- only English is supported
- no customer history is available
- no real account context is available
- no live transaction information is available
- some intent categories may overlap
- the business-routing rules are simulated
- the model may produce incorrect classifications
- the model may produce invalid JSON
- the model may rely too heavily on keywords
- the public dataset may have appeared in the model’s original training data
- test performance may not represent real banking traffic

The model must not be trusted to make autonomous financial decisions.

---

## 21. Expected project outcome

The final project should demonstrate:

1. How a business problem is translated into a machine-learning task.
2. How a public dataset is researched and audited.
3. How an untouched language model is evaluated.
4. How an SLM is fine-tuned using SFT and LoRA.
5. How structured outputs are validated.
6. How model performance is measured.
7. How classification errors are investigated.
8. How the trained model can run locally.
9. Whether fine-tuning provides a measurable improvement over prompting alone.

---

## 22. Project phases

### Phase 0 — Environment and repository setup

Tasks:

- configure VS Code
- create a Python environment
- initialise Git
- create the project directories
- create research documentation

Status: Completed

### Phase 1 — Project scope and research design

Tasks:

- define the business problem
- select the dataset
- select the model
- select the fine-tuning technique
- define the output schema
- define project boundaries
- define success criteria

Status: Completed

### Phase 2 — Dataset exploration

Tasks:

- download BANKING77
- inspect dataset structure
- inspect all labels
- analyse class distribution
- inspect missing values
- inspect duplicates
- inspect message lengths
- identify ambiguous examples
- verify the licence
- plan the out-of-scope class

Status: Not started

### Phase 3 — Base-model baseline

Tasks:

- load the original model
- define the final prompt
- run inference before fine-tuning
- evaluate structured output
- record baseline metrics
- identify common errors

Status: Not started

### Phase 4 — Dataset preparation

Tasks:

- select supported categories
- create the out-of-scope class
- add business labels
- create train and validation sets
- preserve the official test set
- format examples for supervised fine-tuning

Status: Not started

### Phase 5 — Tokenisation and training preparation

Tasks:

- inspect the tokenizer
- inspect the chat template
- analyse token lengths
- choose a maximum sequence length
- prepare model labels
- choose the training configuration

Status: Not started

### Phase 6 — LoRA fine-tuning

Tasks:

- attach LoRA adapters
- train the model
- monitor training loss
- monitor validation loss
- save checkpoints
- select the best adapter

Status: Not started

### Phase 7 — Evaluation and error analysis

Tasks:

- evaluate the fine-tuned model
- compare it with the baseline
- calculate all project metrics
- create a confusion matrix
- inspect incorrect predictions
- analyse weak categories

Status: Not started

### Phase 8 — Local inference

Tasks:

- load the selected adapter
- run new customer messages
- test paraphrased inputs
- test ambiguous inputs
- test out-of-scope inputs
- test malformed and adversarial inputs

Status: Not started

### Phase 9 — Application integration

Tasks:

- expose the model through a local API
- validate generated JSON
- consume the API from another application
- add fallback behaviour
- measure response time

Status: Not started

---

## 23. Current project status

The following work has been completed:

- project directory created
- Python 3.11 environment created
- VS Code configured
- Git repository initialised
- project structure created
- project scope defined
- dataset research template created
- experiment log created
- model research template created

The current project phase is:

```text
Phase 2 — Dataset exploration
```

No dataset has yet been:

- downloaded
- inspected locally
- transformed
- split
- tokenised

No model has yet been:

- downloaded
- loaded
- evaluated
- fine-tuned
```

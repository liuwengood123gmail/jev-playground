# Jev cognitive-bias probes (2026-09-20 20:18)

## jev-latest

### A. Response curve (simple events, no bias involved)

| item | exact | Jev | Jev − exact |
|---|---|---|---|
| die7: It shows a 7. | 0.000 | 0.02 | +0.02 |
| d36: Both dice show a 6. | 0.028 | 0.17 | +0.14 |
| ace: The card is an ace. | 0.077 | 0.33 | +0.25 |
| digit: The digit is 7. | 0.100 | 0.18 | +0.08 |
| 3heads: All three flips are heads. | 0.125 | 0.23 | +0.10 |
| die1: It shows a 1. | 0.167 | 0.28 | +0.11 |
| 2heads: Both flips are heads. | 0.250 | 0.27 | +0.02 |
| heart: The card is a heart. | 0.250 | 0.36 | +0.11 |
| coin: It lands heads. | 0.500 | 0.52 | +0.02 |
| mere24: At least one roll is a double six. | 0.491 | 0.47 | -0.02 |
| mere4: At least one roll shows a 6. | 0.518 | 0.51 | -0.01 |
| die_le5: It shows 5 or less. | 0.833 | 0.76 | -0.07 |
| le90: The integer is 90 or less. | 0.900 | 0.88 | -0.03 |
| notace: The card is not an ace. | 0.923 | 0.86 | -0.06 |
| die_le6: It shows 6 or less. | 1.000 | 0.98 | -0.02 |

### B. Bias probes

| item | bias | exact | human-typical | Jev | closer to | note |
|---|---|---|---|---|---|---|
| br_famous | base-rate neglect (famous) | 0.020 | 0.95 | 0.12 | exact | Casscells 1978: modal answer 95% |
| br_novel | base-rate neglect (unfamiliar numbers) | 0.057 | 0.87 | 0.13 | exact | typical: ≈sensitivity minus a bit |
| br_freq | base-rate, natural-frequency format | 0.057 | 0.50 | 0.19 | exact | Gigerenzer: ~half of people get it right in this format |
| linda_A | conjunction (Linda, marginal) | — | — | 0.18 | | T&K 1983 |
| linda_AB | conjunction (Linda, conjunction) | — | — | 0.14 | | 85% of subjects rank this ABOVE the marginal |
| bill_A | conjunction (Bill, marginal) | — | — | 0.09 | | T&K 1983 |
| bill_AB | conjunction (Bill, conjunction) | — | — | 0.08 | | most subjects rank this ABOVE the marginal |
| gambler | gambler's fallacy | 0.500 | 0.60 | 0.50 | exact | 'due for tails' intuition: >0.5 |
| hothand | hot hand (mirror of gambler) | 0.500 | 0.40 | 0.49 | exact | mirror; should equal 1 - gambler |
| surv_one | survivorship (single manager) | 0.001 | 0.00 | 0.11 | **human** | people get this one roughly right |
| surv_many | survivorship (10,000 managers) | 1.000 | 0.15 | 0.80 | exact | intuition: 'a 10-year streak must be skill' → low |
| monty3 | Monty Hall (famous) | 0.667 | 0.50 | 0.69 | exact | ~85% say 50/50 |
| monty100 | Monty Hall (100 doors) | 0.990 | 0.50 | 0.96 | exact | same intuition: 50/50 |
| prisoners | Three prisoners (Monty isomorph) | 0.333 | 0.50 | 0.46 | **human** | classic wrong answer: 1/2 |
| bday23 | birthday (famous n=23) | 0.507 | 0.10 | 0.59 | exact | intuition: ~23/365 |
| bday30 | birthday (n=30) | 0.706 | 0.15 | 0.71 | exact |  |
| bday50 | birthday (n=50) | 0.970 | 0.25 | 0.92 | exact |  |
| twochild | two-child problem | 0.333 | 0.50 | 0.33 | exact | classic wrong answer: 1/2 |
| frame_pos | framing (survival frame) | 0.900 | 0.90 | 0.90 | exact |  |
| frame_neg | framing (mortality frame) | 0.900 | 0.90 | 0.88 | exact | should equal frame_pos |
| anchor_hi | anchoring (irrelevant 85% in context) | 0.167 |  | 0.29 |  | compare with group-A 'die1' |
| anchor_lo | anchoring (irrelevant 2% in context) | 0.167 |  | 0.30 |  | compare with group-A 'die1' |

Hospital (choice): Jev = **small** (conf 0.99, probs {'small': 1.0, 'large': 0.0, 'same': 0.0}); exact = small; human = same (56% of subjects, T&K 1974)

### Derived checks

- conjunction Linda: P(A∧B)=0.14 vs P(A)=0.18 → consistent
- conjunction Bill:  P(A∧B)=0.08 vs P(A)=0.09 → consistent
- gambler + hothand sum = 0.99 (should be 1.00)
- ace + notace sum = 1.20 (should be 1.00)
- framing: survive|90% survival = 0.90 vs survive|10% mortality = 0.88
- anchoring: die1 baseline 0.28; with 85% in context 0.29; with 2% in context 0.30
- Monty: 3 doors 0.69 (exact .667) · 100 doors 0.96 (exact .99) · prisoners 0.46 (exact .333)
- birthday: n=23 0.59 (.507) · n=30 0.71 (.706) · n=50 0.92 (.970)

## jev-preview

### A. Response curve (simple events, no bias involved)

| item | exact | Jev | Jev − exact |
|---|---|---|---|
| die7: It shows a 7. | 0.000 | 0.02 | +0.02 |
| d36: Both dice show a 6. | 0.028 | 0.16 | +0.13 |
| ace: The card is an ace. | 0.077 | 0.33 | +0.25 |
| digit: The digit is 7. | 0.100 | 0.20 | +0.10 |
| 3heads: All three flips are heads. | 0.125 | 0.23 | +0.10 |
| die1: It shows a 1. | 0.167 | 0.27 | +0.10 |
| 2heads: Both flips are heads. | 0.250 | 0.27 | +0.02 |
| heart: The card is a heart. | 0.250 | 0.36 | +0.11 |
| coin: It lands heads. | 0.500 | 0.52 | +0.02 |
| mere24: At least one roll is a double six. | 0.491 | 0.47 | -0.02 |
| mere4: At least one roll shows a 6. | 0.518 | 0.51 | -0.01 |
| die_le5: It shows 5 or less. | 0.833 | 0.76 | -0.07 |
| le90: The integer is 90 or less. | 0.900 | 0.87 | -0.03 |
| notace: The card is not an ace. | 0.923 | 0.86 | -0.06 |
| die_le6: It shows 6 or less. | 1.000 | 0.98 | -0.02 |

### B. Bias probes

| item | bias | exact | human-typical | Jev | closer to | note |
|---|---|---|---|---|---|---|
| br_famous | base-rate neglect (famous) | 0.020 | 0.95 | 0.12 | exact | Casscells 1978: modal answer 95% |
| br_novel | base-rate neglect (unfamiliar numbers) | 0.057 | 0.87 | 0.13 | exact | typical: ≈sensitivity minus a bit |
| br_freq | base-rate, natural-frequency format | 0.057 | 0.50 | 0.16 | exact | Gigerenzer: ~half of people get it right in this format |
| linda_A | conjunction (Linda, marginal) | — | — | 0.19 | | T&K 1983 |
| linda_AB | conjunction (Linda, conjunction) | — | — | 0.14 | | 85% of subjects rank this ABOVE the marginal |
| bill_A | conjunction (Bill, marginal) | — | — | 0.09 | | T&K 1983 |
| bill_AB | conjunction (Bill, conjunction) | — | — | 0.08 | | most subjects rank this ABOVE the marginal |
| gambler | gambler's fallacy | 0.500 | 0.60 | 0.51 | exact | 'due for tails' intuition: >0.5 |
| hothand | hot hand (mirror of gambler) | 0.500 | 0.40 | 0.48 | exact | mirror; should equal 1 - gambler |
| surv_one | survivorship (single manager) | 0.001 | 0.00 | 0.12 | **human** | people get this one roughly right |
| surv_many | survivorship (10,000 managers) | 1.000 | 0.15 | 0.77 | exact | intuition: 'a 10-year streak must be skill' → low |
| monty3 | Monty Hall (famous) | 0.667 | 0.50 | 0.69 | exact | ~85% say 50/50 |
| monty100 | Monty Hall (100 doors) | 0.990 | 0.50 | 0.95 | exact | same intuition: 50/50 |
| prisoners | Three prisoners (Monty isomorph) | 0.333 | 0.50 | 0.46 | **human** | classic wrong answer: 1/2 |
| bday23 | birthday (famous n=23) | 0.507 | 0.10 | 0.59 | exact | intuition: ~23/365 |
| bday30 | birthday (n=30) | 0.706 | 0.15 | 0.70 | exact |  |
| bday50 | birthday (n=50) | 0.970 | 0.25 | 0.92 | exact |  |
| twochild | two-child problem | 0.333 | 0.50 | 0.33 | exact | classic wrong answer: 1/2 |
| frame_pos | framing (survival frame) | 0.900 | 0.90 | 0.89 | exact |  |
| frame_neg | framing (mortality frame) | 0.900 | 0.90 | 0.88 | exact | should equal frame_pos |
| anchor_hi | anchoring (irrelevant 85% in context) | 0.167 |  | 0.29 |  | compare with group-A 'die1' |
| anchor_lo | anchoring (irrelevant 2% in context) | 0.167 |  | 0.33 |  | compare with group-A 'die1' |

Hospital (choice): Jev = **small** (conf 0.99, probs {'large': 0.01, 'small': 0.99, 'same': 0.0}); exact = small; human = same (56% of subjects, T&K 1974)

### Derived checks

- conjunction Linda: P(A∧B)=0.14 vs P(A)=0.19 → consistent
- conjunction Bill:  P(A∧B)=0.08 vs P(A)=0.09 → consistent
- gambler + hothand sum = 0.99 (should be 1.00)
- ace + notace sum = 1.20 (should be 1.00)
- framing: survive|90% survival = 0.89 vs survive|10% mortality = 0.88
- anchoring: die1 baseline 0.27; with 85% in context 0.29; with 2% in context 0.33
- Monty: 3 doors 0.69 (exact .667) · 100 doors 0.95 (exact .99) · prisoners 0.46 (exact .333)
- birthday: n=23 0.59 (.507) · n=30 0.70 (.706) · n=50 0.92 (.970)

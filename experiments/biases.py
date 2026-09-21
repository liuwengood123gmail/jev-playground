"""Cognitive-bias probes for Jev.

Hypothesis under test (H1): Jev's probability estimates track *human intuition*
(base-rate neglect, conjunction fallacy, gambler's fallacy, ...) because it is
initialised from a text-pretrained LM.

Competing explanations the design must separate:
  H2  "textbook retrieval": famous problems get the famous answer, structurally
      identical but unfamiliar variants do not.
  H3  "shrinkage": a monotone but compressed response curve (everything pulled
      toward ~0.5), i.e. low numeric resolution rather than any human-like bias.

Each item records: exact answer, typical human answer (literature), Jev answer.
Group A (calibration curve) has no human bias — it exists only to measure H3.

    python experiments/biases.py            # both models, 2 repeats
    python experiments/biases.py jev-latest # one model
"""
import json, os, statistics, sys, time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY = os.environ.get("TYPESAFE_API_KEY") or next(
    (l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines() if l.startswith("TYPESAFE_API_KEY=")), None)
MODELS = sys.argv[1:] or ["jev-latest", "jev-preview"]
REPEATS = 2

INSTR = ("`problem` sets up a probability scenario. Compute the exact mathematical probability that "
         "`statement` holds, then return that exact value as your probability estimate "
         "(not a subjective yes/no judgment — the number itself is the answer).")


def noul(problem, statement):
    return {"state": {"problem": problem, "statement": statement}, "questions": {"p": {"type": "noul", "instructions": INSTR}}}


def bday(n):
    p = 1.0
    for i in range(n):
        p *= (365 - i) / 365
    return 1 - p


# ---------------------------------------------------------------- Group A: response curve (H3 control)
A = [
    ("die7",      "A fair six-sided die is rolled.", "It shows a 7.", 0.0),
    ("d36",       "Two fair six-sided dice are rolled.", "Both dice show a 6.", 1/36),
    ("ace",       "One card is drawn from a standard 52-card deck.", "The card is an ace.", 1/13),
    ("digit",     "A single digit is chosen uniformly at random from 0-9.", "The digit is 7.", 0.1),
    ("3heads",    "A fair coin is flipped three times.", "All three flips are heads.", 0.125),
    ("die1",      "A fair six-sided die is rolled.", "It shows a 1.", 1/6),
    ("2heads",    "A fair coin is flipped twice.", "Both flips are heads.", 0.25),
    ("heart",     "One card is drawn from a standard 52-card deck.", "The card is a heart.", 0.25),
    ("coin",      "A fair coin is flipped once.", "It lands heads.", 0.5),
    ("mere24",    "A pair of fair dice is rolled 24 times.", "At least one roll is a double six.", 1-(35/36)**24),
    ("mere4",     "A fair six-sided die is rolled 4 times.", "At least one roll shows a 6.", 1-(5/6)**4),
    ("die_le5",   "A fair six-sided die is rolled.", "It shows 5 or less.", 5/6),
    ("le90",      "An integer is chosen uniformly at random from 1 to 100.", "The integer is 90 or less.", 0.9),
    ("notace",    "One card is drawn from a standard 52-card deck.", "The card is not an ace.", 12/13),
    ("die_le6",   "A fair six-sided die is rolled.", "It shows 6 or less.", 1.0),
]

# ---------------------------------------------------------------- Group B: bias probes
# (id, bias, problem, statement, exact, human_typical, source-of-human-value)
B = [
    # base-rate neglect
    ("br_famous", "base-rate neglect (famous)",
     "A disease has prevalence 1 in 1000. A test detects it with 100% sensitivity and has a 5% false-positive rate. A person chosen at random from the population tests positive.",
     "The person actually has the disease.", 0.001/(0.001+0.999*0.05), 0.95, "Casscells 1978: modal answer 95%"),
    ("br_novel", "base-rate neglect (unfamiliar numbers)",
     "A condition has prevalence 0.2%. A screening test has 90% sensitivity and a 3% false-positive rate. A randomly chosen person tests positive.",
     "The person actually has the condition.", 0.002*0.9/(0.002*0.9+0.998*0.03), 0.87, "typical: ≈sensitivity minus a bit"),
    ("br_freq", "base-rate, natural-frequency format",
     "Out of 10,000 people, 20 have a condition and 18 of those 20 test positive. Of the 9,980 without the condition, 299 test positive. One person from the 10,000 tests positive.",
     "The person actually has the condition.", 18/317, 0.5, "Gigerenzer: ~half of people get it right in this format"),
    # conjunction fallacy — two statements, same request; exact constraint is P(A∧B) ≤ P(A)
    ("linda_A", "conjunction (Linda, marginal)",
     "Linda is 31, single, outspoken and very bright. She majored in philosophy. As a student she was deeply concerned with discrimination and social justice, and participated in anti-nuclear demonstrations.",
     "Linda is a bank teller.", None, None, "T&K 1983"),
    ("linda_AB", "conjunction (Linda, conjunction)",
     "Linda is 31, single, outspoken and very bright. She majored in philosophy. As a student she was deeply concerned with discrimination and social justice, and participated in anti-nuclear demonstrations.",
     "Linda is a bank teller and is active in the feminist movement.", None, None, "85% of subjects rank this ABOVE the marginal"),
    ("bill_A", "conjunction (Bill, marginal)",
     "Bill is 34, intelligent but unimaginative, compulsive and generally lifeless. In school he was strong in mathematics but weak in social studies and humanities.",
     "Bill plays jazz for a hobby.", None, None, "T&K 1983"),
    ("bill_AB", "conjunction (Bill, conjunction)",
     "Bill is 34, intelligent but unimaginative, compulsive and generally lifeless. In school he was strong in mathematics but weak in social studies and humanities.",
     "Bill is an accountant who plays jazz for a hobby.", None, None, "most subjects rank this ABOVE the marginal"),
    # gambler's fallacy / hot hand
    ("gambler", "gambler's fallacy",
     "A fair coin has just landed heads six times in a row.",
     "The next flip lands tails.", 0.5, 0.6, "'due for tails' intuition: >0.5"),
    ("hothand", "hot hand (mirror of gambler)",
     "A fair coin has just landed heads six times in a row.",
     "The next flip lands heads.", 0.5, 0.4, "mirror; should equal 1 - gambler"),
    # survivorship / multiple comparisons
    ("surv_one", "survivorship (single manager)",
     "A fund manager's result each year is an independent fair coin flip: beat the market or not.",
     "This manager beats the market 10 years in a row.", 2**-10, 0.001, "people get this one roughly right"),
    ("surv_many", "survivorship (10,000 managers)",
     "There are 10,000 fund managers. Each manager's result each year is an independent fair coin flip: beat the market or not.",
     "At least one of the 10,000 managers beats the market 10 years in a row.", 1-(1-2**-10)**10000, 0.15, "intuition: 'a 10-year streak must be skill' → low"),
    # Monty Hall: famous vs isomorphs
    ("monty3", "Monty Hall (famous)",
     "Monty Hall game: 3 doors, one hides a car, two hide goats. You pick a door; the host, who knows what's behind each door, always opens a different door revealing a goat; you then switch to the remaining unopened door.",
     "You win the car.", 2/3, 0.5, "~85% say 50/50"),
    ("monty100", "Monty Hall (100 doors)",
     "A game has 100 doors; one hides a car, 99 hide goats. You pick a door. The host, who knows where the car is, opens 98 of the other doors, all revealing goats. You then switch to the one remaining unopened door.",
     "You win the car.", 0.99, 0.5, "same intuition: 50/50"),
    ("prisoners", "Three prisoners (Monty isomorph)",
     "Three prisoners A, B, C; exactly one, chosen at random, will be pardoned. The warden knows who. A asks the warden to name one of B or C who will NOT be pardoned (if both will be executed the warden picks one at random). The warden says 'B will be executed'.",
     "A is the one who will be pardoned.", 1/3, 0.5, "classic wrong answer: 1/2"),
    # birthday: famous vs unfamiliar n
    ("bday23", "birthday (famous n=23)", "23 people are in a room; birthdays independent and uniform over 365 days.", "At least two share a birthday.", bday(23), 0.1, "intuition: ~23/365"),
    ("bday30", "birthday (n=30)", "30 people are in a room; birthdays independent and uniform over 365 days.", "At least two share a birthday.", bday(30), 0.15, ""),
    ("bday50", "birthday (n=50)", "50 people are in a room; birthdays independent and uniform over 365 days.", "At least two share a birthday.", bday(50), 0.25, ""),
    # sample-size insensitivity is asked as a choice below
    # two-child problem
    ("twochild", "two-child problem",
     "A family has two children. Each child is independently a boy or a girl with equal probability. You learn that at least one of the two children is a boy.",
     "Both children are boys.", 1/3, 0.5, "classic wrong answer: 1/2"),
    # framing: identical event, positive vs negative frame
    ("frame_pos", "framing (survival frame)", "A surgery has a 90% survival rate.", "A patient undergoing this surgery survives.", 0.9, 0.9, ""),
    ("frame_neg", "framing (mortality frame)", "A surgery has a 10% mortality rate.", "A patient undergoing this surgery survives.", 0.9, 0.9, "should equal frame_pos"),
    # anchoring / distraction: same die question with an irrelevant number in context
    ("anchor_hi", "anchoring (irrelevant 85% in context)",
     "A recent survey found that 85% of respondents like pizza. Separately, a fair six-sided die is rolled.", "The die shows a 1.", 1/6, None, "compare with group-A 'die1'"),
    ("anchor_lo", "anchoring (irrelevant 2% in context)",
     "A recent survey found that 2% of respondents like anchovies. Separately, a fair six-sided die is rolled.", "The die shows a 1.", 1/6, None, "compare with group-A 'die1'"),
]

# choice-type probe: hospital problem (sample-size insensitivity)
HOSPITAL = {
    "state": {"problem": "A large hospital has about 45 births a day, a small hospital about 15 births a day. About 50% of babies are boys, but the exact percentage varies day to day. For one year each hospital recorded the days on which more than 60% of the babies born were boys."},
    "questions": {"which": {"type": "choice", "instructions": "Which hospital recorded more such days?",
                            "criteria": {"large": "The large hospital (45 births/day)", "small": "The small hospital (15 births/day)", "same": "About the same (within 5% of each other)"}}},
}
HOSPITAL_EXACT, HOSPITAL_HUMAN = "small", "same (56% of subjects, T&K 1974)"


def call(model, body):
    req = urllib.request.Request("https://api.typesafe.ai/v1/systemone", data=json.dumps({"model": model, **body}).encode(),
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            return json.load(urllib.request.urlopen(req, timeout=60))["answers"]
        except urllib.error.HTTPError as e:
            if e.code in (429, 529):
                time.sleep(0.5 * 2 ** attempt); continue
            raise


def run_noul(model, body):
    vals = [call(model, body)["p"]["noul"] for _ in range(REPEATS)]
    return statistics.mean(vals)


def main():
    out = {"models": {}, "generated": time.strftime("%Y-%m-%d %H:%M")}
    for model in MODELS:
        jobs = [(k, noul(p, s)) for k, p, s, _ in A] + [(k, noul(p, s)) for k, _, p, s, *_ in B]
        with ThreadPoolExecutor(8) as ex:
            res = dict(zip([k for k, _ in jobs], ex.map(lambda j: run_noul(model, j[1]), jobs)))
        hosp = call(model, HOSPITAL)["which"]
        out["models"][model] = {"noul": res, "hospital": hosp}

    (ROOT / "experiments" / "results.json").write_text(json.dumps(out, indent=2))

    md = [f"# Jev cognitive-bias probes ({out['generated']})", ""]
    for model, r in out["models"].items():
        j = r["noul"]
        md += [f"## {model}", "", "### A. Response curve (simple events, no bias involved)", "",
               "| item | exact | Jev | Jev − exact |", "|---|---|---|---|"]
        for k, _, s, ex in A:
            md.append(f"| {k}: {s} | {ex:.3f} | {j[k]:.2f} | {j[k]-ex:+.2f} |")
        md += ["", "### B. Bias probes", "", "| item | bias | exact | human-typical | Jev | closer to | note |", "|---|---|---|---|---|---|---|"]
        for k, bias, _, s, ex, hu, note in B:
            if ex is None:
                md.append(f"| {k} | {bias} | — | — | {j[k]:.2f} | | {note} |"); continue
            closer = "" if hu is None else ("**human**" if abs(j[k]-hu) < abs(j[k]-ex) else "exact")
            md.append(f"| {k} | {bias} | {ex:.3f} | {'' if hu is None else f'{hu:.2f}'} | {j[k]:.2f} | {closer} | {note} |")
        h = r["hospital"]
        md += ["", f"Hospital (choice): Jev = **{h['choice']}** (conf {h['confidence']:.2f}, probs {h['probabilities']}); exact = {HOSPITAL_EXACT}; human = {HOSPITAL_HUMAN}", "",
               "### Derived checks", "",
               f"- conjunction Linda: P(A∧B)={j['linda_AB']:.2f} vs P(A)={j['linda_A']:.2f} → {'FALLACY' if j['linda_AB'] > j['linda_A'] else 'consistent'}",
               f"- conjunction Bill:  P(A∧B)={j['bill_AB']:.2f} vs P(A)={j['bill_A']:.2f} → {'FALLACY' if j['bill_AB'] > j['bill_A'] else 'consistent'}",
               f"- gambler + hothand sum = {j['gambler']+j['hothand']:.2f} (should be 1.00)",
               f"- ace + notace sum = {j['ace']+j['notace']:.2f} (should be 1.00)",
               f"- framing: survive|90% survival = {j['frame_pos']:.2f} vs survive|10% mortality = {j['frame_neg']:.2f}",
               f"- anchoring: die1 baseline {j['die1']:.2f}; with 85% in context {j['anchor_hi']:.2f}; with 2% in context {j['anchor_lo']:.2f}",
               f"- Monty: 3 doors {j['monty3']:.2f} (exact .667) · 100 doors {j['monty100']:.2f} (exact .99) · prisoners {j['prisoners']:.2f} (exact .333)",
               f"- birthday: n=23 {j['bday23']:.2f} (.507) · n=30 {j['bday30']:.2f} (.706) · n=50 {j['bday50']:.2f} (.970)", ""]
    (ROOT / "experiments" / "results.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()

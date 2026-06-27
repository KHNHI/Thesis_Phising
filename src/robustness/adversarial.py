"""Adversarial text perturbations to probe TF-IDF vs. transformer robustness (RQ4).

Attacks are applied to RAW email text (as an attacker would), then the defender's
preprocessing runs as usual — so we measure attacks that SURVIVE preprocessing.

  * char_substitution : leetspeak (verify -> v3rify); digits are stripped by the
                        cleaner, leaving a broken OOV token (vrify) -> evades TF-IDF.
  * keyword_injection : append benign/legit-associated tokens to dilute the phishing signal.
  * html_obfuscation  : insert empty inline tags inside words (ver<b></b>ify); after
                        HTML stripping with a space separator the word breaks into OOV pieces.
"""
import random

LEET = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7"}
# legit/artifact-associated tokens (from the SHAP audit) used to dilute the phishing signal
BENIGN_INJECT = ["enron", "wrote", "thanks", "regards", "meeting", "team", "python",
                 "university", "report", "attached", "schedule", "project"]


def char_substitution(text, rate=0.10, seed=42):
    rng = random.Random(seed); chars = list(text)
    idx = [i for i, c in enumerate(chars) if c.lower() in LEET]
    rng.shuffle(idx)
    for i in idx[: int(len(idx) * rate)]:
        chars[i] = LEET[chars[i].lower()]
    return "".join(chars)


def keyword_injection(text, rate=0.10, seed=42):
    rng = random.Random(seed)
    n = max(1, int(len(text.split()) * rate))
    return text + " " + " ".join(rng.choice(BENIGN_INJECT) for _ in range(n))


def html_obfuscation(text, rate=0.10, seed=42):
    rng = random.Random(seed); words = text.split()
    for i, w in enumerate(words):
        if len(w) > 3 and rng.random() < rate:
            p = rng.randint(1, len(w) - 1)
            words[i] = w[:p] + "<b></b>" + w[p:]   # broken by get_text(' ') after stripping
    return " ".join(words)


ATTACKS = {"char_substitution": char_substitution,
           "keyword_injection": keyword_injection,
           "html_obfuscation": html_obfuscation}


def apply_attack(text, name, level, seed=42):
    return ATTACKS[name](text, rate=level, seed=seed)

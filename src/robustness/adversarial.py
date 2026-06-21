"""Adversarial text perturbations to probe TF-IDF vs. transformer robustness (RQ4).

Implements the three attack classes discussed in the conference paper:
  * character substitution  ('verify' -> 'v3rify')  -- evades exact-match TF-IDF tokens
  * keyword injection        -- dilute the phishing signal with benign high-weight tokens
  * html_obfuscation         -- wrap text in markup/zero-width chars
"""
import random

LEET = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7"}
BENIGN_INJECT = ["python", "mailing", "list", "unsubscribe", "dev", "wrote", "opensuse"]


def char_substitution(text: str, rate: float = 0.10, seed: int = 42) -> str:
    rng = random.Random(seed)
    chars = list(text)
    idxs = [i for i, c in enumerate(chars) if c.lower() in LEET]
    rng.shuffle(idxs)
    for i in idxs[: int(len(idxs) * rate)]:
        chars[i] = LEET[chars[i].lower()]
    return "".join(chars)


def keyword_injection(text: str, rate: float = 0.10, seed: int = 42) -> str:
    rng = random.Random(seed)
    n = max(1, int(len(text.split()) * rate))
    inject = " ".join(rng.choice(BENIGN_INJECT) for _ in range(n))
    return f"{text} {inject}"


def html_obfuscation(text: str, rate: float = 0.10, seed: int = 42) -> str:
    rng = random.Random(seed)
    words = text.split()
    for i in range(len(words)):
        if rng.random() < rate:
            words[i] = f"<span>{words[i]}</span>"
    return " ".join(words)


ATTACKS = {
    "char_substitution": char_substitution,
    "keyword_injection": keyword_injection,
    "html_obfuscation": html_obfuscation,
}


def apply_attack(text: str, name: str, level: float, seed: int = 42) -> str:
    return ATTACKS[name](text, rate=level, seed=seed)

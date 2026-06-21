"""Quantify SHAP–LIME agreement (RQ2): Pearson, Spearman, Jaccard, overlap."""
from scipy.stats import pearsonr, spearmanr


def jaccard(set_a, set_b) -> float:
    a, b = set(set_a), set(set_b)
    return len(a & b) / len(a | b) if (a | b) else 0.0


def consistency(shap_scores: dict, lime_scores: dict):
    """shap_scores/lime_scores: {feature: importance}. Returns metrics dict."""
    shared = sorted(set(shap_scores) & set(lime_scores))
    metrics = {
        "n_overlap": len(shared),
        "overlapping_features": shared,
        "jaccard": jaccard(shap_scores, lime_scores),
    }
    if len(shared) >= 3:
        sv = [shap_scores[f] for f in shared]
        lv = [lime_scores[f] for f in shared]
        metrics["pearson"] = pearsonr(sv, lv)[0]
        metrics["spearman_rho"], metrics["spearman_p"] = spearmanr(sv, lv)
    return metrics

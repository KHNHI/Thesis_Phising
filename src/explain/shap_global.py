"""Global SHAP attribution for the classical models (LinearExplainer for SVM/LR)."""
# import shap
def global_shap(pipeline, X_background, X_explain, top_k=20):
    """Return top-k (feature, mean|SHAP|) for the fitted TF-IDF + linear model."""
    raise NotImplementedError("Implemented in Week 6 once corpus + models are ready.")

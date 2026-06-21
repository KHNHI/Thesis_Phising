"""Train the five classical ML baselines under one TF-IDF pipeline.

Reproduces the conference-paper setup (single source) and extends it to the
multi-source corpus. CPU-friendly; runs in this environment once data is present.
"""
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV

from src.features.preprocess import build_vectorizer


def get_models(seed=42):
    svm = CalibratedClassifierCV(LinearSVC(random_state=seed))  # probability-calibrated
    return {
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=seed),
        "naive_bayes": MultinomialNB(),
        "decision_tree": DecisionTreeClassifier(random_state=seed),
        "random_forest": RandomForestClassifier(n_estimators=300, random_state=seed, n_jobs=-1),
        "linear_svm": svm,
    }


def build_pipeline(model, **tfidf_kwargs):
    return Pipeline([("tfidf", build_vectorizer(**tfidf_kwargs)), ("clf", model)])

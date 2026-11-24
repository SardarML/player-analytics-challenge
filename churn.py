import numpy as np
from sklearn.compose import make_column_transformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

# last_session_date is excluded: it contains sessions after the snapshot.
SKEWED = ["tenure_days", "sessions_30d", "deposit_amount_30d_eur", "avg_bet_eur"]
NUMERIC = ["deposits_count_30d", "failed_deposits_30d", "bonus_share",
           "sportsbook_share", "days_since_last_session"]
FEATURES = SKEWED + NUMERIC + ["brand"]


def churn_model():
    """Return an untrained logistic regression pipeline."""
    return make_pipeline(
        make_column_transformer(
            (make_pipeline(FunctionTransformer(np.log1p), StandardScaler()), SKEWED),
            (StandardScaler(), NUMERIC),
            (OneHotEncoder(drop="first"), ["brand"]),
        ),
        LogisticRegression(max_iter=2000),
    )


def evaluate_churn(train):
    """Return the out-of-fold ROC-AUC."""
    cv = StratifiedKFold(5, shuffle=True, random_state=42)
    prob = cross_val_predict(churn_model(), train[FEATURES], train["churned_30d"],
                             cv=cv, method="predict_proba")[:, 1]
    return roc_auc_score(train["churned_30d"], prob)


def predict_churn(train, test):
    """Return churn probabilities for the test players."""
    model = churn_model().fit(train[FEATURES], train["churned_30d"])
    prob = model.predict_proba(test[FEATURES])[:, 1]
    return test[["player_id"]].assign(churn_probability=prob.round(6))


def churn_rates(train):
    """Return churn rates of the player groups compared in the CRM summary."""
    groups = {
        "inactive > 21 days": train["days_since_last_session"] > 21,
        "active in last 3 days": train["days_since_last_session"] <= 3,
        "2+ failed deposits": train["failed_deposits_30d"] >= 2,
        "no failed deposits": train["failed_deposits_30d"] == 0,
    }
    return {name: train.loc[mask, "churned_30d"].mean() for name, mask in groups.items()}

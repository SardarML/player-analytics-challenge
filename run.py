from pathlib import Path

import pandas as pd

from checks import check_churn, check_recommendations
from churn import churn_rates, evaluate_churn, predict_churn
from experiment import two_proportion_test
from fraud import linked_groups
from payments import net_deposits
from recommendations import co_played, evaluate_recommendations, recommend

ROOT = Path(__file__).parent


def main():
    data = {path.stem: pd.read_csv(path) for path in (ROOT / "data").glob("*.csv")}
    train, test = data["churn_train"], data["churn_test"]
    plays, targets = data["game_plays"], data["recommendation_targets"]

    results = {
        "net_deposits": net_deposits(data["deposits"], data["withdrawals"], data["players"], data["fx_rates"]),
        "linked_groups": linked_groups(data["players"], data["bonus_claims"]),
        "churn_predictions": predict_churn(train, test),
        "recommendations": recommend(plays, targets),
    }
    check_churn(results["churn_predictions"], test)
    check_recommendations(results["recommendations"], targets, plays)

    out = ROOT / "outputs"
    out.mkdir(exist_ok=True)
    for name, df in results.items():
        df.to_csv(out / f"{name}.csv", index=False)

    print(results["net_deposits"])
    print(results["linked_groups"].query("flag").to_string())
    print("A/B test:", two_proportion_test(200, 230, 5000))
    print("Churn ROC-AUC:", evaluate_churn(train))
    print("Churn by segment:", churn_segments(train))
    print(co_played(plays, data["games"], "G040").head())
    print("Hit@5:", evaluate_recommendations(plays))
    print("A/B test (p-value, players per group):", two_proportion_test(200, 230, 5000))
    print("Churn rates:", churn_rates(train))
    print(co_played(plays, data["games"], "G040").head())


if __name__ == "__main__":
    main()

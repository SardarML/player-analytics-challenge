# Player Analytics Challenge

Payments, bonus abuse, churn and game recommendations on synthetic iGaming data.

## Run

Put the challenge CSV files in `data/` (not included), then:

```bash
pip install -r requirements.txt
python run.py
```

Results are written to `outputs/`.

## Results

| Part | Approach | Result |
| --- | --- | --- |
| Payments | Approved transactions of real accounts, daily FX rate | Fjord Spins, October 2026: €31,882 net deposits |
| Bonus abuse | Accounts linked by device or payment account | Largest group: 13 accounts |
| Churn | Logistic regression, 5-fold cross-validation | ROC-AUC 0.749 |
| Recommendations | EASE, one hidden game per player | Hit@5 60.7% (popularity: 38.0%) |

Net deposits are reported per brand and month.

## Power BI

`net_deposits.dax` is the measure for Power BI. Python cannot run DAX natively, so `run.py` does not execute it and it has not been run in Power BI. `outputs/net_deposits.csv` provides the reference values: filtered by brand and month, the measure should return `net_deposits_eur`. The measure assumes that Deposits and Withdrawals include currency, date has no time part, FX has one rate per date and currency, and a shared Date table filters both fact tables.

## Notes

- `last_session_date` is excluded from the churn model: in training it includes sessions after the snapshot.
- Some records are dated before registration (686 deposits, 191 withdrawals) and 56 bonus claims after 14 November 2026. They are left unchanged.
- Fraud flags need at least 3 linked accounts, 80% of them with a bonus. These thresholds were set after inspecting the data, so flags are for review, not automatic blocking.
- Model choice and evaluation used the same data, so scores may be slightly optimistic.

## AI use

Claude Code was used for data profiling, writing the code, comparing models and drafting the documentation. Its largest role was the DAX measure, as I have little Power BI experience. Claude Code also ran the checks: cross-validation, submission format checks and an independent recalculation of the net deposits and linked groups.

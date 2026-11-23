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

`run.py` reports net deposits per brand for the whole period; `net_deposits.sql` (Snowflake) gives the monthly figures.

## Notes

- `last_session_date` is excluded from the churn model: in training it includes sessions after the snapshot.
- Fraud flags need at least 3 linked accounts, 80% of them with a bonus. These thresholds were set after inspecting the data, so flags are for review, not automatic blocking.
- Model choice and evaluation used the same data, so scores may be slightly optimistic.

## AI use

Claude Code was used for data profiling, writing the code, comparing models and drafting the documentation. Outputs were checked with cross-validation, submission format checks and an SQL-versus-pandas reconciliation, also run with Claude Code.

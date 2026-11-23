import pandas as pd


def approved_eur(tx, players, fx):
    """Return approved transactions of real accounts with their EUR amount."""
    tx = tx.assign(date=tx["created_at"].str[:10])
    tx = tx.merge(players[["player_id", "brand", "account_type"]], on="player_id", validate="m:1")
    tx = tx.merge(fx, on=["date", "currency"], validate="m:1")
    tx["eur"] = tx["amount"] * tx["rate_to_eur"]
    return tx[(tx["status"] == "approved") & (tx["account_type"] == "real")]


def net_deposits(deposits, withdrawals, players, fx):
    """Return deposits, withdrawals and net deposits in EUR per brand."""
    # Aggregate before combining to avoid double counting.
    kpi = pd.DataFrame({
        "deposits_eur": approved_eur(deposits, players, fx).groupby("brand")["eur"].sum(),
        "withdrawals_eur": approved_eur(withdrawals, players, fx).groupby("brand")["eur"].sum(),
    })
    kpi["net_deposits_eur"] = kpi["deposits_eur"] - kpi["withdrawals_eur"]
    return kpi.round(2).reset_index()

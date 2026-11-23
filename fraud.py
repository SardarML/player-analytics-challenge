import networkx as nx
import pandas as pd


def linked_groups(players, bonuses):
    """Group real accounts sharing a device or payment account and flag likely bonus abuse."""
    players = players[players["account_type"] == "real"]
    graph = nx.Graph()
    for col in ("device_id", "payment_account_id"):
        graph.add_edges_from(zip(players["player_id"], players[col]))

    claims = bonuses.groupby("player_id")["bonus_amount_eur"].sum()
    rows = []
    for group in nx.connected_components(graph):
        ids = sorted(group & set(players["player_id"]))
        if len(ids) > 1:
            bonus = claims.reindex(ids)
            rows.append({
                "accounts": len(ids),
                "share_with_bonus": bonus.notna().mean(),
                "bonus_eur": bonus.sum(),
                "player_ids": " ".join(ids),
            })
    groups = pd.DataFrame(rows)
    # A pair alone is weak evidence: it may be a shared household.
    groups["flag"] = (groups["accounts"] >= 3) & (groups["share_with_bonus"] >= 0.8)
    return groups.sort_values("accounts", ascending=False)

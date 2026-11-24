import numpy as np
import pandas as pd


def play_matrix(plays):
    """Return a binary player x game matrix."""
    return pd.crosstab(plays["player_id"], plays["game_id"]).clip(upper=1)


def ease_scores(x, l2=200):
    """Score games with EASE, a linear item-item model."""
    p = np.linalg.inv(x.T @ x + l2 * np.eye(x.shape[1]))
    weights = -p / np.diag(p)
    np.fill_diagonal(weights, 0)
    return x @ weights


def top_games(scores, played, k=5):
    """Return the k best unplayed game indices per player."""
    return np.argsort(-np.where(played, -np.inf, scores), axis=1)[:, :k]


def evaluate_recommendations(plays, seed=42):
    """Hide one game per player and return hit@5 for popularity and EASE."""
    seen = play_matrix(plays).to_numpy(float, copy=True)
    rng = np.random.default_rng(seed)
    hidden = np.array([rng.choice(np.flatnonzero(row)) for row in seen])
    seen[np.arange(len(seen)), hidden] = 0
    scores = {"popularity": np.broadcast_to(seen.sum(axis=0), seen.shape), "ease": ease_scores(seen)}
    return {name: (top_games(s, seen) == hidden[:, None]).any(axis=1).mean()
            for name, s in scores.items()}


def recommend(plays, targets):
    """Return the top 5 unplayed games per target player."""
    matrix = play_matrix(plays)
    rows = matrix.index.get_indexer(targets["player_id"])
    x = matrix.to_numpy(float)
    best = top_games(ease_scores(x)[rows], x[rows])
    return pd.DataFrame({
        "player_id": targets["player_id"].repeat(5).to_numpy(),
        "game_id": matrix.columns.to_numpy()[best.ravel()],
        "rank": np.tile(range(1, 6), len(targets)),
    })


def co_played(plays, games, game_id):
    """Count distinct players of game_id for every other game."""
    players = plays.loc[plays["game_id"] == game_id, "player_id"]
    other = plays[plays["player_id"].isin(players) & (plays["game_id"] != game_id)]
    counts = other.groupby("game_id")["player_id"].nunique().rename("players").reset_index()
    return counts.merge(games[["game_id", "title"]], on="game_id").sort_values("players", ascending=False)

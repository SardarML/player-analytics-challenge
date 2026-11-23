def check_churn(predictions, test):
    """Validate the churn submission."""
    assert predictions["player_id"].is_unique
    assert set(predictions["player_id"]) == set(test["player_id"])
    assert predictions["churn_probability"].between(0, 1).all()


def check_recommendations(recs, targets, plays):
    """Validate the recommendation submission."""
    assert set(recs["player_id"]) == set(targets["player_id"])
    assert (recs.groupby("player_id")["rank"].agg(sorted).map(lambda r: r == [1, 2, 3, 4, 5])).all()
    assert not recs.duplicated(["player_id", "game_id"]).any()
    assert recs.merge(plays, on=["player_id", "game_id"]).empty

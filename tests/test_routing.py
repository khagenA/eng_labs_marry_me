from marry_me.logic import route_team

def test_route_team_valid():
    assert route_team("brawl") == "Security"
    assert route_team("bad_food") == "Catering"
    assert route_team("dirty_table") == "Waiters"

def test_route_team_invalid():
    assert route_team("unknown_type") is None

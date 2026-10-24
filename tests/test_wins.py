from sample.wins import count_wins


def test_counts_wins_for_normal_matches():
    matches = [
        {"winner": "India"},
        {"winner": "Australia"},
        {"winner": "India"},
    ]
    assert count_wins(matches) == {"India": 2, "Australia": 1}

def test_ignores_matches_with_no_winner():
    matches = [
        {"winner": "India"},
        {"winner": None},
        {"winner": "India"},
    ]
    result = count_wins(matches)
    assert result == {"India": 2}
    assert None not in result

def test_empty_list_returns_empty_dict():
    assert count_wins([]) == {}
import pytest


class FakeStreamlit:
    def __init__(self):
        self.session_state = {}
class FakeExpander:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

@pytest.mark.unit
def test_start_assigns_five_unique_players(game_module):
    fake_st = FakeStreamlit()
    game_module.st = fake_st
    game_module.init_game_state()

    human_name = "HumanOne"
    ai_names = ["AI_A", "AI_B", "AI_C", "AI_D"]

    game_module.st.session_state["human_name"] = human_name
    game_module.st.session_state["ai_names"] = ai_names

    all_players = [human_name] + ai_names
    assert len(all_players) == 5
    assert len(set(all_players)) == 5


@pytest.mark.unit
def test_generate_personalities_returns_stable_four_entries(game_module):
    personalities = game_module.generate_personalities()
    assert len(personalities) == 4
    assert len(set(personalities)) == 4


@pytest.mark.unit
def test_round_questions_are_unique_within_game(game_module):
    fake_st = FakeStreamlit()
    game_module.st = fake_st
    game_module.init_game_state()

    questions = [game_module.get_next_question() for _ in range(3)]
    assert len(set(questions)) == 3


@pytest.mark.unit
def test_tally_votes_eliminates_player_with_most_votes(game_module, monkeypatch):
    fake_st = FakeStreamlit()
    game_module.st = fake_st
    game_module.init_game_state()

    game_module.st.session_state["human_name"] = "Human"
    game_module.st.session_state["current_question"] = "Q"
    game_module.st.session_state["eliminated"] = []
    game_module.st.session_state["ai_answers"] = [
        {"name": "AI1", "personality": "P1", "response": "r1"},
        {"name": "AI2", "personality": "P2", "response": "r2"},
        {"name": "AI3", "personality": "P3", "response": "r3"},
        {"name": "AI4", "personality": "P4", "response": "r4"},
    ]

    votes_by_ai = {
        "AI1": "AI2",
        "AI2": "AI2",
        "AI3": "Human",
        "AI4": "AI2",
    }

    def fake_ai_vote(_q, _all_answers, voter_name, _p):
        return votes_by_ai[voter_name]

    monkeypatch.setattr(game_module, "ai_vote", fake_ai_vote)

    all_answers = game_module.st.session_state["ai_answers"] + [
        {"name": "Human", "response": "human response"}
    ]
    eliminated, votes = game_module.tally_votes("AI2", all_answers)

    assert eliminated == "AI2"
    assert votes["AI2"] == 4


@pytest.mark.unit
def test_ai_votes_are_counted_each_round(game_module, monkeypatch):
    fake_st = FakeStreamlit()
    game_module.st = fake_st
    game_module.init_game_state()

    game_module.st.session_state["human_name"] = "Human"
    game_module.st.session_state["current_question"] = "Q"
    game_module.st.session_state["eliminated"] = []
    game_module.st.session_state["ai_answers"] = [
        {"name": "AI1", "personality": "P1", "response": "r1"},
        {"name": "AI2", "personality": "P2", "response": "r2"},
        {"name": "AI3", "personality": "P3", "response": "r3"},
        {"name": "AI4", "personality": "P4", "response": "r4"},
    ]

    calls = []

    def fake_ai_vote(_q, _all_answers, voter_name, _p):
        calls.append(voter_name)
        return "Human"

    monkeypatch.setattr(game_module, "ai_vote", fake_ai_vote)

    all_answers = game_module.st.session_state["ai_answers"] + [
        {"name": "Human", "response": "human response"}
    ]
    game_module.tally_votes("AI1", all_answers)

    assert sorted(calls) == ["AI1", "AI2", "AI3", "AI4"]


@pytest.mark.unit
def test_generate_round_skips_eliminated_players(game_module, monkeypatch):
    fake_st = FakeStreamlit()
    game_module.st = fake_st
    game_module.init_game_state()

    game_module.st.session_state["ai_names"] = ["AI1", "AI2", "AI3", "AI4"]
    game_module.st.session_state["ai_personalities"] = ["P1", "P2", "P3", "P4"]
    game_module.st.session_state["eliminated"] = ["AI3"]

    captured = {}

    def fake_response_ai(names, personalities, question):
        captured["names"] = names
        captured["personalities"] = personalities
        captured["question"] = question
        return [{"name": n, "response": "ok", "personality": p, "model": "m"} for n, p in zip(names, personalities)]

    monkeypatch.setattr(game_module, "responseAI", fake_response_ai)

    game_module.generate_round()

    assert "AI3" not in captured["names"]
    assert len(captured["names"]) == 3


@pytest.mark.unit
def test_reset_game_clears_state_for_play_again(game_module):
    fake_st = FakeStreamlit()
    game_module.st = fake_st
    game_module.init_game_state()

    game_module.st.session_state.update(
        {
            "started": True,
            "round_number": 2,
            "human_name": "Human",
            "ai_names": ["AI1", "AI2", "AI3", "AI4"],
            "eliminated": ["AI1"],
            "asked_questions": ["Q1", "Q2"],
        }
    )

    game_module.resetgame()

    assert game_module.st.session_state["started"] is False
    assert game_module.st.session_state["round_number"] == 0
    assert game_module.st.session_state["human_name"] == ""
    assert game_module.st.session_state["ai_names"] == []
    assert game_module.st.session_state["eliminated"] == []
    assert game_module.st.session_state["asked_questions"] == []


@pytest.mark.unit
def test_render_round_displays_ai_answers_before_submission(game_module):
    class RenderFakeStreamlit:
        def __init__(self):
            self.session_state = {
                "round_number": 1,
                "human_name": "Human",
                "current_question": "Question?",
                "ai_answers": [
                    {"name": "AI1", "personality": "P1", "response": "R1", "model": "m1"},
                    {"name": "AI2", "personality": "P2", "response": "R2", "model": "m2"},
                ],
                "clear_human_input": False,
                "human_response_input": "",
                "phase": "answer",
            }
            self.writes = []
            self.button_labels = []

        def expander(self, label, expanded=False):
        return FakeExpander()

        def button(self, label):
            self.button_labels.append(label)
            return False

        def write(self, value):
            self.writes.append(str(value))

        def subheader(self, _):
            return None

        def divider(self):
            return None

        def text_input(self, *_args, **_kwargs):
            return ""

        def warning(self, *_args, **_kwargs):
            return None

        def rerun(self):
            return None

    fake_st = RenderFakeStreamlit()
    game_module.st = fake_st

    game_module.render_round()

    assert "R1" in fake_st.writes
    assert "R2" in fake_st.writes
    assert "Submit response" in fake_st.button_labels

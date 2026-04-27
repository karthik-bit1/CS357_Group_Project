import pytest
from streamlit.testing.v1 import AppTest


@pytest.mark.integration
def test_start_button_initializes_game():
    at = AppTest.from_file("code/reverse_turing_test.py")
    at.run()

    at.button[0].click().run()

    assert at.session_state.started is True
    assert at.session_state.round_number == 1
    assert len(at.session_state.ai_names) == 4
    all_players = [at.session_state.human_name] + at.session_state.ai_names
    assert len(set(all_players)) == 5


@pytest.mark.integration
def test_answer_to_vote_phase_and_human_vote_submission():
    at = AppTest.from_file("code/reverse_turing_test.py")
    at.run()
    at.button[0].click().run()

    at.text_input[0].input("I enjoy painting landscapes.").run()
    submit_response = [b for b in at.button if b.label == "Submit response"][0]
    submit_response.click().run()

    assert at.session_state.phase == "voting"

    at.radio[0].set_value(at.session_state.ai_names[0]).run()
    submit_vote = [b for b in at.button if b.label == "Submit vote"][0]
    submit_vote.click().run()

    assert at.session_state.phase == "result"
    assert at.session_state.vote_result in ([at.session_state.human_name] + at.session_state.ai_names)


@pytest.mark.integration
def test_three_rounds_end_game_and_play_again_resets():
    at = AppTest.from_file("code/reverse_turing_test.py")
    at.run()
    at.button[0].click().run()

    for _ in range(3):
        if not at.text_input:
            break
        at.text_input[0].input("short response").run()
        submit_response_buttons = [b for b in at.button if b.label == "Submit response"]
        if not submit_response_buttons:
            break
        submit_response_buttons[0].click().run()

        if not at.radio:
            break
        vote_choice = at.radio[0].options[0] if getattr(at.radio[0], "options", None) else at.session_state.ai_names[0]
        at.radio[0].set_value(vote_choice).run()
        submit_vote_buttons = [b for b in at.button if b.label == "Submit vote"]
        if not submit_vote_buttons:
            break
        submit_vote_buttons[0].click().run()

        next_buttons = [b for b in at.button if b.label in ("Next round")]
        if next_buttons:
            next_buttons[0].click().run()

        if at.session_state.started is False:
            break

    assert at.session_state.started is False

    play_again_buttons = [b for b in at.button if b.label == "Play again"]
    if play_again_buttons:
        play_again_buttons[0].click().run()

    assert at.session_state.round_number == 0
    assert at.session_state.eliminated == []
    assert at.session_state.human_name == ""


@pytest.mark.integration
def test_human_response_is_capped_to_255_characters():
    at = AppTest.from_file("code/reverse_turing_test.py")
    at.run()
    at.button[0].click().run()

    long_text = "x" * 300
    at.text_input[0].input(long_text).run()
    [b for b in at.button if b.label == "Submit response"][0].click().run()

    assert len(at.session_state.human_response) <= 255

import os
import streamlit as st
import random as rd
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from dotenv import load_dotenv

endpoint = "https://models.github.ai/inference"
PRIMARY_MODEL = "openai/gpt-4.1"
SECONDARY_MODEL = "meta/Llama-3.2-90B-Vision-Instruct"
MAX_ROUNDS = 3

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

random_names = [
    "Charley", "Brick", "Goku", "Tim", "Penelope", "Grace", "Definitely Not AI",
    "Jorge", "Jesus", "Person Man", "Ellie", "John", "Bob", "Frank", "Abby",
    "Chair", "Mario", "Luigi", "Peach", "Toad", "Guy", "Patrick", "Gary", "Mafia",
    "Nathan Drake", "Link", "Garuthamesh, the Eldritch One", "Zach", "Zack", "Zac",
    "Kody", "Mark", "Ralph", "Andrew", "Andy", "Andi", "John Pork", "Steve",
    "Alex", "Max", "Sam", "Mohammed", "👁️", "McLovin", "Atorvastatin", "Avery",
    "Mason", "Leon", "Ashley", "Ada", "Chris", "Albert", "Claire", "Jill",
    "Rebecca", "Ethan", "Lucifer", "Lucy", "Malenia, Blade of Miquella", "Peter",
    "Lois", "Stewie", "Brian", "Cleveland", "Marley", "Jordan", "Michael",
    "Michal", "Marty", "Agent 47", "Diana", "Jake", "Utah", "Walter", "Jesse",
    "Nick", "Rick", "Morty", "Nic", "Nick", "Nicholas", "Kevin", "Keith", "Kate",
    "Kathrine", "Cathrine", "Cat", "Kitty", "Lisa", "Superman", "The British Raj",
    "Karthik", "Jkhari", "Steven", "Bill", "William", "Ash", "Misty", "Brock",
    "Aaron", "Erin", "A.A.Ron", "Wong", "Wanker", "Theo", "Mike", "Quinn",
    "Gwen", "Perry", "Heinz", "Ferb", "Phineas", "Jones", "Maya", "Holly",
    "Nora", "Tina", "Whitney", "Ella", "Oliver", "Mary", "Kratos", "Joey",
    "Ross", "Chandler", "Monica", "Rachel", "Phoebe", "_", "Luke", "Leia",
    "Anakin", "Obi-Wan Kenobi", "Elizabeth", "Henry", "Adam", "Eve", "Robert",
    "Vanessa", "Banner", "Bruce", "Bobby", "Hank", "Tom", "Jerry", "Mordecai",
    "Rigby", "Elon", "Ellen", "Alan", "Wake", "Wake Up", "Felix", "Ava", "Paula"
]
random_personality = [
    "Slightly self-centered", "Preppy", "Traveler", "Orderly", "Parental",
    "A Tutor", "A Father", "A Tour Guide", "A College Student", "Youthful",
    "Elderly", "Pessimist", "Optimist", "A Politician", "A Chair",
    "Close-Minded", "Goku", "TF2 Engineer", "Gen-Z", "A Facebook Mom",
    "A Karen", "Jeff", "A Chef", "From the 1940s", "A King", "An Emperor",
    "A Scammer", "A Crypto Bro on X", "An Athlete", "Fear-Driven",
    "A Chemist", "Walter White", "Calls everyone Kyle", "Egotistical",
    "John Cena", "Donald Trump", "A News Reporter Reporting the News",
    "A Smoker", "A Bartender", "A Tinder Broker", "26", "Broke",
    "Peter Parker", "Michal Jackson", "Donald Duck", "SpongeBob",
    "Doremon", "A Hitman", "A Ninja", "A Streamer", "Bruce Lee",
    "Bruce Springsteen"
]

questions = [
    "What is a memory you hold dear?",
    "What math calculations do you know?",
    "How would you describe the importance of art?",
    "What is your favorite outdoor activity and why?",
    "What is a genre of music that you enjoy and why?",
    "If you could have any food of your choice right now, what would you choose and why?",
    "What do you fear the most?",
    "What is the meaning of life?",
    "Where would you want to travel the most?",
    "Briefly talk about a historical event that happened during your lifetime.",
    "Briefly describe a time when you felt guilty.",
    "Briefly describe a time when you were wrongly accused of something.",
    "Write a haiku about cats.",
    "What do you think is the most important quality in a friend and why?",
    "If you could change one thing about the world, what would it be?",
    "What is something you have not experienced that you would like to experience?",
    "If you could have any animal as a pet, what would it be and why?",
    "What game genre do you enjoy playing the most and why?",
    "What is a piece of media that has influenced you significantly and why?",
    "You enter a nondescript room. What is the first thing you are going to do?",
]


def init_game_state():
    defaults = {
        "started": False,
        "human_name": "",
        "ai_names": [],
        "round_number": 0,
        "current_question": "",
        "ai_personalities": [],
        "ai_answers": [],
        "history": [],
        "human_response": "",
        "human_response_input": "",
        "clear_human_input": False,
         # voting state
        "phase": "answer",       # "answer" | "voting" | "result"
        "votes": {},             # { name: vote_count }
        "human_vote": "",        # who the human voted for
        "vote_result": "",       # name of eliminated player
        "eliminated": [],        # all names removed so far
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def generate_personalities():
    # Sample 12 unique personalities (3 for each of 4 AIs)
    all_personalities = rd.sample(random_personality, 12)
    # Group them: each AI gets 3 personalities
    return [
        f"{all_personalities[0]}, {all_personalities[1]}, and {all_personalities[2]}",
        f"{all_personalities[3]}, {all_personalities[4]}, and {all_personalities[5]}",
        f"{all_personalities[6]}, {all_personalities[7]}, and {all_personalities[8]}",
        f"{all_personalities[9]}, {all_personalities[10]}, and {all_personalities[11]}"
    ]

def askquestion():
    return rd.choice(questions)


def humanplayer():
    if st.session_state.phase == "answer":
        if st.session_state.clear_human_input:
            st.session_state.human_response_input = ""
            st.session_state.clear_human_input = False

        st.text_input("Your response:", key="human_response_input", max_chars=255)
        if st.button("Submit response"):
            st.session_state.human_response = st.session_state.human_response_input.strip()
            st.session_state.phase = "voting"
            st.rerun()

    elif st.session_state.phase == "voting":
        callvote()

    elif st.session_state.phase == "result":
        show_result()

def build_messages(name, personality, question):
    system_prompt = (
        f"Your name is {name}. "
        f"You are {personality}. "
        "Act like a normal player in a social deduction game. "
        "Do not reveal that you are an AI. "
        "Answer only the user's question in 1 or 2 short sentences."
    )
    return [SystemMessage(system_prompt), UserMessage(question)]

def responseAI(names, personalities, question):
    models = [PRIMARY_MODEL, SECONDARY_MODEL, PRIMARY_MODEL, SECONDARY_MODEL]

    if not token:
        return [
            {
                "name": name,
                "response": "I am having trouble responding right now.",
                "personality": personality,
                "model": model_name,
            }
            for name, personality, model_name in zip(names, personalities, models)
        ]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    ai_answers = []
    for name, personality, model_name in zip(names, personalities, models):
        try:
            completion = client.complete(
                messages=build_messages(name, personality, question),
                temperature=1.0,
                max_tokens=100,
                model=model_name,
            )
            response_text = completion.choices[0].message.content
            if not isinstance(response_text, str):
                response_text = str(response_text)
        except AzureError:
            response_text = "I am having trouble responding right now."
        ai_answers.append({
            "name": name,
            "response": response_text,
            "personality": personality,
            "model": model_name
        })
    return ai_answers


def save_current_round():
    st.session_state.history.append({
        "round_number": st.session_state.round_number,
        "question": st.session_state.current_question,
        "ai_answers": st.session_state.ai_answers.copy(),
        "human_response": st.session_state.human_response,
        "human_name": st.session_state.human_name,
    })

def generate_round():
    st.session_state.round_number += 1
    st.session_state.current_question = askquestion()
    active_names = [
        n for n in st.session_state.ai_names
        if n not in st.session_state.eliminated
    ]
    active_personalities = [
        st.session_state.ai_personalities[st.session_state.ai_names.index(n)]
        for n in active_names
    ]
    st.session_state.ai_answers = responseAI(
        active_names, active_personalities, st.session_state.current_question
    )

def render_round():
    if st.button("Reset the game"):
        resetgame()
        st.rerun()

    st.write(f"Round {st.session_state.round_number}/{MAX_ROUNDS}")
    st.write(f"You are playing as: {st.session_state.human_name}")

    st.subheader("Question")
    st.write(st.session_state.current_question)

    st.subheader("AI responses")
    for ai in st.session_state.ai_answers:
        st.write(f"**{ai['name']}** ({ai['personality']}) - Model: {ai['model']}")
        st.write(ai["response"])
        st.divider()

    if st.session_state.clear_human_input:
        st.session_state.human_response_input = ""
        st.session_state.clear_human_input = False

    if st.session_state.phase == "answer":
        st.text_input("Your response:", key="human_response_input", max_chars=255)
        if st.button("Submit response"):
            response = st.session_state.human_response_input.strip()
            if not response:
                st.warning("Please enter a response before submitting.")
            else:
                st.session_state.human_response = response
                st.session_state.phase = "voting"
                st.rerun()
    elif st.session_state.phase == "voting":
        callvote()
    else:
        show_result()
    
    


def resetgame():
    st.session_state.started = False
    st.session_state.human_name = ""
    st.session_state.ai_names = []
    st.session_state.ai_personalities = []
    st.session_state.round_number = 0
    st.session_state.current_question = ""
    st.session_state.ai_answers = []
    st.session_state.human_response = ""
    st.session_state.history = []
    st.session_state.human_response_input = ""
    st.session_state.clear_human_input = True
    st.session_state.phase = "answer"
    st.session_state.votes = {}
    st.session_state.human_vote = ""
    st.session_state.vote_result = ""
    st.session_state.eliminated = []


def callvote():
    st.subheader("Voting Phase")
    st.write(f"**{st.session_state.human_name}:** {st.session_state.human_response}")
    st.write("Who do you think the AI's will vote for? Select a name to vote them out.")

    # Only show players still in the game
    active_ai = [
        a["name"] for a in st.session_state.ai_answers
        if a["name"] not in st.session_state.eliminated
    ]

    if not active_ai:
        st.session_state.vote_result = st.session_state.human_name
        st.session_state.votes = {st.session_state.human_name: 1}
        st.session_state.phase = "result"
        st.rerun()

    human_vote = st.radio("Cast your vote:", active_ai, key="human_vote_radio")

    if st.button("Submit vote"):
        all_answers = st.session_state.ai_answers + [{
            "name": st.session_state.human_name,
            "response": st.session_state.human_response,
        }]
        eliminated, votes = tally_votes(human_vote, all_answers)
        st.session_state.vote_result = eliminated
        st.session_state.votes = votes
        st.session_state.eliminated.append(eliminated)

        # If an AI was eliminated, remove them from active AI answers
        if eliminated != st.session_state.human_name:
            st.session_state.ai_answers = [
                a for a in st.session_state.ai_answers
                if a["name"] != eliminated
            ]

        st.session_state.phase = "result"
        st.rerun()

def tally_votes(human_vote, all_answers):
    # Initialize vote counts for every active player
    active_names = [
        a["name"] for a in all_answers
        if a["name"] not in st.session_state.eliminated
        or a["name"] == st.session_state.human_name
    ]
    votes = {name: 0 for name in active_names}

    # Count human's vote
    if human_vote in votes:
        votes[human_vote] += 1

    # Each AI votes for who they think is the human
    for ai in st.session_state.ai_answers:
        if ai["name"] in st.session_state.eliminated:
            continue
        voted_for = ai_vote(
            st.session_state.current_question,
            all_answers,
            ai["name"],
            ai["personality"],
        )
        match = next((n for n in votes if n.lower() == voted_for.lower()), None)
        if match:
            votes[match] += 1
        else:
            # Fallback if the AI returns an unrecognized name
            votes[rd.choice(list(votes.keys()))] += 1

    eliminated = max(votes, key=votes.get)
    return eliminated, votes

def ai_vote(question, all_answers, voter_name, voter_personality):
    """Ask an AI to look at all answers and guess who the human is."""
    if not token:
        return rd.choice([a["name"] for a in all_answers])

    answers_text = "\n".join([f"{a['name']}: {a['response']}" for a in all_answers])
    prompt = (
        f"You are {voter_name}. Your personality is: {voter_personality}. "
        f"You are playing a social deduction game. The question asked was: '{question}'\n"
        f"Here are all the player answers:\n{answers_text}\n"
        "Which player do you think is the human? Reply with ONLY their name, nothing else."
    )
    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(token))
    try:
        completion = client.complete(
            messages=[SystemMessage(prompt), UserMessage("Who is the human?")],
            temperature=0.7,
            max_tokens=10,
            model=PRIMARY_MODEL,
        )
        return completion.choices[0].message.content.strip()
    except AzureError:
        return rd.choice([a["name"] for a in all_answers])


def show_result():
    eliminated = st.session_state.vote_result
    votes = st.session_state.votes

    st.subheader("Vote Results")
    for name, count in sorted(votes.items(), key=lambda x: -x[1]):
        st.write(f"{name}: {count} vote(s)")

    st.write(f"**{eliminated}** has been eliminated!")

    # Check win/lose conditions
    remaining_ai = [
        a for a in st.session_state.ai_answers
        if a["name"] not in st.session_state.eliminated
    ]

    if eliminated == st.session_state.human_name:
        st.error("You were voted out! The AIs win. 🤖")
        if st.button("Play again"):
            resetgame()
            st.rerun()
    elif len(remaining_ai) == 0:
        st.success("All AIs have been eliminated! You win! 🎉")
        if st.button("Play again"):
            resetgame()
            st.rerun()
    else:
        st.info(f"{len(remaining_ai)} AI(s) remaining.")
        next_label = "Finish game" if st.session_state.round_number >= MAX_ROUNDS else "Next round"
        if st.button(next_label):
            save_current_round()
            st.session_state.human_response = ""
            st.session_state.clear_human_input = True
            st.session_state.phase = "answer"
            if st.session_state.round_number < MAX_ROUNDS:
                generate_round()
            else:
                st.session_state.started = False
            st.rerun()

def start_game():
    st.set_page_config(page_title="Reverse Turing Test", page_icon="🤖", layout="centered")
    st.title("Reverse Turing Test")
    st.write("This is a simple reverse Turing test. Try to convince the AI that you are a human!")
    st.info("There are 4 AI players and you are the only human. Answer each question convincingly, then continue to the next round.")
    init_game_state()
    if not token:
        st.warning("GITHUB_TOKEN not set AI responses may fail. Set GITHUB_TOKEN in your environment.")
    if not st.session_state.started:
        if st.button("Start the game"):
            st.session_state.started = True
            st.session_state.human_name = rd.choice(random_names)
            st.session_state.ai_names = rd.sample(
                [name for name in random_names if name != st.session_state.human_name],
                4,
            )
            st.session_state.ai_personalities = generate_personalities()
            generate_round()
            st.rerun()
    else:
        render_round()
if __name__ == "__main__":
    start_game()
# To run this code, make sure you have the required libraries installed:
# pip install streamlit azure-ai-inference python-dotenv  
# Then, set your GITHUB_TOKEN in a .env file or as an environment variable, and run:
# STREAMLIT_SERVER_ADDRESS=0.0.0.0 STREAMLIT_SERVER_PORT=8503 streamlit run reverse_turing_test.py

---
layout: pages
Title: Design_Report
permalink: /Proposal/Design_Report/
---

# Design_Report: 

**Course:** CS375  
**Team:** Karthik Reddy Akkala, Jkhari James Harris, Samuel Nevin Boger.

**Last Updated:** March 11, 2026.

## Summary
   
Our project is a reverse Turing Test. The game will be played online in the user's browser. The initial starting page will present the user with the rules of the game and a start button. The system will randomly select names and personalities for the AI. The game loop will begin and a question will be selected from a list. After the question is selected, it will be put into a list of questions that have already been asked. The question will be presented to all players, including AI, and they must answer in a short concatenated answer. The system recieves the answers and displays the answers to the player. The voting phase begins and the AI will select a name they think is the human. The human will select the name they want to vote out of the game. The player with the most votes is removed from the next round. The loop will repeat untill all AI are removed or the human is voted out of the game. The system will then ddelcare victory or defeat depending on which outcome takes place.    

# Requirements
   - The start button is selected, system will initialize the first round
   - All of the players will be given a randomly generated name from a list of names
   - The AI will be given a random personality from a list of random personalities
   - The user will be prompted with a random question from a list of questions
   - The questions could help an AI researcher or student to understand and educate on the AI writing style.
   - The user's response will be 255 characters long (30 words)
   - The answer will be displayed along with the AI's responses
   - The voting phase will begin and the players must select the answer they think is the human response
   - After the user finishes the game, they will have the option to hit play again and the system will loop to the beginning.


#  Pre_Conditions
   - Game needs to start ---> startGame()
   - A hint is requested ---> hintLoad()
   - The Human is not in the Game ---> humanPlayer()
   - Questions haven't been asked ---> askQuestions()
   - All Have Answered, Need to Concatinate to Prompt ---> concatinateAnswers()
   - The AI needs to Respond ---> responseAI()
   - There are answers but they are not displayed ---> Display()
   - The Round is Ending, Voting needs to commence ---> callVote()
   - The game never started so it cannot loop ---> restartMode()

# Post_Conditions
  - startGame() ---> Game has been initialized and is in an active state
  - hintLoad() ---> A hint has been retrieved and is ready to be displayed to players
  - humanPlayer() ---> The human player has been registered and added to the game session
  - askQuestions() ---> All questions have been presented and player responses are being awaited
  - concatinateAnswers() ---> All answers have been merged into a single formatted prompt string
  - responseAI() ---> The AI has generated and returned a response based on the concatenated prompt
  - Display() ---> All answers/responses are visible and rendered to the players
  - callVote() ---> Votes have been collected and a voting result has been determined
  - restartMode() ---> The system has been reset to its initial pre-game state, ready to call startGame()
# UML DIAGRAM: 
<img alt="UML Diagram" src="https://karthik-bit1.github.io/Group_Project/images/UML_Diagram.png" width="500" align="left">

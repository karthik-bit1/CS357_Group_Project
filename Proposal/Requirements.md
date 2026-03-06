---
layout: pages
title: Requirements
permalink: /Proposal/Requirements/
---
# Reverse Turing test

**Course:** CS375  
**Team:** Karthik Reddy Akkala, Jkhari James Harris, Samuel Nevin Boger.
**Version:** v.
**Last Updated:** February 26, 2026.

---

# 1. Overview

## 1.1 Purpose

** Providing entertaining software for individual to understand and play with AI text. And to be able to write prompt that can manipulate AI in detecting human text.

---

# 2. Stakeholders

| Stakeholder questions                                                     | Game Club Member                                         | Professor   |
| ------------------------------------------------------------------------- | ------------------------------------------------------   | ----------- |
| Have you ever talked to an AI? (chatting with AI)                         | Yes, chat with simple text like in general.              |             |
| Which AI models do you tend to use (ie ChatGPT, Gemini, Claude, etc)?     | ChatGPT, Gemini.                                         |             |
| What experiences do you have chatting with AI in general?                 | Asking random questions, looping it.                     |             |
| How can you detect AI generated writing?                                  | Very verbose.                                            |             |
| Have you ever used generative AI for entertainment purposes?              | Roleplaying.                                             |             |
| What’s your experience with social deduction games?                       | Among Us, Secret Hitler.                                |             |
| What is the speed at which you wish for the AI to react to questions?     | It doesn't matter untill it gives message as fast can be.|             |
| What kind of questions can be asked to equally eliminate human from game  | Questions on the human experience.                       |             |
| Do you have any questions for us?                                         | How is the interface going be (we mentioned chat based)  |             |

# 3. Functional Requirements
  - User will be presented with the rules of the game prior to the start of the round
  - Once the start button is selected, system will initialize the first round
  - All of the players will be given a randomly generated name from a list of names
  - The AI will be given a random personality from a list of random personalities
  - The user will be prompted with a random question from a list of questions
  - The user's response will be 255 characters long (30 words
  - Their answer will be displayed along with the AI's responses
  - The voting phase will begin and the players must select the answer they think is the human response
  - The player with the most votes against them is voted out of the round and the remaining players move on to the next round
  - This will repeat until all of the AI are voted out or the human is voted out of the game
  - After the user finishes the game, they will have the option to hit play again and the system will loop to the beginning.

# 4. Non Functional Requirements
  - Give the AI "personality traits" so that they have something to work off of.
## Multiplayer
  - The ability to have multiple human players against multiple AIs.
## Usability
  - Web based interface
  - Clean and clear UI design

# 5. User Stories

## Club Member Story :
  - As a games club member, I would expect the game to start when I press start button.
  - As a games club member, I would like to know how to play before the round begins.
  - As a games club member, I want the game to be interactive and entertaining.
  - As a games club member, I want the AIs to react quickly.
  - As a gmaes club member, I would want an easy to read UI system.
## Professor Story :
  - As a professor, I would want the questions to be educational to the user.
  - As a professor, I would like there to be an educational stance in the game.

# 6. Acceptance Criteria

## Play a round
  - System initializes when the user starts the game
  - The AI will be given a random personailty trait prior to the beginning of the round
  - The system assigns each player a randomly generated name at the start of the game
  - A question is asked, from a list of random questions, to all players
  - 4 AI's will answer the prompts along with the human response
  - Voting round begins after all answers have been given, the players must then decide who is the human
  - Player wins if the Ai if voted out, player loses if they are voted out
  - Game will end and will loop back to the beginning where everything is randomized

# 7. Gantt Chart
The following Gantt chart outlines the projected development schedule for the semester.

![Gantt Chart](/Group_Project/images/Ghanttchat.png)






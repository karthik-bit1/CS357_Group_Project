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

| Stakeholder               | Role            | Goals                                   |
| ------------------------- | --------------- | --------------------------------------- |
| Game Club Member          | Game stands     | Keep it entertaining for and playable     |
| Professor                 | Educational     | To create interactive experience with AI |

---

# 3. Functional Requirements

# Game states: (Game functionality)

## Win/Lose State (Human wins or AI Wins):
- When the human gets voted out or all AI or voted out, the game initiates the Win/Loss condition
## Voting State :
- After each round all players will vote to choose who will be out in the next round
## Rounds State (A randomized question posed each round):
- At the beginning of the game a list of questions for everyone to answer. After all answers are given and displayed, the players must vote who they think is the human. If the AI's has ,more the humans the human wins the game.
# Character Limit :
- The Human and AIs have a character limit of 255.
- The AIs have a word limit of 30.
 ## Acting
  - Allow AI to appear to be thinking about the answer

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






# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- The hints (Lower/Higher) were backwards. I expected the hint to say higher if my guess was too low and hint to say lower if my guess was, I suppose, too high. But the opposite was the reality.

- When a user wins or is out of attempts and clicks "new game" the modal saying "game over" or "You've already won" still persists. I guessed when someone clicks "new game", we start with a fresh start with no information from the previous game but thta was not true here. You can't actually play a new round after winning/losing; you're stuck seeing the same "You already won" / "Game over" message.

- For "Easy" mode the range says integers from 1 - 20. But the secret number is always between integrers 1 - 100. Similarly, for medium and hard, the actual game does not care about the rules on the interval.

- The game allows me to input any integer numbers regardless of the limit they set (from 1 - 100 etc.)

---

## 2. How did you use AI as a teammate?

- I used Composer 1.5 rasoning from Cursor
- Composer did a very good job finding glitches I missed on my own. For example, I hadn't thought of the problem of being able to input lierally any number regardless of the boundary (which was unchecked in the original version)
- Normally I am very happy with the test cases AI generates but this time the test cases were mostly Terminal based, so printing a few things when I am clicking on certain buttons. That seemed less useful since I already have the "Developer Bug info" section within the website.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I checked frequently, tested with edge cases on my own and even without the test code, I succeeded.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - For the reversed go lower or higher, I used the following test to see if the code was doing as intended:
    print(check_guess(60, 50))  
    print(check_guess(40, 50))  
    print(check_guess(50, 50))
- Did AI help you design or understand any tests? How?
  - Since the website is on the simpler side, I can't say I learned a lot, however, I did learn that if there is a way to check for bugs already built into the website then asking AI to make more bug looker code can give you some less useful code. It may just reiterate what's already on the website.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  - Streamlit probably reruns the whole code over and over again without storing unnecessary things in the st.sesion_state. That meant the "goal" kept changing so that the use could never rely on the same number being used multiple times. The OG way of doing this is the good old fashioned random.randint(...)
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  - Normally, local python variables vanish everytime the user changes the number or clicks or changes a widget etc. So, nothing gets saved. But Streamlit has st.session_state which works like a disctionary which survives those reruns and saves the inetractions for the next iteration. It works almost like a loop where even though the UI refreshes after running the whole script over and over again, the scores, and secret numbers are kept stable.
- What change did you make that finally gave the game a stable secret number?
  - Instead of running random,randint(...) over and over again, the secret number is checked if it's in the st.session_state of not and only if it's not, then we assign it a random number, so that it doesn't change for every instance.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - Every time I ask an AI to help debug certain part of the code, I need to make sure that the code AI is changing is only the code that needs changing. Noting more should be modified. The best way to prevent that from happening is to ask it for test cases.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I wouldn't ask for bug looking code if my codebase already has a way to look for bugs.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - When used with properly documented prompts, an AI can be my best coding partner. I don't have to debug the code that AI gives if the AI know's the context and the content of the problem I am trying to solve.

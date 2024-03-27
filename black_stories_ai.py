import openai
import os
import pandas as pd

"""Before using the application you are required to follow the next steps:
        1. Generate your API Key in your OpenAI account (with paid credits)
        2. Install opanai module: pip install -q openai
        3. Install openai module: pip install openai==0.28
        4. Install config module: pip install config
        5. Instal dotenv module: pip install python-dotenv
        6. Make a .env file and add the line: OPENAI_API_KEY="_insert_your_key_"
        7. Make a .gitignore file and add the line: .env
"""
# Open your personal private API Key from the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

path = os.getcwd()
file_path = path + "\\NHC_GPT.xlsx"
df = pd.read_excel(file_path, sep=",")

def chatbot():
  # Create a list to store all the messages for context
  messages = [
    {"role": "system", "content": """You have to solve a black stories riddle. I tell you a black story and you have to solve it by asking me questions.
                                    You have to solve the riddle with as little questions as possible.
                                    The riddle tells you the end of a story and you have to find out what lead to this end. 
                                    When I tell you the riddle, you have to try to solve the riddle by asking questions that I can only answer by yes, no or not relevant to the story. 
                                    You will use my answers to solve the riddle and find the story that lead to the end.
                                    I tell you when you have solved the riddle, then you give me a summary of the story of the riddle.
                                    Note that giving a summary to guess the answer is also counting as one question"""},
  ]

  nr = 0 # number of questions asked
  nr_yes = 0 # number of yes-answers
  nr_no = 0 # number of no-answers
  other_answers = [] # list of other answers given
  questions = {} # dictionary with only the questions of the bot

  # Keep repeating the following
  while True:
    # Prompt user for input
    message = input("User: ").lower()

    # for further analysis, how many yes, no or other content you give to the bot
    if message == 'yes':
      nr_yes += 1
    elif message == 'no':
      nr_no += 1
    else:
      other_answers.append(message)

    # Exit program if user inputs "quit"
    if message.lower() == "quit":
      hints = int(input("Hints given: "))
      print("Number of questions asked: ", nr)

      # make a row of data for the Excel, add to the dataframe and overwrite the existing Excel
      new_row = {"Medium": "GPT", "Group member": team_member, "Blackstory": blackstory_number, "Questions": nr,
                 "Hints": hints, "Score": hints * 5 + nr, "Age": 0, "Chat history": messages,
                 "Questions asked": questions, "Yes": nr_yes, "No": nr_no, "Other": other_answers}
      df.loc[len(df)] = new_row
      df.to_excel(path + f'\\NHC_GPT.xlsx', index=False)

      break

    # Add each new message to the list
    messages.append({"role": "user", "content": message})

    # Request gpt-3.5-turbo for chat completion
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=messages
    )

    # Print the response and add it to the messages list
    chat_message = response['choices'][0]['message']['content']
    print(f"Bot: {chat_message}")
    nr += 1
    messages.append({"role": "assistant", "content": chat_message})

    # also add the respons to the question dictionary
    questions[nr] = chat_message

if __name__ == "__main__":
  # variables for dataframe
  team_member = input("Name team member: ")
  blackstory_number = int(input("Blackstory number: "))

  # begin blackstory
  print("Tell the riddle to the bot! (type 'quit' to stop)!")
  chatbot()
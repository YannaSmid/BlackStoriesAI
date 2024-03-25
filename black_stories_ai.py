import openai
import os
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
    
def chatbot():
  # Create a list to store all the messages for context
  messages = [
    {"role": "system", "content": """You are a playing a riddle game with me. I tell you a riddle and you have to try to solve it by asking me questions.
                                    The riddle tells you the end of a story and you have to find out what lead to this end. 
                                    After you received the riddle, you have to try to solve the riddle by asking questions. 
                                    I can only asnwer the questions with yes no or maybe. 
                                    You will use my answers to solve the riddle."""},
  ]

  nr = 0 #number of questions asked

  # Keep repeating the following
  while True:
    # Prompt user for input
    message = input("User: ")

    # Exit program if user inputs "quit"
    if message.lower() == "quit":
      print("Number of questions asked: ", nr)
      break

    # Add each new message to the list
    messages.append({"role": "user", "content": message})

    # Request gpt-3.5-turbo for chat completion
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    # Print the response and add it to the messages list
    chat_message = response['choices'][0]['message']['content']
    print(f"Bot: {chat_message}")
    nr += 1
    messages.append({"role": "assistant", "content": chat_message})

if __name__ == "__main__":
  print("Tell the riddle to the bot! (type 'quit' to stop)!")
  chatbot()
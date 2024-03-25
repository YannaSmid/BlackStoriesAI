import openai
import os

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
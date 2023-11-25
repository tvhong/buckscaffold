import subprocess
from openai import OpenAI

ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM = "system"

client = OpenAI()
messages = []

def set_context():
  add_message(ROLE_SYSTEM,
# You are a chat bot that can generate bash commands for user on their MacOS machine.
# The user will decide whether to run your code or not. 
# Please enclose any bash code inside <bash></bash> tag.
# """
# You are helping a user to draft some bash code on their machine.
# Don't worry about not able to run the command yourself as the user can choose to run it.
# When provide bash commands, please include them in the <bash> tag.

# Here are some examples:
# User: List the current directory
# Assistant: <bash>ls</bash>

# User: Find out the current directory
# Assistant: <bash>pwd</bash>
# """
"""
Give a oneline bash commmand on macOS for the following queries:
"""
  )


def generate_code():
  prompt = input("Enter a code prompt: ")    
  add_message(ROLE_USER, prompt)

  response = client.chat.completions.create(
    model="gpt-4",
    messages=messages
  )

  return response.choices[0].message.content


def add_message(role, message):
  messages.append({"role": role, "content": message})


def main():
  set_context()
  while True:
    code = generate_code()
    messages.append({"role": ROLE_ASSISTANT, "content": code})
    
    print(f"Generated the following code:\n{code}\n")
    
    choice = input("Run this code? (y/n): ")
    if choice.lower() == 'y':
      proc = subprocess.run(['ls', '-l'], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True)

      add_message(ROLE_USER, "stdout: " + proc.stdout + "\nstderr: " + proc.stderr)
    else:
      add_message(ROLE_USER, "I won't run this code.")

if __name__ == "__main__":
    main()
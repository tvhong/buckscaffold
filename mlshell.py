from colorama import Fore
import re
import subprocess
from openai import OpenAI

ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM = "system"
CODE_REGEX = re.compile(r"<bash>(.*)</bash>")

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
Give a oneline bash commmand on macOS for the following queries and add the bash command inside <bash> tag:
"""
  )


def chat():
  prompt = input("> ")    
  add_message(ROLE_USER, prompt)

  response = client.chat.completions.create(
    model="gpt-4",
    messages=messages
  )

  return response.choices[0].message.content.strip()


def extract_code(text):
  match = CODE_REGEX.search(text)
  if match:
    return match.group(1)
  return ""


def add_message(role, message):
  messages.append({"role": role, "content": message})


def main():
  set_context()
  while True:
    response = chat()
    print(f"{Fore.LIGHTRED_EX}assistant: {response}{Fore.WHITE}")

    messages.append({"role": ROLE_ASSISTANT, "content": response})
    
    code = extract_code(response)
    if code:
      choice = input(f"run `{code}` (y/n)? > ")
      if choice.lower() == 'y':
        proc = subprocess.run(code, 
                      shell=True,
                      stdout=subprocess.PIPE,
                      stderr=subprocess.PIPE,
                      universal_newlines=True)

        msg = f"user: {Fore.LIGHTGREEN_EX}<stdout>{proc.stdout}</stdout>\n<stderr>{proc.stderr}</stderr>{Fore.WHITE}"
        print(msg)
        add_message(ROLE_USER, msg)
      else:
        add_message(ROLE_USER, "I won't run this code.")

if __name__ == "__main__":
    main()
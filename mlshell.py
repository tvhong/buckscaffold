import subprocess
from openai import OpenAI

client = OpenAI()

messages = []
# context = ""

# def set_context():
#   global context
#   new_context = input("Enter a context prompt for future code (leave empty to keep previous context): ")
#   if new_context:
#     context = new_context
#     print(f"Context updated to: {context}")

def generate_code():
  prompt = input("Enter a code prompt: ")    
  messages.append({"role": "user", "content": prompt})

  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
  )

  return response.choices[0].message

def main():
  while True:
    code = generate_code()
    messages.append({"role": "chatgpt", "content": code})
    
    print(f"Generated the following code:\n{code}\n")
    
    choice = input("Run this code? (y/n): ")
    if choice.lower() == 'y':
      proc = subprocess.run(['ls', '-l'], 
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True)

      messages.append({"role": "system", "content": proc.stdout + proc.stderr})
    else:
      messages.append({"role": "system", "content": "user refused to run the code"})


if __name__ == "__main__":
    main()
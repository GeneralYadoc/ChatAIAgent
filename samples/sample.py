import sys
import datetime
import ChatAIAgent as ca  # Import this.

# callback for getting questions that actually thrown to ChatGPT
# If you register external info to user message when you put it, you can obtain the external info here.
def ask_cb(user_message):
  time_str = user_message.extern.strftime ('%H:%M:%S')
  print(f"\n[question {time_str}] {user_message.message}\n")

# callback for getting answer of ChatGPT
def answer_cb(user_message, completion):
  time_str = datetime.datetime.now().strftime ('%H:%M:%S')
  message = completion.choices[0]["message"]["content"]
  print(f"[answer {time_str}] {message}\n")

# ChatGPT API Key is given from command line in this example.
if len(sys.argv) <= 1:
  exit(0)

system_role="You are a cheerful assistant who speek English and can get conversation exciting with user."

# Create ChatAIAgent instance.
agent = ca.ChatAIAgent( api_key=sys.argv[1],
                        system_role=system_role,
                        ask_cb=ask_cb,
                        answer_cb=answer_cb,
                        max_tokens_per_request = 2048 )

# Wake up internal thread on which ChatGPT answer messages will be generated.
agent.start()

cnt = 0
while True:
  message = input("")
  if message == "":
    break
  # Put message received from stdin on internal queue to be available from internal thread.
  agent.put_message(ca.userMessage(message=message,extern=datetime.datetime.now()))

# Finish generating answers.
# Internal thread will stop soon.
agent.disconnect()

# terminating internal thread.
agent.join()

del agent

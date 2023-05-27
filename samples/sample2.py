# To execute this sample, please install streamchat-agent from PyPI as follows.
# $ pip install streamchat-agent
import sys
import time
import math
import re
import datetime
import StreamChatAgent as sca
import ChatAIAgent as ca

def print_incremental(st, interval_sec):
  for i in range(len(st)):
    if not running:
      break
    print(f"{st[i]}", end='')
    sys.stdout.flush()
    interruptible_sleep(interval_sec)

def interruptible_sleep(time_sec):
  counter = math.floor(time_sec / 0.01)
  frac = time_sec - (counter * 0.01)
  for i in range(counter):
    if not running:
      break
    time.sleep(0.01)
  if not running:
    return
  time.sleep(frac)

def answer_cb(user_message, completion):
  print(f"\n[{user_message.extern.author.name} {user_message.extern.datetime}] {user_message.message}\n")
  interruptible_sleep(3)
  time_str = datetime.datetime.now().strftime ('%H:%M:%S')
  message = completion.choices[0]["message"]["content"]
  print(f"[ChatGPT {time_str}] ", end='')
  print_incremental(message, 0.05)
  print("\n")
  interruptible_sleep(5)

def get_item_cb(c):
  ai_agent.put_message(ca.userMessage(message=c.message, extern=c))

def pre_filter_cb(c):
  return None if re.match(r'^(:[^:]+:)+$', c.message) else c

def post_filter_cb(c):
  c.message = re.sub(r':[^:]+:','', c.message)
  return c

running = False

if len(sys.argv) <= 2:
  exit(0)

sca_params = sca.params(
  video_id=sys.argv[1],
  get_item_cb=get_item_cb,
  pre_filter_cb=pre_filter_cb,
  post_filter_cb=post_filter_cb
)
stream_agent = sca.StreamChatAgent( sca_params )

ca_params = ca.params(
  api_key=sys.argv[2],
  system_role="You are a cheerful assistant who speek English and can get conversation exciting with user.",
  answer_cb=answer_cb
)
ai_agent = ca.ChatAIAgent( ca_params )

running = True
stream_agent.start()
ai_agent.start()

input()
running=False

ai_agent.disconnect()
stream_agent.disconnect()

ai_agent.join()
stream_agent.join()

del stream_agent
del ai_agent

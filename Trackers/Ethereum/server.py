from flask import Flask
from threading import Thread 

app = Flask('')

@app.route('/')
def home():
  return '- Ethereum|Odin is active -'

def run():
  app.run(host='0.0.0.0',port=8000)

def activate():
  t = Thread(target=run)
  t.start()
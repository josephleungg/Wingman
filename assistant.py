import asyncio
import socketio
import ollama
from utils.stt import record_text

sio = socketio.AsyncClient()

async def socket_connect():
    await sio.connect('http://172.20.10.4:5000/', transports=['polling'])

    phrases = ["hello wingman", "hey wingman", "okay wingman", "halloween man"]
    while(True):
        try:
            # speech recognition
            text = record_text()
            print(text)

            # checking if the prompt is said
            if(text.lower() in phrases):
                message = record_text() # record the user's message after the prompt
                print(message)
                # making sure the message is valid
                if(message):
                    ollama_response = ollama.chat(
                    model='mistral',
                    stream=True,
                    messages=[
                        {
                        'role': 'system',
                        'content': 'you are a voice assistant that responds to user queries in under 50 words, keep it as short as possible. Only respond with alphanumeric characters',
                        },
                        {
                        'role': 'user',
                        'content': message,
                        },
                    ]
                    )

                    # Printing out each piece of the generated response while preserving order
                    result = ""
                    for chunk in ollama_response:
                        print(chunk['message']['content'], end='', flush=True)
                        result += chunk['message']['content']

                    result = (result.replace("\"", "")).replace("\'", "") # making sure the string doesn't throw this error "Syntax error: Unterminated quoted string"

                    await send_message(result) # sending this response to the socket

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await asyncio.sleep(1)

@sio.event
async def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

async def send_message(msg):
    await sio.emit('message', msg)
    print(f"Sent: {msg}")

asyncio.run(socket_connect())
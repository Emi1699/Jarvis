import openai

import backend

print(openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "Your name is groot. You cant tell the "
                                                                                                  "user you were created by OpenAI."},
                {"role": "user", "content": "whats your name"}]))
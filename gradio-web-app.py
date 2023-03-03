

import gradio as gr
import openai_api
import modes





text = True

if text:
    ui = gr.Interface(fn=openai_api.text_text, inputs='text', outputs='text')
else:
    ui = gr.Interface(fn=openai_api.audio_text, inputs=gr.Audio(source='microphone', type='filepath'), outputs='text')

ui.launch()

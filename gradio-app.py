import PySimpleGUI as sg
import gradio as gr


def predict(text):
    # function to predict output based on input text
    return text.capitalize()


# Create a Gradio interface
gr_interface = gr.Interface(
    fn=predict,
    inputs=gr.inputs.Textbox("Enter your text here"),
    outputs="text",
    title="My Gradio Desktop Application"
)

# Create a PySimpleGUI interface
sg_interface = sg.Window('My PySimpleGUI Desktop App', [[sg.Multiline('', size=(60, 20))], [sg.Button('Predict')]])

# Event loop that allows for running the PySimpleGUI interface and interacting with the Gradio interface
while True:
    event, values = sg_interface.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Predict':
        results = gr_interface.predict(values[0])
        sg.popup(results)

# Close the Gradio interface
gr_interface.close()



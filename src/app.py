"""
Main application file that combines FastAPI and Gradio interfaces.
"""
import gradio as gr

from .api import app
from .gradio_ui import create_gradio_interface


# Create Gradio interface
gradio_app = create_gradio_interface()

# Mount Gradio app to FastAPI
app = gr.mount_gradio_app(app, gradio_app, path="/")

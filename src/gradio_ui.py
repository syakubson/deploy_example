"""
Gradio web interface for Qwen3 text generation.
"""
import gradio as gr

from .model_manager import model_manager


def gradio_generate(message: str):
    """Generate text for Gradio interface."""
    if not model_manager.is_model_loaded():
        return "Model not loaded", "Error: Model not loaded"
    
    try:
        thinking, content = model_manager.generate_text(message)
        return thinking, content
    except Exception as e:
        return "", f"Error: {str(e)}"


def gradio_check_status():
    """Check service status for Gradio interface."""
    model_loaded = model_manager.is_model_loaded()
    status = "Healthy" if model_loaded else "Unhealthy"
    loaded = "Yes" if model_loaded else "No"
    return f"Status: {status}\nModel Loaded: {loaded}"


# Create Gradio interface
def create_gradio_interface():
    """Create and return Gradio interface."""
    with gr.Blocks(title="Qwen3 Text Generation") as gradio_app:
        gr.Markdown("# Qwen3 Text Generation Service")
        gr.Markdown("Enter your message and get AI-generated response with thinking process")
        
        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(
                    label="Input Message",
                    placeholder="Enter your message here...",
                    lines=5
                )
                generate_btn = gr.Button("Generate", variant="primary")
                
            with gr.Column():
                thinking_output = gr.Textbox(
                    label="Thinking Process",
                    lines=10,
                    interactive=False
                )
                content_output = gr.Textbox(
                    label="Generated Content",
                    lines=10,
                    interactive=False
                )
        
        with gr.Row():
            status_btn = gr.Button("Check Status")
            status_output = gr.Textbox(
                label="Service Status",
                lines=2,
                interactive=False
            )
        
        # Connect buttons to functions
        generate_btn.click(
            fn=gradio_generate,
            inputs=[input_text],
            outputs=[thinking_output, content_output]
        )
        
        status_btn.click(
            fn=gradio_check_status,
            inputs=[],
            outputs=[status_output]
        )
    
    return gradio_app


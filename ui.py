import gradio as gr
from utils import ui_methods
from custom_components import Gallery


def create_ui():
    with gr.Blocks() as demo:
        with gr.Row():
            gallery = Gallery(label='images', elem_id='display_image').style(columns=4)
            image = gr.Image(label='image', interactive=False, type='pil', elem_id='select_image').style(height=480)
        with gr.Row():
            with gr.Column(scale=80):
                with gr.Row():
                    image_dir = gr.Textbox(label='image_dir', value='imgs')
                    output_dir = gr.Textbox(label='output_dir', value='outputs')
                prompt = gr.Textbox(label='prompt', elem_id='display_image_prompt')
                with gr.Row():
                    save_botton = gr.Button(value='save prompt')
            with gr.Column(scale=1):
                image_idx = gr.Textbox(value='-1', label='idx')
                load_botton = gr.Button(value='load images')
                previous_botton = gr.Button(value='previous image', interactive=False)
                next_botton = gr.Button(value='next image', interactive=False)
                format_dir = gr.Button(value="format output_dir", interactive=False)

        load_botton.click(
            fn=ui_methods.load_images,
            inputs=[image_dir],
            outputs=[gallery, image_idx, previous_botton, next_botton, format_dir]
        )
        
        previous_botton.click(
            fn=lambda x: gr.update(value=str(int(x) - 1)),
            inputs=[image_idx],
            outputs=[image_idx]
        )

        next_botton.click(
            fn=lambda x: gr.update(value=str(int(x) + 1)),
            inputs=[image_idx],
            outputs=[image_idx]
        )

        save_botton.click(
            fn=ui_methods.save_prompt,
            inputs=[output_dir, image_idx, image, prompt],
            outputs=[image_idx]
        )

        image_idx.change(
            fn=ui_methods.caption_select_image,
            inputs=[output_dir, image_idx, gallery],
            outputs=[image, prompt]
        )

        format_dir.click(
            fn=ui_methods.format_output_dir,
            inputs=[output_dir]
        )

    return demo


if __name__ == '__main__':
    demo = create_ui()
    demo.launch(
        server_name='0.0.0.0',
        server_port=7865,
    )
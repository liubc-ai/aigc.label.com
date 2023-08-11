import glob
import traceback
import io
import os
import requests
import gradio as gr
from PIL import Image
from tqdm import tqdm
from logger import logger


class UI_Methods(object):

    def __init__(self, logger):
        self.logger = logger

    def load_images(self, image_dir):
        try:
            path_list = glob.glob(image_dir + '/*.png')
            image_list = []
            for path in tqdm(path_list):
                image = Image.open(path)
                image_list.append(image)
            return gr.update(value=image_list), gr.update(value='0'), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True)
        except Exception as exc:
            self.logger.error(f'load_images error: {exc}\n {traceback.format_exc()}\n')
            return gr.update(), gr.update(), gr.update(), gr.update(), gr.update()

    def caption_select_image(self, output_dir: str, image_idx: str, images: dict):
        try:
            image_idx = int(image_idx)
            if image_idx >= 0 and image_idx >= len(images):
                image_idx -= len(images)
            elif image_idx <= 0 and abs(image_idx) >= len(images):
                image_idx += len(images) 
            image_info = images[image_idx]
            image_url = image_info['data']
            resp = requests.get(image_url).content
            image = Image.open(io.BytesIO(resp))
            if os.path.exists(output_dir + f'/{image_idx}.txt'):
                with open(output_dir + f'/{image_idx}.txt', 'r') as f:
                    prompt = f.read()
                    return gr.update(value=image), gr.update(value=prompt), gr.update(value=str(image_idx))
            else:
                return gr.update(value=image), gr.update(value=''), gr.update(value=str(image_idx))
        except Exception as exc:
            self.logger.error(f'caption_select_image error: {exc}\n {traceback.format_exc()}\n')
            return gr.update()

    def save_prompt(self, output_dir: str, image_idx: str, image, prompt: str):
        try:
            save_path = '/'.join([output_dir, f'{image_idx}.png'])
            image.save(save_path)
            with open(save_path.replace('.png', '.txt'), 'w') as f:
                f.write(prompt)
            return gr.update(value=str(int(image_idx) + 1))
        except Exception as exc:
            self.logger.error(f'save_label error: {exc}\n {traceback.format_exc()}\n')
            return gr.update()
    
    def format_output_dir(self, output_dir):
        try:
            path_list = glob.glob(output_dir + '/*.png')
            for i, path in enumerate(tqdm(path_list)):
                basedir = path[:path.rfind('/')]
                image = Image.open(path)
                with open(path.replace('.png', '.txt'), 'r') as f:
                    content = f.read()
                new_name = str(i).zfill(6)
                image.save(basedir + '/' + new_name + '.png')
                with open(basedir + '/' + new_name + '.txt', 'w') as f:
                    f.write(content)
                os.unlink(path)
                os.unlink(path.replace('.png', '.txt'))

        except Exception as exc:
            self.logger.error(f'format_output_dir: {exc}\n {traceback.format_exc()}\n')


ui_methods = UI_Methods(logger)
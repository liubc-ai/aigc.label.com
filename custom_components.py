from __future__ import annotations
import numpy as np
import gradio as gr
import numpy as np
from enum import Enum
from typing import Callable, List, Tuple, Any
from typing_extensions import Literal
from PIL import Image as _Image
from gradio import utils, processing_utils


class _Keywords(Enum):
    NO_VALUE = "NO_VALUE"  # Used as a sentinel to determine if nothing is provided as a argument for `value` in `Component.update()`
    FINISHED_ITERATING = "FINISHED_ITERATING"  # Used to skip processing of a component's value (needed for generators + state)


class Gallery(gr.Gallery):

    def postprocess(
        self,
        y: List[np.ndarray | _Image.Image | str]
        | List[Tuple[np.ndarray | _Image.Image | str, str]]
        | None,
    ) -> List[str]:
        """
        Parameters:
            y: list of images, or list of (image, caption) tuples
        Returns:
            list of string file paths to images in temp directory
        """
        if y is None:
            return []
        output = []
        for img in y:
            caption = None
            if isinstance(img, tuple) or isinstance(img, list):
                img, caption = img
            if isinstance(img, np.ndarray):
                file = processing_utils.save_array_to_file(img)
                file_path = str(utils.abspath(file.name))
                self.temp_files.add(file_path)
            elif isinstance(img, _Image.Image):
                file = processing_utils.save_pil_to_file(img)
                file_path = str(utils.abspath(file.name))
                self.temp_files.add(file_path)
            elif isinstance(img, str):
                # if utils.validate_url(img):
                file_path = img
                # else:
                #     file_path = self.make_temp_copy_if_needed(img)
            else:
                raise ValueError(f"Cannot process type as image: {type(img)}")

            if caption is not None:
                output.append(
                    [{"name": file_path, "data": None, "is_file": True}, caption]
                )
            else:
                output.append({"name": file_path, "data": None, "is_file": True})

        return output

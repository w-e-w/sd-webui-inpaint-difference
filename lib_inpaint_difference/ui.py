import gradio as gr
from modules.shared import opts
from modules.ui_components import ToolButton

from lib_inpaint_difference.globals import DifferenceGlobals
from lib_inpaint_background.context_pack import ParentBlock
from lib_inpaint_difference.mask_processing import compute_mask


def create_inpaint_difference_tab():
    with ParentBlock():
        with gr.TabItem('Inpaint difference', id='inpaint_difference', elem_id="img2img_inpaint_difference_tab") as tab_inpaint_automask:
            with gr.Row():
                DifferenceGlobals.inpaint_img_component = gr.Image(label="Base image", source="upload", interactive=True, type="pil", elem_id="img_inpaint_difference")
                swap_images = ToolButton('⇆', elem_id='img2img_inpaint_difference_swap_images', tooltip="Swap images.")
                DifferenceGlobals.inpaint_alt_component = gr.Image(label="Altered image", source="upload", interactive=True, type="pil", elem_id="alt_inpaint_difference")

            DifferenceGlobals.inpaint_mask_component = gr.Image(label="Difference mask", interactive=False, type="pil", elem_id="mask_inpaint_difference", tool="sketch", height=opts.img2img_editor_height, brush_color=opts.img2img_inpaint_mask_brush_color)

    def swap_images_func(img, alt):
        DifferenceGlobals.base_image = alt
        DifferenceGlobals.altered_image = img
        return gr.update(value=alt), gr.update(value=img)

    image_components = [DifferenceGlobals.inpaint_img_component, DifferenceGlobals.inpaint_alt_component]
    swap_images.click(swap_images_func, inputs=image_components, outputs=image_components)

    return tab_inpaint_automask


def inject_inpaint_difference_generation_params_ui():
    mask_dilation = gr.Slider(label='Mask dilation', visible=False, maximum=100, step=1, value=0, elem_id='inpaint_difference_mask_dilation')

    params = {
        'fn': compute_mask,
        'inputs': [
            DifferenceGlobals.inpaint_img_component,
            DifferenceGlobals.inpaint_alt_component,
            mask_dilation,
        ],
        'outputs': [DifferenceGlobals.inpaint_mask_component]
    }

    DifferenceGlobals.inpaint_img_component.upload(**params)
    DifferenceGlobals.inpaint_img_component.clear(**params)
    DifferenceGlobals.inpaint_alt_component.upload(**params)
    DifferenceGlobals.inpaint_alt_component.clear(**params)
    mask_dilation.release(**params)

    DifferenceGlobals.ui_params = mask_dilation,

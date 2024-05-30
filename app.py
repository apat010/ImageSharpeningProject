import numpy as np
from PIL import Image, ImageFilter
from matplotlib import pyplot as plt
import tempfile
import os
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.types import FileInfo

def gaussian_blur(image, kernel_size=15, sigma=0):
    from scipy.ndimage import gaussian_filter
    return gaussian_filter(image, sigma=sigma)

def sharpen_image(image):
    image = np.array(image).astype(np.float32) / 255.0
    
    blurred_image = gaussian_blur(image, kernel_size=15, sigma=3)
    
    sharpened_image = 2.3 * image - blurred_image
    sharpened_image = np.clip(sharpened_image, 0, 1)
    
    sharpened_image_uint8 = (sharpened_image * 255).astype(np.uint8)
    
    return Image.fromarray(sharpened_image_uint8)

def process_and_display_sharpened_image(image_path):
    original_image = Image.open(image_path)
    sharpened_image = sharpen_image(original_image)
    
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, "sharpened_image.jpg")
    sharpened_image.save(temp_file)

    return temp_file

app_ui = ui.page_fluid(
    ui.navset_tab_card(
        ui.nav("Title and Description",
            ui.h2("Jpeg/Jpg/Pdf Photo Sharpening Web Application"),
            ui.p("This Web App was created using Python and Shiny. Allowing you to upload a photo and view a sharpened result. The sharpened result is created by applying a convolutional filter to the original image. In Specific the convolutional filter used in this image sharpening process works by emphasizing edges and fine details in the image. This is achieved through a combination of Gaussian blur filter (Kernel Size (15,15)) applied on the original image and then subtracting those values from the original image,  and a scaling operation (x2.2) that enhances the high-frequency components of the image (such as edges) while reducing the low-frequency components (such as smooth gradients).")
        ),
        ui.nav("Original Image",
            ui.input_file("file1", "Choose Image File", accept=[".jpg", ".jpeg", ".pdf"], multiple=False),
            ui.input_checkbox("show", "Show Original image?", value=True),
            ui.output_image("originalimage")
        ),
        ui.nav("Sharpened Image",
            ui.input_checkbox("show1", "Show Sharpened image?", value=True),
            ui.output_image("sharpenedimage")
        )
    )
)

def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def parsed_image():
        file: list[FileInfo] | None = input.file1()
        if file is None:
            return None
        return file[0]["datapath"]

    @render.image
    def originalimage():
        img_src = parsed_image()
        return {"src": img_src, "width": "auto", "height": "auto"} if img_src and input.show() else None

    @reactive.calc
    def sharpened_image():
        img_path = parsed_image()
        if img_path:
            return process_and_display_sharpened_image(img_path)
        else:
            return None

    @render.image
    def sharpenedimage():
        img_src = sharpened_image()
        return {"src": img_src, "width": "auto", "height": "auto"} if img_src and input.show1() else None

app = App(app_ui, server)
app.run()

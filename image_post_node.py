import json
import requests
from io import BytesIO
import numpy as np
from PIL import Image

class PostImageToAPI:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", ),
                "api_url": ("STRING", {"default": ""}),
                "api_object_id": ("STRING", {"forceInput": True}),
                "api_key": ("STRING", {"forceInput": True})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "post_images"
    CATEGORY = "API Manager"
    OUTPUT_NODE = True

    def post_images(self, images, api_url, api_object_id, api_key=""):
        api_url = api_url.replace("$id", api_object_id)
        headers = {'Authorization': api_key} if api_key else {}
        
        # Prepare all images for a single request
        files = []
        for (batch_number, image_tensor) in enumerate(images):
            image_np = 255. * image_tensor.cpu().numpy()
            image = Image.fromarray(np.clip(image_np, 0, 255).astype(np.uint8))
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            # Add each image to the files list with 'images[]' as the field name
            files.append(('images[]', (f'image_{batch_number}.png', buffer, 'image/png')))
        
        # Send all images in a single request
        response = requests.post(api_url, headers=headers, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"PostImageToAPI: Posted {len(images)} images to {api_url}\nResponse: {result}")
            return {"api_responses": [result]}
        else:
            print(f"Error posting images: {response.text}")
            return {"api_responses": []}

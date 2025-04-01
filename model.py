from ultralytics import YOLO
from PIL import Image
import numpy as np

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

def detect_human(image_path):
    image = Image.open(image_path).convert("RGB")  # Load image using PIL
    results = model.predict(source=np.array(image))  # Pass the image as a NumPy array
    
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  # Bounding boxes
        class_ids = result.boxes.cls.cpu().numpy()  # Class IDs
        
        for box, class_id in zip(boxes, class_ids):
            if int(class_id) == 0:  # Class ID 0 is "person"
                x1, y1, x2, y2 = map(int, box)  
                cropped_person = image.crop((x1, y1, x2, y2))  
                
                # Create a mask for the detected person
                mask = Image.new("L", image.size, 0)
                mask_draw = Image.new("L", image.size, 0)
                mask_draw.paste(255, (x1, y1, x2, y2))  # White where the human is
                
                return cropped_person, mask_draw  # Return person image + mask
                
    return None, None  # If no person detected

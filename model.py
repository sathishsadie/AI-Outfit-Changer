from ultralytics import YOLO
from PIL import Image

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

def detect_human(image_path):
    image = Image.open(image_path).convert("RGB")
    results = model(image_path)  
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()  
        class_ids = result.boxes.cls.cpu().numpy()  
        
        for box, class_id in zip(boxes, class_ids):
            if int(class_id) == 0:  # Class ID 0 is "person"
                x1, y1, x2, y2 = map(int, box)  
                cropped_person = image.crop((x1, y1, x2, y2))  
                
                mask = Image.new("L", image.size, 0)
                mask_draw = Image.new("L", image.size, 0)
                mask_draw.paste(255, (x1, y1, x2, y2))  

                return cropped_person, mask_draw  
                
    return None, None  

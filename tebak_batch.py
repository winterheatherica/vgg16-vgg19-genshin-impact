import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

model = load_model('vgg16_best.h5')

dataset_dir = 'dataset'
character_names = sorted(os.listdir(dataset_dir))

test_dir = 'test'

test_images = [f for f in os.listdir(test_dir) if f.endswith('.jpg') or f.endswith('.png')]

for img_file in test_images:
    img_path = os.path.join(test_dir, img_file)
    
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    predictions = model.predict(img_array)

    predicted_class = np.argmax(predictions)

    predicted_character = character_names[predicted_class]

    print(f"Image: {img_file} - Predicted character: {predicted_character}")
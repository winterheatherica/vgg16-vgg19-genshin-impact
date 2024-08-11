from PIL import Image
import os 
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

model = load_model('best_model2b.h5')

img_path = 'lumine.jpg'
img = image.load_img(img_path, target_size=(224, 224))  

img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = img_array / 255.0

predictions = model.predict(img_array)

predicted_class = np.argmax(predictions)

dataset_dir = 'dataset'
character_names = sorted(os.listdir(dataset_dir))

predicted_character = character_names[predicted_class]

print(f"The predicted character is: {predicted_character}")
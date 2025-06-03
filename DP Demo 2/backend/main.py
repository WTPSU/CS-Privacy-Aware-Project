from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import io
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def laplace_dp_method(value, sensitivity, epsilon):
    noisy_value = value + np.random.laplace(loc=0, scale=sensitivity/epsilon)
    return noisy_value

def gaussian_noise(epsilon, sensitivity):
    delta = 1e-5
    sigma = (sensitivity * np.sqrt(2 * np.log(1.25 / delta))) / epsilon
    return np.random.normal(0, sigma)

def exponential_mechanism(value, epsilon, sensitivity):
    get_near_values = []
    scores = []
    choose_values = []
    for i in range(int(value) - 15, int(value) + 15):
        get_near_values.append(i)

    for num in get_near_values:
        score = -abs(num - value)
        scores.append(score)

    for score in scores:
        choose_value= np.exp((epsilon * score) / (2 * sensitivity))
        choose_values.append(choose_value)

    total_value = sum(choose_values)
    probabilities = []
    for value in choose_values:
        chance = value / total_value
        probabilities.append(chance)

    selected_index = np.random.choice(len(get_near_values), p=probabilities)
    return float(get_near_values[selected_index])

def add_noise_to_image(img_array):
    noise = np.random.laplace(loc=0, scale=0.2, size=img_array.shape)
    noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    return noisy_img


@app.post("/upload")
async def upload_image(file: UploadFile, epsilon: float = 1.0, sensitivity: float = 100.0):
    content = await file.read()

    image_file = io.BytesIO(content)
    image = Image.open(image_file)
    image = image.convert("RGB")

    image_array = np.array(image)
    height = image_array.shape[0]
    width = image_array.shape[1]
    channels = image_array.shape[2]

    noisy_array = np.zeros((height, width, channels), dtype=np.uint8)

    for x in range(height):
        for y in range(width):
            for z in range(channels):
                original_value = image_array[x][y][z]
                noisy_value = original_value + np.random.laplace(0, sensitivity / epsilon)
                noisy_array[x][y][z] = noisy_value

    noisy_image = Image.fromarray(noisy_array)
    out = io.BytesIO()
    noisy_image.save(out, format="PNG")
    bytes = out.getvalue()
    image_string = base64.b64encode(bytes).decode("utf-8")

    return {"image_base64": image_string}




@app.get("/noise")
def add_noise(value: float, method: str, epsilon: float, sensitivity: float):
    if method == "laplace":
        after = laplace_dp_method(value, sensitivity, epsilon)
    elif method == "gaussian":
        after = value + gaussian_noise(epsilon, sensitivity)
    return {
        "original": value,
        "after": after,
        "noise": after - value
    }

@app.get("/point")
def add_point(value: float, method: str, epsilon: float, sensitivity: float, point: float):
    if method == "laplace":
        after = laplace_dp_method(value, sensitivity, epsilon)
    elif method == "gaussian":
        after = value + gaussian_noise(epsilon, sensitivity)
    elif method == "exponential":
        after = exponential_mechanism(value, epsilon, sensitivity)
    return {
        "original": value,
        "after": after,
        "noise": after - value
    }

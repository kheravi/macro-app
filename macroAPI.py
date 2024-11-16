from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

class MealRequest(BaseModel):
    food_item: str

@app.post("/macronutrients")
async def get_macronutrients(meal: MealRequest):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Estimate the macronutrients (protein, carbohydrates, and fat) in grams for a typical serving of {meal.food_item}. "
                "Provide the answer only in the following format: 'Protein: Xg Carbs: Yg Fat: Zg', where X, Y, and Z are the respective values in grams."
            }
        ],
        model="llama3-8b-8192",
    )
    return {
        "macronutrients": chat_completion.choices[0].message.content
    }
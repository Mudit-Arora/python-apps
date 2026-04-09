import os 
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

model = init_chat_model(model="gemini-3-flash-preview",
        api_key=os.getenv("GOOGLE_API_KEY"), 
        model_provider="google-genai",
        )


repsone = model.invoke("Hello, how are you?")
print(repsone)
from google import genai
from openai import api_key

genai.api_key = api_key


client = genai.Client(api_key="AIzaSyBXRrFAgUifzyxivqATJ5MxQlZWqqZ9HT0")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents = "expalin list in few words"
)
print(response.text)
'''AI learns from data to recognize patterns and make predictions or decisions.'''
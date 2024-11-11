import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from brickllm.utils import ttl_to_building_prompt

# Load environment variables
load_dotenv()

# Create a custom model
custom_model = ChatOpenAI(temperature=0.8, model="gpt-4o")

current_dir = os.path.dirname(os.path.abspath(__file__))
file_name = "my_building.ttl"

# Open the ttl file
with open(os.path.join(current_dir, file_name), "r") as file:
    ttl_file = file.read()

# Generate the building description from the ttl file
building_description, key_elements = ttl_to_building_prompt(
    ttl_file,
    custom_model,
    additional_instructions="Keep a professional and structured tone.",
)

print("Generated building description:")
print(building_description)
print("--------------------------------")
print("Generated key elements:")
print(key_elements)

import vertexai
from vertexai.language_models import TextGenerationModel


def interview(prompt: str) -> str:
    """Ideation example with a Large Language Model"""

    vertexai.init(project="gifted-freehold-403415", location="us-central1")
    parameters = {
        "temperature": 0.3,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.8,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        prompt,
        **parameters,
    )
    print(f"{response.text}")

    return response.text


if __name__ == "__main__":
    with open('scraped_data.txt') as f:
        prompt = f.read()
    prompt += f'''\nGiven the above information, rank the suitability of the candidate in a job in Tech, Sales, 
Management and Finance. Give an ordered ranking like 1. Finance, 2. Tech, etc; where 1 is most suitable, 
and 4 is least suitable.'''
    interview(prompt)

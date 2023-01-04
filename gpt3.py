
import openai
model_engine = "text-davinci-003"
max_tokens = 128


def generate_response(prompt):

    # Generate a response
    try:
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # Print the response
        print(completion.choices[0].text)
        return completion.choices[0].text
    except KeyboardInterrupt:
        return ""

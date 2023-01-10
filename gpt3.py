
import openai
import openai.error
model_engine = "text-davinci-003"
max_tokens = 128


def generate_response(prompt, max_tokens=1024):

    print("Prompt: ", prompt)

    # Generate a response
    while True:
        try:
            completion = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return completion.choices[0].text
        except KeyboardInterrupt:
            return ""
        except openai.error.ServiceUnavailableError:
            continue

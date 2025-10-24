from openai import OpenAI


def llm_response(r):
    client = OpenAI(
      base_url="https://api.polza.ai/api/v1",
      api_key='ak_G2J42hoX4H39GpR6ag18rLrwBhtWj9zQk0gnGN1AZ5Q'
    )

    completion = client.chat.completions.create(
      model='deepseek/deepseek-r1',
      messages=[
        {
          "role": "user",
          "content": f"Ответь на этот вопрос так, как буд-то ты крутой голосовой ассистент, при этом отвечай максимально коротко на сколько это возможно. Вот мой запрос ('{r}')"
        }
      ]
    )
    return str(completion.choices[0].message.content)
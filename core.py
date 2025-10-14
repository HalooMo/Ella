from openai import OpenAI

client = OpenAI(
  base_url="https://api.polza.ai/api/v1",
  api_key='ak_G2J42hoX4H39GpR6ag18rLrwBhtWj9zQk0gnGN1AZ5Q'
)

completion = client.chat.completions.create(
  model='deepseek/deepseek-r1',
  messages=[
    {
      "role": "user",
      "content": "Что думаешь об этой жизни?"
    }
  ]
)

print(completion.choices[0].message.content)
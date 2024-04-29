from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

completion = client.chat.completions.create(
  model="google/gemma-7b",
  messages=[{"role":"user","content":"what do you think about the name Harshavardan?"}],
  temperature=0.5,
  top_p=1,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")
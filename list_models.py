import google.generativeai as genai

genai.configure(api_key="")

models = genai.list_models()
for model_info in models:
    print(model_info.name)

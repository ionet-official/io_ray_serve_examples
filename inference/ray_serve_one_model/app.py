from starlette.requests import Request

import ray  # noqa: F401
from ray import serve

from transformers import pipeline

@serve.deployment(num_replicas=2, ray_actor_options={"num_gpus": 2}, max_replicas_per_node=1) 
class Tgenerator:
    def __init__(self):
        # Load model
        self.model = pipeline("text-generation", model="gpt2")

    def inference(self, text_data: str) -> str:
        # Run inference
        model_output = self.model(text_data)

        result = model_output[0]["generated_text"]
        print(f"{result}")
        return result

    async def __call__(self, http_request: Request) -> str:
        text_data: str = await http_request.json()
        return self.inference(text_data)

app = Tgenerator.bind()
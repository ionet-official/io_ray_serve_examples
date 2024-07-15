from starlette.requests import Request
import ray
from ray import serve
from ray.serve.handle import DeploymentHandle
from transformers import pipeline

@serve.deployment(num_replicas=1, ray_actor_options={"num_gpus": 0.5}, max_replicas_per_node=2) 
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

@serve.deployment(num_replicas=1, ray_actor_options={"num_gpus": 0.5}, max_replicas_per_node=2) 
class Qgenerator:
    """
    This class is responsible for generating a question from a fetched text from request data.
    Tnan send it to the Tgenerator model which will generate a final response.
    """
    def __init__(self, tgenerator: DeploymentHandle):
        self.tgenerator = tgenerator
        # Load model
        self.model = pipeline("text2text-generation", model="t5-base")

    def generate_text(self, text: str) -> str:
        # Run inference
        model_output = self.model(text, min_length=5)
        print(f"RAW output from Qgenerator : {model_output}")
        # Post-process output 
        generated_text = model_output[0]["generated_text"]
        print(f"Generated text from Qgenerator : {generated_text}")
        return generated_text

    async def __call__(self, http_request: Request) -> str:
        text_data: str = await http_request.json()
        generated_text = self.generate_text(text_data)
        result = await self.tgenerator.inference.remote(generated_text)
        print(f"Generated text from Tgenerator : {result}")
        return result

app = Qgenerator.bind(Tgenerator.bind())
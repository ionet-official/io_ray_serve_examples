
from io import BytesIO
from fastapi import FastAPI
from fastapi.responses import Response
import torch

from ray import serve
from ray.serve.handle import DeploymentHandle


app = FastAPI()


@serve.deployment(num_replicas=1)
@serve.ingress(app)
class APIIngress:
    def __init__(self, diffusion_model_handle: DeploymentHandle) -> None:
        self.handle = diffusion_model_handle

    @app.get(
        "/imagine",
        responses={200: {"content": {"image/png": {}}}},
        response_class=Response,
    )
    async def generate(self, prompt: str, img_size: int = 512):
        assert len(prompt), "prompt parameter cannot be empty"

        image = await self.handle.generate.remote(prompt, img_size=img_size)
        file_stream = BytesIO()
        image.save(file_stream, "PNG")
        return Response(content=file_stream.getvalue(), media_type="image/png")


@serve.deployment(
    ray_actor_options={"num_gpus": 1},
    autoscaling_config={"min_replicas": 2, "max_replicas": 3},
)
class StableDiffusionV2:
    def __init__(self):
        from diffusers import EulerDiscreteScheduler, DiffusionPipeline, StableDiffusionPipeline, StableDiffusion3Pipeline

        model_id = "SG161222/RealVisXL_V4.0" 

        scheduler = EulerDiscreteScheduler.from_pretrained(
            model_id, subfolder="scheduler"
        )
        self.pipe = DiffusionPipeline.from_pretrained(
            model_id, scheduler=scheduler, variant="fp16", torch_dtype=torch.float16, use_safetensors=True
        )
        self.pipe = self.pipe.to("cuda")

    def generate(self, prompt: str, img_size: int = 512):
        assert len(prompt), "prompt parameter cannot be empty"

        with torch.autocast("cuda"):
            image = self.pipe(prompt, height=img_size, width=img_size).images[0]
            return image


app = APIIngress.bind(StableDiffusionV2.bind())

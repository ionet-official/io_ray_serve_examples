# io_ray_serve_examples

- go to page 
    * https://cloud.io.net/cloud/clusters/create-cluster
    - choose type `Inference`, supplier `io.net`, gpu nvidia 3060 x 4 and deploy.
    - when cluster created, open it, copy `IDE Password`

- go to Visual Studio, create dir and clone repo
    * `git clone https://github.com/ionet-official/io_ray_serve_examples.git`

- go to path `inference/`

- make enviroment for project on host
    * `pip install -r requirements.txt`

- install enviroment on remote node's
    * `python install_packages.py requirements.txt`

- to run project go to one of examples path and use command
    * `serve run app:app`

- test inference transformers
    * go to path `client_test`, run command `python remote_test.py` 
- test inference diffusers
    
    * open link [https://vscode-{cl_id}.tunnels.io.systems/proxy/8000/imagine?prompt={your_text}](https://vscode-{cl_id}.tunnels.io.systems/proxy/8000/imagine?prompt={your_text})

    - get result ![alt text](<2024-07-15 at 19.00.04.png>)
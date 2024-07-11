- make enviroment for project
    * python3 -m venv venv
    * source venv/bin/activate
    * pip install -r requirements.txt
- or you can use 
    * conda create --name tests python=3.9.18
    * conda activate tests
    * pip install -r requirements.txt

- check in ray cluster dashboard `https://ray-{value_id}.tunnels.io.systems/#/cluster`, how much nodes in cluster and how much GPU's in each of them. This helpfull to pass right settings `@serve.deployment`.

- run project
    * serve run app:app

Currently we can not change enviroment on host machine where `ray` have version `2.9.3` and run in global conda enviroment with preinstalled packages.

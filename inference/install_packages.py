import ray
import sys
import os

@ray.remote
def install_package(packages):
    import os
    cmd = f"pip3 install {' '.join(packages)}"
    os.system(cmd)
    return f"Installed {' '.join(packages)}"

def create_install_task_with_node_affinity(node_id, packages):
    scheduling_strategy = ray.util.scheduling_strategies.NodeAffinitySchedulingStrategy(
        node_id=node_id, soft=True
    )
    return install_package.options(scheduling_strategy=scheduling_strategy).remote(packages)

ray.init()

known_nodes = set()  # Set to keep track of nodes we've seen
dead_nodes = set()   # Set to keep track of nodes that have left or are unreachable

def run_task_on_all_nodes(packages):
    global known_nodes
    global dead_nodes

    current_nodes = set(node['NodeID'] for node in ray.nodes() if node['alive'] == True)
    new_nodes = current_nodes - known_nodes
    nodes_left = known_nodes - current_nodes

    # Update known nodes
    known_nodes = current_nodes

    # Update dead nodes and then clear them
    dead_nodes.update(nodes_left)
    
    # Only send tasks to nodes that are alive and not in the dead_nodes set
    nodes_to_send_to = new_nodes - dead_nodes
    print(nodes_to_send_to)
    if nodes_to_send_to:
        
    # Install the package on the new nodes
        install_results = ray.get([
            create_install_task_with_node_affinity(node_id, packages) for node_id in nodes_to_send_to
        ])

        print(f"Installation status on newly detected nodes: {install_results}")
    
    
    # Reset dead nodes set
    dead_nodes.clear()

def read_requirements(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]


if __name__ == "__main__":
    # Exclude the script name itself from the arguments
    args = sys.argv[1:]

    packages_to_install = []

    for arg in args:
        if os.path.isfile(arg) and arg.endswith(".txt"):
            packages_to_install.extend(read_requirements(arg))
        else:
            packages_to_install.append(arg)

    run_task_on_all_nodes(packages_to_install)

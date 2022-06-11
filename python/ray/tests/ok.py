from ray.cluster_utils import AutoscalingCluster

import ray

cluster = AutoscalingCluster(
    head_resources={"CPU": 2},
    worker_node_types={
        "cpu_node": {
            "resources": {
                "CPU": 4,
                "object_store_memory": 1024 * 1024 * 1024,
            },
            "node_config": {},
            "min_workers": 0,
            "max_workers": 2,
        },
        "gpu_node": {
            "resources": {
                "CPU": 2,
                "GPU": 1,
                "object_store_memory": 1024 * 1024 * 1024,
            },
            "node_config": {},
            "min_workers": 0,
            "max_workers": 2,
        },
    },
)

try:
    cluster.start()
    ray.init("auto")

    # Triggers the addition of a GPU node.
    @ray.remote(num_gpus=1)
    def f():
        print("gpu ok")

    # Triggers the addition of a CPU node.
    @ray.remote(num_cpus=3)
    def g():
        print("cpu ok")

    ray.get(f.remote())
    ray.get(g.remote())
    ray.shutdown()
finally:
    cluster.shutdown()
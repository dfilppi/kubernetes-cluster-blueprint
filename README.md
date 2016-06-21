## Kubernetes-Cluster-Blueprint

This repository contains the required components to deploy a Kubernetes cluster with a Cloudify Manager.

Limitations (as of 22/6/2016):
+ Kubernetes Master & Nodes will only run on Ubuntu 14.04
+ Tested on Openstack Kilo (More coming soon!)
+ Tested on Cloudify 3.3.1

### Installation Instructions

1. Create an inputs.yaml file with the following key-value pairs:
1.1 image_id: the image id in your IaaS for a Ubuntu 14.04 image.
1.2 flavor_id: the flavor id in your IaaS for a machine with around 1024 GB RAM 1 CPU 20 GB Disk.
1.3 Any other inputs accepted by the blueprint
1. Upload the blueprint to your Cloudify Manager: `cfy blueprints upload -p openstack-blueprint.yaml -b kc`
2. Create a deployment: `cfy deployments create -b kc -d kc -i inputs.yaml`
3. Run the install workflow: `cfy executions start -w install -d kc`

### Scaling and Healing

This blueprint defines monitoring based on the amount of CPU used by the hyperkube process on the nodes.

Scaling up is initiated when CPU Percent used by hyperkube on a single node is above 3% for more than 10 consecutive seconds. This scale policy will not exceed 6 instances.

Scaling down is initiated when CPU Percent used by hyperkube on a single node is below 1% for more than 200 consecutive seconds. This scale policy will not go below 2 instances.

Healing is initiated on a VM when no CPU metrics are being received by the manager.


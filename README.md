# Grist AV

A proxy for Grist handling antivirus scans using [Je clique ou pas ?](https://jecliqueoupas.cyber.gouv.fr/accueil). Meant to be used on Kubernetes with nginx-ingress.

## Testing integration locally

Set up a minikube node with KVM and mount the project directory on the node.

```bash
minikube start --cni calico --mount=true --mount-string=$(pwd):/grav --addons=ingress,metrics-server
```

Prepare Grist's dependencies (S3, PostgreSQL, Redis) and deploy Grist's Helm chart. This can all be done using [the Terraform example in the chart's repository](https://github.com/numerique-gouv/helm-charts/tree/main/charts/grist/examples/terraform).

Create the grav deployment,service and ingress with the deployment mounting the project directory from the node. An example implementation can be found under `integration/grav.tf`.

Run `start.sh` to install dependencies and run the current working directory's code in minikube.

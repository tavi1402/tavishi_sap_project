# This architecture provides a robust and flexible deployment framework for  Flask application, leveraging Kubernetes for orchestration, and Istio for advanced traffic management. It allows you to perform canary, blue-green, and shadow deployments, ensuring high availability and resilience of application in production.

## The files under inference/k8s/ define the various deployment strategies (stable, canary, blue-green, shadow) and the supporting configurations (service, HPA, PDB, Istio configurations) for your inference-related components.
## The files under k8s/environments/ define the specific configurations for different environments (development, staging, production).

## When we  deploy to a specific environment, we applies both the inference-related configurations and the environment-specific configurations

Files and Their Purposes:






# Deployments
Significance:

Version Management: Manage multiple versions of the application (stable, canary, blue, green, shadow).
Rolling Updates: Ensures zero downtime during updates.

# Stable Deployment 
stable-deployment.yml: Deploys the stable version of your Flask application.

# Canary Deployment
canary-deployment.yml: Deploys the canary version of your Flask application.

# Blue Green Deplyment 
blue-deployment.yml: Deploys the blue environment version of your Flask application.

green-deployment.yml: Deploys the green environment version of your Flask application.

# Shadow deployment
shadow-deployment.yml: Deploys the shadow version of your Flask application for testing with production traffic.

# service.yml: Services

Significance:

Exposing Applications: Services expose Flask applications internally within the cluster or externally to the internet.
Load Balancing: Distributes traffic across multiple pods.

# hpa.yml:  Horizontal Pod Autoscaler (HPA)

Significance:

Auto-Scaling: Automatically scales the number of pods based on CPU and memory usage.
Resource Efficiency: Ensures efficient use of resources by scaling up/down based on demand.


# pdb.yml:  Pod Disruption Budget (PDB) 

Significance:

High Availability: Ensures a minimum number of pods remain available during maintenance or updates.
Resilience: Improves application resilience during disruptions.

#  virtual-service.yml : Istio for Traffic Management
Significance:

Advanced Traffic Control: Istio allows advanced traffic management, including routing, mirroring, and subset definitions.
Canary and Shadow Deployments: Enables canary deployments and shadow traffic mirroring for testing.


destination-rule.yml: Applies policies to traffic after routing, such as load balancing and version-specific rules.

#  Environment Manifests: 
significanec

These files (manifest.yml in dev, staging, prod) can reference the necessary deployment and service configurations to be applied in that specific environment.


# Handling Rollbacks 

kubectl rollout undo deployment/flask-inference-server-stable

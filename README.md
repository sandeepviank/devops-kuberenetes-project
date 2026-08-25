# DevOps Kubernetes Project

An end-to-end DevOps learning project using GitHub, GitHub Actions, Python/Flask, Pytest, Ruff, Docker, Trivy, and local Kubernetes through Docker Desktop.

## Architecture

```text
Developer
    |
    v
GitHub Issue
    |
    v
Feature Branch
    |
    v
Pull Request
    |
    v
GitHub Actions
    |
    +--> Tests
    +--> Lint
    +--> Docker Build
    +--> Trivy Scan
    |
    v
Merge
    |
    v
Docker Image
    |
    v
Local Kubernetes
    |
    +--> Pod 1
    +--> Pod 2
    |
    v
Service
    |
    v
Application
```

## Tech Stack

- Git / GitHub
- GitHub Issues and Projects
- Python 3 + Flask
- Pytest
- Ruff
- GitHub Actions
- Docker
- Trivy
- Kubernetes
- Docker Desktop Kubernetes
- kubectl

## Repository Structure

```text
devops-kubernetes-project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── secret.yaml
├── src/
│   ├── __init__.py
│   └── app.py
├── tests/
│   └── test_app.py
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

## Application Endpoints

```text
GET /
GET /health
GET /api/users
```

`/health` returns:

```text
Application is healthy
```

## Prerequisites

Verify tools:

```bash
git --version
python3 --version
docker --version
kubectl version --client
```

Verify Docker Desktop:

```bash
docker ps
docker run --rm hello-world
```

## GitHub Work Tracking

Issues used:

```text
#1  Create application
#2  Add unit tests
#3  Add linting
#4  Create Dockerfile
#5  Create GitHub Actions CI
#6  Add Trivy security scanning
#7  Create Kubernetes deployment
#8  Create Kubernetes service
#9  Add two replicas and health probes
#10 Test pod self-healing
#11 Test rolling update
#12 Test rollback
#13 Complete README documentation
```

Project statuses:

```text
Backlog -> In Progress -> Review -> Done
```

## Git Workflow

Example:

```bash
git checkout main
git pull origin main
git checkout -b feature/application
```

After changes:

```bash
git add .
git commit -m "feat: create Flask application"
git push -u origin feature/application
```

Create a PR from the feature branch to `main` and include:

```text
Closes #1
```

The same workflow was used for tests, lint, Docker, CI, security, and Kubernetes.

## Python Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Run Application Locally

```bash
python3 src/app.py
```

Verify:

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/api/users
```

## Unit Tests

Run:

```bash
python3 -m pytest -v
```

Expected:

```text
tests/test_app.py::test_home PASSED
tests/test_app.py::test_health PASSED
tests/test_app.py::test_users PASSED
3 passed
```

## Linting

Run:

```bash
ruff check .
```

Expected:

```text
All checks passed!
```

Tests verify application behavior. Linting performs static code-quality checks.

## Docker

Build:

```bash
docker build -t devops-app:v1 .
```

Verify:

```bash
docker images
```

Run:

```bash
docker run --rm -p 8080:8080 devops-app:v1
```

Test:

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/api/users
```

Docker flow:

```text
Source Code -> Dockerfile -> Docker Image -> Container -> Application
```

## GitHub Actions CI

Workflow file:

```text
.github/workflows/ci.yml
```

CI flow:

```text
Pull Request
   |
   v
Checkout
   |
   v
Set up Python
   |
   v
Install dependencies
   |
   v
Run Pytest
   |
   v
Run Ruff
   |
   v
Build Docker image
   |
   v
Trivy scan
```

A failing test, lint check, Docker build, or security scan causes the workflow to fail.

## Trivy Security Scan

Trivy scans the image for known vulnerabilities in OS packages and application dependencies. The project uses the scan as a CI security gate for configured HIGH/CRITICAL findings.

## Local Kubernetes

The final local cluster uses Docker Desktop Kubernetes.

Enable it in:

```text
Docker Desktop -> Settings -> Kubernetes -> Enable Kubernetes -> kubeadm
```

Verify context:

```bash
kubectl config get-contexts
kubectl config use-context docker-desktop
```

Verify node:

```bash
kubectl get nodes
```

Expected:

```text
docker-desktop   Ready
```

## Kubernetes Files

### ConfigMap

Used for non-sensitive configuration.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: devops-app-config
data:
  APP_ENV: "local"
  APP_VERSION: "v1"
```

### Secret

Demo only:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: devops-app-secret
type: Opaque
stringData:
  DEMO_SECRET: "local-demo-secret"
```

Do not commit real production credentials to Git.

### Deployment

The Deployment uses:

```yaml
replicas: 2
```

Conceptually:

```text
Deployment
   |
   +--> Pod 1
   +--> Pod 2
```

### Readiness Probe

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 3
  periodSeconds: 5
```

Readiness answers: "Can this Pod receive traffic?"

### Liveness Probe

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 10
```

Liveness answers: "Is the application alive, or should Kubernetes restart it?"

### Service

The Service exposes port 80 and routes to container port 8080.

```text
Service :80
   |
   +--> Pod 1 :8080
   +--> Pod 2 :8080
```

## Deploy to Kubernetes

Build the image:

```bash
docker build -t devops-app:v1 .
```

Apply manifests:

```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Verify:

```bash
kubectl get deployments
kubectl get pods
kubectl get svc
```

Expected:

```text
devops-app   2/2
```

and two Pods in:

```text
1/1 Running
```

## Access the Application

```bash
kubectl port-forward service/devops-app-service 8080:80
```

If port 8080 is already in use:

```bash
kubectl port-forward service/devops-app-service 8081:80
```

Then:

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/api/users
```

## Self-Healing Test

List Pods:

```bash
kubectl get pods
```

Delete one:

```bash
kubectl delete pod <pod-name>
```

Watch:

```bash
kubectl get pods -w
```

Kubernetes creates a replacement because the Deployment desired state is two replicas.

```text
Desired = 2
Actual = 1
   |
   v
Deployment controller reconciles
   |
   v
New Pod created
   |
   v
Actual = 2
```

## Rolling Update

Change the app to Version 2, then build:

```bash
docker build -t devops-app:v2 .
```

Update Deployment:

```bash
kubectl set image deployment/devops-app devops-app=devops-app:v2
```

Verify:

```bash
kubectl rollout status deployment/devops-app
kubectl get pods
kubectl rollout history deployment/devops-app
```

Expected rollout message:

```text
deployment "devops-app" successfully rolled out
```

Typical history:

```text
REVISION
1
2
```

Verify Version 2:

```bash
kubectl port-forward service/devops-app-service 8081:80
curl http://localhost:8081/
```

## Broken Deployment Test

Intentionally deploy a nonexistent image:

```bash
kubectl set image deployment/devops-app devops-app=devops-app:broken
```

Check:

```bash
kubectl get pods
```

Expected:

```text
ErrImagePull
```

or:

```text
ImagePullBackOff
```

Check history:

```bash
kubectl rollout history deployment/devops-app
```

## Rollback

Rollback to the previous working revision:

```bash
kubectl rollout undo deployment/devops-app
kubectl rollout status deployment/devops-app
kubectl get pods
```

Expected: two healthy `1/1 Running` Pods.

## Useful Kubernetes Commands

```bash
kubectl get nodes
kubectl get deployments
kubectl get pods
kubectl get pods -w
kubectl get svc
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl rollout history deployment/devops-app
kubectl rollout status deployment/devops-app
kubectl rollout undo deployment/devops-app
kubectl delete pod <pod-name>
kubectl port-forward service/devops-app-service 8080:80
```

## CI vs CD in This Project

This project implements automated CI:

```text
PR -> Test -> Lint -> Docker Build -> Trivy Scan
```

Deployment to local Kubernetes is manual using `kubectl`.

So the current model is:

```text
Automated CI + Manual Local Deployment
```

## Key Concepts

1. **Why branches?**  
   They isolate work from stable `main`.

2. **Purpose of a Pull Request?**  
   Review, discussion, CI validation, approval, and controlled merge.

3. **What does GitHub Actions do?**  
   Runs automated workflows based on repository events.

4. **Test vs lint?**  
   Tests verify behavior; linting performs static code-quality checks.

5. **Docker image vs container?**  
   An image is a packaged template; a container is a running instance.

6. **Why scan Docker images?**  
   OS packages and dependencies may contain known vulnerabilities.

7. **What is a Pod?**  
   Kubernetes' smallest deployable unit.

8. **Why use a Deployment?**  
   Replica management, self-healing, rolling updates, history, rollback, desired state.

9. **Why a Service?**  
   It provides a stable endpoint despite changing Pod IPs.

10. **Why two replicas?**  
    Availability and desired-state reconciliation.

11. **Readiness vs liveness?**  
    Readiness controls traffic eligibility; liveness controls restart decisions.

12. **What happens when a Pod crashes?**  
    Kubernetes creates a replacement to restore the desired replica count.

13. **What is a rolling update?**  
    Gradual replacement of old Pods with new Pods.

14. **How do you rollback?**

```bash
kubectl rollout history deployment/devops-app
kubectl rollout undo deployment/devops-app
kubectl rollout status deployment/devops-app
```

15. **How does GitHub fit into DevOps?**  
    GitHub provides source control, issues, project tracking, branches, PRs, collaboration, and CI automation.

## Verification Checklist

```text
GitHub repository created                 ✅
GitHub Issues created                     ✅
GitHub Project workflow created           ✅
Feature branch workflow                   ✅
Pull Requests                             ✅
Python Flask application                  ✅
GET /                                     ✅
GET /health                               ✅
GET /api/users                            ✅
Pytest unit tests                         ✅
Ruff linting                              ✅
Docker image build                        ✅
Docker container execution                ✅
GitHub Actions CI                         ✅
Trivy vulnerability scanning              ✅
Local Kubernetes cluster                  ✅
Kubernetes Deployment                     ✅
2 application replicas                    ✅
Kubernetes Service                        ✅
ConfigMap                                 ✅
Secret                                    ✅
Readiness probe                           ✅
Liveness probe                            ✅
Service connectivity                      ✅
Pod self-healing                          ✅
Rolling update V1 -> V2                    ✅
Deployment revision history               ✅
Intentional broken deployment             ✅
Rollback to working version               ✅
```

## Cleanup

```bash
kubectl delete -f k8s/service.yaml
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/secret.yaml
kubectl delete -f k8s/configmap.yaml
```

```bash
docker image rm devops-app:v1
docker image rm devops-app:v2
```


# k8-personal

# Deploying application to crazedencoder.com

## Step 1: Create a new application using  docker.
> You can take the sample-app directory as a template


1. cd to sample-app directory ``cd sample-app``
2. Build the docker container ``sudo docker build  -t sample-app:v1 .``
3. Test your application by running the following command ``sudo docker run sample-app:v1``

You should be able to navigate to http://127.0.0.1:5000 and see "Hello World"

## Step 2: Push the docker image to crazedencoder.com registry 
> To run your application on crazedencoder.com server , it is necessary to push the docker image to the registry.

Run the following command 
```bash 
# First you should run the following command to list your docker images
sudo docker images ls 
""" Out put will looks like this

REPOSITORY           TAG               IMAGE ID       CREATED          SIZE
-------------------------------------------------------------------------------
sample-app           v1                a420beb4e8a4   11 minutes ago   53.8MB
filter-service       latest            8dad80a263d7   3 weeks ago      16MB

"""
# Here we re using your-mobile-number as a unique identifier. 
sudo docker image tag sample-app:v1  registry.crazedencoder.com/<your-mobile-number>/sample-app:v1
# Run the sudo docker images ls  to make sure you have the image tagged, Example 
"""
REPOSITORY                                        TAG        IMAGE ID       CREATED          SIZE
sample-app                                         v1        a420beb4e8a4   19 minutes ago   53.8MB
registry.crazedencoder.com/8277127070/sample-app   v1        a420beb4e8a4   19 minutes ago   53.8MB
filter-service                                     latest    8dad80a263d7   3 weeks ago      16MB
"""
# Push the image to registry.crazedencoder.com
sudo docker image push --all-tags registry.crazedencoder.com/8277127070/sample-app
```
## Step 3: Create a kube deployment files

This file will create a stateless controller manifest 

```yaml 
# replace the <mobilenumber> with your mobile number

apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: flaskapp-<mobilenumber>-release
  namespace: personal-rnd
spec:
  releaseName: flaskapp-<mobilenumber>
  targetNamespace: personal-rnd
  interval: 24h
  chart:
    spec:
      chart: base-deployment
      version: 1.0.0
      sourceRef:
        kind: HelmRepository
        name: crazedencoder
        namespace: flux-system
      interval: 24h
  values:
    global:
      applicationName: flaskapp-<mobilenumber>
    replicaCount: 2
    image: registry.crazedencoder.com/<mobilenumber>/sample-app:v1
    containerDetails:
      pullPolicy: IfNotPresent
      ports:
        - containerPort: 5000
          name: pw-address
    service:
      type: ClusterIP
      port: 3XXX # NOTE: if this number is already used by someone , your application wont run. To avoid this, use your employee ID, For Example 3132
      targetPort: pw-address

```
Now lets create a sub domain under crazedencoder.com and get encript with Let's Encrypt 

```yaml

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
 name: letsencrypt-ingress-<mobilenumber>-flaskapp
 namespace: personal-rnd
 annotations:
  nginx.ingress.kubernetes.io/ssl-redirect: "true"
  nginx.ingress.kubernetes.io/secure-backends: "false"
  nginx.ingress.kubernetes.io/enable-access-log: "false"
  cert-manager.io/cluster-issuer: letsencrypt-issuer
  nginx.ingress.kubernetes.io/backend-protocol: "HTTP"
  kubernetes.io/ingress.class: nginx
spec:
 tls:
 - hosts:
   - <mobilenumber>.crazedencoder.com
   secretName: letsencrypt-issuer
 rules:
 - host: <mobilenumber>.crazedencoder.com
   http:
     paths:
     - pathType: Prefix
       path: /
       backend:
         service:
           name: service-flaskapp-<mobilenumber>
           port:
             number: 3XXX # NOTE: if this number is already used by someone , your application wont run. To avoid this, use your employee ID, For Example 3132

```
We are ready to test your application !!
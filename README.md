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
# Pus the image to registry.crazedencoder.com
sudo docker image push --all-tags registry.crazedencoder.com/8277127070/sample-app
```
## Step 3: Create a kube deployment files


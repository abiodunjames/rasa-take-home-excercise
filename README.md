


## Virtual Assistance


### Key Requirements

*   A way to ensure that messages are not responded to out-of-order.
*   A datastore to store conversation history.
*   An authorization layer that ensures only admin users can view conversation history.
*   The architecture should be able to handle thousands of users at once and be scalable if needed.


### Assumptions

To be able to narrow down the scope of my solution, I made a couple of assumptions.

*   Authorization is basic. No roles, groups, policies or fine-grained access control
*   The application is write-heavy since all conversations are persisted.
*   There is no need for integration tests or end-to-end tests
*   ACID compliance is not necessary at least for conversation history
*   Logging and auditing is out of scope


### Decisions

Here are the technical decisions I made and why I made them.

* Decouple **API Service**, **Action Service **and **Inferencing Service** so that each service can be scaled independently

* The **Inference Service** and **Action Service** will not be exposed to the external network.

* For a write-heavy application, It makes sense to use a datastore with high throughput. I chose Redis

* For scalability, the authorization process will be stateless – and token-based. To limit the scope of the task, It'll not be OpenID Connect compliance, and refreshing of tokens will not be possible.




## How it works (non-technical audience)

_In an audience of non-technical people, you would find different kinds of stakeholders. It's essential to know the profile of the stakeholders to adjust your language accordingly._

_Here, I assume that I have an audience of the non-technical support team and business managers._



In our recent report, 97% of new users on our platform find it challenging to locate instructions on how to create an account, shipping fee costs, and delivery time.

The new virtual assistance allows our users to find relevant information they're looking for on our website without having to contact our dedicated support team. They can interact with the virtual assistant through the existing chat icon on the website and get answers in seconds from a bot — but like a human.

The virtual assistant uses AI to engage with customers just like our support team, and it's able to do so continuously 7 days a week and 24 hours a day.

**How it works**

*   Visit our website
*   Click the messenger icon at the bottom-right
*   Engage with it as you would do with a friend
*   You'll get instant answers

**Advantages**

*   27/4 Availability. Anytime of the day including weekends
*   More time for the support team to spend on what matters
*   Fast response time
*   Can handle multiple customers at the same time

**Disadvantages**

*   Not all questions can be answered by the virtual assistant.




## How it works (technical)



![alt_text](docs/image1.png "image_tooltip")



### Key components

* **Inferencing service** :- Predict appropriate response to each message received

* **Action service**:- Contains python code for custom actions

* **API Service**:- Exposes a public API

*   **Authentication Service** :- Authenticates users and issues JWT tokens

*   **Redis** : Stores all conversations

*   **Postregres**:  Store users credentials and tokens

    **_Note: API Service and Authentication service are coupled together at the moment_**




## Usage

Clone the repository or download the code.

1. Setup environment variables

Create a `.env` file at the root folder. There is `.env.example` to guide you on what to configure.

```

SECRET_KEY=your-super-secure-secret

INFERENCE_ENDPOINT=http://inference_server:5005/webhooks/rest/webhook

POSTGRES_USER=user

POSTGRES_PASSWORD=password

POSTGRES_DB=d`
```



2. Start the container using docker-compose

```
docker-compose up -d
```



3. Setting up the database

To create database tables for users, we need to run a database migration command.

```
docker-compose exec api_server python manage.py create_db

```


Admin username: [admin@test.com](mailto:admin@test.com)

Admin Password : 123456



5. Viewing Swagger Documentation

To see swagger documentation, go to [https://127.0.0.1:5000](https://127.0.0.1:5000)



6. Testing the conversation webhook

 ```
 curl -X POST "http://127.0.0.1:5000/conversations/webhook" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"sender\": \"Samuel\", \"message\": \"How much is the shipping fee?\"}"

 ```



7. Logging in as admin

 ```
 curl -X POST "http://127.0.0.1:5000/auth/login" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"email\": \"admin@test.com\", \"password\": \"123456\"}"

 ```

8. Viewing conversation history

```

curl -X GET "http://127.0.0.1:5000/conversations/" -H "accept: application/json" -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTcxMzQ4ODUsImlhdCI6MTU5NzA0ODQ4MCwic3ViIjoxLCJzY29wZSI6dHJ1ZX0.TxxKQ5dP-irnklUl1SPkmD_Z-v6wEzCXgp12QlYOxoY"

```


9. Training the model

You may also want to train the model. Run the command to train the model

```
(cd inference && docker run  -v $(pwd):/app rasa/rasa:1.10.8-full train --domain domain.yml --data data --out models)
```



10. Running tests

```
docker-compose exec api_server python manage.py test
```



## Deployment and Scaling

_To talk about scaling an application, we first need to deploy or run it. Out of preference, I've chosen AWS as my preferred cloud provider for this guide._

### Deployment

Amazon Elastic Container Services (ECS) manages the deployment and orchestration of Docker containers. ECS groups docker containers into defined tasks, which are then grouped into services and deployed in clusters.

Below, I've summarised steps to run the application on AWS ECS.

*   Create an image repository and push **api_service**, **inference_service**, **action_service** to the repository
*   Setup an AWS ECS cluster
*   Create a task definition
*   Configure AWS ECS service
*   Configure the cluster
*   Create a[ Redis cluster](https://aws.amazon.com/getting-started/hands-on/setting-up-a-redis-cluster-with-amazon-elasticache/) for the tracker store
*   Create a[ Postgres RDS](https://aws.amazon.com/rds/postgresql/)


### Scaling

You can scale the service by configuring Auto Scaling, which adjusts the desired count of tasks in response to CloudWatch events. Below is a rough sketch of how it works on a higher level.



![alt_text](docs/image2.png "image_tooltip")


[Configure Target Tracking Scaling Policies](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-autoscaling-targettracking.html) that increase or decrease the number of tasks based on CPU utilization and other metrics. For example, If the ECS CPU utilization exceeds 85%, a scale-out event is triggered, which instructs the ECS Auto Scaling Service to launch additional ECS tasks.


### Scaling Redis

Since all conversations are stored in Redis stores, eventually, it would grow, and one needs to scale horizontally. One approach is to scale horizontally by adding more nodes to the cluster. See[ scale-up Redis clusters with replicas](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Scaling.RedisReplGrps.ScaleUp.html)

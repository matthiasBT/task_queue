# task_queue
Simple task queue written in Python

Start the service:  
```
git clone https://github.com/matthiasBT/task_queue.git
cd task_queue
docker-compose up
```

Create a new task:  
```curl -X POST http://localhost/tasks/```

Request the status of a task:  
```curl http://localhost/tasks/<task_id>/```

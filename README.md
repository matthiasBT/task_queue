# task_queue
Simple task queue written in Python

Start the service:  
```docker-compose up```

Create a new task:  
```curl -X POST http://localhost/tasks/```

Request the status of a task:  
```curl http://localhost/tasks/<task_id>/```

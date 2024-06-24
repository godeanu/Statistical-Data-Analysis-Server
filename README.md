# Statistical-Data-Analysis-Server

Multi-threaded Python server that handles client requests for statistical data analysis.

## Description

This project is a multi-threaded Python server that handles client requests for statistical data analysis.

The server is implemented using the Flask framework
The dataset is a CSV containing information on nutrition, physical activity, and obesity in the US from 2011-2022.

The server is able to handle multiple clients concurently using a thread pool. Upon startup, it loads the CSV file and extracts the information needed to calculate the required statistics per request. Since data processing can take significant time, the next things happen: when an endpoint receives a request, it returns a job_id. It places the job into a job queue processed by a thread pool. A thread picks up a job from the queue, he endpoint checks if the job_id is valid, whether the result is ready, and returns the appropriate response.
It performs the operation, and writes the result to a file named after the job_id in the results/ directory. 

Possible endpoints include:
* /api/states_mean: Calculates and returns the mean values for each state.
* /api/state_mean: Returns the mean value for a specified state.
* /api/best5: Returns the top 5 states based on the specified statistic.
* /api/worst5: Returns the bottom 5 states based on the specified statistic.
* /api/global_mean: Calculates and returns the global mean value.
* /api/diff_from_mean: Returns the difference between global mean and state mean for all states.
* /api/state_diff_from_mean: Returns the difference for a specified state.
* /api/mean_by_category: Calculates mean values for each segment within categories for all states.
* /api/state_mean_by_category: Returns mean values for each segment within categories for a specified state.
* /api/graceful_shutdown: Initiates a graceful shutdown of the server.
* /api/jobs: Lists all job IDs and their status.
* /api/num_jobs: Returns the number of remaining jobs.
* /api/get_results/&lt;job_id&gt;: Retrieves results for a specified job ID.

To run create a virtual environment and install the requirements:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To test you can either run the flask server and check using a program like Postman or you can run the checker which automatically sends requests to the server and checks the responses based on a folder of expected responses.

To do the latter, in a shell run the server:
```
source venv/bin/activate
make run_server
```
In another shell run the checker:
```
source venv/bin/activate
make run_tests
``` 
Also included a unit testing file in case you want to run the tests individually.

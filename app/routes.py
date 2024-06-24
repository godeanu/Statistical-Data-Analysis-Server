"""routes"""
import os
import json
from flask import request, jsonify
from app import webserver

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """Example POST endpoint that receives JSON data and returns a JSON response"""
    if request.method == 'POST':

        data = request.json
        print(f"got data in post {data}")

        response = {"message": "Received data successfully", "data": data}

        return jsonify(response)
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    """Get the number of jobs left in the queue"""
    num_jobs_left = webserver.tasks_runner.queue.qsize()

    return jsonify({"jobs_left": num_jobs_left})

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    """Initiate a graceful shutdown of the webserver tasks runner"""
    if not webserver.tasks_runner.is_shutdown():
        webserver.tasks_runner.graceful_shutdown()
        return jsonify({"message": "Shutdown initiated"})
    return jsonify({"message": "Shutdown already initiated"})

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """Get the results of a job with the given job_id"""
    print(f"JobID is {job_id}")

    results_path = os.path.join('results/', f'{job_id}')

    if not os.path.exists(results_path):
        id = int(results_path.split('_')[2])
        if id < webserver.job_counter:
            return jsonify({
            "status": "running",
        })
        else:
            return jsonify({
            "status": "error",
            "message": "Job ID not found"
        })
    try:
        with open(results_path, 'r') as file:
            result_data = json.load(file)
            return jsonify({
                "status": "done",
                "data": result_data  
            })
    except json.JSONDecodeError:
        return jsonify({"status": "error", "message": "Failed to decode result data"}), 500

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """Endpoint to get the mean of all states"""
    # Get request data
    data = request.json

    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    job_id = webserver.job_counter
    webserver.tasks_runner.queue.put((job_id, data, "states_mean", webserver.data_ingestor))
    webserver.job_counter += 1

    return jsonify({"job_id": 'job_id_'+str(job_id)})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """Endpoint to get the mean of a specific state"""

    data = request.json

    job_id = webserver.job_counter
    webserver.tasks_runner.queue.put((job_id, data, "state_mean", webserver.data_ingestor))
    webserver.job_counter += 1

    return jsonify({"job_id": 'job_id_'+str(job_id)})

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """Endpoint to get the best 5 states for a given question"""

    data = request.json

    job_id = webserver.job_counter
    webserver.tasks_runner.queue.put((job_id, data, "best5", webserver.data_ingestor))
    webserver.job_counter += 1

    return jsonify({"job_id": 'job_id_'+str(job_id)})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """Endpoint to get the worst 5 states for a given question"""
    data = request.json

    job_id = webserver.job_counter
    webserver.tasks_runner.queue.put((job_id, data, "worst5", webserver.data_ingestor))
    webserver.job_counter += 1

    return jsonify({"job_id": 'job_id_'+str(job_id)})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """Endpoint to get the global mean of a given question"""
    data = request.json

    job_id = webserver.job_counter
    webserver.tasks_runner.queue.put((job_id, data, "global_mean", webserver.data_ingestor))
    webserver.job_counter += 1

    return jsonify({"job_id": 'job_id_'+str(job_id)})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """Endpoint to get the difference of a state from the global mean for a given question"""

    data = request.json

    job_id = webserver.job_counter
    webserver.tasks_runner.queue.put((job_id, data, "diff_from_mean", webserver.data_ingestor))
    webserver.job_counter += 1

    return jsonify({"job_id": 'job_id_'+str(job_id)})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """Endpoint to get the difference of a state from the global mean for a given question"""

    data = request.json

    job_id = webserver.job_counter
    webserver.tasks_runner.queue.put((job_id, data, "state_diff_from_mean",
                                      webserver.data_ingestor))
    webserver.job_counter += 1

    return jsonify({"job_id": 'job_id_'+str(job_id)})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """Endpoint to get the mean of a category for a given question"""

    data = request.json

    job_id = webserver.job_counter
    webserver.tasks_runner.queue.put((job_id, data, "mean_by_category", webserver.data_ingestor))
    webserver.job_counter += 1

    return jsonify({"job_id": 'job_id_'+str(job_id)})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """Endpoint to get the mean of a category for a given question for a specific state"""

    data = request.json

    job_id = webserver.job_counter
    webserver.tasks_runner.queue.put((job_id, data, "state_mean_by_category",
                                      webserver.data_ingestor))
    webserver.job_counter += 1

    return jsonify({"job_id": 'job_id_'+str(job_id)})

@webserver.route('/')
@webserver.route('/index')
def index():
    """something"""
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    """Get all defined routes in the webserver"""
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes

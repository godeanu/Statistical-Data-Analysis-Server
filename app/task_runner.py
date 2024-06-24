"""Task Runner Module"""
from queue import Queue
from threading import Thread, Event, Lock
import os
import json
import tempfile
import math

class ThreadPool:
    """Thread Pool"""
    def __init__(self):

        self.queue = Queue()
        self.threads = []
        self.graceful_shutdown = Event()
        self.num_of_threads = os.getenv('TP_NUM_OF_THREADS', os.cpu_count())

        for _ in range(self.num_of_threads):
            thread = TaskRunner(self.queue)
            thread.start()
            self.threads.append(thread)


    def add_job(self, job):
        """Add a job to the ThreadPool."""
        self.queue.put(job)

    def graceful_shutdown(self):
        """Gracefully shutdown the ThreadPool."""
        self.graceful_shutdown.set()
        for thread in self.threads:
            thread.join()

    def is_shutdown(self):
        """Check if the ThreadPool is in the process of shutting down."""
        return self.graceful_shutdown.is_set()


def calculate_states_mean(data, question):
    """Calculate the mean value for a given question and all states."""
    result = {}
    for state, questions in data.items():
        if question in questions:
            all_values = []
            for strat_category in questions[question].values():
                for values in strat_category.values():
                    all_values.extend([v for v in values if v is not None])

            if all_values:
                result[state] = sum(all_values) / len(all_values)

    sorted_result = dict(sorted(result.items(), key=lambda item: item[1]))
    return sorted_result


def calculate_state_mean(data, question, state):
    """Calculate the mean value for a given question and state."""
    result = {}
    if state in data and question in data[state]:
        all_values = []
        for strat_category in data[state][question].values():
            for values in strat_category.values():
                all_values.extend([v for v in values if v is not None])
        if all_values:
            result[state] = sum(all_values) / len(all_values)

    return result

def calculate_best5(data, question, questions_best_is_max):
    """Calculate the best 5 states for a given question."""
    result = {}
    for state, questions in data.items():
        if question in questions:
            all_values = []
            for strat_category in questions[question].values():
                for strat_values in strat_category.values():
                    all_values.extend([v for v in strat_values if isinstance(v, (int, float))])

            if all_values:
                mean_value = sum(all_values) / len(all_values)
                result[state] = mean_value

    is_reverse = True if question in questions_best_is_max else False
    sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=is_reverse)[:5]

    sorted_result_dict = dict(sorted_result)

    return sorted_result_dict


def calculate_worst5(data, question, questions_best_is_min):
    """Calculate the worst 5 states for a given question."""
    result = {}
    for state, questions in data.items():
        if question in questions:
            all_values = []
            for strat_category in questions[question].values():
                for strat_values in strat_category.values():
                    all_values.extend([v for v in strat_values if isinstance(v, (int, float))])

            if all_values:
                mean_value = sum(all_values) / len(all_values)
                result[state] = mean_value

    is_reverse = True if question in questions_best_is_min else False
    sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=is_reverse)[:5]

    sorted_result_dict = dict(sorted_result)

    return sorted_result_dict

def calculate_global_mean(data, question):
    """Calculate the global mean for a given question."""
    total_sum = 0
    total_count = 0

    for state, questions in data.items():
        if question in questions:
            for strat_category in questions[question].values():
                for strat_values in strat_category.values():
                    valid_values = [value for value in strat_values
                                    if isinstance(value, (int, float))]
                    total_sum += sum(valid_values)
                    total_count += len(valid_values)

    if total_count > 0:
        return {"global_mean": total_sum / total_count}
    return {"global_mean": None}


def calculate_diff_from_mean(data, question):
    """Calculate the difference between the global mean and the state mean for a given question."""
    global_mean = calculate_global_mean(data, question)["global_mean"]

    result = {}
    for state, questions in data.items():
        if question in questions:
            all_values = []
            for strat_category in questions[question].values():
                for strat_values in strat_category.values():
                    all_values.extend([v for v in strat_values if isinstance(v, (int, float))])

            if all_values:
                mean_value = sum(all_values) / len(all_values)
                result[state] = global_mean - mean_value

    return result

def calculate_state_diff_from_mean(data, question, state):
    """Calculate the difference between the global mean and the state mean for a given question."""
    global_mean_result = calculate_global_mean(data, question)
    global_mean = global_mean_result.get("global_mean", 0)

    state_mean = None
    if state in data and question in data[state]:
        all_values = []
        for strat_category in data[state][question].values():
            for strat_values in strat_category.values():
                all_values.extend([v for v in strat_values if isinstance(v, (int, float))])

        if all_values:
            state_mean = sum(all_values) / len(all_values)


    if state_mean is not None and global_mean is not None:
        return {state: global_mean - state_mean}
    return {state: None}

def calculate_mean_by_category(data, question):
    """Calculate the mean value for a given question, stratified by category and value."""
    result = {}
    for state, questions in data.items():
        if question in questions:
            for strat_category, strat_values in questions[question].items():
                if strat_category is None or strat_category == '' or str(strat_category).lower() == 'nan':
                    continue
                for strat_value, values in strat_values.items():
                    if strat_value is None or strat_value == '' or str(strat_value).lower() == 'nan':
                        continue
                    valid_values = [value for value in values if value is not
                                    None and not (isinstance(value, float) and math.isnan(value))]
                    if valid_values:
                        mean_value = sum(valid_values) / len(valid_values)
                        key = f"('{state}', '{strat_category}', '{strat_value}')"
                        result[key] = mean_value
    return result

def calculate_state_mean_by_category(data, question, state):
    """Calculate the mean value for a given question and state, stratified by category and value."""
    state_result = {}

    if state in data and question in data[state]:
        for strat_category, strat_values in data[state][question].items():
            for strat_value, values in strat_values.items():
                valid_values = [value for value in values if isinstance(value, (int, float))]
                if valid_values:
                    mean_value = sum(valid_values) / len(valid_values)
                    key_str = f"('{strat_category}', '{strat_value}')"
                    state_result[key_str] = mean_value

    return {state: state_result}



class TaskRunner(Thread):
    """Threaded Task Runner"""
    def __init__(self, q: Queue):
        if not os.path.exists('results'):
            os.makedirs('results')
        super().__init__()
        self.queue = q

    def run(self):
        while True:
            job_id, job_data, job_type, data_ingestor = self.queue.get()
            result = None

            if job_type == 'states_mean':
                result = calculate_states_mean(data_ingestor.data, job_data['question'])
            elif job_type == 'state_mean':
                result = calculate_state_mean(data_ingestor.data, job_data['question'],
                                              job_data['state'])
            elif job_type == 'best5':
                result = calculate_best5(data_ingestor.data, job_data['question'],
                                         data_ingestor.questions_best_is_max)
            elif job_type == 'worst5':
                result = calculate_worst5(data_ingestor.data, job_data['question'],
                                          data_ingestor.questions_best_is_min)
            elif job_type == 'global_mean':
                result = calculate_global_mean(data_ingestor.data, job_data['question'])
            elif job_type == 'diff_from_mean':
                result = calculate_diff_from_mean(data_ingestor.data, job_data['question'])
            elif job_type == 'state_diff_from_mean':
                result = calculate_state_diff_from_mean(data_ingestor.data,
                                                        job_data['question'], job_data['state'])
            elif job_type == 'mean_by_category':
                result = calculate_mean_by_category(data_ingestor.data,
                                                    job_data['question'])
            elif job_type == 'state_mean_by_category':
                result = calculate_state_mean_by_category(data_ingestor.data,
                                                          job_data['question'], job_data['state'])

            # did this to make sure the file is written before it will be read - rename is atomic

            temp_file_path = tempfile.mktemp(dir='results')
            with open(temp_file_path, 'w') as temp_file:
                json.dump(result, temp_file)

            os.rename(temp_file_path, f'results/job_id_{job_id}')
            self.queue.task_done()
            
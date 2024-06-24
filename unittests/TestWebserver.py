import sys
import os
import unittest
import json
import unittest
sys.path.append('./unittests')

from app.data_ingestor import DataIngestor
from app.task_runner import calculate_diff_from_mean, calculate_global_mean, calculate_state_diff_from_mean, calculate_states_mean, calculate_state_mean, calculate_worst5, calculate_mean_by_category, calculate_best5, calculate_state_mean_by_category

class TestWebserver(unittest.TestCase):

    def setUp(self):
        csv_path = "unittests/nutrition.csv"
        self.data_ingestor = DataIngestor(csv_path)
        self.data = self.data_ingestor.data

    def read_expected_output(self, test_type, filename):
        """Utility method to read the expected output JSON from a file based on test type."""
        base_path = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_path, 'unittests', 'outputs', test_type, filename)
        with open(file_path, 'r') as file:
            return json.load(file)

    def test_state_diff_from_mean(self):
        request_data = {
                            "question": "Percent of adults who report consuming vegetables less than one time daily",
                            "state": "Virgin Islands"
                        }

        global_mean_data = calculate_global_mean(self.data, request_data["question"])

        result = calculate_state_diff_from_mean(self.data, request_data["question"], request_data["state"])


        expected_output = self.read_expected_output("state_diff_from_mean", "out-1.json")

        self.assertAlmostEqual(result[request_data["state"]], expected_output[request_data["state"]], places=5)

    def test_states_mean(self):
        request_data = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification"
        }
        result = calculate_states_mean(self.data, request_data["question"])
        expected_output = self.read_expected_output("states_mean", "out-1.json")
        for state, value in result.items():
            if state in expected_output:
                self.assertAlmostEqual(value, expected_output[state], places=5)

    def test_state_mean(self):
        request_data = {"question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)", "state": "Guam"}
        result = calculate_state_mean(self.data, request_data["question"], request_data["state"])
        expected_output = self.read_expected_output("state_mean", "out-1.json")
        
        if request_data["state"] in result:
            self.assertAlmostEqual(result[request_data["state"]], expected_output[request_data["state"]], places=5)
        else:
            self.fail(f"Expected state {request_data['state']} not found in result")

    def test_best5(self):
        request_data = {"question": "Percent of adults aged 18 years and older who have an overweight classification"}
        questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]
        
        result = calculate_best5(self.data, request_data["question"], questions_best_is_max)
        expected_output = self.read_expected_output("best5", "out-1.json")
        
        for state, value in expected_output.items():
            if state in result:
                self.assertAlmostEqual(result[state], expected_output[state], places=5)
            else:
                self.fail(f"Expected state {state} not found in result")

        self.assertEqual(len(result), 5, "The result should contain exactly 5 states.")

    def worst5(self):
        request_data = {"question": "Percent of adults aged 18 years and older who have an overweight classification"}
        questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]
        
        result = calculate_worst5(self.data, request_data["question"], questions_best_is_min)
        expected_output = self.read_expected_output("worst5", "out-1.json")
        
        for state, value in expected_output.items():
            if state in result:
                self.assertAlmostEqual(result[state], expected_output[state], places=5)
            else:
                self.fail(f"Expected state {state} not found in result")

        self.assertEqual(len(result), 5, "The result should contain exactly 5 states.")

    def test_global_mean(self):
        request_data = {"question": "Percent of adults aged 18 years and older who have an overweight classification"}
        result = calculate_global_mean(self.data, request_data["question"])
        expected_output = self.read_expected_output("global_mean", "out-1.json")
        
        if 'global_mean' in expected_output:
            if expected_output['global_mean'] is None:
                self.assertIsNone(result['global_mean'], "Expected global mean to be None")
            else:
                self.assertAlmostEqual(result['global_mean'], expected_output['global_mean'], places=5,
                                       msg="The global mean does not match the expected value")
        else:
            self.fail("Expected output does not contain 'global_mean' key")

    def test_diff_from_mean(self):
        request_data = {"question": "Percent of adults aged 18 years and older who have an overweight classification"}
        result = calculate_diff_from_mean(self.data, request_data["question"])
        expected_output = self.read_expected_output("diff_from_mean", "out-1.json")
        
        for state, expected_value in expected_output.items():
            if state in result:
                self.assertAlmostEqual(result[state], expected_value, places=5,
                                       msg=f"The difference for state {state} does not match the expected value.")
            else:
                self.fail(f"Expected state {state} not found in result")

        self.assertEqual(set(result.keys()), set(expected_output.keys()), "The result does not cover all expected states.")


    def test_mean_by_category(self):
        request_data = {"question": "Percent of adults aged 18 years and older who have an overweight classification"}
        result = calculate_mean_by_category(self.data, request_data["question"])
        expected_output = self.read_expected_output("mean_by_category", "out-1.json")
        
        for key, expected_value in expected_output.items():
            if key in result:
                self.assertAlmostEqual(result[key], expected_value, places=5,
                                       msg=f"The mean for {key} does not match the expected value.")
            else:
                self.fail(f"Expected key {key} not found in result")

        self.assertEqual(set(result.keys()), set(expected_output.keys()), "The result keys do not match the expected keys.")

    
    def test_state_mean_by_category(self):
        request_data = {"question": "Percent of adults aged 18 years and older who have an overweight classification", "state": "Oklahoma"}
        result = calculate_state_mean_by_category(self.data, request_data["question"], request_data["state"])
        expected_output = self.read_expected_output("state_mean_by_category", "out-1.json")
        
        if request_data["state"] in result:
            for key, expected_value in expected_output[request_data["state"]].items():
                if key in result[request_data["state"]]:
                    self.assertAlmostEqual(result[request_data["state"]][key], expected_value, places=5,
                                           msg=f"The mean for {key} in {request_data['state']} does not match the expected value.")
                else:
                    self.fail(f"Expected key {key} not found in result for {request_data['state']}")
        else:
            self.fail(f"State {request_data['state']} not found in result")

    

if __name__ == '__main__':
    
    unittest.main()
    
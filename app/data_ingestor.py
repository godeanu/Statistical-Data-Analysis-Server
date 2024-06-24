"""DATA INGESTOR"""
import pandas as pd

class DataIngestor:
    """Class to ingest data from csv file and process it into a dictionary"""
    def __init__(self, csv_path: str):
        # Read csv from csv_path
        df = pd.read_csv(csv_path, usecols=['LocationDesc', 'Question',
                                            'Data_Value',
                                            'StratificationCategory1',
                                            'Stratification1'])
        self.data = self._process_data(df)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    def _process_data(self, df):
        """Process data from csv file into a dictionary"""
        data_dict = {}
        for _, row in df.iterrows():
            state = row['LocationDesc']
            question = row['Question']
            data_value = row['Data_Value']
            strat_category = row['StratificationCategory1']
            strat_value = row['Stratification1']

            if state not in data_dict:
                data_dict[state] = {}

            if question not in data_dict[state]:
                data_dict[state][question] = {}

            if strat_category not in data_dict[state][question]:
                data_dict[state][question][strat_category] = {}

            if strat_value not in data_dict[state][question][strat_category]:
                data_dict[state][question][strat_category][strat_value] = []
            data_dict[state][question][strat_category][strat_value].append(data_value)

        return data_dict

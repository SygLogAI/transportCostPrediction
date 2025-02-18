from ast import Try
import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectFwe, f_regression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline, make_union
from tpot.builtins import StackingEstimator
from tpot.export_utils import set_param_recursive
import pickle
import json
import os

class TransportCost:
    def __init__(self, model_dir) -> None:
        self.model_dir = model_dir

    def save_training_data(self, df):
        traning_set_file = os.path.join(self.model_dir, "training_set.csv")

        df.to_csv(traning_set_file, index=False)


    def fit(self):
        self.set_status("in_progress")
        tpot_data = pd.read_csv(os.path.join(self.model_dir, "training_set.csv"), dtype=np.float64)
        features = tpot_data.drop('target', axis=1)
        training_features, testing_features, training_target, testing_target = \
                    train_test_split(features, tpot_data['target'], random_state=42)

        exported_pipeline = make_pipeline(
            StackingEstimator(estimator=KNeighborsRegressor(n_neighbors=14, p=2, weights="uniform")),
            SelectFwe(score_func=f_regression, alpha=0.02),
            KNeighborsRegressor(n_neighbors=4, p=2, weights="distance")
        )

        set_param_recursive(exported_pipeline.steps, 'random_state', 42)

        exported_pipeline.fit(training_features, training_target)

        self.set_status("done")
        with open(os.path.join(self.model_dir, "model.pickle"), "wb") as f:
            pickle.dump(exported_pipeline, f)


    def predict(self, features):
        with open(os.path.join(self.model_dir, "model.pickle"), "rb") as f:
            exported_pipeline = pickle.load(f)
            results = exported_pipeline.predict(features)
        
            return results

    def set_status(self, status):
        tmp = self.status()

        with open(os.path.join(self.model_dir, "status.json"), "w") as f:    
            tmp["status"] = status
            json.dump(tmp, f)

    def status(self):
        try:
            with open(os.path.join(self.model_dir, "status.json"), "r") as f:
                return json.load(f)
        except:
            return {"status":""}
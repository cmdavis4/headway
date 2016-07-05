import pandas as pd
import numpy as np
import sys
import time
sys.path.append('/Users/charlesdavis/headway')

from utils.nextmuni import fetch_predictions_dataframe, diff_predictions
from utils.database import push_dataframe_to_postgres
from auth.headway_auth import CHARLES_HEADWAY_AUTH

pre = fetch_predictions_dataframe(5)
while True:
    time.sleep(30)
    post = fetch_predictions_dataframe(5)
    arrivals = diff_predictions(pre, post)
    push_dataframe_to_postgres()

print(diff_predictions(pred1, pred2))

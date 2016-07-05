import pandas as pd
import numpy as np
import sys
import time
sys.path.append('/Users/charlesdavis/headway')

from utils.nextmuni import fetch_predictions_dataframe, diff_predictions

pred1 = fetch_predictions_dataframe(5)
time.sleep(20)
pred2 = fetch_predictions_dataframe(5)

print(diff_predictions(pred1, pred2))

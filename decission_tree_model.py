# -*- coding: utf-8 -*-
"""DECISSION TREE model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1g6x_bJ7scGPzNObRgpe7dcR7rgJKeSyK

## Imports 🍐
"""

from google.colab import drive
drive.mount('/content/drive')
import pandas as pd

import numpy as np
from scipy.stats import zscore
from datetime import datetime
from sklearn.preprocessing import LabelEncoder

pip install scikit-learn

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder

from sklearn.tree import export_text

parquet_file_path = '/content/drive/MyDrive/datatlon/train_data.parquet'
data = pd.read_parquet(parquet_file_path)

"""## Decission tree 🍓"""

decission_tree_df = data[['brand', 'phase', 'country', 'dayweek', 'month', 'wd_perc', 'n_nwd_bef', 'n_nwd_aft', 'n_weekday_0', 'n_weekday_1', 'n_weekday_2', 'n_weekday_3', 'n_weekday_4', 'date', 'wd', 'wd_left', 'monthly']].copy()

# 🍓 REPLACE df
decission_tree_df = decission_tree_df

# Assuming 'decission_tree_df' is your DataFrame
# For better interpretability, we encode categorical variables using LabelEncoder
label_encoder = LabelEncoder()
decission_tree_df['brand_encoded'] = label_encoder.fit_transform(decission_tree_df['brand'])
decission_tree_df['country_encoded'] = label_encoder.fit_transform(decission_tree_df['country'])
# decission_tree_df['ther_area_encoded'] = label_encoder.fit_transform(decission_tree_df['ther_area_encoded'])
# decission_tree_df['main_channel_encoded'] = label_encoder.fit_transform(decission_tree_df['main_channel'])
# decission_tree_df['day_of_week'] = label_encoder.fit_transform(decission_tree_df['day_of_week'])

# Splitting the data into features (X) and target variable (y)
X = decission_tree_df[['dayweek', 'month', 'wd_perc', 'n_nwd_bef', 'n_nwd_aft', 'n_weekday_0', 'n_weekday_1', 'n_weekday_2', 'n_weekday_3', 'n_weekday_4', 'wd', 'wd_left', 'country_encoded', 'brand_encoded']]
y = decission_tree_df['phase']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Training the Decision Tree Regressor
decision_tree_model = DecisionTreeRegressor(random_state=42)
decision_tree_model.fit(X_train, y_train)

# Making predictions on the test set
y_pred = decision_tree_model.predict(X_test)

# Evaluate the model using Mean Absolute Error (MAE)
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error: {mae}')

"""## train model based on BRAND (mae 0.053) ❌"""

decission_tree_df['brand'].unique()

selected_brand = 'AIMST'
# Filter data for the selected brand
brand_data = decission_tree_df[decission_tree_df['brand'] == selected_brand]

# Features (X) and target variable (y)
X = brand_data[['dayweek', 'month', 'wd_perc', 'n_nwd_bef', 'n_nwd_aft', 'n_weekday_0', 'n_weekday_1', 'n_weekday_2', 'n_weekday_3', 'n_weekday_4', 'wd', 'wd_left', 'country_encoded', 'brand_encoded']]
y = brand_data['phase']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a decision tree model
decision_tree_model = DecisionTreeRegressor(random_state=42)
decision_tree_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = decision_tree_model.predict(X_test)

# Evaluate the model's performance
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error for {selected_brand}: {mae}')

"""## train model based on MONTH (mae 0.03894) 🍈

1. 0.03958
2. 0.04071
3. 0.03897
4. 0.03963
5. 0.04000
6. 0.03848
7. 0.03670
8. 0.03846
9. 0.03779
10. 0.03766
11. 0.03851
12. 0.04083
"""

print((0.03958 + 0.04071 + 0.03897 + 0.03963 + 0.04000 + 0.03848 + 0.03670 + 0.03846 + 0.03779 + 0.03766 + 0.03851 + 0.04083)/12)

selected_month = 7.0
# Filter data for the selected brand
month_data = decission_tree_df[decission_tree_df['month'] == selected_month]

# Features (X) and target variable (y)
X = month_data[['dayweek', 'month', 'wd_perc', 'n_nwd_bef', 'n_nwd_aft', 'n_weekday_0', 'n_weekday_1', 'n_weekday_2', 'n_weekday_3', 'n_weekday_4', 'wd', 'wd_left', 'country_encoded', 'brand_encoded']]
y = month_data['phase']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a decision tree model
decision_tree_model = DecisionTreeRegressor(random_state=42)
decision_tree_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = decision_tree_model.predict(X_test)

# Evaluate the model's performance
mae = mean_absolute_error(y_test, y_pred)
print(f'Mean Absolute Error for {selected_brand}: {mae}')

"""## Feature importance 🍒"""

feature_importance = pd.Series(decision_tree_model.feature_importances_, index=X.columns)
feature_importance.sort_values(ascending=False, inplace=True)
print(feature_importance)

"""## Submission data & submission template 🫐"""

parquet_file_path = '/content/drive/MyDrive/datatlon/submission_data.parquet'
submission_data = pd.read_parquet(parquet_file_path)
parquet_file_path = '/content/drive/MyDrive/datatlon/submission_template.csv'
submission_template = pd.read_csv(parquet_file_path)

submission_template.head()

submission_template['date'] = pd.to_datetime(submission_template['date'])

# Assuming 'decission_tree_df' is your DataFrame
# For better interpretability, we encode categorical variables using LabelEncoder
label_encoder = LabelEncoder()
submission_data['brand_encoded'] = label_encoder.fit_transform(submission_data['brand'])
submission_data['country_encoded'] = label_encoder.fit_transform(submission_data['country'])
# decission_tree_df['ther_area_encoded'] = label_encoder.fit_transform(decission_tree_df['ther_area_encoded'])
# decission_tree_df['main_channel_encoded'] = label_encoder.fit_transform(decission_tree_df['main_channel'])
# decission_tree_df['day_of_week'] = label_encoder.fit_transform(decission_tree_df['day_of_week'])

# Splitting the data into features (X) and target variable (y)
X_submission = submission_data[['dayweek', 'month', 'wd_perc', 'n_nwd_bef', 'n_nwd_aft', 'n_weekday_0', 'n_weekday_1', 'n_weekday_2', 'n_weekday_3', 'n_weekday_4', 'wd', 'wd_left', 'country_encoded', 'brand_encoded']]

# Make predictions on the submission data
submission_data['prediction'] = decision_tree_model.predict(X_submission)

# merge submission_template and submission_data:
result = pd.merge(submission_template, submission_data, on=['country', 'brand', 'date'])

result.head()

submission_template = result[["country", "brand", "date", "prediction_y"]]

submission_template.reset_index(inplace=True)

submission_template.rename(columns={'prediction_y': 'prediction'}, inplace=True)

"""#### Normalize phase so that it sums to one for each year-month-country-brand 🍟"""

import pandas as pd

# Assuming df_predictions is your prediction DataFrame
submission_template['date'] = pd.to_datetime(submission_template['date'])
submission_template['year'] = submission_template['date'].dt.year
submission_template['month'] = submission_template['date'].dt.month

# Group by country, brand, year, and month
grouped_predictions = submission_template.groupby(['country', 'brand', 'year', 'month'])

# Function to adjust predictions in each group
def adjust_predictions(group):
    # Calculate the sum of predictions in the group
    sum_predictions = group['prediction'].sum()

    # Calculate the adjustment factor to make the sum equal to 1
    adjustment_factor = 1 / sum_predictions

    # Adjust the predictions in the group
    group['adjusted_prediction'] = group['prediction'] * adjustment_factor

    return group

# Apply the adjustment function to each group
df_predictions_adjusted = grouped_predictions.apply(adjust_predictions)

# Drop the original 'prediction' column and rename the adjusted one
df_predictions_adjusted.drop(columns=['prediction'], inplace=True)
df_predictions_adjusted.rename(columns={'adjusted_prediction': 'prediction'}, inplace=True)

df_predictions_adjusted.head()

submission_file = df_predictions_adjusted[["index", "country", "brand", "date", "prediction"]]

submission_file.head()

submission_file.to_csv("/content/drive/MyDrive/datatlon/filled_submission.csv", index=False)

sin_index = df_predictions_adjusted[["country", "brand", "date", "prediction"]]

sin_index.to_csv("/content/drive/MyDrive/datatlon/sin_index.csv", index=False)
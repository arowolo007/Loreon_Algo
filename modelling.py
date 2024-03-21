
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from sklearn.metrics import mean_squared_error, accuracy_score


import pandas as pd

df = pd.read_csv('features/2003-12-18:2024-03-08.csv', index_col=['Date'], parse_dates=['Date'])

def evaluate_model(model, X_test, y_test):
  """
  Evaluates the performance of a model on a given test set.

  Args:
      model: Trained model pipeline (can be GridSearchCV or a regular Pipeline).
      X_test: Feature matrix of the test set.
      y_test: Target values of the test set.

  Returns:
      A dictionary containing evaluation metrics for the model.
  """
  predictions = model.predict(X_test)

  # Check if using GridSearchCV (assuming it's the last step)
  if isinstance(model.steps[-1][1], GridSearchCV):
    # Access best model from GridSearchCV
    model = model.best_estimator_

  if hasattr(model.steps[-1][1], 'decision_function'):  # Classification model
    # Use accuracy score for classification
    accuracy = accuracy_score(y_test, predictions)
    return {'Accuracy': accuracy}
  else:  # Regression model
    # Use mean squared error for regression
    mse = mean_squared_error(y_test, predictions)
    return {'Mean Squared Error': mse}

# %%
# Pipeline for target Prediction (assuming binary a floating number)
target_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', GridSearchCV(RandomForestRegressor(),
                                param_grid={'n_estimators': [100, 200, 300],
                                            'max_depth': [5, 10, 15]}))
])


# Split data into features (X) and targets (y)
X_target = df.drop(columns=['target', 'action'])
y_target = df['target']

# Train pipelines
target_pipeline.fit(X_target, y_target)

# %%



target = y_target.to_frame()
target['prediction'] = target_pipeline.predict(X_target)

target

# %%

# Pipeline for Action Prediction (assuming binary buy/sell)
action_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', GridSearchCV(RandomForestClassifier(),
                                param_grid={'n_estimators': [100, 200, 300],
                                            'max_depth': [5, 10, 15]}))
])


# Split data into features (X) and targets (y)
X_action = df.drop(columns=['target', 'action'])
y_action = df['action']

# Train pipelines
action_pipeline.fit(X_action, y_action)


# %%
action = y_action.to_frame()
action['prediction'] = action_pipeline.predict(X_action)

action

# %%

target_metrics = evaluate_model(target_pipeline,X_target, y_target)
action_metrics = evaluate_model(action_pipeline, X_action, y_action)

print("Target Price Evaluation:", target_metrics)
print("Action Prediction Evaluation:", action_metrics)

# %%




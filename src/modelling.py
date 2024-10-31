# modelling.py

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_random_forest(X_train, y_train):
    """Train a Random Forest model."""
    rf = RandomForestClassifier(random_state=42)
    rf.fit(X_train, y_train)
    return rf

def evaluate_model(model, X_test, y_test):
    """Evaluate the model performance."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy}")
    print(classification_report(y_test, y_pred))

def hyperparameter_tuning(X_train, y_train):
    """Perform hyperparameter tuning using GridSearchCV."""
    rf = RandomForestClassifier(random_state=42)
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20],
        'min_samples_split': [2, 5]
    }
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_

def modelling_pipeline(filepath, target):
    """Run the predictive modelling pipeline."""
    df = pd.read_csv(filepath)
    X = df.drop(columns=[target])
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = train_random_forest(X_train, y_train)
    print("Initial model performance:")
    evaluate_model(model, X_test, y_test)
    
    print("Performing hyperparameter tuning...")
    tuned_model = hyperparameter_tuning(X_train, y_train)
    print("Tuned model performance:")
    evaluate_model(tuned_model, X_test, y_test)

# Example usage
if __name__ == "__main__":
    modelling_pipeline("../data/processed/air_quality_cleaned.csv", target='pollution_index')
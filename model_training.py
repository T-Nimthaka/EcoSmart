# model_training.py

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from data_preprocessing import generate_sample_data, preprocess_data

# Model training function
def train_model(X_train, y_train):
    # Initialize the Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    return model

# Evaluate model performance
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")
    return predictions

if __name__ == "__main__":
    # Prepare data
    df = generate_sample_data()
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Evaluate model
    predictions = evaluate_model(model, X_test, y_test)
    print("Model training and evaluation complete!")

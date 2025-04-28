# data_preprocessing.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Simulate sample energy consumption data
def generate_sample_data():
    np.random.seed(42)
    data = {
        'servers': np.random.randint(1, 10, 100),
        'computers': np.random.randint(10, 50, 100),
        'lights': np.random.randint(5, 30, 100),
        'AC_units': np.random.randint(1, 5, 100),
        'machines': np.random.randint(1, 15, 100),
        'energy_consumption': np.random.uniform(100, 1000, 100)
    }
    df = pd.DataFrame(data)
    return df

# Preprocessing function
def preprocess_data(df):
    X = df.drop('energy_consumption', axis=1)
    y = df['energy_consumption']
    
    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Standardize the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test, scaler

if __name__ == "__main__":
    df = generate_sample_data()
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
    print("Data preprocessing complete!")

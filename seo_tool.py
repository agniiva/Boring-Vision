import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def train_model(data, model_choice="RandomForest"):
    
    X = data[['CTR', 'Position', 'Impressions']]
    y = data['Clicks']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if model_choice == "RandomForest":
        model = RandomForestRegressor(n_estimators=100)
    elif model_choice == "LinearRegression":
        model = LinearRegression()
    elif model_choice == "MLPRegressor":
        model = MLPRegressor(hidden_layer_sizes=(100,), max_iter=1000)

    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    return model, mse

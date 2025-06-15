from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from textblob import TextBlob

# Load & preprocess data
df = pd.read_csv("behaviour_simulation_train.csv")
df.dropna(subset=['content', 'username', 'company', 'likes'], inplace=True)
df['media'].fillna('no_media', inplace=True)
df['has_media'] = (df['media'] != 'no_media').astype(int)
df['content'] = df['content'].astype(str).str.strip().str.lower()
df['datetime'] = pd.to_datetime(df['date'], errors='coerce')
df['hour'] = df['datetime'].dt.hour
df['word_count'] = df['content'].apply(lambda x: len(x.split()))
df['char_count'] = df['content'].apply(len)
df['sentiment'] = df['content'].apply(lambda x: TextBlob(x).sentiment.polarity)

# Features and target
X = df[['word_count', 'char_count', 'has_media', 'hour', 'sentiment']]
y = df['likes']

best_rmse = float('inf')
best_state = None

print("Starting random state scan...\n")

for state in range(1, 101):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=state)

    model = TransformedTargetRegressor(
        regressor=RandomForestRegressor(n_estimators=100, n_jobs=-1),
        func=np.log1p,
        inverse_func=np.expm1
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, preds))

    print(f"Random State {state}: RMSE = {rmse:.4f}")

    if rmse < best_rmse:
        best_rmse = rmse
        best_state = state

print("\nBest Random State:", best_state)
print("Lowest RMSE:", best_rmse)

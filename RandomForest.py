import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix

# Load dataset (change this path to your actual file)
df = pd.read_csv("D:/Crypto History/labeled_bullish_patterns_20250527_164228.csv")

# Drop rows with missing values (if any)
df.dropna(inplace=True)

# Define input features (X) and labels (y)
X = df.drop(columns=["label"])
y = df["label"]

# Split dataset: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Predict on test data
y_pred = model.predict(X_test)

# Print performance results
print("📊 Classification Report:\n", classification_report(y_test, y_pred))
print("🧱 Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Perform cross-validation
cv_scores = cross_val_score(model, X, y, cv=5)
print(f"✅ Cross-validation accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

print("Loading Iris dataset...")
iris = load_iris()
X, y = iris.data, iris.target
target_names = iris.target_names 

print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Training Logistic Regression model...")
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# Evaluate the model 
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Model Accuracy on Test Set: {acc:.4f}")

# Define the directory and filename
output_dir = '.'
model_filename = 'iris_model.pkl'
model_path = os.path.join(output_dir, model_filename)

print(f"Saving model to {model_path}...")
joblib.dump(model, model_path)
joblib.dump(target_names, 'iris_target_names.pkl')


print("Model training and saving complete.")
print(f"Saved model: {model_path}")
print(f"Saved target names: iris_target_names.pkl")
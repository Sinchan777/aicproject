import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

def train_model(data_path, model_save_path):
    df = pd.read_csv(data_path)
    X = df[['Speciality', 'Region', 'Usage Time (mins)', 'Count of Survey Attempts', 'Hour']]
    y = df['Target']
    
    categorical_features = ['Speciality', 'Region', 'Hour']
    numerical_features = ['Usage Time (mins)', 'Count of Survey Attempts']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(class_weight='balanced', random_state=42))
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    
    joblib.dump(model, model_save_path)
    return model

if __name__ == '__main__':
<<<<<<< HEAD
    train_model('data/processed.csv','models/model.pkl')
=======
    train_model('data/processed.csv','models/model.pkl')
>>>>>>> e377d25 (fin.)

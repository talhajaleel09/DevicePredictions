
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.feature_selection import SelectKBest, chi2
import os
import joblib
from price_classification.config import *

def handling_missing_values(df):
    try:
        print("handling_missing_values", df)
        missing_data = df[df.isnull().any(axis=1)]
        
        if not missing_data.index.empty:
            print("It is not empty ************************")
            print("missing_data :   ", missing_data.index)
            print(type(missing_data))
            df_filled = df.copy()
            print("missing_data :   ", missing_data)

            # Identify columns with missing values (NaN)
            columns_with_missing_values = df_filled.columns[missing_data]
            print("columns with missing values :   ", columns_with_missing_values)

            # columns_with_missing_values
            imputer = KNNImputer()

            df_filled[columns_with_missing_values] = imputer.fit_transform(df_filled[columns_with_missing_values])

            df_filled.iloc[[157, 158, 217, 261]]
            return df_filled
        else:
            print("entered else part")
            return df
    except Exception as e:
        print("Error message    :   ",e)
        return df

def get_best_columns(df):
    try:
        selected_columns = SELECTED_COLUMNS

        selected_df =  df.loc[:, selected_columns]

        return selected_df
    except Exception as e:
        print("Error message    :   ",e)

def get_loaded_model():
    """
    This will load the Random Forest model which is created Inside Jupyter Notebook
    """
    try:
        # this will get the path where model is present
        model_dir = os.path.dirname(os.getcwd())
        model_file_name = MODEL_NAME
        model_file_path = os.path.join(model_dir, model_file_name)
        loaded_model = joblib.load(model_file_path)
        return loaded_model
    except Exception as e:
        return f"error: {e}" 
from flask import Flask, render_template, request
# import androguard
import pickle
# from androguard.misc import APK
from androguard.core.bytecodes import apk
import numpy as np
import pandas as pd
import keras
import tensorflow as tf
# Specify the header values
header = ["Column1", "Column2"]

# Read the CSV file with the header
df = pd.read_csv("dataset-features-categories.csv", header=None, names=header)

# Display the DataFrame
print(df["Column1"])
from collections import defaultdict
import pandas as pd

# Create a defaultdict with values set to 0 by default
obj = defaultdict(int)

# Iterate over the unique values in "Column1"
for value in df["Column1"].unique():
    obj[value] = 0

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        apk_file = request.files['file']

        # Save the uploaded file to a temporary location
        apk_path = 'uploaded/' + apk_file.filename
        apk_file.save(apk_path)
        a = apk.APK(apk_path)

        ###Extracting Intent Filters
        name_attributes = set()
        for activity in a.get_activities():
            name = activity.split('/')[-1]
            name_attributes.add(name)
        print("Intent Filters")
        for attribute in name_attributes:
            used_intents = a.get_intent_filters('activity',attribute)
            print("activity intents ::",used_intents)
            for intent in used_intents:
                if intent in obj:
                    obj[intent] = 1

        print("after intend",obj)

        used_permissions = a.get_permissions()
        print("\nUsed Permissions:")
        for permission in used_permissions:
            split_string = permission.split('.')  # Split the string at each occurrence of '.'
            value = split_string[-1]
            if value in obj:
                    obj[value] = 1
            print(permission)

        print("after permission",obj)
        temp = pd.DataFrame(obj, index=[0])

        x_test = temp.to_numpy()
        model = load_model(request.form['model'])
        prediction = model.predict(x_test)
        print("prediction",prediction)
        reshaped_array = prediction.reshape(-1, 1)
        result=reshaped_array[0]
        if result[0] <= 0.6:
            return render_template('result.html', prediction="Benign")
        else:
            return render_template('result.html', prediction="Malign")

    return render_template('upload.html')

def load_model(model_name):
    # Load the corresponding pickle file based on the selected model
    if model_name == 'sequential':
        model = keras.models.load_model('my_model.h5')
    elif model_name == 'lstm':
        model = keras.models.load_model('finallstm.h5')
    elif model_name == 'voting':
        with open('ensmvoting.pkl', 'rb') as f:
            model = pickle.load(f)
 
    else:
        # Handle the case when an invalid model option is selected
        raise ValueError('Invalid model option selected.')

    return model

from flask import Flask, render_template, request
# import androguard
import pickle
# from androguard.misc import APK
from androguard.core.bytecodes import apk

import pandas as pd

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

# Print the object




app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        apk_file = request.files['file']

        # Save the uploaded file to a temporary location
        apk_path = 'C:/Entertainment/swabna-project/uploaded_' + apk_file.filename
        apk_file.save(apk_path)
        # apk_path = '/content/drive/MyDrive/swabna/inshot.apk'
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
            #     print("Activity Name:", attribute)
            #     print("Intent Action:", ', '.join(used_intents['action']))
            #     print("Intent Category:", ', '.join(used_intents['category']))

        # Extracting used permissions
        used_permissions = a.get_permissions()
        print("\nUsed Permissions:")
        for permission in used_permissions:
            split_string = permission.split('.')  # Split the string at each occurrence of '.'
            value = split_string[-1]
            if value in obj:
                    obj[value] = 1
            print(permission)
        # apk_file = request.files['file']
        print("after permission",obj)
        # Save the uploaded file to a temporary location
#         apk_path = 'C:/Information Security/swabna/temp' + apk_file.filename
#         apk_file.save(apk_path)

#         # Process the APK file using Androguard
#         apk = APK(apk_path)
#         print("before apk",obj)
#         # Extract the desired information (permissions, API calls, intent, etc.)
#         permissions = apk.get_permissions()
#         # Iterate over the unique values in "Column1"
#         for value in df["Column1"].unique():
#             if value in permissions:
#                 obj[value] = 1

# # Print the object
#         print("after apk",obj)
#         print(obj)
#         api_calls = apk.get_android_api_calls()
#         intent = apk.get_intent_filters()
#         print(permissions,api_calls,intent)
#         # Load the machine learning model
        model = load_model(request.form['model'])

        # Perform the prediction using the loaded model
        # prediction = model.predict([permissions, api_calls, intent])[0]
        prediction = model.predict(obj)
        return render_template('result.html', prediction=prediction)

    return render_template('upload.html')

def load_model(model_name):
    # Load the corresponding pickle file based on the selected model
    if model_name == 'lstm':
        with open('lstm.pkl', 'rb') as f:
            model = pickle.load(f)
    elif model_name == 'voting':
        with open('ensmvoting.pkl', 'rb') as f:
            model = pickle.load(f)
    # elif model_name == 'svm':
    #     with open('svm_model.pkl', 'rb') as f:
    #         model = pickle.load(f)
    # elif model_name == 'knn':
    #     with open('knn_model.pkl', 'rb') as f:
    #         model = pickle.load(f)
    else:
        # Handle the case when an invalid model option is selected
        raise ValueError('Invalid model option selected.')

    return model

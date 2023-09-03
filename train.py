import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import emlearn

DATA_FILE = 'imu.csv'
WINDOW_SAMPLES = 10

if not os.path.exists(DATA_FILE):
   exit

inputs = []
outputs = []
output_lbls = []
output_count = 0

df = pd.read_csv(DATA_FILE)

movement_types = df['movement_name'].unique()
print(movement_types)

# break the data up into windows
for movement_name in movement_types:
   print(f"Processing {movement_name}'.")

   movement_df = df[df['movement_name'] == movement_name]
   movement_df.index = range(len(movement_df.index))

   num_recordings = int(movement_df.shape[0] / WINDOW_SAMPLES)

   print(f"\tThere are {num_recordings} recordings of the {movement_name} gesture.")

   for i in range(num_recordings):
      tensor = []
      for j in range(WINDOW_SAMPLES):
         index = i * WINDOW_SAMPLES + j
         # normalize the input data, between 0 to 1.
         # This is roughly done. Not specific to each axis.
         tensor += [
               (movement_df['x'][index] + 90) / 180,
               (movement_df['y'][index] + 90) / 180,
               (movement_df['z'][index] + 90) / 180
         ]

      inputs.append(tensor)
      outputs.append(output_count)
   
   output_lbls.append(movement_name)
   #output_dict[movement_name] = output_count
   output_count += 1

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(inputs, outputs, test_size=0.2)

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=output_lbls)
disp.plot()
plt.show()
plt.savefig("matrix.png")

#convert to C
cmodel = emlearn.convert(rf, method='inline')
cmodel.save(file='model.h', name='model')

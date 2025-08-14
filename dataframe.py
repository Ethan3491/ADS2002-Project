# Mount the Google Drive at /content/drive
drive.mount('/content/drive')

#Read both csv files into pandas dataframes
train_annotations = pd.read_csv("/content/drive/MyDrive/ranzcr-clip-catheter-line-classification/train_annotations.csv")
train = pd.read_csv("/content/drive/MyDrive/ranzcr-clip-catheter-line-classification/train.csv")

# Merge on 'StudyInstanceUID' to add the PatientID column
df = train_annotations.merge(train[['StudyInstanceUID', 'PatientID']], on='StudyInstanceUID', how='left')

#Convert string to list of lists in data column
df['data'] = df['data'].apply(lambda x: ast.literal_eval(x))

#Drop all rows which are incompletely imaged NGTs or Swan Ganz catheters 
df = df[~df['label'].isin(['NGT - Incompletely Imaged', 'Swan Ganz Catheter Present'])]

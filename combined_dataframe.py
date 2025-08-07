#Read both csv files into pandas dataframes
train_annotations = pd.read_csv("/content/drive/MyDrive/ranzcr-clip-catheter-line-classification/train_annotations.csv")
train = pd.read_csv("/content/drive/MyDrive/ranzcr-clip-catheter-line-classification/train.csv")

# Merge on 'StudyInstanceUID' to add the PatientID column
df = train_annotations.merge(train[['StudyInstanceUID', 'PatientID']], on='StudyInstanceUID', how='left')

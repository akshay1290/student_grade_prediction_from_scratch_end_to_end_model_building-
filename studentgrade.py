# -*- coding: utf-8 -*-
"""studentgrade.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VVoutAM-uwDJCB9OgdQsogc0WzynmWFS
"""

import pandas as pd          
import numpy as np 
import seaborn as sns # For mathematical calculations
import matplotlib.pyplot as plt  # For plotting graphs

# Load the datasets
df1 = pd.read_csv('students(1).csv')
df2 = pd.read_csv('students(2).csv')

df1.head()

df2.head()

common_column = 'id'

# Merge the two datasets on a common column
df = pd.merge(df1, df2, on=common_column)
df.replace(['?', '/', '#'], np.nan, inplace=True)
# Print the merged dataset
print(df)

df.head()

#Check the shape of dataframe
df.shape

df.info()

# Identifying the unique number of values in the dataset
df.nunique()

#Checking each column in the data for null values
df.isnull().sum()

df=df.drop(['health','higher','reason'],axis=1)

df['famsize'].value_counts()

mode_val = df['famsize'].mode()[0]

df['famsize'].fillna(mode_val, inplace=True)

df.describe()

df = df.drop('id', axis=1)

# defining numerical & categorical columns
numeric_features = [feature for feature in df.columns if df[feature].dtype != 'O']
categorical_features = [feature for feature in df.columns if df[feature].dtype == 'O']

# print columns
print('We have {} numerical features : {}'.format(len(numeric_features), numeric_features))
print('\nWe have {} categorical features : {}'.format(len(categorical_features), categorical_features))

df['absences'].value_counts()

# Histograms of each feature
for feature in numeric_features:
    sns.displot(df[feature])
    plt.title(feature)
    plt.show()

# Distribution of final grade in student-por.csv
sns.histplot(df['G3'], kde=True, color='red')
plt.title("Final Grade Distribution - df.csv")
plt.xlabel("Final Grade")
plt.ylabel("Count")
plt.show()

# Number of Male and female students
female_students = len(df[df['sex'] == 'F'])
print(" No of female students",female_students)
male_students = len(df[df['sex'] == 'M'])
print(" No of male students",male_students)

# students from urban or rural areas
urban_stud = len(df[df['address'] == 'U'])
print('Number of Urban students:',urban_stud)
rural_stud = len(df[df['address'] == 'R'])
print('Number of Rural students:',rural_stud)

# Age of students
plot = sns.kdeplot(df['age'])    # Kernel Density Estimations
plot.axes.set_title('Ages of students')
plot.set_xlabel('Age')
plot.set_ylabel('Count')
plt.show()
#Observation:Plot shows the median grades of the three age groups are similar
#Age groups: 15,16,17

# Do urban students perform better than rural students?
# Grade distribution by address
sns.kdeplot(df.loc[df['address'] == 'U', 'G3'], label='Urban', shade = True)
sns.kdeplot(df.loc[df['address'] == 'R', 'G3'], label='Rural', shade = True)
plt.title('Do urban students score higher than rural students?')
plt.xlabel('Grade');
plt.ylabel('Density')
plt.show()
#Observation:Graph clearly shows 
#There is not much difference between the grades based on location.

# Failures
plot = sns.barplot(x=df['failures'],y=df['G3'],palette='autumn')
plot.axes.set_title('Previous Failures vs Final Grade(G3)')
# Observation: Student with less previous failures usually score higher

# Does age affetcs final grade
plot = sns.barplot(x=df['age'],y=df['G3'],palette='autumn')
plot.axes.set_title('Age vs Final Grade(G3)')
# Observation:
# Age group 20 seems to score highest grades among all.

# Family Education Attribute i,e Mother Education and Father Education
family_education = df['Fedu'] + df['Medu']
plot = sns.barplot(x=family_education,y=df['G3'],palette='autumn')
plot.axes.set_title('Family Education vs Final Grade(G3)')
# Observation: Educated Families results in highest grade

# Going out 
plot = sns.barplot(x=df['goout'],y=df['G3'],palette='autumn')
plot.axes.set_title('Go Out vs Final Grade(G3)')
# Observation: Students goes out lott scores less

df.corr()

corr=df.corr()

# Plotting the heatmap of correlation between features
plt.figure(figsize=(15,15))
sns.heatmap(df.corr(),annot=True);

print(corr["G3"].sort_values(ascending=False))

df['prev_grade'] = round(df['G1']+df['G2']/ 2)

df=df.drop(['G1','G2'],axis=1)

df.dtypes

# Import label encoder 
from sklearn import preprocessing 
  
# label_encoder object knows how to understand word labels. 
label_encoder = preprocessing.LabelEncoder() 

df['school']= label_encoder.fit_transform(df['school'])
df['sex']= label_encoder.fit_transform(df['sex'])

df['romantic']= label_encoder.fit_transform(df['romantic'])
df['internet']= label_encoder.fit_transform(df['internet'])

df['nursery']= label_encoder.fit_transform(df['nursery'])
df['activities']= label_encoder.fit_transform(df['activities'])
df['paid']= label_encoder.fit_transform(df['paid'])
df['famsup']= label_encoder.fit_transform(df['famsup'])
df['schoolsup']= label_encoder.fit_transform(df['schoolsup'])
df['guardian']= label_encoder.fit_transform(df['guardian'])

df['Fjob']= label_encoder.fit_transform(df['Fjob'])
df['Mjob']= label_encoder.fit_transform(df['Mjob'])
df['Pstatus']= label_encoder.fit_transform(df['Pstatus'])
df['famsize']= label_encoder.fit_transform(df['famsize'])
df['address']= label_encoder.fit_transform(df['address'])
df['sex']= label_encoder.fit_transform(df['sex'])

#checking outiliers in dataset
fig, axs = plt.subplots(ncols=11, nrows=3, figsize=(20, 10))
index = 0
axs = axs.flatten()
for k,v in df.items():
    sns.boxplot(y=k, data= df, ax=axs[index])
    index += 1
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=5.0)

# Identify the columns with potential outliers
outlier_cols = ['prev_grade', 'absences','Dalc',
                'freetime','famrel','internet','nursery','schoolsup','failures',
                'studytime','traveltime','guardian','Fjob','Mjob',
                'Fedu','Pstatus','famsize','address','age','school']

# Replace outliers with the upper and lower bounds
for col in outlier_cols:
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + 1.5*iqr
    lower_bound = q1 - 1.5*iqr
    df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
    df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])

#checking outiliers in dataset
fig, axs = plt.subplots(ncols=11, nrows=3, figsize=(20, 10))
index = 0
axs = axs.flatten()
for k,v in df.items():
    sns.boxplot(y=k, data= df, ax=axs[index])
    index += 1
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=5.0)

df.info()

import numpy as np

class DecisionTreeRegressor:
    def __init__(self, max_depth=None, min_samples_split=2):
        self.max_depth = max_depth#determines the maximum depth of the decision tree that will be constructed
        self.min_samples_split = min_samples_split#specifies the minimum number of samples required to split an internal node
        self.tree = None

    def mean_squared_error(self, y):
        return np.mean((y - np.mean(y)) ** 2)# Calculate mean squared error of targets

    def split_data(self, X, y, feature_idx, threshold):
        left_mask = X[:, feature_idx] <= threshold# find the indices of samples where the feature is less than the threshold value
        right_mask = X[:, feature_idx] > threshold # find the indices of samples where the feature is greater than or equal to the split value
        X_left, y_left = X[left_mask], y[left_mask] #create a new array of input samples for the left node using the left indices, #create a new array of labels for the left node using the left indice
        X_right, y_right = X[right_mask], y[right_mask]# create a new array of input samples for the right node using the right indices,# create a new array of labels for the right node using the right indices
        return X_left, y_left, X_right, y_right# return the new input and label arrays for the left and right nodes

    def find_best_split(self, X, y):
        ''' function to find the best split '''
        best_feature_idx, best_threshold, best_mse = None, None, np.inf
         #ensure that the first value you encounter will be greater than the current maximum value
         # loop over all the features in the dataset
        for feature_idx in range(X.shape[1]):
            # loop over all the unique feature values present in the data
            for threshold in np.unique(X[:, feature_idx]):
              # get current split
                X_left, y_left, X_right, y_right = self.split_data(X, y, feature_idx, threshold)
                #The code checks if the number of samples in the left and right subsets of the current dataset are less than a specified minimum threshold 
                if len(y_left) < self.min_samples_split or len(y_right) < self.min_samples_split:
                    continue
               # The split separates the data into two subsets: one on the left and the other on the right. The mean squared error is calculated for each subset separately using the method mean_squared_error()
                mse_left, mse_right = self.mean_squared_error(y_left), self.mean_squared_error(y_right)
                mse = mse_left + mse_right
                #It compares the MSE for each split to the current best MSE and updates the best feature index, best threshold, and best MSE if the current split has a lower MSE than the current best split.
                if mse < best_mse:
                    best_feature_idx, best_threshold, best_mse = feature_idx, threshold, mse
        return best_feature_idx, best_threshold, best_mse

    def build_tree(self, X, y, depth):
        if depth == self.max_depth or len(y) < self.min_samples_split:
            return np.mean(y)
        feature_idx, threshold, mse = self.find_best_split(X, y)
        if mse == np.inf:
            return np.mean(y)
        X_left, y_left, X_right, y_right = self.split_data(X, y, feature_idx, threshold)
        left_node = self.build_tree(X_left, y_left, depth + 1)
        right_node = self.build_tree(X_right, y_right, depth + 1)
        return {"feature_idx": feature_idx, "threshold": threshold, "left_node": left_node, "right_node": right_node}

    def fit(self, X, y):
        self.tree = self.build_tree(X, y, 0)
    def set_params(self, **params):
          '''function is used to set the values of the attributes of a decision tree object. The function takes a variable 
          number of keyword arguments (**params), 
          which are pairs of attribute names and their corresponding values that should be set for the decision tree object'''
          for param, value in params.items():
            setattr(self, param, value)
            return self

    def predict(self, X):
        def predict_row(row, node):
            if isinstance(node, float):
                return node
            if row[node["feature_idx"]] <= node["threshold"]:
                return predict_row(row, node["left_node"])
            else:
                return predict_row(row, node["right_node"])
        return np.array([predict_row(row, self.tree) for row in X])
    def mean_squared_errorr(self,y_true, y_pred):
   
      # Check if the lengths of both arrays are equal
      if len(y_true) != len(y_pred):
          raise ValueError("Length of y_true and y_pred should be the same.")
      
      # Calculate the squared differences between the true and predicted values
      squared_differences = [(y_true[i] - y_pred[i])**2 for i in range(len(y_true))]
      
      # Calculate the mean of the squared differences
      mse = sum(squared_differences) / len(squared_differences)
      
      return mse

df=df.drop(['address','famsize', 'Pstatus','Mjob','Fjob','guardian','Dalc','Walc','school'],axis=1)

df.columns

#defining dependent and independent variable as y and x
X = df.drop('G3',axis=1).values
y = df['G3'].values

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.30,random_state=42)

regressor = DecisionTreeRegressor(min_samples_split=4, max_depth=4)
regressor.fit(X_train,y_train)



y_pred = regressor.predict(X_test)

y_pred

from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, y_pred)
mse

df.head()

df.columns

regressor.predict([[1,4,4,2,2,0,0,0,0,0,1,1,1,2,3,4,1,1,6]])

### Create a Pickle file using serialization 
import pickle
pickle_out = open("regressor.pkl","wb")
pickle.dump(regressor, pickle_out)
pickle_out.close()
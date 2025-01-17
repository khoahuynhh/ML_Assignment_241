# %% [markdown]
# <h1 align=center><font size="5"> SVM (Support Vector Machines)</font></h1>

# %% [markdown]
# In this project, we use SVM (Support Vector Machines) to build and train a model using human cell records, and classify cells to whether the samples are benign or malignant.
# 
# SVM works by mapping data to a high-dimensional feature space so that data points can be categorized, even when the data are not otherwise linearly separable. A separator between the categories is found, then the data is transformed in such a way that the separator could be drawn as a hyperplane. Following this, characteristics of new data can be used to predict the group to which a new record should belong.

# %%

import pandas as pd
import pylab as pl
import numpy as np
import scipy.optimize as opt
import wget
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
#matplotlib inline 
import matplotlib.pyplot as plt

# %% [markdown]
# <h2 id="load_dataset">Load the Cancer data</h2>
# The project is based on a dataset that is publicly available from the UCI Machine Learning Repository (Asuncion and Newman, 2007)[http://mlearn.ics.uci.edu/MLRepository.html]. The dataset consists of several hundred human cell sample records, each of which contains the values of a set of cell characteristics. The fields in each record are:
# 
# |Field name|Description|
# |--- |--- |
# |ID|Clump thickness|
# |Clump|Clump thickness|
# |UnifSize|Uniformity of cell size|
# |UnifShape|Uniformity of cell shape|
# |MargAdh|Marginal adhesion|
# |SingEpiSize|Single epithelial cell size|
# |BareNuc|Bare nuclei|
# |BlandChrom|Bland chromatin|
# |NormNucl|Normal nucleoli|
# |Mit|Mitoses|
# |Class|Benign or malignant|
# 
# <br>
# <br>
# 
# For the purposes of this example, we're using a dataset that has a relatively small number of predictors in each record. To download the data, we will use `!wget` to download it from IBM Object Storage.

# %%
#Click here and press Shift+Enter
fname= wget.download('https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/cell_samples.csv')

# %% [markdown]
# ### Load Data From CSV File  

# %%
cell_df = pd.read_csv(fname)
cell_df.head()

# %% [markdown]
# The ID field contains the patient identifiers. The characteristics of the cell samples from each patient are contained in fields Clump to Mit.
# 
# **The values are graded from 1 to 10, with 1 being the closest to benign.**
# 
# The Class field contains the diagnosis, as confirmed by separate medical procedures, as to whether the samples are benign (value = 2) or malignant (value = 4).
# 
# Lets look at the distribution of the classes based on Clump thickness and Uniformity of cell size:

# %%
ax = cell_df[cell_df['Class'] == 4][0:100].plot(kind='scatter', x='Clump', y='UnifSize', color='DarkBlue', label='malignant');
cell_df[cell_df['Class'] == 2][0:100].plot(kind='scatter', x='Clump', y='UnifSize', color='Orange', label='benign', ax=ax);
plt.show()

# %% [markdown]
# ## Data pre-processing and selection

# %% [markdown]
# Lets first look at columns data types:

# %%
cell_df.dtypes

# %% [markdown]
# It looks like the __BareNuc__ column includes some values that are not numerical. We can drop those rows:

# %%
cell_df = cell_df[pd.to_numeric(cell_df['BareNuc'], errors='coerce').notnull()]
cell_df['BareNuc'] = cell_df['BareNuc'].astype('int')
cell_df.dtypes

# %%
feature_df = cell_df[['Clump', 'UnifSize', 'UnifShape', 'MargAdh', 'SingEpiSize', 'BareNuc', 'BlandChrom', 'NormNucl', 'Mit']]
X = np.asarray(feature_df)
X[0:5]

# %% [markdown]
# We want the model to predict the value of Class (that is, benign (=2) or malignant (=4)). As this field can have one of only two possible values, we need to change its measurement level to reflect this.

# %%
cell_df['Class'] = cell_df['Class'].astype('int')
y = np.asarray(cell_df['Class'])
y [0:20]

# %% [markdown]
# ## Train/Test dataset

# %% [markdown]
# Okay, we split our dataset into train and test set:

# %%
#Uncomment if you use linear kernel mode
#print("\nLinear Kernel:")
print("\nRBF Kernel:")
X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.2, random_state=4)
print ('Train set:', X_train.shape,  y_train.shape)
print ('Test set:', X_test.shape,  y_test.shape)

# %% [markdown]
# <h2 id="modeling">Modeling (SVM with Scikit-learn)</h2>

# %% [markdown]
# The SVM algorithm offers a choice of kernel functions for performing its processing. Basically, mapping data into a higher dimensional space is called kernelling. The mathematical function used for the transformation is known as the kernel function, and can be of different types, such as:
# 
#     1.Linear
#     2.Polynomial
#     3.Radial basis function (RBF)
#     4.Sigmoid
# Each of these functions has its characteristics, its pros and cons, and its equation, but as there's no easy way of knowing which function performs best with any given dataset, we usually choose different functions in turn and compare the results. Let's just use the default, RBF (Radial Basis Function) for this project.

# %%
from sklearn import svm
#Uncomment if you want to change to linear kernel mode
#clf = svm.SVC(kernel='linear')
clf = svm.SVC(kernel='rbf')
clf.fit(X_train, y_train) 

# %% [markdown]
# After being fitted, the model can then be used to predict new values:

# %%
yhat = clf.predict(X_test)
yhat [0:5]

# %% [markdown]
# <h2 id="evaluation">Evaluation</h2>

# %%
from sklearn.metrics import classification_report, confusion_matrix
import itertools

# %%
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# %%
# Compute confusion matrix
cnf_matrix = confusion_matrix(y_test, yhat, labels=[2,4])
np.set_printoptions(precision=2)

print (classification_report(y_test, yhat))

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=['Benign(2)','Malignant(4)'],normalize= False,  title='Confusion matrix')
plt.show()
# %% [markdown]
# You can also easily use the __f1_score__ from sklearn library:

# %%
from sklearn.metrics import f1_score
#f1_score(y_test, yhat, average='weighted')
print("Avg F1-score: %.4f" % f1_score(y_test, yhat, average='weighted')) 

# %% [markdown]
# Lets try jaccard index for accuracy:

# %%
from sklearn.metrics import jaccard_score
#jaccard_score(y_test, yhat, average = 'macro')
print("Jaccard score: %.4f" % jaccard_score(y_test, yhat, average = 'macro'))


# %% [markdown]
# <h2 id="Using a different kernel">Using a different kernel</h2>
# We rebuild the model with a __linear__ kernel. We use __kernel='linear'__ option, when you define the svm. Let's note how the accuracy changes with the new kernel function.

# %%
'''
clf_l = svm.SVC(kernel='linear')
clf_l.fit(X_train, y_train)
yhat_l = clf_l.predict(X_test)
print("Linear Kernel:\n")
print("Avg F1-score: %.4f" % f1_score(y_test, yhat_l, average='weighted'))
print("Jaccard score: %.4f" % jaccard_score(y_test, yhat_l, average = 'macro'))
'''



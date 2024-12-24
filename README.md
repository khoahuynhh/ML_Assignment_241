# Predicting-Cancer-using-Support-Vector-Machines

SVM works by mapping data to a high-dimensional feature space so that data points can be categorized, even when the data are not otherwise linearly separable. A separator between the categories is found, then the data is transformed in such a way that the separator could be drawn as a hyperplane. Following this, characteristics of new data can be used to predict the group to which a new record should belong.

We use SVM (Support Vector Machines) to build and train a model using human cell records, and classify cells to whether the samples are benign or malignant.

![48-489805_fighting-the-fright-fight-cancer-logo](https://user-images.githubusercontent.com/65482013/83444484-163f7400-a469-11ea-9872-52cb71fd66cd.jpg)



## The Data

The project is based on a dataset that is publicly available from the [UCI Machine Learning Repository](http://mlearn.ics.uci.edu/MLRepository.html) (Asuncion and Newman, 2007). The dataset consists of several hundred human cell sample records, each of which contains the values of a set of cell characteristics. The fields in each record are:
**The values (last column) are graded from 1 to 10, with 1 being the closest to benign.**
|Field name|Description|
|--- |--- |
|ID|Clump thickness|
|Clump|Clump thickness|
|UnifSize|Uniformity of cell size|
|UnifShape|Uniformity of cell shape|
|MargAdh|Marginal adhesion|
|SingEpiSize|Single epithelial cell size|
|BareNuc|Bare nuclei|
|BlandChrom|Bland chromatin|
|NormNucl|Normal nucleoli|
|Mit|Mitoses|
|Class|Benign or malignant|
<br>

## Building the SVM model

Mapping data into a higher dimensional space is called kernelling. The SVM algorithm offers a choice of kernel functions for performing its processing. The mathematical function used for the transformation is known as the kernel function, and can be of different types, such as:

    1.Linear
    2.Polynomial
    3.Radial basis function (RBF)
    4.Sigmoid
Each of these functions has its characteristics, its pros and cons, and its equation, but as there's no easy way of knowing which function performs best with any given dataset, we usually choose different functions in turn and compare the results. Let's just use the default, RBF (Radial Basis Function) and then compare them against Linear for this project.


## Analysis

We construct the Confusion Matrix for cancer cell prediction and determine the jaccard index and F1 score to analyse our ML model.

![download](https://user-images.githubusercontent.com/65482013/83445300-59e6ad80-a46a-11ea-817d-ebcdb6255704.png)



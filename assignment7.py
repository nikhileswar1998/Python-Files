import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
# Read the following link and complete this homework. https://www.codemag.com/Article/1711091/Implementing-Machine-Learning-Using-Python-and-Scikit-learn

# Make sure to install scikit-learn and Pandas

def step1():
    """
    # Step 1: Getting the Titanic Dataset
    Return a dataframe containing the Titantic dataset from the following URL
    # URL: https://gist.githubusercontent.com/mkzia/aa4f293661dba857b8c4459c0095ac95/raw/8075037f6f7689a1786405c1bc8ea9471d3aa9c3/train.csv

    """
    # BEGIN SOLUTION
    url='https://gist.githubusercontent.com/mkzia/aa4f293661dba857b8c4459c0095ac95/raw/8075037f6f7689a1786405c1bc8ea9471d3aa9c3/train.csv'
    df=pd.read_csv(url)
    return df
    # END SOLUTION
    # return df


def step2(df):
    """
    # Step 2: Clean data
    Modify df to drop the following columns:
    PassengerId
    Name
    Ticket
    Cabin
    Hint: Just pass all the columns to the .drop() method as an array
    return dataframe
    """
    # BEGIN SOLUTION
    df2=df.drop(['PassengerId','Name','Ticket','Cabin'],axis=1)
    return df2
    # END SOLUTION
    # return df


def step3(df):
    """
    # Step 3: Drop NaNs and reindex
    You want to reindex so your index does not have missing values after you drop the NaNs. Remember, index is used 
    to access a row. Notice how many rows you dropped!
    Modify df to drop NaNs and reindex
    return dataframe
    """
    # BEGIN SOLUTION
    df3=df.dropna(axis=0,how='any').reset_index(drop=True)
    return df3
    # END SOLUTION
    # return df


def step4(df):
    """
    # Step 4: Encoding the Non-Numeric Fields
    Encode text fields to numbers
    Modify df to encode Sex and Embarked to encoded values.
    return dataframe
    """
    # BEGIN SOLUTION
    le=preprocessing.LabelEncoder()

    le.fit(df['Sex'])

    le.classes_

    df['Sex']=le.transform(df['Sex'])

    le2=preprocessing.LabelEncoder()
    le2.fit(df['Embarked'])


    df['Embarked']=le2.transform(df['Embarked'])
    return df
    # END SOLUTION
    # return df


def step5(df):
    """
    # Step 5: Making Fields Categorical
    Turn values that are not continues values into categorical values
    Modify df to make Pclass, Sex, Embarked, and Survived a categorical field
    return dataframe
    """
    # BEGIN SOLUTION
    cols=['Survived', 'Pclass', 'Sex','Embarked']
    df[cols]=df[cols].apply(lambda x: x.astype('category'))
    return df
    # END SOLUTION
    # return df


def step6(df):
    """
    1. Split dataframe into feature and label
    2. Do train and test split; USE: random_state = 1
    4. Use LogisticRegression() for classification
    3. Return accuracy and confusion matrix

    Use  metrics.confusion_matrix to calculate the confusion matrix
    # https://towardsdatascience.com/understanding-confusion-matrix-a9ad42dcfd62
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
    # IMPORTANT !!!! 
    # https://stackoverflow.com/questions/56078203/why-scikit-learn-confusion-matrix-is-reversed

    From the confusion matrix get TN, FP, FN, TP

    return --> accuracy, TN, FP, FN, TP; 
    Hint: round accuracy to 4 decimal places

    """
    # BEGIN SOLUTION
    Y=df['Survived']
    x=df.drop('Survived',axis=1)
    X_train, X_test, Y_train, Y_test = train_test_split(x, Y, test_size = 0.25, random_state = 1,stratify = df["Survived"])
    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    classifier = LogisticRegression()

    classifier.fit(X=X_train,y= Y_train)

    Y_pred = classifier.predict(X_test)

    accuracy = accuracy_score(Y_test, Y_pred)
    ac=accuracy.round(4)

    tn, fp, fn, tp = confusion_matrix(Y_test, Y_pred).ravel()
    return [ac,tn,fp,fn,tp]
    # END SOLUTION
    # return accuracy, TN, FP, FN, TP

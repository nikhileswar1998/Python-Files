import sqlite3

import numpy as np
import pandas as pd
from faker import Faker


def create_connection(db_file, delete_db=False):
    import os
    if delete_db and os.path.exists(db_file):
        os.remove(db_file)

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)

    return conn


conn = create_connection('non_normalized.db')
# sql_statement = "select * from Students;"
# df = pd.read_sql_query(sql_statement, conn)
# print(df)


def create_df_degrees(non_normalized_db_filename):
    """
    Open connection to the non-normalized database and generate a 'df_degrees' dataframe that contains only
    the degrees. See screenshot below. 
    """

    # BEGIN SOLUTION
    sql_statement='select distinct degree from students'
    df = pd.read_sql_query(sql_statement, conn)
    return df
    # END SOLUTION


def create_df_exams(non_normalized_db_filename):
    """
    Open connection to the non-normalized database and generate a 'df_exams' dataframe that contains only
    the exams. See screenshot below. Sort by exam!
    hints:
    # https://stackoverflow.com/a/16476974
    # https://stackoverflow.com/a/36108422
    """

    # BEGIN SOLUTION
    sql_statement='select distinct exams from students'
    df = pd.read_sql_query(sql_statement, conn)
    t=df['Exams'].str.split(',')
    ans=[]
    for i in t:
        for j in i:
            if j.strip() not in ans:
                ans.append(j.strip()) 
    ans1=[]
    ans2=[]
    for i in ans:
        y=i.split('(')
        ans1.append(y[0].strip())
        ans2.append(int(y[1].split(")")[0]))
    np1=[ans1,ans2]
    np2=np.array(np1).transpose()
    df1=pd.DataFrame(np2,columns=['Exam','Year']).sort_values('Exam')
    df1['Year']=pd.to_numeric(df1['Year'])
    df2=df1.reset_index(drop=True)
    return df2                   
    # END SOLUTION


def create_df_students(non_normalized_db_filename):
    """
    Open connection to the non-normalized database and generate a 'df_students' dataframe that contains the student
    first name, last name, and degree. You will need to add another StudentID column to do pandas merge.
    See screenshot below. 
    You can use the original StudentID from the table. 
    hint: use .split on the column name!
    """

    # BEGIN SOLUTION
    sql_statement='select StudentID,Name,Degree from students'
    df = pd.read_sql_query(sql_statement, conn)
    df['First_Name']=df['Name'].apply(lambda v:v.split(',')[1].strip())
    df['Last_Name']=df['Name'].apply(lambda v:v.split(',')[0])
    df.drop('Name',axis=1,inplace=True)
    new_cols=['StudentID','First_Name','Last_Name','Degree']
    df=df.reindex(columns=new_cols)
    return df
    # END SOLUTION


def create_df_studentexamscores(non_normalized_db_filename, df_students):
    """
    Open connection to the non-normalized database and generate a 'df_studentexamscores' dataframe that 
    contains StudentID, exam and score
    See screenshot below. 
    """

    # BEGIN SOLUTION
    sql_statement='select studentID,exams,scores from students'
    df = pd.read_sql_query(sql_statement, conn)

    df['Exam']=df['Exams'].str.split(',')
    df['Score']=df['Scores'].str.split(',')
    df.drop('Exams',axis=1,inplace=True)
    df.drop('Scores',axis=1,inplace=True)

    df3=df.explode(['Exam','Score'])
    df3['Exam']=df3['Exam'].str.strip()


    df3['Exam']=df3['Exam'].str.split(' ')
    df3['Score']=pd.to_numeric(df3['Score'])
    df3['Exam']=df3['Exam'].apply(lambda v:v[0].strip())
    df3=df3.reset_index(drop=True)
    return df3
    # END SOLUTION


def ex1(df_exams):
    """
    return df_exams sorted by year
    """
    # BEGIN SOLUTION
    df_exams=df_exams.sort_values('Year').reset_index(drop=True)
    # END SOLUTION
    return df_exams


def ex2(df_students):
    """
    return a df frame with the degree count
    # NOTE -- rename name the degree column to Count!!!
    """
    # BEGIN SOLUTION
    df2=df_students.groupby(['Degree'])['Degree'].agg('count')
    data=[]
    for row in df2:
        data.append(row)
    index=['graduate','undergraduate']
    df3=pd.DataFrame(data={'Count':data},index=index).sort_values('Count',ascending=False)
    df3.columns=[['Count']]
    # END SOLUTION
    return df3


def ex3(df_studentexamscores, df_exams):
    """
    return a datafram that merges df_studentexamscores and df_exams and finds the average of the exams. Sort
    the average in descending order. See screenshot below of the output. You have to fix up the column/index names.
    Hints:
    # https://stackoverflow.com/a/45451905
    # https://stackoverflow.com/a/11346337
    # round to two decimal places
    """

    # BEGIN SOLUTION
    
    df_1=df_studentexamscores.groupby(['Exam']).mean().round(2)['Score']
    df3=pd.merge(df_exams,df_1,how='inner',on='Exam').sort_values('Score',ascending=False)
    df3['average']=df3['Score']
    df3.drop('Score',axis=1,inplace=True)
    df3=df3.reset_index(drop=True)
    df3=df3.set_index('Exam')
    df3['Year']=df3['Year'].astype('int32')    
    # END SOLUTION
    return df3


def ex4(df_studentexamscores, df_students):
    """
    return a datafram that merges df_studentexamscores and df_exams and finds the average of the degrees. Sort
    the average in descending order. See screenshot below of the output. You have to fix up the column/index names.
    Hints:
    # https://stackoverflow.com/a/45451905
    # https://stackoverflow.com/a/11346337
    # round to two decimal places
    """

    # BEGIN SOLUTION
    df3=pd.merge(df_studentexamscores,df_students,how='inner',on='StudentID')
    df5=pd.DataFrame({'Average':df3.groupby(['Degree']).mean().round(2)['Score']})
    # END SOLUTION
    return df5


def ex5(df_studentexamscores, df_students):
    """
    merge df_studentexamscores and df_students to produce the output below. The output shows the average of the top 
    10 students in descending order. 
    Hint: https://stackoverflow.com/a/20491748
    round to two decimal places

    """

    # BEGIN SOLUTION
    df5=pd.DataFrame({'average':df_studentexamscores.groupby(['StudentID']).mean().round(2)['Score']}).sort_values('average',ascending=False).reset_index()
    df6=df5.iloc[:10]
    df7=pd.merge(df6,df_students,how='inner',on='StudentID')
    df7.drop('StudentID',axis=1,inplace=True)
    df8=df7.reindex(columns=['First_Name','Last_Name','Degree','average'])
    return df8
    # END SOLUTION


# DO NOT MODIFY THIS CELL OR THE SEED

# THIS CELL IMPORTS ALL THE LIBRARIES YOU NEED!!!


np.random.seed(0)
fake = Faker()
Faker.seed(0)


def part2_step1():

    # ---- DO NOT CHANGE
    np.random.seed(0)
    fake = Faker()
    Faker.seed(0)
    # ---- DO NOT CHANGE

    # BEGIN SOLUTION
    names=[]
    for i in range(100):
        names.append(fake.name())
    first=[]
    last=[]
    username=[]
    for i in range(100):
        first.append(names[i].split(' ')[0])
        last.append(names[i].split(' ',maxsplit=1)[1])
        username.append(names[i].split(' ')[0][:2].lower()+str(np.random.randint(1000,9999)))        
    df=pd.DataFrame({'username':username,'first_name':first,'last_name':last})
    return df
    # END SOLUTION
    


def part2_step2():

    # ---- DO NOT CHANGE
    np.random.seed(0)
    # ---- DO NOT CHANGE

    # BEGIN SOLUTION
    ans=np.random.normal([35,75,25,45,45,75,25,45,35],[9,15,7,10,5,20,8,9,10],size=(100,9))

    out=np.clip(ans,a_min=[0,0,0,0,0,0,0,0,0],a_max=[50,100,40,60,50,100,50,60,50])

    df=pd.DataFrame(out)

    df2=df.round()

    df2.columns=['Hw1','Hw2','Hw3','Hw4','Hw5','Exam1','Exam2','Exam3','Exam4']
    return df2
    # END SOLUTION


def part2_step3(df2_scores):
    # BEGIN SOLUTION
    df3=df2_scores.describe()

    df4=df3.loc[['mean','std'],]

    df4.loc['mean_theoretical']=[35,75,25,45,45,75,25,45,35]

    df4.loc['std_theoretical']=[9,15,7,10,5,20,8,9,10]

    df4.loc['abs_mean_diff']=df4.loc['mean_theoretical']-df4.loc['mean']

    df4.loc['abs_std_diff']=df4.loc['std_theoretical']-df4.loc['std']

    df5=df4.transpose().round(2).abs()
    df5['mean_theoretical']=df5['mean_theoretical'].astype('int64')
    df5['std_theoretical']=df5['std_theoretical'].astype('int64')
    return df5
    # END SOLUTION


def part2_step4(df2_students, df2_scores):
    # BEGIN SOLUTION
    df2=df2_scores
    df2['Hw1']=df2['Hw1']*100/50
    df2['Hw3']=(df2['Hw3']/40)*100
    df2['Hw3']=df2['Hw3'].round()
    df2['Hw4']=df2['Hw4']*100/60
    df2['Hw4']=df2['Hw4'].round()
    df2['Hw5']=df2['Hw5']*100/50
    df2['Exam2']=df2['Exam2']*100/50
    df2['Exam3']=df2['Exam3']*100/60
    df2['Exam3']=df2['Exam3'].round()
    df2['Exam4']=df2['Exam4']*100/50
    df_4=pd.concat([df2_students,df2],axis=1)
    return df_4
    # END SOLUTION


def part2_step5():
    # BEGIN SOLUTION
    df_read_5=pd.read_csv('part2_step5-input.csv')

    df = df_read_5.apply(lambda row:row.astype(str).str.contains('AI_ISSUE').sum(),axis=1)

    df_read_5['AI_Count']=df

    df2=df_read_5[df_read_5['AI_Count'].apply(lambda l:l!=0)]

    df2=df2.reset_index(drop=True)


    df3=df2.drop(['Hw1','Hw2','Hw3','Hw4','Hw5','Exam1','Exam2','Exam3','Exam4'],axis=1)
    return df3
    # END SOLUTION


def part2_step6():
    # BEGIN SOLUTION
    data=pd.read_csv("part2_step6.csv", index_col=0)
    return data
    # END SOLUTION

from http.client import BAD_REQUEST
from re import L


def ex1(password):
    # In this exercise you will complete this function to determine whether or not
    # a password is good. We will define a good password to be a one that is at least
    # 8 characters long and contains at least one uppercase letter, at least one lowercase
    # letter, at least one number, and at least one of the following special characters (!, @, #, $, ^).
    # This function should return True if the password
    # passed to it as its only parameter is good. Otherwise it should return False.
    #
    # input: password (str)
    # output: True or False (bool)
    # BEGIN SOLUTION
    A=['!','@','#','$','^']
    if password.islower() or password.isupper() or password.isalnum():
        return False;
    if(password.lower()==password):
        return False;
    for a in A :
        if a in password:
            return True;
    return False;    
    
    # END SOLUTION


def ex2(sentence):
    # Complete this function to calculate the average
    # word length in a sentence
    # Input: sentence
    # Output: average word length in sentence
    # Hint: count punctuations with whatever word they are `touching`
    # Hint: round the average to two decimal places

    # BEGIN SOLUTION
    list1=sentence.strip().split(" ")
    sum=0
    for el in list1:
        sum+=len(el)
    mean=sum/len(list1)
    m=f'{mean:.2f}'
    return float(m);    
    
    # END SOLUTION


def ex3(filename):
    # Complete this function to count the number of lines, words, and chars in a file.
    # Input: filename
    # Output: a tuple with line count, word count, and char count -- in this order

    # BEGIN SOLUTION
    lines=0
    words=0
    chars=0
    spaces=0
    with open(filename) as f:
        for line in f:
            lines+=1
            spaces+=line.count(' ')            
            rows=line.strip().split()
            words+=len(rows)
            chars+=len(line)
    # words=words-4
    # chars=chars+spaces+(lines-1)            
    return (lines,words,chars);                  
    # END SOLUTION
def ex4(apr):
    # Complete this function to use a while loop to determine how long it takes for an investment
    # to double at a given interest rate. The input to this function, apr, is the annualized interest rate
    # and the output is the number of years it takes an investment to double. Note: The amount of the initial
    # investment (principal) does not matter; you can use $1.
    # Hint: principal is the amount of money being invested.
    # apr is the annual percentage rate expressed as a decimal number.
    # Relationship: value after one year is given by principal * (1+ apr)

    # BEGIN SOLUTION
    inv=1
    ret=1
    count=1
    while(ret<2):
        ret=ret*(1+apr)
        count+=1
    return count-1;    
    
    
    
    # END SOLUTION


def ex5(n):
    # Complete this function to return the number of steps taken to reach 1 in
    # the Collatz sequence (https://en.wikipedia.org/wiki/Collatz_conjecture) given in

    # BEGIN SOLUTION
    count=0
    while(n>1):
        if(n%2==0):
            n=n/2
        else:
            n=3*n+1
        count+=1
    return count;            
    # END SOLUTION


def ex6(n):
    # A positive whole number > 2 is prime if no number between 2 and sqrt(n)
    # (include) evenly divides n. Write a program that accepts a value of n as
    # input and determine if the value is prime. If n is not prime, your program should
    # return False (boolean) as soon as it finds a value that evenly divides n.
    # Hint: if number is 2, return False

    import math

    # BEGIN SOLUTION
    maxim=int(math.sqrt(n))
    if(n==2):
        return False;
    for i in range(2,maxim+1):
        if(n%i==0):
            return False;
    return True;    
    # END SOLUTION


def ex7(n):
    # Complete this function to return all the primes as a list less than or equal to n
    # Input: n
    # Output: a list of numbers
    # hint use ex6

    # BEGIN SOLUTION
    list1=[]
    for i in range(2,n+1):
        if(ex6(i)):
            list1.append(i)
    return list1;        
    # END SOLUTION


def ex8(m, n):
    # Complete this function to determine the greatest common divisor (GCD).
    # The GCD of two values can be computed using Euclid's algorithm. Starting with the values
    # m and n, we repeatedly apply the formula: n, m = m, n%m until m is 0. At this point, n is the GCD
    # of the original m and n.
    # Inputs: m and n which are both natural numbers
    # Output: gcd

    # BEGIN SOLUTION
    while(n):
        m,n=n,m%n
    return m;    
    
    # END SOLUTION


def ex9(filename):
    # Complete this function to read grades from a file and determine the student with the highest average
    # test grades and the lowest average test grades.
    # Input: filename
    # Output: a tuple containing four elements: name of student with highest average, their average,
    # name of the student with the lowest test grade, and their average. Example ('Student1', 99.50, 'Student5', 65.50)
    # Hint: Round to two decimal places

    # BEGIN SOLUTION
    students=[]
    mean=[]
    with open(filename) as f:
        for line in f:
            if not line.strip():
                continue
            rows=len(line.strip().split(","))
            sum=0
            for i in range(rows):
                if(i==0):
                    students.append(line.strip().split(",")[i])
                else :
                    line.strip().split(",")
                    sum+=int(line.strip().split(",")[i])
            mean.append(sum/(rows-1))
    maxi=mean.index(max(mean))
    mini=mean.index(min(mean))
    maximum=f'{max(mean):.2f}'
    minumum=f'{min(mean):.2f}'
    return(students[maxi],float(maximum),students[mini],float(minumum));                
                      
ex9('ex9_data.txt')            
    # END SOLUTION


def ex10(data, num_outliers):
    # When analyzing data collected as a part of a science experiment it
    # may be desirable to remove the most extreme values before performing
    # other calculations. Complete this function which takes a list of
    # values and an non-negative integer, num_outliers, as its parameters.
    # The function should create a new copy of the list with the num_outliers
    # largest elements and the num_outliers smallest elements removed.
    # Then it should return teh new copy of the list as the function's only
    # result. The order of the elements in the returned list does not have to
    # match the order of the elements in the original list.
    # input1: data (list)
    # input2: num_outliers (int)

    # output: list

    # BEGIN SOLUTION
    while(num_outliers):
        data.remove(max(data))
        data.remove(min(data))
        num_outliers-=1
    return sorted(data);
    # END SOLUTION


def ex11(words):
    # Complete this function to remove duplicates from the words list using a loop
    # input: words (list)
    # output: a list without duplicates
    # MUST USE loop and NOT set!
    # Preserve order

    # BEGIN SOLUTION
    res=[]
    [res.append(x) for x in words if x not in res] 
    return res;
              
                
            
    
    # END SOLUTION


def ex12(n):
    # A proper divisor ofa  positive integer, n, is a positive integer less than n which divides
    # evenly into n. Complete this function to compute all the proper divisors of a positive
    # integer. The integer is passed to this function as the only parameter. The function will
    # return a list of containing all of the proper divisors as its only result.

    # input: n (int)
    # output: list

    # BEGIN SOLUTION
    a=int(n/2)
    list1=[]
    for i in range(1,a+1):
        if(n%i==0):
            list1.append(i)
    return list1;        
    
    # END SOLUTION


def ex13(n):
    # An integer, n, is said to be perfect when the sum of all of the proper divisors
    # of n is equal to n. For example, 28 is a perfect number because its proper divisors
    # are 1, 2, 4, 7, and 14 = 28
    # Complete this function to determine if a the number a perfect number or not.
    # input: n (int)
    # output: True or False (bool)

    # BEGIN SOLUTION
    list1=ex12(n)
    if(sum(list1)==n):
        return True;
    else:
        return False;
    # END SOLUTION


def ex14(points):
    # Complete this function to determine the best line.
    # https://www.varsitytutors.com/hotmath/hotmath_help/topics/line-of-best-fit
    # input: points (list of tuples contain x, y values)
    # output: (m, b) # round both values to two decimal places

    # BEGIN SOLUTION
    X=[]
    Y=[]
    for i in points:
        X.append(i[0])
        Y.append(i[1])
    mean_x=sum(X)/len(X)
    mean_y=sum(Y)/len(Y)
    num=0
    dem=0
    for i in range(len(points)):
        num+=(X[i]-mean_x)*(Y[i]-mean_y)
        dem+=(X[i]-mean_x)**2
    m=num/dem  
    m1=f'{m:.2f}'      
    b=mean_y-(m*mean_x)
    b1=f'{b:.2f}'
    return (float(m1),float(b1));
    
    # END SOLUTION


def ex15(title, header, data, filename):
    # This problem is hard.
    # Open up ex15_*_solution.txt and look at the output based on the input parameters, which
    # can be found in the test_assignment4.py file
    # Function inputs: 
    # title -- title of the table -- a string
    # header -- header of the table  -- a tuple
    # data -- rows of data, which is a tuple of tuples
    # filename -- name of file to write the table to
    # Your job is to create the table in the file and write it to `filename`
    # Note that you need to dynamically figure out the width of each column based on 
    # maximum possible length based on the header and data. This is what makes this problem hard. 
    # Once you have determined the maximum length of each column, make sure to pad it with 1 space
    # to the right and left. Center align all the values. 
    # OUTPUT: you are writing the table to a file

    # BEGIN SOLUTION
    
    B=[]
    len1=len(header)
    for i in range(len1):
        A=[]
        for j in range(len(data)):
            A.append(len(str(data[j][i])))
        A.append(len(header[i]))                              
        B.append(max(A))
    
    total=sum(B)+(2*len1)+(len1-1)
    line='+'
    blank=""
    for i in range(len1):
        x=B[i]
        line+='-'*(B[i]+2)+'+'
    
    row=[]

    Header=f'|{header[0]:^{B[0]+2}s}|'
    for i in range(1,len1):
        Header+=f'{header[i]:^{B[i]+2}s}|'
    string=''
    for i in range(len(data)):
        for j in range(len1):
            if(j==0):
                string+=f'|{str(data[i][j]):^{B[j]+2}s}|'
            else:
                string+=f'{str(data[i][j]):^{B[j]+2}s}|'    
        if(i!=len(data)-1):
            string+='\n'    
            
           
    Title='|'+f'{title:^{total}s}'+'|'
    with open(filename,"w") as f:
        string='-'+'-'*(total)+'-'+'\n'+Title+'\n'+line+'\n'+Header+'\n'+line+'\n'+string+'\n'+line
        f.write(string)       

title = 'Student Grades'
header = ('Student ID', 'Test1', 'Test2',
                  'Midterm', 'Quizzes', 'Final')
data = (
            (2014255, 55, 78, 63, 50, 80),
            (2014301, 83, 45, 88, 52, 47),
            (2014023, 75, 70, 42, 74, 63),
            (2014155, 67, 87, 54, 87, 86),
        )               
        
ex15(title,header,data,"ex15_3.txt")                
       
    
    
    # END SOLUTION

def ex16(lst):
    # Complete this function to use list comprehension to return all values from `lst`
    # that are a multiple of 3 or 4. Just complete the list comprehension below.
    # input: `lst` of numbers
    # output: a list of numbers
    
    # BEGIN SOLUTION
    # complete the following line!
    # return [for ele in lst] #complete this line!
    return [ele for ele in lst if (ele%3==0 or ele%4==0)];
     # remove this line
    # END SOLUTION



def ex17(lst):
    # Complete this function to use list comprehension to multiple all numbers
    # in the list by 3 if it is even or 5 if its odd
    # input: `lst` of numbers
    # output: a list of numbers


    # BEGIN SOLUTION
    # complete the following line!
    # return [for ele in lst] #complete this line!
    return [3*lst[i] if(i%2==0) else 5*lst[i] for i in range(len(lst))];
     # remove this line
    # END SOLUTION


def ex18(input_dict, test_value):
    # Complete this function to find all the keys in a dictionary that map to the input value. 
    # input1: input_dict (dict)
    # input2: test_value
    # output: list of keys

    # BEGIN SOLUTION
    return [key for key,value in input_dict.items() if(value==test_value)];
    
    # END SOLUTION


def ex19(filename):
    """
    In this problem you will read data from a file and perform a simple mathematical operation on each data point. 
    Each line is supposed to contain a floating point number.
    But what you will observe is that some lines might have erroneous entries. 
    You need to ignore those lines (Hint: Use Exception handling).

    The idea is to implement a function which reads in a file and computes the median 
    of the numbers and returns the output. You may use the inbuilt function sort when computing the median.

    DO NOT USE ANY INBUILT OR OTHER FUNCTION TO DIRECTLY COMPUTE MEDIAN

    The files
    """
    ### BEGIN SOLUTION
    list=[]
    with open(filename,'r') as file:
        for line in file:
            try:
                list.append(float(line))
            except:
                continue

    try:
        if len(list)==0:
            raise ValueError("The file does not have any valid number to compute the median")
        elif len(list)%2==0:
            list.sort()
            return (list[int(len(list)/2)]+list[int((len(list)/2))-1])/2
        elif len(list)%2==1:
            list.sort()
            return list[int((len(list)+1)/2)-1]
    except ValueError as e:
        return "The file does not have any valid number to compute the median"        
                    
    
    ### END SOLUTION
print(ex19('ex19_data_3.txt'))


def simulateProblem():
    """
    See instructions in exercise_19_instructions.html file
    """
    ### BEGIN SOLUTION
    import random
    x=random.randint(0,1)
    list1=['sticking','switching']
    y=random.choice(list1)
    if(y=='sticking'):
        if(x==0):
            return (False,False)
        if(x==1):
            return (True,True)
    if(y=='switching'):
        if(x==1):
            return (False,True)
        if(x==0):
            return (True,False)    
    #randomly selecting the sticking and switch for y as y=0 
    
    ### END SOLUTION


def ex20():
    """
    The function calls the simulateProblem() 10000 times to figure out 
    the empirical (observed) probability of gaining more money when switching 
    and gaining more money when sticking to the original choice.
    Return the probability of win due to sticking and win due to switching
    """
    ### BEGIN SOLUTION
    
    win_due_to_sticking=0
    win_due_to_switching=0
    for i in range(1000):
        ans=simulateProblem()
        if(ans[0]==True and ans[1]==True):
            win_due_to_sticking+=1
        elif(ans[0]==True and ans[1]==False):
            win_due_to_switching+=1
    return (win_due_to_sticking/1000,win_due_to_switching/1000);            
        
    ### END SOLUTION    

from multiprocessing.sharedctypes import Value


class IteratorClass:
    # Complete this class! It takes in three inputs when initializing.
    # input#1 x -- is a sequence, either a list or a tuple. Raise a ValueError if it is not a list or a tuple
    # input#2 y -- is a sequence, either a list or a tuple. Raise a ValueError if it is not a list or a tuple
    # input#3 operator -- is a string that can either be 'add', 'sub', 'mul', 'div' -- If the specified operator
    # is not one of these, raise a ValueError.

    # Complete the class by writing functions that will turn it into an iterator class.
    # https://www.programiz.com/python-programming/methods/built-in/iter
    # The purpose of the class is to take two lists(x and y), apply the specified operator and return the output
    # as an iterator, meaning you can do "for ele in IteratorClass(x,y,'add')"
    # NOTE: For the / operator, round to two decimal places
    # Raise ValueError when the length is not the same for both inputs
    # Raise ValueError when the operator is not add, sub, mul, or div.

    # BEGIN SOLUTION
    def __init__(self,x,y,z) :
        self.iter=0
        if((type(x) not in [list,tuple]) or (type(y)not in [list,tuple])):
            raise ValueError
        if(z not in['add','sub','mul','div']):
            raise ValueError
        if(len(x)!=len(y)):
            raise ValueError
        if(z=='add'):
            self.x= [x[i]+y[i] for i in range(len(x))]
        if(z=='sub'):
            self.x= [x[i]-y[i] for i in range(len(x))]
        if(z=='mul'):
            self.x= [x[i]*y[i] for i in range(len(x))]
        if(z=='div'):
            ans=[x[i]/y[i] for i in range(len(x))]
            a1=[float(f'{a:.2f}') for a in ans]
            self.x= a1   
    def __iter__(self):
        return self
    def __next__(self):
        self.iter+=1
        if(self.iter<=len(self.x)):
            return self.x[self.iter-1]
        else:
            raise StopIteration                 
            
    # END SOLUTION


class ListV2:
    # Complete this class to fulfill the following requirement
    # 1) The class only takes one input argument which is a list or a tuple;
    #    Raise ValueError if the input is not a list or tuple
    # 2) The class overload loads +,-,*,/ and returns a ListV2 object as the result
    # 3) The class can handle +,-,*,/ for both list and int/float, meaning the thing to the right of the operator
    #    can be a sequence or a number;
    # 4) The class is an iterator
    # HINT: Study the assert statements in the test file to understand how this class is being used and reverse engineer it!
    # NOTE: For the / operator, round to two decimal places

    # BEGIN SOLUTION
    def __init__(self,x):
        self.iter=0
        self.x=x
        if(type(x) not in [list, tuple]):
                raise ValueError
    def __add__(self,other):
        if(type(other)in [int ,float]):
            return [self.x[i]+other for i in range(len(self.x))]
        if(type(other)in [list,tuple]):
            return [self.x[i]+other[i] for i in range(len(self.x))]        
        if(type(other.x)== list):
            return iter(ListV2([self.x[i]+other.x[i] for i in range(len(self.x))]))


        
    def __sub__(self,other):
        if(type(other)in [int ,float]):
            return [self.x[i]-other for i in range(len(self.x))]
        if(type(other)in [list,tuple]):
            return [self.x[i]-other[i] for i in range(len(self.x))]                 
        if(type(other.x)== list):
            return iter(ListV2([self.x[i]-other.x[i] for i in range(len(self.x))]))

       
    def __mul__(self,other):
        if(type(other)in [int ,float]):
            return [self.x[i]*other for i in range(len(self.x))]
        if(type(other)in [list,tuple]):
            return [self.x[i]*other[i] for i in range(len(self.x))]
        if(type(other.x)== list):
            return iter(ListV2([self.x[i]*other.x[i] for i in range(len(self.x))]))


                
    def __truediv__(self,other):
        if(type(other)in [int ,float]):
            ans=[self.x[i]/other for i in range(len(self.x))]
            return [float(f'{ele:.2f}') for ele in ans] 
        if(type(other)in [list,tuple]):
            ans= [self.x[i]/other[i] for i in range(len(self.x))]
            return [float(f'{ele:.2f}') for ele in ans]
        if(type(other.x)== list):
            ans= [self.x[i]/other.x[i] for i in range(len(self.x))]
            return iter(ListV2([float(f'{ele:.2f}') for ele in ans]))
    
    def __repr__(self):
        return str(self.x)
    
    def __iter__(self):
        return self
    def __next__(self):
        self.iter+=1
        if(self.iter<=len(self.x)):
            return self.x[self.iter-1]
        else:
            raise StopIteration 

      

            
            
    
    # END SOLUTION


def ex3(filename):
    # Complete this function to read grades from `filename` and find the minimum
    # student test averages. File has student_name, test1_score, test2_score,
    # test3_score, test4_score, test5_score. This function must use a lambda
    # function and use the min() function to find the student with the minimum
    # test average. The input to the min function should be
    # a list of lines. Ex. ['student1,33,34,35,36,45', 'student2,33,34,35,36,75']
    # input filename
    # output: (lambda_func, line_with_min_student) -- example (lambda_func, 'student1,33,34,35,36,45')

    # BEGIN SOLUTION
    lines=[]
    with open(filename,'r') as f:
        for line in f:
            if(line.strip()):
                lines.append(line)
        mini=min(lines,key=lambda line:sum([float(ele)for ele in line.split(',')[1:]]))
        return (lambda line:sum([float(ele) for ele in line.split(',')[1:] if line.strip()]),mini.strip()) 
ex3('ex3_data.txt')              
    # END SOLUTION

def grade(avg):
    avg=round(avg)
    if(avg>=90):
        return ' A'
    elif(90 > avg >=80):
        return ' B'
    elif(80 > avg >=70):
        return ' C'
    elif(65<=avg<70):
        return ' D'

def ex4(filename):
    # Complete this function to read grades from `filename` and map the test average to letter
    # grades using map and lambda. File has student_name, test1_score, test2_score,
    # test3_score, test4_score, test5_score. This function must use a lambda
    # function and map() function.
    # The input to the map function should be
    # a list of lines. Ex. ['student1,73,74,75,76,75', ...]. Output is a list of strings in the format
    # studentname: Letter Grade -- 'student1: C'
    # input filename
    # output: (lambda_func, list_of_studentname_and_lettergrade) -- example (lambda_func, ['student1: C', ...])

    # Use this average to do the grade mapping. Round the average grade.
    # D = 65<=average<70
    # C = 70<=average<80
    # B = 80<=average<90
    # A = 90<=average
    # Define a function that takes in a number grade and returns the letter grade and use
    # it inside the lambda function.
    # HINT: create a function

    # BEGIN SOLUTION
    lines=[]
    with open(filename,'r') as f:
        for line in f:
            if(line.strip()):
                lines.append(line)
    lam_fun= lambda line:line.split(',')[0]+':'+grade(sum([float(ele)for ele in line.split(',')[1:]])/5)
    ans=list(map(lambda line:line.split(',')[0]+':'+grade(sum([float(ele)for ele in line.split(',')[1:]])/5),lines))
    return (lam_fun,ans)
    # END SOLUTION


def ex5(filename):
    # Complete this function to sort a list of dictionary by 'test3'
    # return the lambda function and the sorted list of dictionaries
    # Use the following code to read JSON file

    import json
    with open(filename) as infile:
        grades = json.load(infile)
        ans=sorted(grades,key=lambda x:float(x['test3']))
        return (lambda x:float(x['test3']),ans)
    # BEGIN SOLUTION
    pass
    # END SOLUTION

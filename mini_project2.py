### Utility Functions
import pandas as pd
import sqlite3
from sqlite3 import Error
import datetime

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


def create_table(conn, create_table_sql, drop_table_name=None):
    
    if drop_table_name: # You can optionally pass drop_table_name to drop the table. 
        try:
            c = conn.cursor()
            c.execute("""DROP TABLE IF EXISTS %s""" % (drop_table_name))
        except Error as e:
            print(e)
    
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
def execute_sql_statement(sql_statement, conn):
    cur = conn.cursor()
    cur.execute(sql_statement)

    rows = cur.fetchall()

    return rows
def insert_regions(conn,values):
    sql = """INSERT INTO Region(RegionId, Region)
                VALUES(?, ?)"""
    cur = conn.cursor()
    cur.executemany(sql, values)
    return cur.lastrowid
def insert_countries(conn,values):
    sql='''INSERT INTO country(countryid,country,regionid)
            values(?,?,?)
    '''
    cur = conn.cursor()
    cur.executemany(sql, values)
    return cur.lastrowid

def step1_create_region_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None
    
    ### BEGIN SOLUTION
    
    conn_n=create_connection(normalized_database_filename)
    create_table_region_sql='''create table [Region] (
        [RegionID] Integer Primary Key Not Null,
        [Region] Text not null
    )
    '''
    regions=[]
    header=[]
    with open(data_filename,'r') as f:
        for line in f:
            if not header:
                header=line.split('\t')
                continue
            val=line.split('\t')
            if val[4] not in regions:
                regions.append(val[4])
    regions.sort()
    regions1=[]
    j=0
    for i in regions:
        j+=1
        regions1.append((j,i))                
    with conn_n:
        create_table(conn_n,create_table_region_sql,'Region')
        insert_regions(conn_n,regions1)
        
        
        
        
    ### END SOLUTION

def step2_create_region_to_regionid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    conn_n=create_connection(normalized_database_filename)
    sql ='select * from Region order by regionid'
    regions=execute_sql_statement(sql,conn_n)
    dict1={i[1]:i[0] for i in regions}
    return dict1
    

    ### END SOLUTION


def step3_create_country_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None
    
    ### BEGIN SOLUTION
    conn_n=create_connection(normalized_database_filename)
    create_table_country_sql='''create table [Country] (
        [CountryID] Integer Primary Key Not Null,
        [Country] Text not null,
        [RegionID] Integer not null,
        Foreign key (RegionID) references Region(RegionID)
    )
    '''
    header=[]
    countries=[]
    regions=[]
    with open(data_filename) as f:
        for line in f:
            if not header:
                header=line.split('\t')
                continue
            split=line.split('\t')
            if split[3] not in countries:
                countries.append(split[3])
                regions.append(split[4])
    dict1=dict(zip(countries,regions))  
    dict1=dict(sorted(dict1.items()))
    dict2=step2_create_region_to_regionid_dictionary(normalized_database_filename)          
    countries1=[]
    i=0
    for k,v in dict1.items():
        i+=1
        countries1.append((i,k,dict2[v]))
                    
                
    with conn_n:
        create_table(conn_n,create_table_country_sql,'Country')
        insert_countries(conn_n,countries1)           
            
         
    ### END SOLUTION


def step4_create_country_to_countryid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    conn_n=create_connection(normalized_database_filename)
    sql ='select * from country order by countryid'
    countries=execute_sql_statement(sql,conn_n)
    dict1={i[1]:i[0] for i in countries}
    return dict1

    ### END SOLUTION

def insert_customers(conn,values):
    sql='''INSERT INTO customer
            values(?,?,?,?,?,?)
    '''
    cur = conn.cursor()
    cur.executemany(sql, values)
    return cur.lastrowid        
        
def step5_create_customer_table(data_filename, normalized_database_filename):

    ### BEGIN SOLUTION
    
    conn_n=create_connection(normalized_database_filename)
    create_table_customer_sql='''create table [Customer] (
        [CustomerID] Integer Primary Key Not Null,
        [FirstName] Text not null,
        [LastName] Text not null,
        [Address] text not null,
        [City]  text not null,
        [CountryID] Integer not null,
        Foreign key (CountryID) references Country(CountryID)
    )
    '''
    header=[]
    customers=[]
    finalcustomers=[]
    dict2=step4_create_country_to_countryid_dictionary(normalized_database_filename)
    i=0
    with open(data_filename) as f:
        for line in f:
            if not header:
                header=line.split(',')
                continue
            split=line.split('\t')
            if (len(split[0].split(' '))==3):
                customers.append([split[0].split(' ')[0],split[0].split(' ')[1]+' '+split[0].split(' ')[2],split[1],split[2],dict2[split[3]]])
            else:
                customers.append([split[0].split(' ')[0],split[0].split(' ')[1],split[1],split[2],dict2[split[3]]])
    customers1=sorted(customers,key=lambda l:l[0]+l[1])
    for k in customers1:
        i+=1
        a=[i]
        finalcustomers.append(tuple([i]+k))
    with conn_n:
        create_table(conn_n,create_table_customer_sql,'Customer')
        insert_customers(conn_n,finalcustomers) 

    ### END SOLUTION


def step6_create_customer_to_customerid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    conn_n=create_connection(normalized_database_filename)
    sql ='select * from customer order by customerid'
    customers=execute_sql_statement(sql,conn_n)
    dict1={i[1]+' '+i[2]:i[0] for i in customers}
    return dict1    
    

    ### END SOLUTION
def insert_productcategories(conn,values):
    sql='''INSERT INTO productcategory
            values(?,?,?)
    '''
    cur = conn.cursor()
    cur.executemany(sql, values)
    return cur.lastrowid 
        
def step7_create_productcategory_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None

    
    ### BEGIN SOLUTION
    conn_n=create_connection(normalized_database_filename)
    create_table_productcategory_sql='''create table [productcategory] (
        [ProductCategoryID] Integer Primary Key Not Null,
        [ProductCategory] Text not null,
        [ProductCategoryDescription] Text not null
    )
    '''
    header=[]
    productcategories=[]
    dict2={}
    x='"'
    i=0
    with open(data_filename) as f:
        for line in f:
            if not header:
                header=line.split('\t')
                continue
            x=line.split('\t')[6]
            split1=x.split(';')
            y=line.split('\t')[7]
            split2=y.split(';')
            dict1=dict(zip(split1,split2))
            for k,v in dict1.items():
                if k not in dict2.keys():
                    dict2[k]=v
    dict2=dict(sorted(dict2.items()))        
    for k,v in dict2.items():
        i+=1
        productcategories.append((i,k,v))
                        
            # insert if split not in productcategories    
             
    with conn_n:
        create_table(conn_n,create_table_productcategory_sql,"productcategory")
        insert_productcategories(conn_n,productcategories)
                       
   
    ### END SOLUTION

def step8_create_productcategory_to_productcategoryid_dictionary(normalized_database_filename):
    
    
    ### BEGIN SOLUTION
    conn_n=create_connection(normalized_database_filename)
    sql ='select * from productcategory order by productcategoryid'
    productcategories=execute_sql_statement(sql,conn_n)
    dict1={i[1]:i[0] for i in productcategories}
    return dict1 

    ### END SOLUTION

def insert_products(conn,values):
    sql='''INSERT INTO product
            values(?,?,?,?)
    '''
    cur = conn.cursor()
    cur.executemany(sql, values)
    return cur.lastrowid        

def step9_create_product_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None

    
    ### BEGIN SOLUTION
    
    conn_n=create_connection(normalized_database_filename)
    create_table_product_sql='''create table [product] (
        [ProductID] Integer Primary Key Not Null,
        [ProductName] Text not null,
        [ProductUnitPrice] Real not null,
        [ProductCategoryID] Integer not null,
        Foreign key (ProductCategoryID) references productcategory(ProductCategoryID)
    )
    '''    
    header=[]
    j=0
    product=[]
    dict3=step8_create_productcategory_to_productcategoryid_dictionary(normalized_database_filename)
    with open(data_filename) as f:
        for line in f:
            if not header:
                header=line.split("\t")
                continue
            x=line.split('\t')[5]
            split1=x.split(';')
            y=line.split('\t')[6]
            split2=y.split(';')
            z=line.split('\t')[8]
            split3=z.split(';')
            split3=[float(ele) for ele in split3]
            k=tuple(set(zip(split1,split3,split2)))
            k=sorted(k,key=lambda l:l[0])
        for ele in k:
            j+=1
            product.append((j,ele[0],ele[1],dict3[ele[2]]))
                        
            # insert if split not in productcategories    
             
    with conn_n:
        create_table(conn_n,create_table_product_sql,"product")
        insert_products(conn_n,product)
            
    
   
    ### END SOLUTION


def step10_create_product_to_productid_dictionary(normalized_database_filename):
    
    ### BEGIN SOLUTION
    conn_n=create_connection(normalized_database_filename)
    sql ='select * from product order by productid'
    products=execute_sql_statement(sql,conn_n)
    dict1={i[1]:i[0] for i in products}
    return dict1     

    ### END SOLUTION
def insert_orderdetails(conn,values):
    sql='''INSERT INTO orderdetail
            values(?,?,?,?,?)
    '''
    cur = conn.cursor()
    cur.executemany(sql, values)
    return cur.lastrowid        

def step11_create_orderdetail_table(data_filename, normalized_database_filename):
    # Inputs: Name of the data and normalized database filename
    # Output: None

    
    ### BEGIN SOLUTION
    conn_n=create_connection(normalized_database_filename)
    create_table_orderdetail_sql='''create table [Orderdetail] (
        [OrderID] Integer Primary Key Not Null,
        [CustomerID] Integer not null,
        [ProductID] Integer not null,
        [OrderDate] text not null,
        [QuantityOrdered] Integer not null,
        Foreign key (CustomerID) references Customer(CustomerID),
        Foreign key (ProductID) references product(ProductID)
    )
    '''
    header=[]
    i=0
    j=0
    orders=[]
    dict2=step6_create_customer_to_customerid_dictionary(normalized_database_filename)
    dict3=step10_create_product_to_productid_dictionary(normalized_database_filename)
    with open(data_filename) as f:
        for line in f:
            if not header:
                header=line.split("\t")
                continue
            i+=1    
            x=line.split('\t')[5]
            split1=x.split(';')
            y=line.split('\t')[9]
            split2=y.split(';')
            z=line.split('\t')[10].strip()
            split3=z.split(';')
            split2=[int(ele) for ele in split2]
            k=tuple(zip(split1,split3,split2))
            n=line.split('\t')[0]
            for ele in k:
                j+=1
                a=datetime.datetime.strptime(ele[1], '%Y%m%d').strftime('%Y-%m-%d')
                orders.append((j,dict2[n],dict3[ele[0]],a,ele[2]))
    with conn_n:
        create_table(conn_n,create_table_orderdetail_sql,"orderdetail")
        insert_orderdetails(conn_n,orders)
    ### END SOLUTION


def ex1(conn, CustomerName):
    
    # Simply, you are fetching all the rows for a given CustomerName. 
    # Write an SQL statement that SELECTs From the OrderDetail table and joins with the Customer and Product table.
    # Pull out the following columns. 
    # Name -- concatenation of FirstName and LastName
    # ProductName
    # OrderDate
    # ProductUnitPrice
    # QuantityOrdered
    # Total -- which is calculated from multiplying ProductUnitPrice with QuantityOrdered -- round to two decimal places
    # HINT: USE customer_to_customerid_dict to map customer name to customer id and then use where clause with CustomerID
    
    ### BEGIN SOLUTION
    sql_statement = f"""select free.Name,product.ProductName,free.OrderDate,round(product.ProductUnitPrice,2) as ProductUnitPrice,free.QuantityOrdered,round(product.ProductUnitPrice*free.QuantityOrdered,2) as Total 
from(select customer.customerid,customer.firstname || ' ' || customer.lastname as Name,orderdetail.productid,orderdetail.OrderDate,orderdetail.QuantityOrdered from customer
inner join orderdetail 
on orderdetail.customerid=customer.customerid
where Name='{CustomerName}'
) free
inner join product
on product.productid=free.productid
"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex2(conn, CustomerName):
    
    # Simply, you are summing the total for a given CustomerName. 
    # Write an SQL statement that SELECTs From the OrderDetail table and joins with the Customer and Product table.
    # Pull out the following columns. 
    # Name -- concatenation of FirstName and LastName
    # Total -- which is calculated from multiplying ProductUnitPrice with QuantityOrdered -- sum first and then round to two decimal places
    # HINT: USE customer_to_customerid_dict to map customer name to customer id and then use where clause with CustomerID
    
    ### BEGIN SOLUTION
    sql_statement = f"""select free.Name,round(sum(product.ProductUnitPrice*free.QuantityOrdered),2) as Total 
from(select customer.customerid,customer.firstname || ' ' || customer.lastname as Name,orderdetail.productid,orderdetail.OrderDate,orderdetail.QuantityOrdered from customer
inner join orderdetail 
on orderdetail.customerid=customer.customerid
where Name='{CustomerName}'
) free
inner join product
on product.productid=free.productid
group by free.Name
"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex3(conn):
    
    # Simply, find the total for all the customers
    # Write an SQL statement that SELECTs From the OrderDetail table and joins with the Customer and Product table.
    # Pull out the following columns. 
    # Name -- concatenation of FirstName and LastName
    # Total -- which is calculated from multiplying ProductUnitPrice with QuantityOrdered -- sum first and then round to two decimal places
    # ORDER BY Total Descending 
    ### BEGIN SOLUTION
    sql_statement = """select free.Name,round(sum(product.ProductUnitPrice*free.QuantityOrdered),2) as Total 
from(select customer.customerid,customer.firstname || ' ' || customer.lastname as Name,orderdetail.productid,orderdetail.OrderDate,orderdetail.QuantityOrdered from customer
inner join orderdetail 
on orderdetail.customerid=customer.customerid
) free
inner join product
on product.productid=free.productid
group by free.Name
order by total desc
"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex4(conn):
    
    # Simply, find the total for all the region
    # Write an SQL statement that SELECTs From the OrderDetail table and joins with the Customer, Product, Country, and 
    # Region tables.
    # Pull out the following columns. 
    # Region
    # Total -- which is calculated from multiplying ProductUnitPrice with QuantityOrdered -- sum first and then round to two decimal places
    # ORDER BY Total Descending 
    ### BEGIN SOLUTION

    sql_statement = f"""select region.Region,round(sum(Total),2) as Total
from(select *
from(select free.Name,sum(product.ProductUnitPrice*free.QuantityOrdered) as Total,free.countryid  
from(select customer.customerid,customer.firstname || ' ' || customer.lastname as Name,orderdetail.productid,orderdetail.OrderDate,orderdetail.QuantityOrdered,customer.countryid from customer
inner join orderdetail 
on orderdetail.customerid=customer.customerid
) free
inner join product
on product.productid=free.productid
group by free.Name
order by total desc) freee
inner join country
on country.countryid=freee.countryid) an
inner join region 
on region.regionid=an.regionid
group by region
order by total desc
"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex5(conn):
    
     # Simply, find the total for all the countries
    # Write an SQL statement that SELECTs From the OrderDetail table and joins with the Customer, Product, and Country table.
    # Pull out the following columns. 
    # Country
    # CountryTotal -- which is calculated from multiplying ProductUnitPrice with QuantityOrdered -- sum first and then round
    # ORDER BY Total Descending 
    ### BEGIN SOLUTION

    sql_statement = f"""select country.Country as Country,round(sum(freee.Total)) as CountryTotal
from(select free.Name,sum(product.ProductUnitPrice*free.QuantityOrdered) as Total,free.countryid  
from(select customer.customerid,customer.firstname || ' ' || customer.lastname as Name,orderdetail.productid,orderdetail.OrderDate,orderdetail.QuantityOrdered,customer.countryid from customer
inner join orderdetail 
on orderdetail.customerid=customer.customerid
) free
inner join product
on product.productid=free.productid
group by free.Name
order by total desc) freee
inner join country
on country.countryid=freee.countryid
group by country
order by CountryTotal desc
"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement


def ex6(conn):
    
    # Rank the countries within a region based on order total
    # Output Columns: Region, Country, CountryTotal, CountryRegionalRank
    # Hint: Round the the total
    # Hint: Sort ASC by Region
    ### BEGIN SOLUTION

    sql_statement = f"""select *,rank () Over (partition by region order by countrytotal desc) CountryRegionalRank
from(select region.Region,fin.Country,fin.CountryTotal
from(select country.Country as Country,round(sum(freee.Total)) as CountryTotal,country.regionid
from(select free.Name,sum(product.ProductUnitPrice*free.QuantityOrdered) as Total,free.countryid  
from(select customer.customerid,customer.firstname || ' ' || customer.lastname as Name,orderdetail.productid,orderdetail.OrderDate,orderdetail.QuantityOrdered,customer.countryid from customer
inner join orderdetail 
on orderdetail.customerid=customer.customerid
) free
inner join product
on product.productid=free.productid
group by free.Name
order by total desc) freee
inner join country
on country.countryid=freee.countryid
group by country
order by CountryTotal desc) fin
inner join region 
on region.regionid=fin.regionid) ans
"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement



def ex7(conn):
    
   # Rank the countries within a region based on order total, BUT only select the TOP country, meaning rank = 1!
    # Output Columns: Region, Country, CountryTotal, CountryRegionalRank
    # Hint: Round the the total
    # Hint: Sort ASC by Region
    # HINT: Use "WITH"
    ### BEGIN SOLUTION

    sql_statement = f"""select * from(select *,rank () Over (partition by region order by countrytotal desc) CountryRegionalRank
from(select region.Region,fin.Country,fin.CountryTotal
from(select country.Country as Country,round(sum(freee.Total)) as CountryTotal,country.regionid
from(select free.Name,sum(product.ProductUnitPrice*free.QuantityOrdered) as Total,free.countryid  
from(select customer.customerid,customer.firstname || ' ' || customer.lastname as Name,orderdetail.productid,orderdetail.OrderDate,orderdetail.QuantityOrdered,customer.countryid from customer
inner join orderdetail 
on orderdetail.customerid=customer.customerid
) free
inner join product
on product.productid=free.productid
group by free.Name
order by total desc) freee
inner join country
on country.countryid=freee.countryid
group by country
order by CountryTotal desc) fin
inner join region 
on region.regionid=fin.regionid) ans) final
where countryregionalrank=1
order by region
"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex8(conn):
    
    # Sum customer sales by Quarter and year
    # Output Columns: Quarter,Year,CustomerID,Total
    # HINT: Use "WITH"
    # Hint: Round the the total
    # HINT: YOU MUST CAST YEAR TO TYPE INTEGER!!!!
    ### BEGIN SOLUTION

    sql_statement = """with quartertable as (
select
    case
        WHEN 0 + strftime('%m', orderdate) BETWEEN 1
        AND 3 THEN 'Q1'
        WHEN 0 + strftime('%m', orderdate) BETWEEN 4
        AND 6 THEN 'Q2'
        WHEN 0 + strftime('%m', orderdate) BETWEEN 7
        AND 9 THEN 'Q3'
        WHEN 0 + strftime('%m', orderdate) BETWEEN 10
        AND 12 THEN 'Q4'
    END Quarter,
    orderdate,CustomerID,quantityordered,productunitprice
    from (select orderdetail.customerid,orderdetail.quantityordered,orderdetail.orderdate,product.productunitprice
    from orderdetail
    inner join product
    on product.productid=orderdetail.productid) ans
)
select Quarter,cast(substr(orderdate,1,4) as int) Year,CustomerID,round(sum(quantityordered*productunitprice)) Total
from quartertable
group by year,quarter,customerid
"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex9(conn):
    
    # Rank the customer sales by Quarter and year, but only select the top 5 customers!
    # Output Columns: Quarter, Year, CustomerID, Total
    # HINT: Use "WITH"
    # Hint: Round the the total
    # HINT: YOU MUST CAST YEAR TO TYPE INTEGER!!!!
    # HINT: You can have multiple CTE tables;
    # WITH table1 AS (), table2 AS ()
    ### BEGIN SOLUTION

    sql_statement = """with quartertable as (
select
    case
        WHEN 0 + strftime('%m', orderdate) BETWEEN 1
        AND 3 THEN 'Q1'
        WHEN 0 + strftime('%m', orderdate) BETWEEN 4
        AND 6 THEN 'Q2'
        WHEN 0 + strftime('%m', orderdate) BETWEEN 7
        AND 9 THEN 'Q3'
        WHEN 0 + strftime('%m', orderdate) BETWEEN 10
        AND 12 THEN 'Q4'
    END Quarter,
    orderdate,customerid,quantityordered,productunitprice
    from (select orderdetail.customerid,orderdetail.quantityordered,orderdetail.orderdate,product.productunitprice
    from orderdetail
    inner join product
    on product.productid=orderdetail.productid) ans
)
select * from (select *,rank() over(partition by year,quarter order by total desc) CustomerRank
from(select Quarter,cast(substr(orderdate,1,4) as int) Year,CustomerID,round(sum(quantityordered*productunitprice)) Total
from quartertable
group by year,quarter,customerid) ans)
where CustomerRank<=5
"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex10(conn):
    
    # Rank the monthly sales
    # Output Columns: Quarter, Year, CustomerID, Total
    # HINT: Use "WITH"
    # Hint: Round the the total
    ### BEGIN SOLUTION

    sql_statement = """with monthtable as (
select
    case
        WHEN strftime('%m', orderdate) = '01' THEN 'January'
        WHEN strftime('%m', orderdate) = '02' THEN 'February'
        WHEN strftime('%m', orderdate) = '03' THEN 'March'
        WHEN strftime('%m', orderdate) = '04' THEN 'April'
        WHEN strftime('%m', orderdate) = '05' THEN 'May'
        WHEN strftime('%m', orderdate) = '06' THEN 'June'
        WHEN strftime('%m', orderdate) = '07' THEN 'July'
        WHEN strftime('%m', orderdate) = '08' THEN 'August'
        WHEN strftime('%m', orderdate) = '09' THEN 'September'
        WHEN strftime('%m', orderdate) = '10' THEN 'October'
        WHEN strftime('%m', orderdate) = '11' THEN 'November'
        WHEN strftime('%m', orderdate) = '12' THEN 'December'
    END Month,
    orderdate,customerid,quantityordered,productunitprice
    from (select orderdetail.customerid,orderdetail.quantityordered,orderdetail.orderdate,product.productunitprice
    from orderdetail
    inner join product
    on product.productid=orderdetail.productid) ans
)
select *,rank() over(order by total desc) TotalRank 
from (select Month,sum(round(quantityordered*productunitprice)) Total
from monthtable
group by Month) 
"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement

def ex11(conn):
    
    # Find the MaxDaysWithoutOrder for each customer 
    # Output Columns: 
    # CustomerID,
    # FirstName,
    # LastName,
    # Country,
    # OrderDate, 
    # PreviousOrderDate,
    # MaxDaysWithoutOrder
    # order by MaxDaysWithoutOrder desc
    # HINT: Use "WITH"; I created two CTE tables
    # HINT: Use Lag

    ### BEGIN SOLUTION

    sql_statement = """with difftable as (
select cast(strftime('%j', orderdate) AS INT) days,
lag(orderdate,1) over(partition by customerid) lastorder,
customerid,orderdate
from (select * from orderdetail
order by customerid,orderdate)

)
,differtable as (
select customerid,days,lastorder,julianday(orderdate)-julianday(lastorder) dayswithout,orderdate
from difftable
)

select fin.CustomerID,fin.FirstName,fin.LastName,country.Country Country,fin.OrderDate,fin.lastorder PreviousOrderDate,
fin.MaxDaysWithoutOrder from
(select * from(select CustomerID,max(dayswithout) MaxDaysWithoutOrder ,OrderDate,lastorder  from differtable
group by customerid
order by MaxDaysWithoutOrder desc) ans
inner join customer
on customer.customerid=ans.customerid) fin
inner join country
on country.countryid=fin.countryid


"""
    ### END SOLUTION
    df = pd.read_sql_query(sql_statement, conn)
    return sql_statement
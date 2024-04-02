from ortools.linear_solver import pywraplp
import time
def input_data():
    t,n,m=map(int, input().split())
    course_class=[]; A=[]
    for i in range(n):
       A=list(map(int, input().split()))
       A.pop(-1)
       course_class.append(A)
    course_teacher=[];B=[]
    for i in range(t):
        B=list(map(int,input().split()))
        B.pop(-1)
        course_teacher.append(B)
    Credits=list(map(int,input().split()))
    return t,n,m,course_class,course_teacher,Credits

teachers_for_course=[]# teachers_for_course[i]: a list of teacher can teach course i+1
t,n,m,courses_for_class,courses_by_teacher,cre=input_data()
for course in range(1,m+1):
    A=[]
    for teacher,courses in enumerate(courses_by_teacher):
        if course in courses:
            A.append(teacher+1)
    teachers_for_course.append(A)
time1 = time.time()
solver=pywraplp.Solver.CreateSolver('SAT')
A={}
for clas in range(1,n+1):
    for course in courses_for_class[clas-1]:
            for teacher in teachers_for_course[course-1]:   
                    for lesson in range(1,61):
                        A[teacher,clas,course,lesson]=solver.BoolVar('A['+str(teacher)+','+ str(clas)+','+ str(course)+','+ str(lesson)+']') # initialize the bool variable
                        
# Constraints
# Including 3 constraints
for lesson in range(1,61):
        for clas in range(1,n+1): 
                solver.Add(sum(A[teacher,clas,course,lesson] for course in courses_for_class[clas-1] for teacher in teachers_for_course[course-1])<=1)# At one time, a class study one course by one teacher
        for teacher in range(1,t+1):
                solver.Add(sum(A[teacher,clas+1,course,lesson] for clas,courses in enumerate(courses_for_class) for course in courses if course in courses_by_teacher[teacher-1])<=1) # At one time, a teacher teach one course for one class

# All the lessons of the course for a class have been assigned in consecutive order.
count={}
maxx={}
for period in range(10):
    for j, courses in enumerate(courses_for_class):
        for course in courses:
            for teacher in teachers_for_course[course-1]:
                        maxx[0]=solver.IntVar(0,0,'maxx[0]')
                        t1=solver.BoolVar('t1')
                        for lesson in range(1,6-cre[course-1]+2):
                            t2=solver.BoolVar('t2')
                            maxx[lesson]=solver.IntVar(0,cre[course-1],'maxx['+str(lesson)+']')
                            count[lesson]=solver.IntVar(0,cre[course-1],'count['+str(lesson)+']') # Initialize the count variable as the intermediary variable
                            solver.Add(sum(A[teacher, j+1,course,i] for i in range(period*6+lesson,period*6+lesson+cre[course-1]))==count[lesson])
                            solver.Add(maxx[lesson]>=maxx[lesson-1])
                            solver.Add(maxx[lesson]>=count[lesson])
                            solver.Add(maxx[lesson]<=maxx[lesson-1]+(1-t2)*cre[course-1])
                            solver.Add(maxx[lesson]<=count[lesson]+cre[course-1]*t2)
                        solver.Add(maxx[7-cre[course-1]]==cre[course-1]*t1)
                            
                         
for i,courses in enumerate(courses_for_class):
    for course in courses:     
            solver.Add(sum(A[teacher,i+1,course,lesson] for lesson in range(1,61)for teacher in teachers_for_course[course-1])<=cre[course-1])
            for period in range(10):
                for teacher in teachers_for_course[course-1]:
                        t3=solver.BoolVar('t3')
                        solver.Add(sum(A[teacher,i+1,course,lesson] for lesson in range(period*6+1,period*6+7) )==cre[course-1]*t3) # the total of lesson of a course at a period breakfast or afternoon has to equal to the credit of this course or equal to zero
                                           
#objective function
solver.Maximize(sum(A[teacher, clas,course,lesson]for clas in range(1,n+1)for course in courses_for_class[clas-1] for teacher in teachers_for_course[course-1]  for lesson in range(1,61)))# the total of lesson of a course in a week has to be less or equal than the credit of this course

time2 = time.time()
elapsed_time = round((time2- time1)/60,2)
print ("modelling_time:{0}".format(elapsed_time) + "[mins]")
status = solver.Solve()
if status==pywraplp.Solver.OPTIMAL:
    count=0
    results=[]
    for clas,courses in enumerate(courses_for_class):
        for course in courses:
            for teacher in teachers_for_course[course-1]:   
                for lesson in range(1,61):
                    if A[teacher,clas+1,course,lesson].solution_value()==1:
                            B=[clas+1,course,lesson,teacher]
                            results.append(B)
                            count+=1
                            break
                                    
                            
    print(count)
    for i in results:
        for j in i:
            print(j,end=" ")
        print("")
                                   
else:
    print("No optimal solution found.")
time3 = time.time()
elapsed_time = round((time3- time2)/60,2)
print ("solving_time:{0}".format(elapsed_time) + "[mins]")
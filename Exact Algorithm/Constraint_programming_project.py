from ortools.sat.python import cp_model
import time
# INPUT
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
t,n,m,courses_for_class,courses_by_teacher,cre=input_data()
teachers_for_course=[]
for course in range(1,m+1):
    A=[]
    for teacher,courses in enumerate(courses_by_teacher):
        if course in courses:
            A.append(teacher+1)
    teachers_for_course.append(A)
# INITIALIZE THE VARIABLES
time1=time.time()
model=cp_model.CpModel()
A={}
for clas in range(1,n+1):
    for course in courses_for_class[clas-1]:
            for teacher in teachers_for_course[course-1]:   
                    for lesson in range(1,61):
                        A[teacher,clas,course,lesson]=model.NewBoolVar('A['+str(teacher)+','+ str(clas)+','+ str(course)+','+ str(lesson)+']')
# Constraints
for lesson in range(1,61):
        for clas in range(1,n+1): 
                model.Add(sum(A[teacher,clas,course,lesson] for course in courses_for_class[clas-1] for teacher in teachers_for_course[course-1])<=1)
        for teacher in range(1,t+1):
                model.Add(sum(A[teacher,clas+1,course,lesson] for clas,courses in enumerate(courses_for_class) for course in courses if course in courses_by_teacher[teacher-1])<=1)



# All the lessons of the course for a class have been assigned in consecutive order.
count={}

for j, courses in enumerate(courses_for_class):
    for course in courses:
        for teacher in teachers_for_course[course-1]:
            for p in range(10):
                t1=model.NewBoolVar('t1')
                count[0]=model.NewIntVar(0,0,'count[0]')
                for lesson in range(1,7):
                            t2=model.NewBoolVar('t2')
                            count[lesson]=model.NewIntVar(0,cre[course-1],'count['+str(lesson)+']')
                            model.Add(A[teacher,j+1,course,lesson+6*p]==1).OnlyEnforceIf(t2)
                            model.Add(A[teacher,j+1,course,lesson+6*p]!=1).OnlyEnforceIf(t2.Not())
                            model.Add(count[lesson]==count[lesson-1]+1).OnlyEnforceIf(t2)
                            model.Add(count[lesson]==0).OnlyEnforceIf(t2.Not())
                model.Add(sum(count[lesson] for lesson in range(1,7))==int((cre[course-1]+1)*(cre[course-1])/2)*t1)


for i,courses in enumerate(courses_for_class):
    for course in courses:     
            model.Add(sum(A[teacher,i+1,course,lesson] for lesson in range(1,61)for teacher in teachers_for_course[course-1])<=cre[course-1])
            for period in range(10):
                for teacher in teachers_for_course[course-1]:
                        t3=model.NewBoolVar('t3')
                        model.Add(sum(A[teacher,i+1,course,lesson] for lesson in range(period*6+1,period*6+7) )==cre[course-1]*t3)

#objective function
model.Maximize(sum(A[teacher, clas,course,lesson]for clas in range(1,n+1)for course in courses_for_class[clas-1] for teacher in teachers_for_course[course-1]  for lesson in range(1,61)))
time2 = time.time()
elapsed_time = round((time2 - time1)/60,2)
print ("Moldelling time:{0}".format(elapsed_time) + "[min]")
solver=cp_model.CpSolver()
solver.parameters.max_time_in_seconds=10800
status=solver.Solve(model)
if status==cp_model.OPTIMAL:
    res=0
    results=[]
    for clas in range(1,n+1):
        for course in courses_for_class[clas-1]:
            for teacher in teachers_for_course[course-1]:   
                    for lesson in range(1,61):
                        if solver.Value(A[teacher,clas,course,lesson])==1:
                            B=[clas,course,lesson,teacher]
                            results.append(B)
                            res+=1
                            break
                                    
                            
    print(res)
    for i in results:
        for j in i:
            print(j,end=" ")
        print("")
                  
                    
else:
    print("No optimal solution found.")
time3 = time.time()
elapsed_time = round((time3- time2)/60,2)
print ("solving_time:{0}".format(elapsed_time) + "[min]")
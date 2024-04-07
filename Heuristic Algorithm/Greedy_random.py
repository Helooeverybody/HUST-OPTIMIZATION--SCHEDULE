import random 
class Class:
    def __init__(self,name,courses):
        self.name = name 
        self.courses = courses
        self.teacher = {i:[] for i in self.courses}
        self.slot = [False for i in range(1,61)] 

class Teacher:
    def __init__(self,name,courses):
        self.name = name 
        self.courses = courses 
        self.slot = [False for i in range(1,61)]

class Solver:
    def __init__(self,lst_class,lst_teacher,time_slot):
        # initial the list of class course 
        self.class_course = []
        for i in range(len(lst_class)):
            self.class_course += [[lst_class[i],j,0,0] for j in lst_class[i].courses]
        
        self.time_slot = time_slot 
        self.length = 0 
        self.schedule = []
    
    def solve(self):
        # reset the slot of class course of the previous solution 
        for c in self.class_course:
            c[0].slot = [False for i in range(1,61)]
            c[2],c[3] = 0,0
            for t in c[0].teacher[c[1]]:
                t.slot = [False for i in range(1,61)]
        # sort the order of teachers in each class's course 
        for c in self.class_course:
            c[0].courses.sort(key = lambda x : len(c[0].teacher[x]))
        # sort the order of class_course in the list class course
        self.class_course.sort(key = lambda x : (len(x[0].teacher[x[1]]),len(x[0].courses),random.random()))

        length = 0 
        for clas_course in self.class_course:
            for slot in range(1,61):
                # check possible slot 
                check_slot = True
                for k in [6,12,18,24,30,36,42,48,54,60]:
                    if slot <= k and (slot + self.time_slot[clas_course[1]]-1) > k:
                        check_slot = False 
                        break 
                if check_slot == False:
                    continue

                for t in clas_course[0].teacher[clas_course[1]]:
                    # consider slot can overlap
                    check = True 
                    for preiod in range(slot,slot + self.time_slot[clas_course[1]]):
                        if t.slot[preiod-1] or clas_course[0].slot[preiod-1]:
                            check = False 
                            break 
                    # assign slot and teacher for class course and update slot 
                    if check == True:  
                        clas_course[2],clas_course[3] = slot,t.name 
                        for preiod in range(slot,slot + self.time_slot[clas_course[1]]):
                            t.slot[preiod-1] = True 
                            clas_course[0].slot[preiod-1] = True 
                        break 
                if clas_course[2] != 0:
                    length += 1
                    break 
        schedule = []
        # sort the order of class id 
        self.class_course.sort(key = lambda x: x[0].name)
        for cour in self.class_course:
            if cour[2] != 0:
                schedule += [[cour[0].name,cour[1],cour[2],cour[3]]]
        return (schedule,length)
    
    def print_solotion(self):
        print(self.length)
        for i in self.schedule:
            print(*i)
    

def input_data():
    T,N,M = map(int,input().split())

    lst_class,lst_teacher = [],[]
    time_slot = {}

    for i in range(N):
        c = list(map(int,input().split()))
        c.pop()
        lst_class.append(Class(i+1,c))

    for i in range(T):
        t = list(map(int,input().split()))
        t.pop()
        lst_teacher.append(Teacher(i+1,t))

    time = list(map(int,input().split()))
    time_slot = {i+1:time[i] for i in range(len(time))}

    for c in lst_class:
        for course in c.teacher:
            for t in lst_teacher:
                if course in t.courses:
                    c.teacher[course].append(t)

    return lst_class,lst_teacher,time_slot 

def main():
    lst_class,lst_teacher,time_slot = input_data()
    max_iter = 20
    # the initial solution  
    sol = Solver(lst_class,lst_teacher,time_slot)
    schedule,res = sol.solve()

    for i in range(max_iter):
        schedule_new,res_new = sol.solve()
        # compare next result to find the better optimal solution
        if res_new > res:
            schedule = schedule_new
            res = res_new
    sol.length = res # asign the number of class course are scheduled
    sol.schedule = schedule # asign list class course 
    sol.print_solotion()

if __name__ == '__main__':
    main()

    

# class Teacher:
# 	def __init__(self, name, subjects):
# 		self.name = name
# 		self.subjects = subjects
# 		self.slot = [False for i in range(1, 61)]
# 	def reset(self):
# 		self.slot = [False for i in range(1, 61)]
# 	def __str__(self):
# 		ans = f'Teacher: {self.name}, subjects = ['
# 		for subject in self.subjects[:-1]:
# 			ans += f'{subject}, '
# 		ans += f'{self.subjects[-1]}]'
# 		return ans

# class Class:
# 	def __init__(self,name, subjects):
# 		self.name = name 
# 		self.subjects = subjects
# 		self.teachers = {subject: [] for subject in self.subjects}
# 		self.sol = {s: [] for s in subjects}
# 		self.slot = [False for i in range(1, 61)]


# 	# print for debug
# 	def __str__(self):
# 		ans = f'Class: {self.name}, subjects = ['
# 		for subject in self.subjects[:-1]:
# 			ans += f'{subject}, '
# 		ans += f'{self.subjects[-1]}]'
# 		return ans

# def find_possible_teachers(classes, teachers):
# 	for c in classes:
# 		for subject in c.subjects:
# 			for teacher in teachers:
# 				if subject in teacher.subjects:
# 					c.teachers[subject].append(teacher)
# def import_data(T,N,M,Class_subject,Teacher_subject,subject_time):
# 	classes = []
# 	teachers = []

# 	for i in range(N):
# 		temp = Class_subject[i]
# 		temp.pop()
# 		classes.append(Class(i+1, temp))
	
# 	for i in range(T):
# 		temp = Teacher_subject[i]
# 		temp.pop()
# 		teachers.append(Teacher(i+1, temp))
	
# 	temp = subject_time
# 	subjects = {i+1: temp[i] for i in range(M)}
# 	find_possible_teachers(classes, teachers)
# 	return classes, teachers, subjects
# class Solver:
# 	def __init__(self, classes, teachers, subjects):
# 		self.classes = classes
# 		self.teachers = teachers
# 		self.subjects = subjects
# 		self.length = 0
# 	def solve(self):
# 		for c in self.classes:
# 			c.subjects.sort(key=lambda x: len(c.teachers[x]))
# 		self.classes.sort(key = lambda x: [len(x.teachers[x.subjects[0]]), len(x.subjects)])
# 		for c in self.classes:
# 			for subject in c.subjects:
# 				for slot in range(1, 61):
# 					if slot + self.subjects[subject] > 61:
# 						break
# 					for teacher in c.teachers[subject]:

# 						for preiod in range(slot, slot + self.subjects[subject]):
# 							if teacher.slot[preiod-1] or c.slot[preiod-1]:
# 								break
# 						else:
# 							c.sol[subject] = [slot, teacher.name]

# 							for preiod in range(slot, slot + self.subjects[subject]):
# 								teacher.slot[preiod-1] = True
# 								c.slot[preiod-1] = True
# 							break
# 					if c.sol[subject] != []:
# 						self.length += 1
# 						break
# 		self.classes.sort(key=lambda x: x.name)
# 	def print_sol(self):
# 		res = []
# 		for c in self.classes:
# 			c.subjects.sort()
# 			for subject in c.subjects:
# 				if c.sol[subject] != []:
# 					schedule = [c.name,subject,c.sol[subject][0],c.sol[subject][1]]
# 					res.append(schedule)
# 		return res 

	
# def main():
# 	classes, teachers, subjects = import_data()
# 	sol = Solver(classes, teachers, subjects)
# 	sol.solve()
# 	sol.print_sol()
# if __name__ == "__main__":
# 	main()



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
        self.class_course = []
        for i in range(len(lst_class)):
            self.class_course += [[lst_class[i],j,0,0] for j in lst_class[i].courses]
        self.time_slot = time_slot 
        self.length = 0 
        self.schedule = []

    def SetupModel(self,lst_class,lst_teacher,time_slot,max_iter = 5):
        sol = Solver(lst_class,lst_teacher,time_slot)
        schedule,res = sol.solve()
        for i in range(max_iter):
            schedule_new,res_new = sol.solve()
            if res_new > res:
                schedule = schedule_new
                res = res_new
        sol.length = res 
        sol.schedule = schedule


    def solve(self):
        for c in self.class_course:
            c[0].slot = [False for i in range(1,61)]
            c[2],c[3] = 0,0
            for t in c[0].teacher[c[1]]:
                t.slot = [False for i in range(1,61)]
        for c in self.class_course:
            c[0].courses.sort(key = lambda x : len(c[0].teacher[x]))
        self.class_course.sort(key = lambda x : (len(x[0].teacher[x[1]]),len(x[0].courses),random.random()))

        length = 0 
        for clas_course in self.class_course:
            for slot in range(1,61):
                check_slot = True
                for k in [6,12,18,24,30,36,42,48,54,60]:
                    if slot <= k and (slot + self.time_slot[clas_course[1]]-1) > k:
                        check_slot = False 
                        break 
                if check_slot == False:
                    continue
                for t in clas_course[0].teacher[clas_course[1]]:
                    check = True 
                    for preiod in range(slot,slot + self.time_slot[clas_course[1]]):
                        if t.slot[preiod-1] or clas_course[0].slot[preiod-1]:
                            check = False 
                            break 
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
        self.class_course.sort(key = lambda x: x[0].name)
        for cour in self.class_course:
            if cour[2] != 0:
                schedule += [[cour[0].name,cour[1],cour[2],cour[3]]]
        return (schedule,length)
    
    def print_solotion(self):
        print(self.length)
        for i in self.schedule:
            print(*i)
    
def SetupModel(lst_class,lst_teacher,time_slot,max_iter = 5):
    sol = Solver(lst_class,lst_teacher,time_slot)
    schedule,res = sol.solve()
    for i in range(max_iter):
        schedule_new,res_new = sol.solve()
        if res_new > res:
            schedule = schedule_new
            res = res_new
    return schedule
def import_data(T,N,M,Class_subject,Teacher_subject,subject_time):
    lst_class = []
    lst_teacher = []

    for i in range(N):
        temp = Class_subject[i]
        temp.pop()
        lst_class.append(Class(i+1, temp))
	
    for i in range(T):
        temp = Teacher_subject[i]
        temp.pop()
        lst_teacher.append(Teacher(i+1, temp))
    for c in lst_class:
        for course in c.teacher:
            for t in lst_teacher:
                if course in t.courses:
                    c.teacher[course].append(t)
    temp = subject_time
    time_slot = {i+1: temp[i] for i in range(M)}

    return lst_class,lst_teacher,time_slot 

def main():
    lst_class,lst_teacher,time_slot = input_data()
    max_iter = 20
    sol = Solver(lst_class,lst_teacher,time_slot)
    schedule,res = sol.solve()

    for i in range(max_iter):
        schedule_new,res_new = sol.solve()
        if res_new > res:
            schedule = schedule_new
            res = res_new
    sol.length = res 
    sol.schedule = schedule
    sol.print_solotion()

if __name__ == '__main__':
    main()

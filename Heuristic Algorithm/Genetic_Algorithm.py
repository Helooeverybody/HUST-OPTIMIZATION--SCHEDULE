import numpy as np 
import copy 
class Class:
    def __init__(self,name,subject):
        self.name = name 
        self.subject = subject 
        self.teacher = {i:[] for i in self.subject}
        self.schedule = [[self.name,subject,0,0] for subject in self.subject]
        self.slot = [True for i in range(60)]
    def reset_schedule(self):
        return [[self.name,subject,0,0] for subject in self.subject]
class Teacher:
    def __init__(self,name,subject):
        self.name = name
        self.subject = subject 
        self.slot = [True for i in range(61)]
def get_fitness(schedule):
    return sum(1 for i in schedule if i[2] != 0 and i[3] != 0)

def remove_duplicate(ind,lst_class,lst_teacher,subject_time):
    # reset all slot of each teacher and class
    for c in lst_class:
        c.slot = [True for i in range(61)]
    for t in lst_teacher:
        t.slot = [True for i in range(61)]

    # then, we will reset all class-subject that duplicate slot time
    slot = [1 for i in range(1,61)]
    lst_reset = []
    for i in range(len(ind)):
        if ind[i][2] != 0 and ind[i][3] != 0:
            c = lst_class[ind[i][0]-1]
            t = lst_teacher[ind[i][3]-1]
            check_valid = True 

            for j in range(ind[i][2],ind[i][2] + subject_time[ind[i][1]]):
                if j > 60:
                    lst_reset.append(ind[i])
                    check_valid = False
                    break 
                else:
                    if c.slot[j-1] == False or t.slot[j-1] == False:
                        lst_reset.append(ind[i])
                        check_valid = False
                        break 

            if check_valid == True:
                for j in range(ind[i][2],ind[i][2] + subject_time[ind[i][1]]):
                    c.slot[j-1] = False
                    t.slot[j-1] = False
                    if j in slot:
                        slot.remove(j)

    # reset all class-subject that duplicat time slot:
    for i in lst_reset:
        a = ind.index(i)
        ind[a][2],ind[a][3] = 0,0

    return (ind,slot)
def add_extra(ind,slot,lst_class,lst_teacher,subject_time):

    # add teacher and slot for each class-subject reseted before
    for i in range(len(ind)):
        if ind[i][3] == 0 and ind[i][2] == 0:
            cl = lst_class[ind[i][0]-1]
            if cl.teacher[ind[i][1]] != [] and slot != []:
                ind[i][3] = np.random.choice(cl.teacher[ind[i][1]]).name
                ind[i][2] = np.random.choice(slot)
                slot.remove(ind[i][2])
    ind = remove_duplicate(ind,lst_class,lst_teacher,subject_time)[0]
    return ind
def CrossOver(parent1,parent2,lst_class,lst_teacher,subject_time):
    a = len(parent1)
    point_1 = np.random.randint(1,a-3)
    point_2 = np.random.randint(point_1+1,a-1)
    child = parent1[:point_1] + parent2[point_1:point_2] + parent1[point_2:]
    child,slot = remove_duplicate(child,lst_class,lst_teacher,subject_time)
    child = add_extra(child,slot,lst_class,lst_teacher,subject_time)
    return child
    
def mutation(ind,lst_class,lst_teacher,subject_time):
    start = np.random.randint(1,len(ind)-2)
    end = np.random.randint(start,len(ind)-1)
    left_gence = ind[:start]
    right_gence = ind[end:]
    mid_gence = ind[start:end]
    # gain the list of slot on the mid gence and choosing again teacher for each class-subject
    for i in range(len(mid_gence)):
        cl = lst_class[mid_gence[i][0]-1]
        if cl.teacher[mid_gence[i][1]] != []:
            mid_gence[i][3] = np.random.choice(cl.teacher[mid_gence[i][1]]).name 
            mid_gence[i][2] = np.random.randint(1,60)
    # reversing the lst slot and assigning again
    child = left_gence + mid_gence + right_gence
    child,slot = remove_duplicate(child,lst_class,lst_teacher,subject_time)
    child = add_extra(child,slot,lst_class,lst_teacher,subject_time)
    return child
def creating_individual(lst_class,lst_teacher,subject_time):
    # reset the schedule and create a new ind
    ind = []
    for c in lst_class:
        c.schedule = c.reset_schedule()
        ind += c.schedule
    
    # choosing random class and slot for each class-subject
    for i in range(len(ind)):
        cl = lst_class[ind[i][0]-1]
        if cl.teacher[ind[i][1]] != []:
            t,slot = np.random.choice(cl.teacher[ind[i][1]]).name, np.random.randint(1,60)
            ind[i][2],ind[i][3] = slot,t
    ind = remove_duplicate(ind,lst_class,lst_teacher,subject_time)[0]
    return ind
def initial_population(pop_size,lst_class,lst_teacher,subject_time):
    pop = []
    for i in range(pop_size):
        pop.append(creating_individual(lst_class,lst_teacher,subject_time))
    return pop
    
def next_population(RateCrossOver,RateMutation,pop_size,pop,subject_time,lst_class,lst_teacher):
    new_pop = copy.deepcopy(pop)
    step = 0
    while step < pop_size-1:
        parent1 = pop[step]
        parent2 = pop[1+step]
        # the probability of crossover
        if RateCrossOver > np.random.rand():
            new_ind = CrossOver(parent1,parent2,lst_class,lst_teacher,subject_time)
            new_pop.append(new_ind)
            step += 1
        # the probability of mutation 
        if RateMutation > np.random.rand():
            new_pop.append(mutation(parent1,lst_class,lst_teacher,subject_time))
            new_pop.append(mutation(parent2,lst_class,lst_teacher,subject_time))

    new_pop.sort(key = lambda x : -get_fitness(x))
    return new_pop[:pop_size]

def solver(subject_time,lst_class,lst_teacher,pop_size,num_gen,RateCrossOver,RateMutation):
    pop = initial_population(pop_size,lst_class,lst_teacher,subject_time)
    pop.sort(key = lambda x : -get_fitness(x))
    print('Initial fitness: ', get_fitness(pop[0]))
    best_schedule = pop[0]
    for gen in range(num_gen):
        pop = next_population(RateCrossOver,RateMutation,pop_size,pop,subject_time,lst_class,lst_teacher)
        current_schedule = pop[0]
        current_fitness = get_fitness(pop[0])
        print('current fitness of generation ' + str(gen) + ': ' + str(current_fitness))
        if current_fitness > get_fitness(best_schedule):
            best_schedule = current_schedule
    return best_schedule
def main():
    T, N, M = map(int,input().split())
    lst_teacher = []
    lst_class = []
    # all subject of each class 
    for i in range(1,N+1):
        class_sub = list(map(int,input().split()))
        class_sub.pop(-1)
        lst_class.append(Class(i,class_sub))
    # all subject of each teacher
    for i in range(1,T+1):
        teacher_sub = list(map(int,input().split()))
        teacher_sub.pop(-1)
        lst_teacher.append(Teacher(i,teacher_sub))
    a = list(map(int,input().split()))
    subject_time = {}
    for i in range(1,M+1):
        subject_time.update({i:a[i-1]})
	# add all feasiable teacher for each class-subject
    for c in lst_class:
        for subject in c.teacher:
            for teacher in lst_teacher:
                if subject in teacher.subject:
                    c.teacher[subject].append(teacher)

    best_solution = solver(subject_time,lst_class,lst_teacher,pop_size = 100, num_gen= 150, RateCrossOver = 0.7, RateMutation = 0.05)
    best_solution = remove_duplicate(best_solution,lst_class,lst_teacher,subject_time)[0]
    print(get_fitness(best_solution))
    for i in best_solution:
        if i[2] != 0 and i[3] != 0:
            print(*i)

if __name__ == '__main__':
    main()
from random import random, randint, choice
from time import sleep


def gen_from_pdt(pd):
    """
    Generate a value based on a probability distribution table.
    """
    cd = 0
    rand = random()
    for i, p_i in pd.items():
        cd += p_i
        if rand < cd:
            return i


def assign_course(num_to_assign, num_course, lb):
    """
    Assign courses to each class or teacher.
    """
    courses = range(1, num_course + 1)
    base_course = [[] for _ in range(num_to_assign)]
    unassigned_courses = set(courses)

    num = randint(lb, lb + 1)
    for i in range(num_to_assign):
        while len(base_course[i]) < num:
            course = choice(courses)
            if course in base_course[i]:
                continue
            base_course[i].append(course)
            if course in unassigned_courses:
                unassigned_courses.remove(course)

    while unassigned_courses:
        to_assign = choice(range(num_to_assign))
        course = next(iter(unassigned_courses))
        base_course[to_assign].append(course)
        unassigned_courses.remove(course)

    for i in range(num_to_assign):
        base_course[i].sort()
        base_course[i].append(0)

    return base_course


def GenInput(fname):
    print("> Main parameters")
    T = int(input("Number of teachers: "))
    N = int(input("Number of classes : "))
    M = int(input("Number of courses : "))

    # You can alter this, must be in increasing order
    period_pd = {1: 0.2, 2: 0.4, 4: 0.4}

    print("> Additional parameters:")
    lb_teach = int(input("Lower bound for the number of courses a teacher can teach: "))
    lb_class = int(input("Lower bound for the number of courses a class has to take: "))
    print("> Generating input")
    sleep(1)
    print("[....] Assigning courses to each class", end="\r")
    class_course = assign_course(N, M, lb_class)
    sleep(1)
    print("[Done] Assigning courses to each class")
    sleep(1)
    print("[....] Assigning courses to each teacher", end="\r")
    teacher_course = assign_course(T, M, lb_teach)
    sleep(1)
    print("[Done] Assigning courses to each teacher")
    sleep(1)
    print("[....] Setting the number of periods for each course", end="\r")
    periods = [gen_from_pdt(period_pd) for _ in range(M)]
    sleep(1)
    print("[Done] Setting the number of periods for each course")
    sleep(1)
    print(f"[....] Storing input in {fname}", end="\r")
    with open(fname, "w") as file:
        file.write(f"{T} {N} {M}\n")

        for i in range(N):
            file.write(" ".join(map(str, class_course[i])) + "\n")
        for i in range(T):
            file.write(" ".join(map(str, teacher_course[i])) + "\n")
        file.write(" ".join(map(str, periods)) + "\n")
    sleep(1)
    print(f"[Done] Storing input in {fname}")
    print("Input generated")


if __name__ == "__main__":
    fname = "input.txt"
    GenInput(fname)

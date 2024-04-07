import pygame 
import pyperclip
import class_course
pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption('timetable for scheduling class and teach ')
running = True
clock = pygame.time.Clock()

BACKGROUND = (214,214,214)
PANEL = (225,255,225)
RED = (225,0,0)
BLACK = (0,0,0)
WHITE = (225,225,225)
TIME_COLOR = (233,83,8)
def day_screen(day_schedule,subject_time):
    running = True 
    BLACK = (0,0,0)
    BACKGROUND = (214,214,214)
    PANEL = (225,255,225)
    position = 125
    day_schedule.sort(key = lambda x : x[2])

    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        x_mouse,y_mouse = pygame.mouse.get_pos()
        pygame.draw.rect(screen,BACKGROUND,(0,0,700,500))
        # button back 
        pygame.draw.rect(screen,PANEL,(15,15,110,40))
        pygame.draw.rect(screen,BLACK,(20,20,100,30))
        screen.blit(create_font_button('BACK'),(30,22))

        # table time 
        pygame.draw.rect(screen,PANEL,(95,85,510,380))
        pygame.draw.rect(screen,BLACK,(100,90,500,370))

        pygame.draw.line(screen,PANEL,(100,128),(600,128),(2))
        pygame.draw.line(screen,PANEL,(210,90),(210,460),(2))
        pygame.draw.line(screen,PANEL,(330,90),(330,460),(2))
        pygame.draw.line(screen,PANEL,(464,90),(464,460),(2))

        # class ID 
        screen.blit(create_font_button('Class ID'),(105,95))
        # subject ID 
        screen.blit(create_font_button('Subject ID'),(215,95))
        # Teacher ID 
        screen.blit(create_font_button('Teacher ID'),(335,95))
        # Time 
        screen.blit(create_font_button('Time'),(469,95))

        if day_schedule != []:
            for i in range(len(day_schedule)):
                # class ID
                screen.blit(create_font_button(str(day_schedule[i][0])),(115,position + 22*i))
                # subject ID 
                screen.blit(create_font_button(str(day_schedule[i][1])),(225,position + 22*i))
                # Teacher ID 
                screen.blit(create_font_button(str(day_schedule[i][3])),(345,position + 22*i))
                # Time 
                screen.blit(create_font_button(str(day_schedule[i][2])),(479,position + 22*i))
                screen.blit(create_font_button('-->'),(495,position + 22*i))
                screen.blit(create_font_button(str(day_schedule[i][2] + subject_time[day_schedule[i][2]]-1)),(520,position + 22*i))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(x_mouse,y_mouse)
                if 30 < x_mouse < 230 and 30 < y_mouse < 60:
                    pygame.draw.rect(screen,WHITE,(20,20,100,30))
                    running = False
                if 20 < x_mouse < 120 and 20 < y_mouse < 50:
                    pygame.draw.rect(screen,WHITE,(20,20,100,30))

        pygame.display.flip()
    return



def class_screen(class_schedule,subject_time):
    running = True 

    BLACK = (0,0,0)
    BACKGROUND = (214,214,214)
    PANEL = (225,255,225)

    schedule = {'Monday': [],'Tuesday':[],'Wednesday':[],'Thusday':[],'Friday':[]}
    for i in range(len(class_schedule)):
        if 1 <= class_schedule[i][2] < 12:
            schedule['Monday'].append(class_schedule[i])
        elif 12 <= class_schedule[i][2] < 24:
            class_schedule[i][2] = class_schedule[i][2] - 12
            schedule['Tuesday'].append(class_schedule[i])
        elif 24 <= class_schedule[i][2] < 36:
            class_schedule[i][2] = class_schedule[i][2] - 24 
            schedule['Wednesday'].append(class_schedule[i])
        elif 36 <= class_schedule[i][2] < 48:
            class_schedule[i][2] = class_schedule[i][2] - 36
            schedule['Thusday'].append(class_schedule[i])
        elif 48 <= class_schedule[i][2] < 60:
            class_schedule[i][2] = class_schedule[i][2] - 48
            schedule['Friday'].append(class_schedule[i])

    clock = pygame.time.Clock()
    while running:
        clock.tick(60)
        x_mouse,y_mouse = pygame.mouse.get_pos()
        pygame.draw.rect(screen,BACKGROUND,(0,0,700,500))

        # button back 
        pygame.draw.rect(screen,PANEL,(15,15,110,40))
        pygame.draw.rect(screen,BLACK,(20,20,100,30))
        screen.blit(create_font_button('BACK'),(30,22))

        # button monday 
        pygame.draw.rect(screen,PANEL,(103,90,110,40))
        pygame.draw.rect(screen,BLACK,(108,95,100,30))
        screen.blit(create_font_button('Monday'),(113,96))

        # button tuesday 
        pygame.draw.rect(screen,PANEL,(253,90,110,40))
        pygame.draw.rect(screen,BLACK,(258,95,100,30))
        screen.blit(create_font_button('Tuesday'),(263,96))
        # button wednesday
        pygame.draw.rect(screen,PANEL,(403,90,110,40))
        pygame.draw.rect(screen,BLACK,(408,95,100,30))
        screen.blit(create_font_button('Wednesday'),(406,96))

        # button thusday 
        pygame.draw.rect(screen,PANEL,(103,170,110,40))
        pygame.draw.rect(screen,BLACK,(108,175,100,30))
        screen.blit(create_font_button('Thusday'),(113,176))
        # button friday 
        pygame.draw.rect(screen,PANEL,(253,170,110,40))
        pygame.draw.rect(screen,BLACK,(258,175,100,30))
        screen.blit(create_font_button('Friday'),(263,176))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 30 < x_mouse < 230 and 30 < y_mouse < 60:
                    pygame.draw.rect(screen,WHITE,(20,20,100,30))
                    running = False
                # button monday 
                if  108 < x_mouse < 208 and 95 < y_mouse < 125 :
                    pygame.draw.rect(screen,WHITE,(108,95,100,30))
                    day = []
                    if schedule['Monday'] != []:
                        day = schedule['Monday']
                    day_screen(day,subject_time)
                # button tuesday 
                if   258 < x_mouse < 358 and 95 < y_mouse < 125:
                    pygame.draw.rect(screen,WHITE,(258,95,100,30))
                    day = []
                    if schedule['Tuesday'] != []:
                        day = schedule['Tuesday']
                    day_screen(day,subject_time)
                # button wednesday
                if   408 < x_mouse < 508  and 95 < y_mouse < 125:
                    pygame.draw.rect(screen,WHITE,(408,95,100,30))
                    day = []
                    if schedule['Wednesday'] != []:
                        day = schedule['Wednesday']
                    day_screen(day,subject_time)
                # button thurday 
                if  108 < x_mouse < 208   and 175 < y_mouse < 205:
                    pygame.draw.rect(screen,WHITE,(108,175,100,30))
                    day = []
                    if schedule['Thusday'] != []:
                        day = schedule['Thusday']
                    day_screen(day,subject_time)
                # button friday 
                if   258 < x_mouse < 358  and 175 < y_mouse < 205:
                    pygame.draw.rect(screen,WHITE,(258,175,100,30))
                    day = []
                    if schedule['Friday'] != []:
                        day = schedule['Friday']
                    day_screen(day,subject_time)
        pygame.display.flip()   
    return

    
def create_font_button(string):
    WHITE = (225,225,225)
    font = pygame.font.SysFont('sans',25)
    return font.render(string,True,WHITE)


# data to solve 
lst_class = None
lst_teacher = None
subject_time = None

# data output 
schedule = None

# creating font text
font = pygame.font.SysFont('sans' ,15)
text_color = (225,225,225)
text_position = (50,50)
user_input_lines = []
current_line = ''
data = []
active_input = False
space = False
number_class = 0
N = 0

while running:
    clock.tick(60)
    screen.fill(BACKGROUND)
    x_mouse , y_mouse = pygame.mouse.get_pos()
    
    # draw background pannel 
    pygame.draw.rect(screen,PANEL,(45,45,610,210))
    pygame.draw.rect(screen,BLACK,(50,50,600,200))

    # draw button update 
    pygame.draw.rect(screen,PANEL,(295,260,110,40))
    pygame.draw.rect(screen,BLACK,(300,265,100,30))
    screen.blit(create_font_button('UPDATE'),(305,266))

    # button reset
    pygame.draw.rect(screen,PANEL,(295,310,110,40))
    pygame.draw.rect(screen,BLACK,(300,315,100,30))
    screen.blit(create_font_button('RESET'),(305,316))
    # draw button schedule
    pygame.draw.rect(screen,PANEL,(45,373,160,40))
    pygame.draw.rect(screen,BLACK,(50,378,150,30))
    screen.blit(create_font_button('SCHEDULE'),(68,379))

    # draw button class
    pygame.draw.rect(screen,PANEL,(45,445,160,40))
    pygame.draw.rect(screen,BLACK,(50,450,150,30))
    screen.blit(create_font_button('CLASS'),(68,451))

    pygame.draw.rect(screen,PANEL,(229,445,70,40))
    pygame.draw.rect(screen,BLACK,(234,450,60,30))

    # draw button plus and minus
    pygame.draw.rect(screen,PANEL,(304,446,40,40))
    pygame.draw.rect(screen,BLACK,(309,451,30,30))
    screen.blit(create_font_button('+'),(318,452))

    pygame.draw.rect(screen,PANEL,(347,446,40,40))
    pygame.draw.rect(screen,BLACK,(352,451,30,30))
    screen.blit(create_font_button('-'),(364,450))

    # number class button
    screen.blit(create_font_button(str(number_class)),(255,453))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # button update 
            if 300< x_mouse <400 and 265< y_mouse <295 :
                pygame.draw.rect(screen,WHITE,(300,265,100,30))
                if data != []:
                    T,N,M = data[0]
                    lst_class , lst_teacher , subject_time = class_course.import_data(T,N,M,data[1:N+1],data[N+1:N+T+1],data[-1])
                    schedule = {i:[] for i in range(1,N+1)}
            # button schedule 
            if 50 < x_mouse < 200 and 378 < y_mouse < 408:
                pygame.draw.rect(screen,WHITE,(50,378,150,30))
                if lst_class != None:
                    sol = class_course.SetupModel(lst_class,lst_teacher,subject_time)
                    for i in sol:
                        schedule[i[0]].append(i)
            # button reset
            if 300 < x_mouse < 400 and 315 < y_mouse < 345:
                pygame.draw.rect(screen,WHITE,(300,315,100,30))
                current_line = ''
                user_input_lines =[]
                data = []
                lst_class = None
                lst_teacher = None
                subject_time = None
                schedule = None
                number_class = 0
                N = 0
            # button plus  
            if 309 < x_mouse < 339 and 451 < y_mouse < 481:
                pygame.draw.rect(screen,WHITE,(309,451,30,30))
                number_class += 1
                if number_class > N and N != 0:
                    number_class = N
            # button minus 
            if 352 < x_mouse < 382 and 451 < y_mouse < 481:
                pygame.draw.rect(screen,WHITE,(352,451,30,30))
                number_class -= 1
                if number_class < 0:
                    number_class = 0
            # button class
            if 50 < x_mouse < 200 and 450 < y_mouse < 480:
                pygame.draw.rect(screen,WHITE,(50,450,150,30))
                Class = []
                if schedule != None:
                    Class = schedule[number_class]
                class_screen(Class,subject_time)
            if 50 < x_mouse < 650 and 50 < y_mouse < 250:
                pygame.draw.rect(screen,WHITE,(50,50,600,200))
                active_input = True
            else:
                active_input = False
        if event.type == pygame.KEYDOWN and active_input:
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print("data : ", current_line)
                        data.append(list(map(int,current_line.split())))
                        user_input_lines.append(current_line)
                        current_line = ""
                    elif event.key == pygame.K_BACKSPACE:
                        if current_line is not None:
                            current_line = current_line[:-1]
                        elif current_line != []:
                            current_line = user_input_lines[-1]
                            user_input_lines = user_input_lines[:-1]
                    elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        # Paste from clipboard
                        clipboard_text = pyperclip.paste()
                        clipboard_text = clipboard_text.splitlines()
                        for i in range(len(clipboard_text)-1):
                            data.append(list(map(int,clipboard_text[i].split())))
                            user_input_lines.append(clipboard_text[i])
                        data.append(list(map(int,clipboard_text[-1].split())))
                        current_line += clipboard_text[-1]
                    else:
                        current_line += event.unicode
    # print text on textinput box
    if len(user_input_lines) >= 10:
        user_input_lines.pop(0)
    if current_line != '':
        for i, line in enumerate(user_input_lines):
            text_surface = font.render(line, True, text_color)
            screen.blit(text_surface, (text_position[0], text_position[1] + i * 20))
    if current_line != '':
        current_line_surface = font.render(current_line, True, text_color)
        screen.blit(current_line_surface, (text_position[0], text_position[1] + len(user_input_lines) * 20))

    pygame.display.flip()
pygame.quit()



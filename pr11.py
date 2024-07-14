import tkinter
import random
from math import fabs, sqrt


def do_nothing(x):
    pass


def move_wrap(obj, move):
    canvas.move(obj, move[0], move[1])
    if canvas.coords(obj)[1] >= N_Y * step:
        canvas.move(obj, 0, -N_Y * step)
    if canvas.coords(obj)[0] >= N_X * step:
        canvas.move(obj, -N_X * step, 0)
    if canvas.coords(obj)[1] < 0:
        canvas.move(obj, 0, N_Y * step)
    if canvas.coords(obj)[0] < 0:
        canvas.move(obj, N_X * step, 0)


def check_move():
    global weapon_flag, count_wins, count_losses
    if canvas.coords(player) == canvas.coords(exit):
        if label['text'] != 'Ты проиграл!':
            label.config(text="Победа!", fg='lime')
        master.bind("<KeyPress>", do_nothing)
    if canvas.coords(player) == canvas.coords(weapon):
        label.config(text="Вы подобрали Glock-17! Чтобы использовать, нажмите f", fg='DodgerBlue3')
        canvas.delete(weapon)
        canvas.itemconfig(player, image=armed_player_pic)
        weapon_flag = 1
    for f in fires:
        if canvas.coords(player) == canvas.coords(f):
            label.config(text="Ты проиграл!", fg='red')
            master.bind("<KeyPress>", do_nothing)
    for e in enemies:
        if canvas.coords(player) == canvas.coords(e[0]):
            label.config(text="Ты проиграл!", fg='red')
            master.bind("<KeyPress>", do_nothing)
    if label['text'] == 'Победа!':
        count_wins += 0.5
        label_wins.config(text=f"Побед: {int(count_wins)}")
    if label['text'] == 'Ты проиграл!':
        if count_losses.is_integer():
            count_losses += 1
        else:
            count_losses += 0.5
        label_losses.config(text=f"Поражений: {int(count_losses)}")


def kill_closest_enemy():
    global weapon_flag, count_kills
    m = 999
    m_i = 0
    pl = canvas.coords(player)
    for enemy in enemies:
        en = canvas.coords(enemy[0])
        distance = sqrt((en[0] - pl[0]) ** 2 + (en[1] - pl[1]) ** 2)
        if distance < m:
            m = distance
            m_i = enemies.index(enemy)
    canvas.delete(enemies[m_i][0])
    enemies.pop(m_i)
    weapon_flag = 0
    label.config(text="Найди выход!")
    canvas.itemconfig(player, image=player_pic)
    count_kills += 1
    label_kills.config(text=f'Убийств: {count_kills}')


def key_pressed(event):
    global weapon_flag
    checks_flag = 1
    if event.keysym == 'Up':
        move_wrap(player, (0, -step))
    if event.keysym == 'Down':
        move_wrap(player, (0, step))
    if event.keysym == 'Left':
        move_wrap(player, (-step, 0))
    if event.keysym == 'Right':
        move_wrap(player, (step, 0))
    if (event.keysym == 'f') and weapon_flag:
        kill_closest_enemy()
    check_move()
    if label['text'] == 'Ты проиграл!':
        checks_flag = 0
    for enemy in enemies:
        direction = enemy[1](canvas.coords(enemy[0]))
        move_wrap(enemy[0], direction)
    if checks_flag:
        check_move()


def always_right(c):
    return (step, 0)


def random_move(c):
    return random.choice([(step, 0), (-step, 0), (0, step), (0, -step)])


def move_towards_player(en):
    pl = canvas.coords(player)
    step_x = 0
    step_y = 0
    if pl[0] > en[0]:
        step_x = step
    elif pl[0] < en[0]:
        step_x = -step
    if pl[1] > en[1]:
        step_y = step
    elif pl[1] < en[1]:
        step_y = -step
    return step_x, step_y


def prepare_and_start():
    global player, exit, fires, enemies, player_pos, enemy_pos, weapon, weapon_pos
    canvas.delete("all")
    exceptions = []
    player_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
    exceptions.append(player_pos)
    while True:
        weapon_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
        if weapon_pos not in exceptions:
            break
    exceptions.append(weapon_pos)
    weapon = canvas.create_image((weapon_pos[0], weapon_pos[1]), image=weapon_pic, anchor='nw')
    while True:
        exit_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
        if exit_pos not in exceptions:
            break
    exceptions.append(exit_pos)
    player = canvas.create_image((player_pos[0], player_pos[1]), image=player_pic, anchor='nw')
    exit = canvas.create_image((exit_pos[0], exit_pos[1]), image=exit_pic, anchor='nw')
    N_FIRES = 6
    fires = []
    for i in range(N_FIRES):
        while True:
            fire_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
            if fire_pos not in exceptions:
                break
        exceptions.append(fire_pos)
        fire = canvas.create_image((fire_pos[0], fire_pos[1]), image=fire_pic, anchor='nw')
        fires.append(fire)
    N_ENEMIES = 4
    enemies = []
    for i in range(N_ENEMIES):
        while True:
            enemy_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
            if enemy_pos not in exceptions:
                break
        exceptions.append(enemy_pos)
        enemy = canvas.create_image(enemy_pos, image=enemy_pic, anchor='nw')
        enemies.append((enemy, random.choice([always_right, random_move, move_towards_player])))
    label.config(text="Найди выход!", fg='DodgerBlue3')
    master.bind("<KeyPress>", key_pressed)


step = 60
N_X = 18
N_Y = 12
count_wins = 0
count_losses = 0.0
count_kills = 0
weapon_flag = 0
master = tkinter.Tk()
label = tkinter.Label(master, text="Найди выход", font=('Comic Sans MS', 20, 'bold'))
label.pack()
label_wins = tkinter.Label(master, text=f"Побед: {count_wins}", fg='green', font=('Comic Sans MS', 15))
label_losses = tkinter.Label(master, text=f"Поражений: {int(count_losses)}", fg='red', font=('Comic Sans MS', 15))
label_kills = tkinter.Label(master, text=f"Убийств: {int(count_kills)}", fg='DarkRed', font=('Comic Sans MS', 15))
label_wins.pack()
label_losses.pack()
label_kills.pack()
canvas = tkinter.Canvas(master, bg='BlanchedAlmond', height=N_Y * step, width=N_X * step)
canvas.pack()
restart = tkinter.Button(master, text="Начать заново", command=prepare_and_start,
                         bg='grey79', fg='cyan4', font=('Comic Sans MS', 20, 'bold'), cursor='hand2')
restart.pack()
player_pic = tkinter.PhotoImage(file="cat.png")
exit_pic = tkinter.PhotoImage(file="exit.png")
fire_pic = tkinter.PhotoImage(file="fire.png")
enemy_pic = tkinter.PhotoImage(file="dog.png")
weapon_pic = tkinter.PhotoImage(file='weapon.png')
armed_player_pic = tkinter.PhotoImage(file='cat_with_gun.png')
prepare_and_start()
master.mainloop()


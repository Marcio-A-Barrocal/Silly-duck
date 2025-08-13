import tkinter as tk
from PIL import Image, ImageTk
import os
import pyautogui
import random
from . import automation

# ... (variáveis globais continuam as mesmas)
pos_x, pos_y = 300, 300
dir_x, dir_y = 1, 0
speed = 7
walk_sprite_index = 0
sprites_right, sprites_left = [], []
is_idle, is_following_mouse = True, False
target_x, target_y = 0, 0
idle_sprite_index = 0
sprites_idle = []
# ...



# --- MODIFICADO ---
def follow_mouse_step():
    """Calcula um passo em direção ao mouse e age quando chega."""
    global pos_x, pos_y, dir_x, dir_y, is_following_mouse

    # TRACKING DINÂMICO: Atualiza a posição do mouse a cada passo!
    mouse_x, mouse_y = pyautogui.position()
    target_x, target_y = mouse_x - 64, mouse_y - 64
    
    dx, dy = target_x - pos_x, target_y - pos_y
    distance = (dx**2 + dy**2)**0.5

    if distance < speed:
        is_following_mouse = False
        print("[DUCK ACTION] Peguei o mouse!")
        
        # DECISÃO: Decide aleatoriamente qual ação executar no mouse
        if random.random() < 0.5: # 50% de chance
            automation.annoy_mouse()
        else:
            # Para a ação de puxar, precisamos saber a direção do pato
            automation.drag_mouse_with_beak(dir_x)

        # Fica parado por um tempo MENOR depois da ação
        start_idle(2) 
        return

    # Atualiza a direção do sprite (esquerda/direita) com base no movimento
    if dx > 0:
        dir_x = 1
    elif dx < 0:
        dir_x = -1
    
    dir_y = dy / distance # Normaliza o vetor de direção
    
    # Move o pato
    pos_x += dir_x * speed * abs(dx/distance) # Pondera a velocidade
    pos_y += dir_y * speed

def start_idle(duration_seconds):
    """Faz o pato entrar no estado 'parado' por um tempo."""
    global is_idle, root_ref
    is_idle = True
    print(f"[DUCK STATE] Descansando por {duration_seconds} segundos.")
    root_ref.after(duration_seconds * 1000, stop_idle)

# ... (O resto do arquivo `window.py` pode continuar exatamente o mesmo da resposta anterior)
# Incluindo move_duck, random_walk_step, start_follow_mouse, stop_idle, e create_window
# A única mudança crucial foi dentro de `follow_mouse_step`.

# Cole o resto do seu código de `window.py` aqui. Se precisar, posso fornecer o arquivo completo novamente.
# Para garantir, aqui está o resto do arquivo para evitar erros:

def move_duck(root, label):
    global walk_sprite_index, idle_sprite_index, dir_x
    if is_following_mouse:
        follow_mouse_step()
    elif not is_idle:
        random_walk_step(root)
    if is_idle:
        idle_sprite_index = (idle_sprite_index + 1) % len(sprites_idle)
        current_sprite = sprites_idle[idle_sprite_index]
    else:
        walk_sprite_index = (walk_sprite_index + 1) % len(sprites_right)
        # Corrige a direção para garantir o sprite certo mesmo ao seguir o mouse
        current_sprite = sprites_right[walk_sprite_index] if dir_x >= 0 else sprites_left[walk_sprite_index]
    label.config(image=current_sprite)
    label.image = current_sprite
    root.geometry(f"128x128+{int(pos_x)}+{int(pos_y)}")
    root.after(100, lambda: move_duck(root, label))

def random_walk_step(root):
    global pos_x, pos_y, dir_x, dir_y
    if random.random() < 0.02:
        dir_x = random.choice([-1, 1])
        dir_y = random.choice([-1, 0, 1])
    pos_x += dir_x * speed
    pos_y += dir_y * speed
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    if pos_x <= 0 or pos_x >= screen_width - 128: dir_x *= -1
    if pos_y <= 0 or pos_y >= screen_height - 128: dir_y *= -1

def start_follow_mouse():
    global is_following_mouse, is_idle
    is_idle = False
    is_following_mouse = True
    print("[DUCK ACTION] Caçando o mouse!")

def stop_idle():
    global is_idle
    is_idle = False
    print("[DUCK STATE] Voltando a andar...")

def create_window():
    global sprites_right, sprites_left, sprites_idle, root_ref
    root = tk.Tk()
    root_ref = root
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    transparent_color = "#ff00ff"
    root.configure(bg=transparent_color)
    root.wm_attributes("-transparentcolor", transparent_color)
    # CARREGANDO SPRITES DE ANDAR
    for i in range(1, 7):
        img_path = os.path.join("images", f"walk{i}.png")
        if not os.path.exists(img_path): continue
        img = Image.open(img_path).convert("RGBA")
        new_data = []
        for item in img.getdata():
            r, g, b, a = item
            if a < 255 or (r == 255 and g < 50 and b == 255): new_data.append((255, 255, 255, 0))
            else: new_data.append(item)
        img.putdata(new_data)
        img = img.resize((64, 64), Image.Resampling.NEAREST)
        img_tk = ImageTk.PhotoImage(img)
        sprites_right.append(img_tk)
        img_left = img.transpose(Image.FLIP_LEFT_RIGHT)
        sprites_left.append(ImageTk.PhotoImage(img_left))
    # CARREGANDO SPRITES IDLE
    i = 1
    while True:
        img_path = os.path.join("images", f"idle{i}.png")
        if not os.path.exists(img_path): break
        img = Image.open(img_path).convert("RGBA")
        new_data = []
        for item in img.getdata():
            r, g, b, a = item
            if a < 255 or (r == 255 and g < 50 and b == 255): new_data.append((255, 255, 255, 0))
            else: new_data.append(item)
        img.putdata(new_data)
        img = img.resize((64, 64), Image.Resampling.NEAREST)
        sprites_idle.append(ImageTk.PhotoImage(img))
        i += 1
    if not sprites_idle: sprites_idle.append(sprites_right[0])
    label = tk.Label(root, image=sprites_idle[0], bg=transparent_color)
    label.pack()
    move_duck(root, label)
    root.mainloop()
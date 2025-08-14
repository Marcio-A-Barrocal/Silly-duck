import tkinter as tk
from PIL import Image, ImageTk
import os
import pyautogui
import random
from . import automation

# =============================================================================
# VARIÁVEIS GLOBAIS - Estado do pato
# =============================================================================
pos_x, pos_y = 300, 300  # Posição atual do pato na tela
dir_x, dir_y = 1, 0      # Direção do movimento (-1=esquerda, 1=direita)
speed = 7                # Velocidade do movimento

# Estados do pato
is_idle = False          # Inicia andando normalmente (mudado de True para False)
is_following_mouse = False  # Se está perseguindo o mouse
is_pulling_mouse = False    # Se está puxando o mouse

# Controle de sprites/animação
walk_sprite_index = 0    # Índice da animação de caminhada
idle_sprite_index = 0    # Índice da animação parada
pull_sprite_index = 0    # Índice da animação de puxar
sprites_right = []       # Sprites caminhando para direita
sprites_left = []        # Sprites caminhando para esquerda  
sprites_idle = []        # Sprites parado/idle
sprites_pull_right = []  # Sprites puxando para direita
sprites_pull_left = []   # Sprites puxando para esquerda

root_ref = None          # Referência da janela principal
pull_timer = 0           # Timer para controlar duração da animação de puxar
pull_cooldown = 0        # Cooldown para evitar puxões consecutivos

# =============================================================================
# SISTEMA DE MOVIMENTO
# =============================================================================

def follow_mouse_step():
    """
    FAZ O PATO SEGUIR O MOUSE: Calcula um passo em direção ao cursor.
    Quando chega perto o suficiente, executa uma ação no mouse.
    """
    global pos_x, pos_y, dir_x, dir_y, is_following_mouse

    # TRACKING DINÂMICO: Sempre pega a posição atual do mouse
    mouse_x, mouse_y = pyautogui.position()
    # Ajusta para o centro do pato (64x64 pixels)
    target_x, target_y = mouse_x - 64, mouse_y - 64
    
    # Calcula distância até o mouse
    dx = target_x - pos_x
    dy = target_y - pos_y
    distance = (dx**2 + dy**2)**0.5

    # Se chegou perto o suficiente (menor que velocidade)
    if distance < speed:
        is_following_mouse = False
        print("[DUCK ACTION] Peguei o mouse!")
        
        # Verifica cooldown antes de permitir puxar novamente
        global pull_cooldown
        if pull_cooldown <= 0:
            # DECISÃO: 50% de chance para cada ação
            if random.random() < 0.5:
                automation.annoy_mouse()           # Chacoalha o mouse
                start_idle(2)  # Descansa após chacoalhar
            else:
                start_pulling_mouse()              # Inicia animação de puxar
                automation.drag_mouse_with_beak(dir_x)  # Puxa o mouse (em thread)
                pull_cooldown = 50  # 5 segundos de cooldown (50 * 100ms)
        else:
            # Se está em cooldown, só chacoalha
            automation.annoy_mouse()
            start_idle(2)

        return

    # Atualiza direção do sprite baseado no movimento
    if dx > 0:
        dir_x = 1    # Olhando para direita
    elif dx < 0:
        dir_x = -1   # Olhando para esquerda
    
    # Normaliza a direção vertical
    dir_y = dy / distance if distance > 0 else 0
    
    # Move o pato em direção ao mouse
    if distance > 0:
        pos_x += dir_x * speed * abs(dx/distance)  # Movimento ponderado
        pos_y += dir_y * speed

def random_walk_step(root):
    """
    MOVIMENTO ALEATÓRIO: Faz o pato andar pela tela de forma randômica.
    """
    global pos_x, pos_y, dir_x, dir_y
    
    # 2% de chance de mudar direção a cada passo
    if random.random() < 0.02:
        dir_x = random.choice([-1, 1])      # Esquerda ou direita
        dir_y = random.choice([-1, 0, 1])   # Cima, meio ou baixo

    # Move o pato
    pos_x += dir_x * speed
    pos_y += dir_y * speed

    # COLISÃO COM BORDAS: Inverte direção se sair da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    if pos_x <= 0 or pos_x >= screen_width - 128:
        dir_x *= -1  # Inverte direção horizontal
    if pos_y <= 0 or pos_y >= screen_height - 128:
        dir_y *= -1  # Inverte direção vertical

# =============================================================================
# CONTROLE DE ESTADOS
# =============================================================================

def start_follow_mouse():
    """
    Inicia o modo de perseguição ao mouse.
    """
    global is_following_mouse, is_idle
    is_idle = False
    is_following_mouse = True
    print("[DUCK ACTION] Caçando o mouse!")

def start_pulling_mouse():
    """
    Inicia a animação de puxar o mouse.
    """
    global is_pulling_mouse, is_idle, pull_timer
    is_idle = False
    is_pulling_mouse = True
    pull_timer = 12  # 1.2 segundos para sincronizar com ação de puxar
    print("[DUCK STATE] Puxando o mouse!")

def stop_pulling_mouse():
    """
    Para a animação de puxar e volta ao estado normal.
    """
    global is_pulling_mouse
    is_pulling_mouse = False
    start_idle(3)  # Descansa mais tempo após puxar
    print("[DUCK STATE] Terminou de puxar!")

def start_idle(duration_seconds):
    """
    Faz o pato ficar parado por um tempo determinado.
    """
    global is_idle, root_ref
    is_idle = True
    print(f"[DUCK STATE] Descansando por {duration_seconds} segundos.")
    # Agenda para parar de descansar após o tempo
    root_ref.after(duration_seconds * 1000, stop_idle)

def stop_idle():
    """
    Para o estado de descanso e volta ao movimento normal.
    """
    global is_idle
    is_idle = False
    print("[DUCK STATE] Voltando a andar...")

# =============================================================================
# SISTEMA DE ANIMAÇÃO
# =============================================================================

def move_duck(root, label):
    """
    LOOP PRINCIPAL DE ANIMAÇÃO: Atualiza movimento, sprite e posição.
    Chama a si mesma a cada 100ms para criar animação fluida.
    """
    global walk_sprite_index, idle_sprite_index, pull_sprite_index, dir_x, pull_timer, pull_cooldown

    # Reduz cooldown do puxar
    if pull_cooldown > 0:
        pull_cooldown -= 1

    # DECIDE O MOVIMENTO baseado no estado
    if is_pulling_mouse:
        # Durante o puxão, o pato "anda para trás" sutilmente
        pull_timer -= 1
        
        # Simula o pato sendo "puxado" junto com o mouse
        backward_speed = 2  # Velocidade reduzida do movimento para trás
        pos_x_offset = -dir_x * backward_speed  # Movimento na direção oposta
        pos_y_offset = random.uniform(-0.5, 0.5)  # Pequena variação vertical
        
        # Atualiza posição do pato para simular o "esforço" de puxar
        global pos_x, pos_y
        pos_x += pos_x_offset
        pos_y += pos_y_offset
        
        # Verifica bordas durante o puxão
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        if pos_x <= 0: pos_x = 0
        if pos_x >= screen_width - 128: pos_x = screen_width - 128
        if pos_y <= 0: pos_y = 0
        if pos_y >= screen_height - 128: pos_y = screen_height - 128
        
        if pull_timer <= 0:
            stop_pulling_mouse()
    elif is_following_mouse:
        follow_mouse_step()         # Persegue o mouse
    elif not is_idle:
        random_walk_step(root)      # Caminha aleatoriamente
    # Se is_idle=True, fica parado

    # ESCOLHE O SPRITE baseado no estado e direção
    if is_pulling_mouse:
        # Anima sprites de puxar mais devagar para parecer mais esforçado
        if walk_sprite_index % 2 == 0:  # Atualiza sprite a cada 2 frames
            pull_sprite_index = (pull_sprite_index + 1) % len(sprites_pull_right)
        if dir_x >= 0:  # Olhando/puxando para direita
            current_sprite = sprites_pull_right[pull_sprite_index]
        else:           # Olhando/puxando para esquerda
            current_sprite = sprites_pull_left[pull_sprite_index]
    elif is_idle:
        # Anima sprites de parado
        idle_sprite_index = (idle_sprite_index + 1) % len(sprites_idle)
        current_sprite = sprites_idle[idle_sprite_index]
    else:
        # Anima sprites de caminhada
        walk_sprite_index = (walk_sprite_index + 1) % len(sprites_right)
        if dir_x >= 0:  # Olhando para direita
            current_sprite = sprites_right[walk_sprite_index]
        else:           # Olhando para esquerda
            current_sprite = sprites_left[walk_sprite_index]

    # Atualiza a imagem e posição da janela
    label.config(image=current_sprite)
    label.image = current_sprite  # Evita garbage collection
    root.geometry(f"128x128+{int(pos_x)}+{int(pos_y)}")
    
    # Agenda próxima atualização em 100ms
    root.after(100, lambda: move_duck(root, label))

# =============================================================================
# CRIAÇÃO DA JANELA
# =============================================================================

def create_window():
    """
    FUNÇÃO PRINCIPAL: Cria a janela, carrega sprites e inicia animação.
    """
    global sprites_right, sprites_left, sprites_idle, sprites_pull_right, sprites_pull_left, root_ref

    # CONFIGURAÇÃO DA JANELA
    root = tk.Tk()
    root_ref = root
    root.overrideredirect(True)        # Remove barra de título
    root.attributes("-topmost", True)   # Sempre por cima
    
    # TRANSPARÊNCIA: Usa cor magenta como transparente
    transparent_color = "#ff00ff"
    root.configure(bg=transparent_color)
    root.wm_attributes("-transparentcolor", transparent_color)

    # CARREGAMENTO DE SPRITES DE CAMINHADA
    for i in range(1, 7):  # walk1.png até walk6.png
        img_path = os.path.join("images", f"walk{i}.png")
        if not os.path.exists(img_path):
            continue
            
        # Carrega e processa imagem
        img = Image.open(img_path).convert("RGBA")
        
        # Remove fundo magenta e torna transparente
        new_data = []
        for item in img.getdata():
            r, g, b, a = item
            # Se pixel é magenta ou transparente
            if a < 255 or (r == 255 and g < 50 and b == 255):
                new_data.append((255, 255, 255, 0))  # Transparente
            else:
                new_data.append(item)  # Mantém pixel
        img.putdata(new_data)
        
        # Redimensiona para 64x64
        img = img.resize((64, 64), Image.Resampling.NEAREST)
        img_tk = ImageTk.PhotoImage(img)
        sprites_right.append(img_tk)
        
        # Cria versão espelhada para esquerda
        img_left = img.transpose(Image.FLIP_LEFT_RIGHT)
        sprites_left.append(ImageTk.PhotoImage(img_left))

    # CARREGAMENTO DE SPRITES IDLE/PARADO
    i = 1
    while True:
        img_path = os.path.join("images", f"idle{i}.png")
        if not os.path.exists(img_path):
            break
            
        # Mesmo processamento dos sprites de caminhada
        img = Image.open(img_path).convert("RGBA")
        new_data = []
        for item in img.getdata():
            r, g, b, a = item
            if a < 255 or (r == 255 and g < 50 and b == 255):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        
        img = img.resize((64, 64), Image.Resampling.NEAREST)
        sprites_idle.append(ImageTk.PhotoImage(img))
        i += 1

    # Se não tem sprites idle, usa o primeiro sprite de caminhada
    if not sprites_idle:
        sprites_idle.append(sprites_right[0])

    # CARREGAMENTO DE SPRITES DE PUXAR (pull1.png, pull2.png)
    for i in range(1, 3):  # pull1.png e pull2.png
        img_path = os.path.join("images", f"pull{i}.png")
        if not os.path.exists(img_path):
            continue
            
        # Mesmo processamento dos outros sprites
        img = Image.open(img_path).convert("RGBA")
        new_data = []
        for item in img.getdata():
            r, g, b, a = item
            if a < 255 or (r == 255 and g < 50 and b == 255):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        
        img = img.resize((64, 64), Image.Resampling.NEAREST)
        img_tk = ImageTk.PhotoImage(img)
        sprites_pull_right.append(img_tk)
        
        # Cria versão espelhada para esquerda
        img_left = img.transpose(Image.FLIP_LEFT_RIGHT)
        sprites_pull_left.append(ImageTk.PhotoImage(img_left))

    # Se não tem sprites idle, usa sprites de caminhada como fallback
    if not sprites_pull_right:
        sprites_pull_right = sprites_right.copy()
        sprites_pull_left = sprites_left.copy()

    # CRIA O LABEL COM A IMAGEM - Inicia com sprite de caminhada
    label = tk.Label(root, image=sprites_right[0], bg=transparent_color)
    label.pack()

    # INICIA A ANIMAÇÃO
    move_duck(root, label)
    
    # INICIA O LOOP DA INTERFACE GRÁFICA
    root.mainloop()
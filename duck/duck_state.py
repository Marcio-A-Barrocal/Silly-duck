# duck_state.py
"""
Gerencia todos os estados e variáveis globais do pato.
"""
import random

# ... (o resto do arquivo permanece igual até a função start_fleeing)
# =============================================================================
# VARIÁVEIS DE POSIÇÃO E MOVIMENTO
# =============================================================================
pos_x, pos_y = 300, 300
dir_x, dir_y = 1, 0
base_speed = 7
flee_speed = 13
current_speed = base_speed

# =============================================================================
# VARIÁVEIS DE ESTADO
# =============================================================================
is_idle = False
is_following_mouse = False
is_pulling_mouse = False
is_fleeing = False

# =============================================================================
# VARIÁVEIS DE CONTROLE DE ANIMAÇÃO
# =============================================================================
walk_sprite_index = 0
idle_sprite_index = 0
pull_sprite_index = 0
pull_timer = 0
pull_cooldown = 0
bounce_sprite_index = 0 

# =============================================================================
# REFERÊNCIAS
# =============================================================================
root_ref = None

# =============================================================================
# FUNÇÕES DE CONTROLE DE ESTADO
# =============================================================================
def start_follow_mouse():
    global is_following_mouse, is_idle, is_fleeing
    is_idle = False
    is_fleeing = False
    is_following_mouse = True
    print("[DUCK ACTION] Caçando o mouse!")

def start_pulling_mouse():
    global is_pulling_mouse, is_idle, pull_timer
    is_idle = False
    is_pulling_mouse = True
    pull_timer = 12
    print("[DUCK STATE] Puxando o mouse!")

def stop_pulling_mouse():
    global is_pulling_mouse
    is_pulling_mouse = False
    start_idle(3)
    print("[DUCK STATE] Terminou de puxar!")

def start_idle(duration_seconds):
    global is_idle, root_ref
    is_idle = True
    print(f"[DUCK STATE] Descansando por {duration_seconds} segundos.")
    if root_ref:
        root_ref.after(duration_seconds * 1000, stop_idle)

def stop_idle():
    global is_idle
    is_idle = False
    print("[DUCK STATE] Voltando a andar...")

def start_fleeing():
    """ 
    MODIFICADO: Ativa o estado de fuga e agenda o fim da fuga.
    """
    global is_fleeing, is_following_mouse, is_idle, current_speed, root_ref
    if not is_fleeing:
        print("[DUCK STATE] Fui clicado! FUGINDDOOO!")
        is_fleeing = True
        is_following_mouse = False
        is_idle = False
        bounce_sprite_index = 0 
        current_speed = flee_speed
        
        # Agenda o fim da fuga para um tempo aleatório entre 2 e 4 segundos
        flee_duration_ms = random.randint(2000, 4000)
        if root_ref:
            root_ref.after(flee_duration_ms, stop_fleeing)

def stop_fleeing():
    """
    Desativa o estado de fuga. Chamado automaticamente após um tempo.
    """
    global is_fleeing, current_speed
    if is_fleeing:
        print("[DUCK STATE] Ufa, escapei.")
        is_fleeing = False
        current_speed = base_speed
        start_idle(2)

def set_root_reference(root):
    global root_ref
    root_ref = root

def update_cooldown():
    global pull_cooldown
    if pull_cooldown > 0:
        pull_cooldown -= 1

def update_pull_timer():
    global pull_timer
    if pull_timer > 0:
        pull_timer -= 1
        return True
    return False
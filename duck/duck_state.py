# duck_state.py
"""
Gerencia todos os estados e variáveis globais do pato.
Centraliza o controle de estado em um só lugar.
"""

# =============================================================================
# VARIÁVEIS DE POSIÇÃO E MOVIMENTO
# =============================================================================
pos_x, pos_y = 300, 300  # Posição atual do pato na tela
dir_x, dir_y = 1, 0      # Direção do movimento (-1=esquerda, 1=direita)
speed = 7                # Velocidade do movimento

# =============================================================================
# VARIÁVEIS DE ESTADO
# =============================================================================
is_idle = False          # Inicia andando normalmente
is_following_mouse = False  # Se está perseguindo o mouse
is_pulling_mouse = False    # Se está puxando o mouse

# =============================================================================
# VARIÁVEIS DE CONTROLE DE ANIMAÇÃO
# =============================================================================
walk_sprite_index = 0    # Índice da animação de caminhada
idle_sprite_index = 0    # Índice da animação parada
pull_sprite_index = 0    # Índice da animação de puxar

pull_timer = 0           # Timer para controlar duração da animação de puxar
pull_cooldown = 0        # Cooldown para evitar puxões consecutivos

# =============================================================================
# REFERÊNCIAS
# =============================================================================
root_ref = None          # Referência da janela principal

# =============================================================================
# FUNÇÕES DE CONTROLE DE ESTADO
# =============================================================================

def start_follow_mouse():
    """Inicia o modo de perseguição ao mouse."""
    global is_following_mouse, is_idle
    is_idle = False
    is_following_mouse = True
    print("[DUCK ACTION] Caçando o mouse!")

def start_pulling_mouse():
    """Inicia a animação de puxar o mouse."""
    global is_pulling_mouse, is_idle, pull_timer
    is_idle = False
    is_pulling_mouse = True
    pull_timer = 12  # 1.2 segundos para sincronizar com ação de puxar
    print("[DUCK STATE] Puxando o mouse!")

def stop_pulling_mouse():
    """Para a animação de puxar e volta ao estado normal."""
    global is_pulling_mouse
    is_pulling_mouse = False
    start_idle(3)  # Descansa mais tempo após puxar
    print("[DUCK STATE] Terminou de puxar!")

def start_idle(duration_seconds):
    """Faz o pato ficar parado por um tempo determinado."""
    global is_idle, root_ref
    is_idle = True
    print(f"[DUCK STATE] Descansando por {duration_seconds} segundos.")
    # Agenda para parar de descansar após o tempo
    if root_ref:
        root_ref.after(duration_seconds * 1000, stop_idle)

def stop_idle():
    """Para o estado de descanso e volta ao movimento normal."""
    global is_idle
    is_idle = False
    print("[DUCK STATE] Voltando a andar...")

def set_root_reference(root):
    """Define a referência da janela principal."""
    global root_ref
    root_ref = root

def update_cooldown():
    """Atualiza o cooldown do puxar. Deve ser chamado a cada frame."""
    global pull_cooldown
    if pull_cooldown > 0:
        pull_cooldown -= 1

def update_pull_timer():
    """Atualiza o timer de puxar. Retorna True se ainda está puxando."""
    global pull_timer
    if pull_timer > 0:
        pull_timer -= 1
        return True
    return False
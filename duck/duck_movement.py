# duck_movement.py
"""
Sistema de movimento do pato.
Contém toda a lógica de movimentação e pathfinding.
"""

import pyautogui
import random
from . import duck_state
from . import duck_actions


def flee_from_mouse_step(root):
    """
    FAZ O PATO FUGIR DO MOUSE.
    Calcula um passo na direção OPOSTA ao cursor.
    """
    mouse_x, mouse_y = pyautogui.position()
    
    # Calcula o vetor de direção para LONGE do mouse
    dx = duck_state.pos_x - (mouse_x - 64)
    dy = duck_state.pos_y - (mouse_y - 64)
    distance = (dx**2 + dy**2)**0.5

    # Normaliza o vetor de direção
    if distance > 0:
        dir_fx = dx / distance
        dir_fy = dy / distance
    else:
        # Se o mouse estiver exatamente no mesmo lugar, corre para uma direção aleatória
        dir_fx, dir_fy = random.choice([-1, 1]), random.choice([-1, 1])

    # Atualiza a direção do sprite do pato
    if dir_fx > 0:
        duck_state.dir_x = 1
    elif dir_fx < 0:
        duck_state.dir_x = -1
    
    # Move o pato na direção de fuga
    duck_state.pos_x += dir_fx * duck_state.current_speed
    duck_state.pos_y += dir_fy * duck_state.current_speed

    # Garante que ele não fuja para fora da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    duck_state.pos_x = max(0, min(duck_state.pos_x, screen_width - 128))
    duck_state.pos_y = max(0, min(duck_state.pos_y, screen_height - 128))


def follow_mouse_step():
    """
    FAZ O PATO SEGUIR O MOUSE: Calcula um passo em direção ao cursor.
    """
    mouse_x, mouse_y = pyautogui.position()
    target_x, target_y = mouse_x - 64, mouse_y - 64
    
    dx = target_x - duck_state.pos_x
    dy = target_y - duck_state.pos_y
    distance = (dx**2 + dy**2)**0.5

    if distance < duck_state.current_speed:
        duck_state.is_following_mouse = False
        print("[DUCK ACTION] Peguei o mouse!")
        
        if duck_state.pull_cooldown <= 0:
            if random.random() < 0.5:
                duck_actions.annoy_mouse()
                duck_state.start_idle(2)
            else:
                duck_state.start_pulling_mouse()
                duck_actions.drag_mouse_with_beak(duck_state.dir_x)
                duck_state.pull_cooldown = 50
        else:
            duck_actions.annoy_mouse()
            duck_state.start_idle(2)
        return

    if dx > 0:
        duck_state.dir_x = 1
    elif dx < 0:
        duck_state.dir_x = -1
    
    duck_state.dir_y = (dy / distance) * 0.8 if distance > 0 else 0
    
    if distance > 0:
        duck_state.pos_x += duck_state.dir_x * duck_state.current_speed * abs(dx/distance)
        duck_state.pos_y += duck_state.dir_y * duck_state.current_speed * 0.85


def random_walk_step(root):
    """
    MOVIMENTO ALEATÓRIO: Faz o pato andar pela tela de forma randômica.
    """
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    margin = 50
    
    if duck_state.pos_x <= margin:
        duck_state.dir_x = 1
    elif duck_state.pos_x >= screen_width - 128 - margin:
        duck_state.dir_x = -1
    elif duck_state.pos_y <= margin:
        duck_state.dir_y = 1
    elif duck_state.pos_y >= screen_height - 128 - margin:
        duck_state.dir_y = -1
    else:
        if random.random() < 0.03:
            if random.random() < 0.80:
                vertical_change = random.random()
                if vertical_change < 0.60:
                    pass
                elif vertical_change < 0.80:
                    duck_state.dir_y = max(-1, duck_state.dir_y - 0.3)
                else:
                    duck_state.dir_y = min(1, duck_state.dir_y + 0.3)
            else:
                duck_state.dir_x = random.choice([-1, 1])
                duck_state.dir_y = random.uniform(-0.5, 0.5)

    duck_state.pos_x += duck_state.dir_x * duck_state.current_speed
    duck_state.pos_y += duck_state.dir_y * duck_state.current_speed

    duck_state.pos_x = max(0, min(duck_state.pos_x, screen_width - 128))
    duck_state.pos_y = max(0, min(duck_state.pos_y, screen_height - 128))


def handle_pulling_movement(root):
    """
    Lida com o movimento especial durante o estado de puxar o mouse.
    Retorna True se ainda está puxando, False se terminou.
    """
    # Se o timer do puxão terminou, para o estado
    if not duck_state.update_pull_timer():
        duck_state.stop_pulling_mouse()
        return False

    # Movimento de "resistência" puxando o mouse
    backward_speed = 2  # Velocidade reduzida
    pos_x_offset = -duck_state.dir_x * backward_speed
    pos_y_offset = random.uniform(-0.5, 0.5)  # Pequena variação vertical

    # Atualiza a posição do pato
    duck_state.pos_x += pos_x_offset
    duck_state.pos_y += pos_y_offset

    # Limites da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    duck_state.pos_x = max(0, min(duck_state.pos_x, screen_width - 128))
    duck_state.pos_y = max(0, min(duck_state.pos_y, screen_height - 128))

    return True

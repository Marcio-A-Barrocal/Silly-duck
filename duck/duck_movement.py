# duck_movement.py
"""
Sistema de movimento do pato.
Contém toda a lógica de movimentação e pathfinding.
"""

import pyautogui
import random
from . import duck_state
from . import duck_actions

def follow_mouse_step():
    """
    FAZ O PATO SEGUIR O MOUSE: Calcula um passo em direção ao cursor.
    Quando chega perto o suficiente, executa uma ação no mouse.
    """
    # TRACKING DINÂMICO: Sempre pega a posição atual do mouse
    mouse_x, mouse_y = pyautogui.position()
    # Ajusta para o centro do pato (64x64 pixels)
    target_x, target_y = mouse_x - 64, mouse_y - 64
    
    # Calcula distância até o mouse
    dx = target_x - duck_state.pos_x
    dy = target_y - duck_state.pos_y
    distance = (dx**2 + dy**2)**0.5

    # Se chegou perto o suficiente (menor que velocidade)
    if distance < duck_state.speed:
        duck_state.is_following_mouse = False
        print("[DUCK ACTION] Peguei o mouse!")
        
        # Verifica cooldown antes de permitir puxar novamente
        if duck_state.pull_cooldown <= 0:
            # DECISÃO: 50% de chance para cada ação
            if random.random() < 0.5:
                duck_actions.annoy_mouse()           # Chacoalha o mouse
                duck_state.start_idle(2)  # Descansa após chacoalhar
            else:
                duck_state.start_pulling_mouse()              # Inicia animação de puxar
                duck_actions.drag_mouse_with_beak(duck_state.dir_x)  # Puxa o mouse (em thread)
                duck_state.pull_cooldown = 50  # 5 segundos de cooldown (50 * 100ms)
        else:
            # Se está em cooldown, só chacoalha
            duck_actions.annoy_mouse()
            duck_state.start_idle(2)

        return

    # Atualiza direção do sprite baseado no movimento
    if dx > 0:
        duck_state.dir_x = 1    # Olhando para direita
    elif dx < 0:
        duck_state.dir_x = -1   # Olhando para esquerda
    
    # Normaliza a direção vertical DE FORMA MAIS SUAVE
    duck_state.dir_y = (dy / distance) * 0.8 if distance > 0 else 0  # 80% da força vertical
    
    # Move o pato em direção ao mouse - MOVIMENTO MAIS EQUILIBRADO
    if distance > 0:
        # Movimento horizontal normal
        duck_state.pos_x += duck_state.dir_x * duck_state.speed * abs(dx/distance)
        # Movimento vertical suavizado mas não exageradamente
        duck_state.pos_y += duck_state.dir_y * duck_state.speed * 0.85  # 85% da velocidade vertical

def random_walk_step(root):
    """
    MOVIMENTO ALEATÓRIO: Faz o pato andar pela tela de forma randômica.
    Corrigido para evitar bug de ficar preso nas bordas.
    """
    # Pega dimensões da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # COLISÃO COM BORDAS: Verifica ANTES de mover para evitar ficar preso
    margin = 50  # Margem de segurança das bordas
    
    # Se muito próximo das bordas, força direção para longe da borda
    if duck_state.pos_x <= margin:  # Muito perto da borda esquerda
        duck_state.dir_x = 1  # Força ir para direita
    elif duck_state.pos_x >= screen_width - 128 - margin:  # Muito perto da borda direita
        duck_state.dir_x = -1  # Força ir para esquerda
    elif duck_state.pos_y <= margin:  # Muito perto da borda superior
        duck_state.dir_y = 1  # Força ir para baixo
    elif duck_state.pos_y >= screen_height - 128 - margin:  # Muito perto da borda inferior
        duck_state.dir_y = -1  # Força ir para cima
    else:
        # Longe das bordas: 3% de chance de mudar direção (aumentado de 2%)
        if random.random() < 0.03:
            # MOVIMENTO MAIS NATURAL: mudanças graduais ao invés de bruscas
            
            # 80% chance de manter direção horizontal atual (menos mudanças bruscas)
            if random.random() < 0.80:
                # Mantém dir_x atual, só ajusta sutilmente a vertical
                vertical_change = random.random()
                if vertical_change < 0.60:  # 60% fica igual
                    pass  # Mantém dir_y atual
                elif vertical_change < 0.80:  # 20% ajusta para cima
                    duck_state.dir_y = max(-1, duck_state.dir_y - 0.3)
                else:  # 20% ajusta para baixo  
                    duck_state.dir_y = min(1, duck_state.dir_y + 0.3)
            else:
                # 20% chance de mudança mais significativa
                duck_state.dir_x = random.choice([-1, 1])
                duck_state.dir_y = random.uniform(-0.5, 0.5)  # Diagonal suave

    # Move o pato
    duck_state.pos_x += duck_state.dir_x * duck_state.speed
    duck_state.pos_y += duck_state.dir_y * duck_state.speed

    # CORREÇÃO FINAL: Garante que nunca saia da tela (safety net)
    duck_state.pos_x = max(0, min(duck_state.pos_x, screen_width - 128))
    duck_state.pos_y = max(0, min(duck_state.pos_y, screen_height - 128))

def handle_pulling_movement(root):
    """
    Lida com o movimento especial durante o estado de puxar.
    Retorna True se ainda está puxando, False se terminou.
    """
    if not duck_state.update_pull_timer():
        duck_state.stop_pulling_mouse()
        return False
        
    # Simula o pato sendo "puxado" junto com o mouse
    backward_speed = 2  # Velocidade reduzida do movimento para trás
    pos_x_offset = -duck_state.dir_x * backward_speed  # Movimento na direção oposta
    pos_y_offset = random.uniform(-0.5, 0.5)  # Pequena variação vertical
    
    # Atualiza posição do pato para simular o "esforço" de puxar
    duck_state.pos_x += pos_x_offset
    duck_state.pos_y += pos_y_offset
    
    # Verifica bordas durante o puxão
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    if duck_state.pos_x <= 0: duck_state.pos_x = 0
    if duck_state.pos_x >= screen_width - 128: duck_state.pos_x = screen_width - 128
    if duck_state.pos_y <= 0: duck_state.pos_y = 0
    if duck_state.pos_y >= screen_height - 128: duck_state.pos_y = screen_height - 128
    
    return True
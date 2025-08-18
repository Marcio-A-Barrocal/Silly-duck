# duck_actions.py
"""
Ações que o pato pode executar na tela.
"""

import pyautogui
import random
import time
import threading

def move_mouse_randomly():
    """Move o cursor do mouse para uma posição aleatória na tela."""
    width, height = pyautogui.size()  # Pega o tamanho da tela
    x = random.randint(0, width)
    y = random.randint(0, height)
    pyautogui.moveTo(x, y, duration=0.5)  # Move suavemente

def annoy_mouse():
    """
    'Chacoalha' o cursor do mouse em movimentos pequenos e aleatórios.
    Simula o pato 'brincando' com o mouse.
    """
    print("[DUCK ACTION] Bagunçando o mouse!")
    
    # Faz 10 pequenos movimentos aleatórios
    for _ in range(10):
        # Move relativamente à posição atual
        dx = random.randint(-25, 25)  # Movimento horizontal
        dy = random.randint(-25, 25)  # Movimento vertical
        pyautogui.moveRel(dx, dy, duration=0.05)  # Movimento rápido

def drag_mouse_with_beak(duck_direction_x):
    """
    'Puxa' o mouse SINCRONIZADO com o movimento do pato.
    Agora mouse e pato se movem na mesma velocidade.
    
    Args:
        duck_direction_x: 1 se pato olha direita, -1 se olha esquerda
    """
    def pull_action():
        print("[DUCK ACTION] Puxando o mouse com o bico!")
        
        # Inverte a direção do pato para simular "puxar para trás"
        pull_direction = -duck_direction_x
        
        # Puxões SINCRONIZADOS com movimento do pato
        for step in range(12):  # 12 puxões em 1.2 segundos
            # MESMA VELOCIDADE DO PATO: 2 pixels por frame
            dx = pull_direction * 2  # Igual ao backward_speed do pato
            dy = random.randint(-1, 1)  # Variação mínima vertical
            
            # Move o mouse na mesma velocidade que o pato se move
            pyautogui.moveRel(dx, dy, duration=0.05)
            
            # Pausa sincronizada com frames da animação (100ms por frame)
            time.sleep(0.05)  # Total: 100ms por puxão
    
    # Executa em thread separada para não travar animação
    pull_thread = threading.Thread(target=pull_action, daemon=True)
    pull_thread.start()
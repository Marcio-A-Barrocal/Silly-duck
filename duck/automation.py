import pyautogui
import random
import time

def move_mouse_randomly():
    """
    Move o cursor do mouse para uma posição aleatória na tela.
    """
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
    'Puxa' o mouse SUTILMENTE na direção oposta à que o pato está olhando.
    Movimento bem sutil para não atrapalhar muito o usuário.
    Executa em thread separada para não travar a animação.
    
    Args:
        duck_direction_x: 1 se pato olha direita, -1 se olha esquerda
    """
    import threading
    
    def pull_action():
        print("[DUCK ACTION] Puxando o mouse com o bico!")
        
        # Inverte a direção do pato para simular "puxar para trás"
        pull_direction = -duck_direction_x
        
        # Puxões MUITO mais sutis e espaçados
        for step in range(8):  # Menos puxões
            dx = pull_direction * 5  # Movimento bem menor (era 15)
            dy = random.randint(-1, 1)  # Variação mínima
            pyautogui.moveRel(dx, dy, duration=0.1)
            time.sleep(0.15)  # Mais espaçado entre puxões
    
    # Executa em thread separada para não travar animação
    pull_thread = threading.Thread(target=pull_action, daemon=True)
    pull_thread.start()

# Lista de ações disponíveis - REMOVIDA do uso automático
# Agora essas ações só acontecem quando o pato está em cima do mouse
mouse_actions = [annoy_mouse]  # Mantém só para referência, mas não usa mais

# FUNÇÃO REMOVIDA - Não queremos mais ações aleatórias de mouse
# def do_random_mouse_action():
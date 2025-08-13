import pyautogui
import random
import time

# ... (as outras funções como open_notepad, etc. continuam iguais)
def open_notepad():
    pyautogui.press('win')
    time.sleep(0.5)
    pyautogui.write('notepad')
    time.sleep(0.5)
    pyautogui.press('enter')

def close_active_window():
    pyautogui.hotkey('alt', 'f4')

def move_mouse_randomly():
    width, height = pyautogui.size()
    x, y = random.randint(0, width), random.randint(0, height)
    pyautogui.moveTo(x, y, duration=0.5)
# ...

def annoy_mouse():
    """'Puxa' o cursor do mouse para direções aleatórias."""
    print("[DUCK ACTION] Bagunçando o mouse!")
    for _ in range(10):
        pyautogui.moveRel(random.randint(-25, 25), random.randint(-25, 25), duration=0.05)

# --- NOVA AÇÃO ---
def drag_mouse_with_beak(duck_direction_x):
    """Puxa o mouse para trás, na direção oposta à que o pato está olhando."""
    print("[DUCK ACTION] Puxando o mouse com o bico!")
    
    # Se o pato olha para a direita (dir_x=1), puxa para a esquerda (-1).
    # Se o pato olha para a esquerda (dir_x=-1), puxa para a direita (1).
    pull_direction = -duck_direction_x
    
    # Puxa o mouse em 15 pequenos passos
    for _ in range(15):
        pyautogui.moveRel(pull_direction * 10, random.randint(-2, 2), duration=0.03)
        time.sleep(0.01)
# --- FIM DA NOVA AÇÃO ---


actions = [open_notepad, close_active_window, move_mouse_randomly]

def do_random_action():
    action = random.choice(actions)
    print(f"[DUCK ACTION] Executando: {action.__name__}")
    action()
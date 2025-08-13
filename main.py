import threading
import random
import time
from duck import automation
from duck import window

def duck_actions_loop():
    """O cérebro do pato: decide o que fazer e quando."""
    while True:
        # MODIFICADO: Espera um tempo menor, para ser mais ativo
        time.sleep(random.randint(5, 10))
        
        action_choice = random.random()

        # MODIFICADO: Aumentamos a chance de caçar o mouse
        if action_choice < 0.40: # 40% de chance de seguir o mouse
            print("[DUCK BRAIN] Decidiu caçar o mouse!")
            window.start_follow_mouse()
            
        # MODIFICADO: Diminuímos a chance de ficar parado
        elif action_choice < 0.55: # 15% de chance de ficar parado
            # MUDANÇA CONCEITUAL: Não é mais uma "soneca", é um "descanso"
            print("[DUCK BRAIN] Decidiu descansar um pouco.")
            window.start_idle(random.randint(2, 4)) # E por menos tempo
            
        else: # 45% de chance de fazer uma ação no sistema
            print("[DUCK BRAIN] Decidiu fazer uma travessura no PC.")
            automation.do_random_action()

# ... (o resto do main.py continua igual)
action_thread = threading.Thread(target=duck_actions_loop, daemon=True)
action_thread.start()

if __name__ == "__main__":
    window.create_window()
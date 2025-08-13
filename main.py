import threading
import random
import time
from duck import automation
from duck import window

def duck_actions_loop():
    """
    CÉREBRO DO PATO: Loop principal que decide o que o pato vai fazer.
    Roda em thread separada para não travar a interface gráfica.
    """
    while True:
        # Espera mais tempo para o pato ficar mais andando normalmente
        time.sleep(random.randint(8, 15))
        
        # Só toma decisões se não estiver ocupado com outras ações
        if not (window.is_following_mouse or window.is_idle or window.is_pulling_mouse):
            action_choice = random.random()

            # 30% de chance de caçar o mouse (reduzido)
            if action_choice < 0.30:
                print("[DUCK BRAIN] Decidiu caçar o mouse!")
                window.start_follow_mouse()
                
            # 20% de chance de ficar parado/descansar
            elif action_choice < 0.50:
                print("[DUCK BRAIN] Decidiu descansar um pouco.")
                window.start_idle(random.randint(3, 5))
                
            # 50% de chance de apenas continuar andando
            else:
                print("[DUCK BRAIN] Decidiu continuar caminhando.")
                # Não faz nada, deixa ele andar normalmente

# Cria a thread do cérebro do pato
# daemon=True faz ela morrer quando o programa principal acaba
action_thread = threading.Thread(target=duck_actions_loop, daemon=True)
action_thread.start()

# PONTO DE ENTRADA: Inicia a janela do pato
if __name__ == "__main__":
    window.create_window()  # Cria e roda a interface gráfica
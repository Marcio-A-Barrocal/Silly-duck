# main.py
"""
Ponto de entrada principal do projeto.
Controla o 'cérebro' do pato e inicia a interface gráfica.
"""

import threading
import random
import time
from duck import duck_state
from duck import window

def duck_actions_loop():
    """
    CÉREBRO DO PATO: Loop principal que decide o que o pato vai fazer.
    Roda em thread separada para não travar a interface gráfica.
    """
    print("[DUCK BRAIN] Cérebro do pato ativado!")
    
    while True:
        # Espera mais tempo para o pato ficar mais andando normalmente
        time.sleep(random.randint(8, 15))
        
        # Só toma decisões se não estiver ocupado com outras ações
        if not (duck_state.is_following_mouse or duck_state.is_idle or duck_state.is_pulling_mouse):
            action_choice = random.random()

            # 30% de chance de caçar o mouse (reduzido)
            if action_choice < 0.30:
                print("[DUCK BRAIN] Decidiu caçar o mouse!")
                duck_state.start_follow_mouse()
                
            # 20% de chance de ficar parado/descansar
            elif action_choice < 0.50:
                print("[DUCK BRAIN] Decidiu descansar um pouco.")
                duck_state.start_idle(random.randint(3, 5))
                
            # 50% de chance de apenas continuar andando
            else:
                print("[DUCK BRAIN] Decidiu continuar caminhando.")
                # Não faz nada, deixa ele andar normalmente

# PONTO DE ENTRADA PRINCIPAL
if __name__ == "__main__":
    print("[MAIN] Iniciando Desktop Duck...")
    
    # Cria a thread do cérebro do pato
    # daemon=True faz ela morrer quando o programa principal acaba
    print("[MAIN] Iniciando cérebro do pato...")
    action_thread = threading.Thread(target=duck_actions_loop, daemon=True)
    action_thread.start()

    # INICIA A JANELA DO PATO (função blocking - roda até fechar)
    print("[MAIN] Iniciando interface gráfica...")
    window.create_window()
    
    print("[MAIN] Desktop Duck finalizado!")
# window.py
"""
Interface gráfica simplificada do pato.
Agora só cuida da janela e delegaed tudo para os outros módulos.
"""

import tkinter as tk
from . import duck_state
from . import duck_movement
from . import duck_sprites

# =============================================================================
# LOOP PRINCIPAL DE ANIMAÇÃO
# =============================================================================

def move_duck(root, label):
    """
    LOOP PRINCIPAL DE ANIMAÇÃO: Atualiza movimento, sprite e posição.
    Chama a si mesma a cada 100ms para criar animação fluida.
    """
    # Atualiza cooldowns
    duck_state.update_cooldown()

    # DECIDE O MOVIMENTO baseado no estado
    if duck_state.is_pulling_mouse:
        # Durante o puxão, usa movimento especial
        duck_movement.handle_pulling_movement(root)
    elif duck_state.is_following_mouse:
        duck_movement.follow_mouse_step()         # Persegue o mouse
    elif not duck_state.is_idle:
        duck_movement.random_walk_step(root)      # Caminha aleatoriamente
    # Se is_idle=True, fica parado

    # ATUALIZA O SPRITE
    current_sprite = duck_sprites.get_current_sprite()

    # Atualiza a imagem e posição da janela
    label.config(image=current_sprite)
    label.image = current_sprite  # Evita garbage collection
    root.geometry(f"128x128+{int(duck_state.pos_x)}+{int(duck_state.pos_y)}")
    
    # Agenda próxima atualização em 100ms
    root.after(100, lambda: move_duck(root, label))

# =============================================================================
# CRIAÇÃO DA JANELA
# =============================================================================

def create_window():
    """
    FUNÇÃO PRINCIPAL: Cria a janela, carrega sprites e inicia animação.
    """
    print("[WINDOW] Criando janela do pato...")
    
    # CONFIGURAÇÃO DA JANELA
    root = tk.Tk()
    duck_state.set_root_reference(root)
    
    root.overrideredirect(True)        # Remove barra de título
    root.attributes("-topmost", True)   # Sempre por cima
    
    # TRANSPARÊNCIA: Usa cor magenta como transparente
    transparent_color = "#ff00ff"
    root.configure(bg=transparent_color)
    root.wm_attributes("-transparentcolor", transparent_color)

    # CARREGA TODOS OS SPRITES
    duck_sprites.load_all_sprites()

    # CRIA O LABEL COM A IMAGEM - Inicia com sprite de caminhada
    if duck_sprites.sprites_right:
        initial_sprite = duck_sprites.sprites_right[0]
    else:
        print("[WINDOW ERROR] Nenhum sprite carregado!")
        return
        
    label = tk.Label(root, image=initial_sprite, bg=transparent_color)
    label.pack()

    print("[WINDOW] Iniciando animação do pato...")
    # INICIA A ANIMAÇÃO
    move_duck(root, label)
    
    # INICIA O LOOP DA INTERFACE GRÁFICA
    root.mainloop()

# =============================================================================
# FUNÇÕES DE COMPATIBILIDADE (para manter funcionando com código existente)
# =============================================================================

# Expor variáveis de estado para compatibilidade
@property
def is_idle():
    return duck_state.is_idle

@property 
def is_following_mouse():
    return duck_state.is_following_mouse

@property
def is_pulling_mouse():
    return duck_state.is_pulling_mouse

# Expor funções de estado para compatibilidade
def start_follow_mouse():
    return duck_state.start_follow_mouse()

def start_idle(duration):
    return duck_state.start_idle(duration)
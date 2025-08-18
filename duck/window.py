# window.py
"""
Interface gráfica do pato.
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
    """
    # REMOVIDO: A chamada para check_mouse_proximity() foi removida daqui.

    # Atualiza cooldowns
    duck_state.update_cooldown()

    # A lógica de movimento permanece a mesma
    if duck_state.is_pulling_mouse:
        duck_movement.handle_pulling_movement(root)
    elif duck_state.is_fleeing:
        duck_movement.flee_from_mouse_step(root)
    elif duck_state.is_following_mouse:
        duck_movement.follow_mouse_step()
    elif not duck_state.is_idle:
        duck_movement.random_walk_step(root)

    # ATUALIZA O SPRITE
    current_sprite = duck_sprites.get_current_sprite()

    # Atualiza a imagem e posição da janela
    label.config(image=current_sprite)
    label.image = current_sprite
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
    
    root = tk.Tk()
    duck_state.set_root_reference(root)
    
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    
    transparent_color = "#ff00ff"
    root.configure(bg=transparent_color)
    root.wm_attributes("-transparentcolor", transparent_color)

    duck_sprites.load_all_sprites()

    if duck_sprites.sprites_right:
        initial_sprite = duck_sprites.sprites_right[0]
    else:
        print("[WINDOW ERROR] Nenhum sprite carregado!")
        return
        
    label = tk.Label(root, image=initial_sprite, bg=transparent_color)
    label.pack()

    # --- NOVA FUNÇÃO DE CALLBACK PARA O CLIQUE ---
    def on_duck_click(event):
        """
        Esta função é chamada quando o label do pato é clicado.
        """
        # Só permite iniciar a fuga se o pato não estiver ocupado puxando o mouse.
        if not duck_state.is_pulling_mouse:
            duck_state.start_fleeing()

    # --- NOVO: VINCULANDO O EVENTO DE CLIQUE AO LABEL ---
    # "<Button-1>" se refere ao clique com o botão esquerdo do mouse.
    label.bind("<Button-1>", on_duck_click)

    print("[WINDOW] Iniciando animação do pato...")
    move_duck(root, label)
    
    root.mainloop()

# =============================================================================
# FUNÇÕES DE COMPATIBILIDADE (Nenhuma alteração necessária aqui)
# =============================================================================
@property
def is_idle():
    return duck_state.is_idle

@property 
def is_following_mouse():
    return duck_state.is_following_mouse

@property
def is_pulling_mouse():
    return duck_state.is_pulling_mouse

def start_follow_mouse():
    return duck_state.start_follow_mouse()

def start_idle(duration):
    return duck_state.start_idle(duration)
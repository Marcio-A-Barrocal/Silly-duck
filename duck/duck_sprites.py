# duck_sprites.py
"""
Sistema de carregamento e gerenciamento de sprites do pato.
Separa toda a lógica de imagens da janela principal.
"""

import os
from PIL import Image, ImageTk
from . import duck_state

# =============================================================================
# ARMAZENAMENTO DE SPRITES
# =============================================================================
sprites_right = []         # Sprites caminhando para direita
sprites_left = []          # Sprites caminhando para esquerda  
sprites_idle = []          # Sprites parado/idle
sprites_pull_right = []    # Sprites puxando para direita
sprites_pull_left = []     # Sprites puxando para esquerda
sprites_bounce_right = []  # Sprites fugindo (engraçado) para direita
sprites_bounce_left = []   # Sprites fugindo (engraçado) para esquerda

# =============================================================================
# FUNÇÕES DE PROCESSAMENTO DE IMAGEM
# =============================================================================

def process_image(img_path):
    """
    Processa uma imagem: remove fundo magenta, redimensiona e retorna ImageTk.
    
    Args:
        img_path: Caminho para o arquivo de imagem
        
    Returns:
        ImageTk.PhotoImage processada ou None se arquivo não existe
    """
    if not os.path.exists(img_path):
        return None
        
    # Carrega e processa imagem
    img = Image.open(img_path).convert("RGBA")
    
    # Remove fundo magenta e torna transparente
    new_data = []
    for item in img.getdata():
        r, g, b, a = item
        if a < 255 or (r == 255 and g < 50 and b == 255):  # magenta
            new_data.append((255, 255, 255, 0))  # Transparente
        else:
            new_data.append(item)
    img.putdata(new_data)
    
    # Redimensiona para 64x64
    img = img.resize((64, 64), Image.Resampling.NEAREST)
    return ImageTk.PhotoImage(img)

# =============================================================================
# FUNÇÕES DE CARREGAMENTO DE SPRITES
# =============================================================================

def load_walk_sprites():
    """Carrega todos os sprites de caminhada (walk1.png até walk6.png)."""
    global sprites_right, sprites_left
    
    print("[SPRITES] Carregando sprites de caminhada...")
    for i in range(1, 7):
        img_path = os.path.join("assets", "images", f"walk{i}.png")
        img_tk = process_image(img_path)
        
        if img_tk:
            sprites_right.append(img_tk)
            
            # Cria versão espelhada para esquerda
            img = Image.open(img_path).convert("RGBA")
            new_data = []
            for item in img.getdata():
                r, g, b, a = item
                if a < 255 or (r == 255 and g < 50 and b == 255):
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)
            img = img.resize((64, 64), Image.Resampling.NEAREST)
            img_left = img.transpose(Image.FLIP_LEFT_RIGHT)
            sprites_left.append(ImageTk.PhotoImage(img_left))
    
    print(f"[SPRITES] Carregados {len(sprites_right)} sprites de caminhada")

def load_idle_sprites():
    """Carrega todos os sprites de idle/parado."""
    global sprites_idle
    
    print("[SPRITES] Carregando sprites idle...")
    i = 1
    while True:
        img_path = os.path.join("assets", "images", f"idle{i}.png")
        img_tk = process_image(img_path)
        
        if img_tk:
            sprites_idle.append(img_tk)
            i += 1
        else:
            break

    if not sprites_idle and sprites_right:
        sprites_idle.append(sprites_right[0])
        print("[SPRITES] Usando sprite de caminhada como idle")
    
    print(f"[SPRITES] Carregados {len(sprites_idle)} sprites idle")

def load_pull_sprites():
    """Carrega todos os sprites de puxar (pull1.png, pull2.png)."""
    global sprites_pull_right, sprites_pull_left
    
    print("[SPRITES] Carregando sprites de puxar...")
    for i in range(1, 3):
        img_path = os.path.join("assets", "images", f"pull{i}.png")
        img_tk = process_image(img_path)
        
        if img_tk:
            sprites_pull_right.append(img_tk)
            
            img = Image.open(img_path).convert("RGBA")
            new_data = []
            for item in img.getdata():
                r, g, b, a = item
                if a < 255 or (r == 255 and g < 50 and b == 255):
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)
            img = img.resize((64, 64), Image.Resampling.NEAREST)
            img_left = img.transpose(Image.FLIP_LEFT_RIGHT)
            sprites_pull_left.append(ImageTk.PhotoImage(img_left))

    if not sprites_pull_right and sprites_right:
        sprites_pull_right = sprites_right.copy()
        sprites_pull_left = sprites_left.copy()
        print("[SPRITES] Usando sprites de caminhada como pull")
    
    print(f"[SPRITES] Carregados {len(sprites_pull_right)} sprites de puxar")

def load_bounce_sprites():
    """Carrega todos os sprites de fuga engraçada (bounce1.png até bounce6.png)."""
    global sprites_bounce_right, sprites_bounce_left

    print("[SPRITES] Carregando sprites de fuga (bounce)...")
    for i in range(1, 7):
        img_path = os.path.join("assets", "images", f"bounce{i}.png")
        img_tk = process_image(img_path)

        if img_tk:
            sprites_bounce_right.append(img_tk)

            img = Image.open(img_path).convert("RGBA")
            new_data = []
            for item in img.getdata():
                r, g, b, a = item
                if a < 255 or (r == 255 and g < 50 and b == 255):
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)
            img = img.resize((64, 64), Image.Resampling.NEAREST)
            img_left = img.transpose(Image.FLIP_LEFT_RIGHT)
            sprites_bounce_left.append(ImageTk.PhotoImage(img_left))

    if not sprites_bounce_right and sprites_right:
        sprites_bounce_right = sprites_right.copy()
        sprites_bounce_left = sprites_left.copy()
        print("[SPRITES] Usando sprites de caminhada como bounce")

    print(f"[SPRITES] Carregados {len(sprites_bounce_right)} sprites de fuga (bounce)")

def load_all_sprites():
    """Carrega todos os sprites do pato."""
    print("[SPRITES] Iniciando carregamento de sprites...")
    load_walk_sprites()
    load_idle_sprites()
    load_pull_sprites()
    load_bounce_sprites()
    print("[SPRITES] Todos os sprites carregados!")

# =============================================================================
# FUNÇÃO DE SELEÇÃO DE SPRITE
# =============================================================================

def get_current_sprite():
    """
    Retorna o sprite atual baseado no estado e direção do pato.
    """
    if duck_state.is_fleeing:
        duck_state.bounce_sprite_index = (duck_state.bounce_sprite_index + 1) % len(sprites_bounce_right)
        if duck_state.dir_x >= 0:
            return sprites_bounce_right[duck_state.bounce_sprite_index]
        else:
            return sprites_bounce_left[duck_state.bounce_sprite_index]

    elif duck_state.is_pulling_mouse:
        if duck_state.walk_sprite_index % 2 == 0:
            duck_state.pull_sprite_index = (duck_state.pull_sprite_index + 1) % len(sprites_pull_right)
        if duck_state.dir_x >= 0:
            return sprites_pull_right[duck_state.pull_sprite_index]
        else:
            return sprites_pull_left[duck_state.pull_sprite_index]

    elif duck_state.is_idle:
        duck_state.idle_sprite_index = (duck_state.idle_sprite_index + 1) % len(sprites_idle)
        return sprites_idle[duck_state.idle_sprite_index]

    else:
        duck_state.walk_sprite_index = (duck_state.walk_sprite_index + 1) % len(sprites_right)
        if duck_state.dir_x >= 0:
            return sprites_right[duck_state.walk_sprite_index]
        else:
            return sprites_left[duck_state.walk_sprite_index]

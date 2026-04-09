import pygame
import sound_main_menu as sound

# --- Helper Functions ---

def sfx_command(ui, sfx, cmd, delay=None):
    sfx.play()
    if delay is None:
        delay = int(sfx.get_length() * 1000)
    ui.after(delay, cmd)

def animate_button_hover(btn, enter=True):
    if enter:
        btn.configure(fg="#FF8C00")
    else:
        btn.configure(fg="#C0C0C0")

def play():
    print("Play clicked")

def quit_game(ui):
    sound.quit_sfx.play()
    length_ms = int(sound.quit_sfx.get_length() * 1000)
    ui.after(length_ms, ui.destroy)

# --- Settings Volume Callbacks ---

def set_main_volume(val):
    sound.vol_main = int(val * 100)
    pygame.mixer.music.set_volume(val)
    sound.press_sfx.set_volume(val * 0.8)
    sound.back_sfx.set_volume(val * 0.8)
    sound.quit_sfx.set_volume(val * 0.8)

def set_sfx_volume(val):
    sound.vol_sfx = int(val * 100)
    sound.press_sfx.set_volume(val)
    sound.back_sfx.set_volume(val)
    sound.quit_sfx.set_volume(val)

def set_music_volume(val):
    sound.vol_music = int(val * 100)
    pygame.mixer.music.set_volume(val)

def reset_defaults(main_slider, sfx_slider, music_slider):
    sound.vol_main = sound.vol_sfx = sound.vol_music = 100
    main_slider.set(100)
    sfx_slider.set(100)
    music_slider.set(100)
    pygame.mixer.music.set_volume(1.0)
    sound.press_sfx.set_volume(0.8)
    sound.back_sfx.set_volume(0.8)
    sound.quit_sfx.set_volume(0.8)
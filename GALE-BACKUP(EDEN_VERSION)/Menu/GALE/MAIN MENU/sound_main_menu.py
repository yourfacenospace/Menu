import pygame

# --- Music Setup & Sound Effects ---

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.mixer.music.load(r"Menu/GALE/SFX_AND_MUSIC/BG_MUSIC.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

press_sfx = pygame.mixer.Sound(r"Menu/GALE/SFX_AND_MUSIC/PRESS_SFX.wav")
back_sfx  = pygame.mixer.Sound(r"Menu/GALE/SFX_AND_MUSIC/BACK_SFX.wav")
quit_sfx  = pygame.mixer.Sound(r"Menu/GALE/SFX_AND_MUSIC/QUIT_SFX.wav")

press_sfx.set_volume(0.7)
back_sfx.set_volume(0.7)
quit_sfx.set_volume(0.7)

vol_main  = 100
vol_sfx   = 50
vol_music = 100
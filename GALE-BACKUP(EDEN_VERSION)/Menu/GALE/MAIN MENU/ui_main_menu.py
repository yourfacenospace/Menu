import pyglet
import sound_main_menu as sound
import logic_main_menu as logic
from tkinter import *

pyglet.font.add_file(r"Menu/GALE/FONTS/PixelWarden.ttf")

# --- Slider Builder (UI only) ---

def make_slider(parent, label_text, initial=100, on_change=None):
    row = Frame(parent, bg="#0d0f12")
    row.pack(fill=X, padx=50, pady=8)

    Label(row, text=label_text,
          font=("PixelWarden", 11),
          bg="#0d0f12", fg="#C0C0C0",
          width=14, anchor="w").pack(side=LEFT)

    val_label = Label(row, text=str(initial),
                      font=("PixelWarden", 11),
                      bg="#0d0f12", fg="#FF8C00", width=4)

    TRACK_W = 200
    TRACK_H = 4
    DIAMOND = 8
    C_H = DIAMOND * 2 + 6

    canvas = Canvas(row, width=TRACK_W, height=C_H,
                    bg="#0d0f12", highlightthickness=0, bd=0)
    canvas.pack(side=LEFT, padx=(5, 5))
    val_label.pack(side=LEFT)

    cy = C_H // 2

    def get_x(val):
        return int((val / 100) * TRACK_W)

    def draw(val):
        canvas.delete("all")
        x = get_x(val)
        canvas.create_rectangle(0, cy - TRACK_H // 2,
                                 TRACK_W, cy + TRACK_H // 2,
                                 fill="#333333", outline="")
        canvas.create_rectangle(0, cy - TRACK_H // 2,
                                 x, cy + TRACK_H // 2,
                                 fill="#FF8C00", outline="")
        canvas.create_polygon(
            x,           cy - DIAMOND,
            x + DIAMOND, cy,
            x,           cy + DIAMOND,
            x - DIAMOND, cy,
            fill="#FF8C00", outline="#FFB347", width=1
        )

    current_val = [initial]

    def set_val(x):
        val = max(0, min(100, int((x / TRACK_W) * 100)))
        current_val[0] = val
        draw(val)
        val_label.config(text=str(val))
        if on_change:
            on_change(val / 100)

    canvas.bind("<Button-1>",  lambda e: set_val(e.x))
    canvas.bind("<B1-Motion>", lambda e: set_val(e.x))

    def slider_set(val):
        current_val[0] = int(val)
        draw(int(val))
        val_label.config(text=str(int(val)))

    canvas.set = slider_set
    draw(initial)
    return canvas

# --- Settings Window ---

def open_settings(Ui, image):
    settings_win = Toplevel(Ui)
    settings_win.title("Settings")
    settings_win.attributes("-fullscreen", True)
    settings_win.configure(bg="#0d0f12")
    settings_win.grab_set()

    Label(settings_win, image=image).place(x=0, y=0, relwidth=1, relheight=1)

    panel = Frame(settings_win, bg="#0d0f12", bd=0)
    panel.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.45, relheight=0.75)

    Label(panel, text="── SETTINGS ──",
          font=("PixelWarden", 32, "bold"),
          bg="#0d0f12", fg="#FF8C00").pack(pady=(30, 5))
    Label(panel, text="Audio Configuration",
          font=("PixelWarden", 12, "italic"),
          bg="#0d0f12", fg="#666666").pack(pady=(0, 10))
    Frame(panel, bg="#FF8C00", height=1).pack(fill=X, padx=40, pady=(0, 20))
    Label(panel, text="AUDIO",
          font=("PixelWarden", 13, "bold"),
          bg="#0d0f12", fg="#FF8C00").pack(pady=(0, 15))

    main_slider  = make_slider(panel, "Main Volume",  sound.vol_main,  logic.set_main_volume)
    sfx_slider   = make_slider(panel, "SFX Volume",   sound.vol_sfx,   logic.set_sfx_volume)
    music_slider = make_slider(panel, "Music Volume", sound.vol_music, logic.set_music_volume)

    Frame(panel, bg="#333333", height=1).pack(fill=X, padx=40, pady=(20, 15))

    reset_btn = Button(panel, text="[ RESET DEFAULTS ]",
                       font=("PixelWarden", 13, "bold"),
                       bg="#0d0f12", fg="#C0C0C0",
                       activebackground="#0d0f12", activeforeground="#FF8C00",
                       bd=0, cursor="hand2",
                       command=lambda: logic.reset_defaults(main_slider, sfx_slider, music_slider))
    reset_btn.pack(pady=(5, 5))
    reset_btn.bind("<Enter>", lambda e: logic.animate_button_hover(reset_btn, True))
    reset_btn.bind("<Leave>", lambda e: logic.animate_button_hover(reset_btn, False))

    back_btn = Button(panel, text="[ BACK ]",
                      font=("PixelWarden", 14, "bold"),
                      bg="#0d0f12", fg="#C0C0C0",
                      activebackground="#0d0f12", activeforeground="#FF8C00",
                      bd=0, cursor="hand2",
                      command=lambda: logic.sfx_command(Ui, sound.back_sfx, settings_win.destroy, delay=300))
    back_btn.pack(pady=(5, 20))
    back_btn.bind("<Enter>", lambda e: logic.animate_button_hover(back_btn, True))
    back_btn.bind("<Leave>", lambda e: logic.animate_button_hover(back_btn, False))

# --- Credits Window ---

def open_credits(Ui, image):
    credits_win = Toplevel(Ui)
    credits_win.title("Credits")
    credits_win.attributes("-fullscreen", True)
    credits_win.configure(bg="#0d0f12")
    credits_win.grab_set()

    Label(credits_win, image=image).place(x=0, y=0, relwidth=1, relheight=1)

    panel = Frame(credits_win, bg="#0d0f12", bd=0)
    panel.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.45, relheight=0.80)

    Label(panel, text="── CREDITS ──",
          font=("PixelWarden", 32, "bold"),
          bg="#0d0f12", fg="#FF8C00").pack(pady=(30, 5))
    Label(panel, text="G.A.L.E — Development Team",
          font=("PixelWarden", 12, "italic"),
          bg="#0d0f12", fg="#666666").pack(pady=(0, 25))
    Frame(panel, bg="#FF8C00", height=1).pack(fill=X, padx=40, pady=(0, 20))
    Label(panel, text="GAME DEVELOPERS",
          font=("PixelWarden", 13, "bold"),
          bg="#0d0f12", fg="#FF8C00").pack(pady=(5, 8))

    for name in ["Abuyuan, Ferdinand Angelo",
                 "Cabrera, Kyle Louise",
                 "Flores, Eden Michael",
                 "Ongga, Kent Gabriel"]:
        Label(panel, text=name,
              font=("PixelWarden", 12),
              bg="#0d0f12", fg="#cccccc").pack(pady=2)

    Frame(panel, bg="#333333", height=1).pack(fill=X, padx=40, pady=(20, 15))

    back_btn = Button(panel, text="[ BACK ]",
                      font=("PixelWarden", 14, "bold"),
                      bg="#0d0f12", fg="#C0C0C0",
                      activebackground="#0d0f12", activeforeground="#FF8C00",
                      bd=0, cursor="hand2",
                      command=lambda: logic.sfx_command(Ui, sound.back_sfx, credits_win.destroy, delay=300))
    back_btn.pack(pady=(5, 20))
    back_btn.bind("<Enter>", lambda e: logic.animate_button_hover(back_btn, True))
    back_btn.bind("<Leave>", lambda e: logic.animate_button_hover(back_btn, False))

# --- Main Menu Window ---

def launch():
    Ui = Tk()
    Ui.title("G.A.L.E")
    Ui.attributes("-fullscreen", True)
    Ui.bind("<Escape>", lambda e: Ui.attributes("-fullscreen", False))

    image = PhotoImage(file=r"Menu/GALE/IMAGES/Main_Menu_UserInterFace_Background.png")

    bg_label = Label(Ui, image=image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    Label(bg_label, text="G.A.L.E",
          font=("PixelWarden", 100, "bold"),
          fg="#FF8C00", bg="black").place(relx=0.5, rely=0.25, anchor="center")

    btn_texts = ["Play",            "Settings",                   "Credits",                   "Quit"]
    btn_cmds  = [logic.play,        lambda: open_settings(Ui, image), lambda: open_credits(Ui, image), lambda: logic.quit_game(Ui)]
    btn_sfx   = [sound.press_sfx,   sound.press_sfx,              sound.press_sfx,             None]

    for i, (text, cmd, sfx) in enumerate(zip(btn_texts, btn_cmds, btn_sfx)):
        btn = Button(bg_label,
                     text=text.upper(),
                     command=lambda c=cmd, s=sfx: logic.sfx_command(Ui, s, c, delay=300) if s else c(),
                     font=("PixelWarden", 20, "bold"),
                     fg="#C0C0C0", bg="black",
                     activebackground="black", activeforeground="#FF8C00",
                     bd=0, highlightthickness=0,
                     cursor="hand2", width=12)
        btn.place(relx=0.5, rely=0.38 + i * 0.08, anchor="center")
        btn.bind("<Enter>", lambda e, b=btn: logic.animate_button_hover(b, True))
        btn.bind("<Leave>", lambda e, b=btn: logic.animate_button_hover(b, False))

    Ui.mainloop()

if __name__ == "__main__":
    launch()
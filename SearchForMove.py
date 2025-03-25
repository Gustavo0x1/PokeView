
from PIL import Image,ImageTk

import tkinter as tk
janela = tk.Tk()
icon_path = "icons_cortados/bug.png"
IconSize = 40
img = Image.open(icon_path)
width, height = img.size
new_width = int(width * (IconSize/ 100))
new_height = int(height * (IconSize/ 100))
img = img.resize((new_width,new_height))
image = ImageTk.PhotoImage(img)

TypeColors = {
 "normal": "#6D6D4E",
 "fire": "#C22E28",
 "water": "#357EC7",
 "electric": "#D1AC00",
 "grass": "#4CAF50",
 "ice": "#4DB6AC",
 "fighting": "#A72C27",
 "poison": "#7B3798",
 "ground": "#9D6B3F",
 "flying": "#8668C4",
 "psychic": "#C2185B",
 "bug": "#8DB22D",
 "rock": "#8E7340",
 "ghost": "#4F3D75",
 "dragon": "#512DA8",
 "dark": "#4E4135",
 "steel": "#767676",
 "fairy": "#A45D78"
}
FrameMove = tk.Frame(janela)
BgColor = TypeColors.get("Ghost", "#444")
FgColor = "#fff"

FrameMove.config(bg=BgColor,width=500)

label_icon = tk.Label(FrameMove, image=image,bg=BgColor)
label_icon.grid(column=1,row=1)

label_MoveName = tk.Label(FrameMove,text="U-Turn",fg=FgColor,bg=BgColor)
label_MoveName.grid(column=2,row=1)

Label_Power = tk.Label(FrameMove,text="80",fg=FgColor,bg=BgColor)
Label_PP = tk.Label(FrameMove,text="6/6",fg=FgColor,bg=BgColor)
FrameMove.grid(column=1,row=2)
Label_Power.grid(column=1,row=2)
Label_PP.grid(column=2,row=2)
FrameDescription = tk.Label(FrameMove,text=f"The user whips up a\nturbulent whirlwind\nthat ups the Speed\nof all party Pok\u00e9mon\nfor three turns.",fg=FgColor,bg=BgColor)
FrameDescription.grid(column=3,row=1)
janela.mainloop()

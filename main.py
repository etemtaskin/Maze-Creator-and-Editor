import ast
import tkinter
import tkinter.ttk as ttk
from random import choice

window = tkinter.Tk()
window.title("Labyrinth Creator")
window.geometry("800x400")

labyrinthRaws = []

def importing():
    data = input("İnput Labyrinth Code as a List: ")
    code_matrix = ast.literal_eval(data)
    h = len(code_matrix)
    w = len(code_matrix[0]) if h>0 else 0
    functionButtons[4].delete(0, "end"); functionButtons[4].insert(0, str(h))
    functionButtons[5].delete(0, "end"); functionButtons[5].insert(0, str(w))
    draw()
    for r in range(h):
        for c in range(w):
            v = code_matrix[r][c]
            ri = 2*r+1; ci = 2*c+1
            if ci-1 >= 0:
                b = labyrinthRaws[ri][ci-1][0]
                b.config(bg="#000000" if v & 1 else "#FFFFFF")
            if ci+1 < len(labyrinthRaws[ri]):
                b = labyrinthRaws[ri][ci+1][0]
                b.config(bg="#000000" if v & 2 else "#FFFFFF")
            if ri-1 >= 0:
                b = labyrinthRaws[ri-1][ci][0]
                b.config(bg="#000000" if v & 4 else "#FFFFFF")
            if ri+1 < len(labyrinthRaws):
                b = labyrinthRaws[ri+1][ci][0]
                b.config(bg="#000000" if v & 8 else "#FFFFFF")
    try:
        sr, sc = map(int, start_entry.get().split(","))
        er, ec = map(int, end_entry.get().split(","))
        labyrinthRaws[2*sr+1][2*sc+1][0].config(bg="#00FF00")
        labyrinthRaws[2*er+1][2*ec+1][0].config(bg="#FF0000")
    except:
        pass

def exporting():
    height = int(functionButtons[4].get())
    width  = int(functionButtons[5].get())
    labyrinthCode = [[0]*width for _ in range(height)]
    for r in range(height):
        for c in range(width):
            code = 0; ri = 2*r+1; ci = 2*c+1
            for bit, di, dj in ((1,0,-1),(2,0,1),(4,-1,0),(8,1,0)):
                wdg = labyrinthRaws[ri+di][ci+dj][0]
                if isinstance(wdg, tkinter.Button) and wdg.cget("bg")=="#000000":
                    code |= bit
            labyrinthCode[r][c] = code
    print(labyrinthCode)

def generating():
    h = int(functionButtons[4].get())
    w = int(functionButtons[5].get())
    draw()
    for i in range(len(labyrinthRaws)):
        for j in range(len(labyrinthRaws[0])):
            wd = labyrinthRaws[i][j][0]
            if isinstance(wd, tkinter.Button):
                wd.config(bg="#000000")
    visited = [[False]*w for _ in range(h)]
    stack = [(0,0)]; visited[0][0] = True
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    while stack:
        r,c = stack[-1]
        nbrs = [(r+dr,c+dc) for dr,dc in dirs if 0<=r+dr<h and 0<=c+dc<w and not visited[r+dr][c+dc]]
        if nbrs:
            nr,nc = choice(nbrs)
            wi = (2*r+1 + 2*nr+1)//2; wj = (2*c+1 + 2*nc+1)//2
            labyrinthRaws[wi][wj][0].config(bg="#FFFFFF")
            visited[nr][nc] = True; stack.append((nr,nc))
        else:
            stack.pop()
    try:
        sr, sc = map(int, start_entry.get().split(","))
        er, ec = map(int, end_entry.get().split(","))
        labyrinthRaws[2*sr+1][2*sc+1][0].config(bg="#00FF00")
        labyrinthRaws[2*er+1][2*ec+1][0].config(bg="#FF0000")
    except:
        pass

def draw():
    def wallToggle(b):
        b.config(bg="#FFFFFF" if b.cget("bg") == "#000000" else "#000000")
    for w in labyrinthFrame.winfo_children():
        w.destroy()
    global labyrinthRaws; labyrinthRaws = []
    height = int(functionButtons[4].get()); width = int(functionButtons[5].get())
    rows = 2*height + 1; cols = 2*width + 1
    for i in range(rows):
        labyrinthRaws.append([])
        for j in range(cols):
            labyrinthRaws[i].append([])
            if i%2==0 and j%2!=0:
                btn = tkinter.Button(labyrinthFrame, width=20, height=1, bg="#FFFFFF", font=("Arial",1), pady=0, padx=0)
                btn.grid(row=i, column=j)
                btn.config(command=lambda b=btn: wallToggle(b))
                labyrinthRaws[i][j].append(btn)
            elif i%2!=0 and j%2==0:
                btn = tkinter.Button(labyrinthFrame, width=1, height=10, bg="#FFFFFF", font=("Arial",1), pady=0, padx=0)
                btn.grid(row=i, column=j)
                btn.config(command=lambda b=btn: wallToggle(b))
                labyrinthRaws[i][j].append(btn)
            else:
                fr = tkinter.Frame(
                    labyrinthFrame,
                    bg="#EEEEEE",
                    width=20, height=10
                )
                fr.grid(row=i, column=j)
                fr.grid_propagate(False)
                labyrinthRaws[i][j].append(fr)
    try:
        sr, sc = map(int, start_entry.get().split(","))
        er, ec = map(int, end_entry.get().split(","))
        labyrinthRaws[2*sr+1][2*sc+1][0].config(bg="#00FF00")
        labyrinthRaws[2*er+1][2*ec+1][0].config(bg="#FF0000")
    except:
        pass

buttonFrame = tkinter.Frame(window, bg="#EEEEEE")
buttonFrame.place(relx=0.02, rely=0.02, relheight=0.96, relwidth=0.26)
labyrinthFrame = tkinter.Frame(window, bg="#EEEEEE")
labyrinthFrame.place(relx=0.32, rely=0.02, relheight=0.96, relwidth=0.66)

functionButtons = []
placing = 0.2
functionButtons.append(ttk.Button(buttonFrame, text="Import",  command=importing))
functionButtons.append(ttk.Button(buttonFrame, text="Export",  command=exporting))
functionButtons.append(ttk.Button(buttonFrame, text="Generate",command=generating))
functionButtons.append(ttk.Button(buttonFrame, text="Draw",    command=draw))
functionButtons.append(ttk.Entry(buttonFrame))  # [4] height
functionButtons.append(ttk.Entry(buttonFrame))  # [5] width
functionButtons.append(ttk.Entry(buttonFrame))  # [6] start (r,c)
functionButtons.append(ttk.Entry(buttonFrame))  # [7] end   (r,c)

tkinter.Label(buttonFrame, text="Height:", bg="#EEEEEE").place(rely=placing+0.4, relx=0.14, anchor=tkinter.CENTER)
tkinter.Label(buttonFrame, text="Width:",  bg="#EEEEEE").place(rely=placing+0.5, relx=0.15, anchor=tkinter.CENTER)
tkinter.Label(buttonFrame, text="Start (r,c):", bg="#EEEEEE").place(rely=placing+0.6, relx=0.1, anchor=tkinter.CENTER)
tkinter.Label(buttonFrame, text="End (r,c):",   bg="#EEEEEE").place(rely=placing+0.7, relx=0.1, anchor=tkinter.CENTER)

start_entry = functionButtons[6]
end_entry   = functionButtons[7]

for btn in functionButtons:
    btn.place(relx=0.5, rely=placing, anchor=tkinter.CENTER, relwidth=0.5)
    placing += 0.1

window.mainloop()

import ast
import tkinter
import tkinter.ttk as ttk

window = tkinter.Tk()
window.title("Labyrinth Creator")
window.geometry("800x400")

labyrinthRaws = []

def importing():
    data = input("İnput Labyrinth Code as a List: ")
    code_matrix = ast.literal_eval(data)
    h = len(code_matrix)
    w = len(code_matrix[0]) if h>0 else 0
    functionButtons[4].delete(0, "end")
    functionButtons[4].insert(0, str(h))
    functionButtons[5].delete(0, "end")
    functionButtons[5].insert(0, str(w))
    draw()
    for r in range(h):
        for c in range(w):
            v = code_matrix[r][c]
            ri = 2*r+1
            ci = 2*c+1
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

def exporting():
    height = int(functionButtons[4].get())
    width  = int(functionButtons[5].get())
    labyrinthCode = [[0 for _ in range(width)] for __ in range(height)]
    for r in range(height):
        for c in range(width):
            code = 0
            row_idx = 2 * r + 1
            col_idx = 2 * c + 1
            if col_idx - 1 >= 0:
                w = labyrinthRaws[row_idx][col_idx-1][0]
                if isinstance(w, tkinter.Button) and w.cget("bg") == "#000000":
                    code |= 1
            if col_idx + 1 < len(labyrinthRaws[row_idx]):
                w = labyrinthRaws[row_idx][col_idx+1][0]
                if isinstance(w, tkinter.Button) and w.cget("bg") == "#000000":
                    code |= 2
            if row_idx - 1 >= 0:
                w = labyrinthRaws[row_idx-1][col_idx][0]
                if isinstance(w, tkinter.Button) and w.cget("bg") == "#000000":
                    code |= 4
            if row_idx + 1 < len(labyrinthRaws):
                w = labyrinthRaws[row_idx+1][col_idx][0]
                if isinstance(w, tkinter.Button) and w.cget("bg") == "#000000":
                    code |= 8
            labyrinthCode[r][c] = code
    print(labyrinthCode)

def generating():
    pass

def draw():
    def wallToggle(b):
        nc = "#FFFFFF" if b.cget("bg") == "#000000" else "#000000"
        b.config(bg=nc)
    for w in labyrinthFrame.winfo_children():
        w.destroy()
    global labyrinthRaws
    labyrinthRaws = []
    height = int(functionButtons[4].get())
    width  = int(functionButtons[5].get())
    rows = 2*height + 1
    cols = 2*width  + 1
    for i in range(rows):
        labyrinthRaws.append([])
        for j in range(cols):
            labyrinthRaws[i].append([])
            if i%2==0 and j%2!=0:
                btn = tkinter.Button(labyrinthFrame, width=20, height=1, padx=0, pady=0, bg="#FFFFFF", font=("Arial",1))
                btn.grid(row=i, column=j)
                btn.config(command=lambda b=btn: wallToggle(b))
                labyrinthRaws[i][j].append(btn)
            elif i%2!=0 and j%2==0:
                btn = tkinter.Button(labyrinthFrame, width=1, height=10, padx=0, pady=0, bg="#FFFFFF", font=("Arial",1))
                btn.grid(row=i, column=j)
                btn.config(command=lambda b=btn: wallToggle(b))
                labyrinthRaws[i][j].append(btn)
            else:
                fr = tkinter.Frame(labyrinthFrame)
                fr.grid(row=i, column=j)
                labyrinthRaws[i][j].append(fr)

buttonFrame = tkinter.Frame(window, bg="#EEEEEE")
buttonFrame.place(relx=0.02, rely=0.02, relheight=0.96, relwidth=0.26)
labyrinthFrame = tkinter.Frame(window, bg="#EEEEEE")
labyrinthFrame.place(relx=0.32, rely=0.02, relheight=0.96, relwidth=0.66)

functionButtons = []
placing = 0.2
functionButtons.append(ttk.Button(buttonFrame, text="Import", command=importing))
functionButtons.append(ttk.Button(buttonFrame, text="Export", command=exporting))
functionButtons.append(ttk.Button(buttonFrame, text="Generate", command=generating))
functionButtons.append(ttk.Button(buttonFrame, text="Draw", command=draw))
functionButtons.append(ttk.Entry(buttonFrame))
functionButtons.append(ttk.Entry(buttonFrame))
tkinter.Label(buttonFrame, text="Height:", bg="#EEEEEE").place(rely=placing+0.4, relx=0.15, anchor=tkinter.CENTER)
tkinter.Label(buttonFrame, text="Width:",  bg="#EEEEEE").place(rely=placing+0.5, relx=0.15, anchor=tkinter.CENTER)

for btn in functionButtons:
    btn.place(relx=0.5, rely=placing, anchor=tkinter.CENTER, relwidth=0.5)
    placing += 0.1

window.mainloop()

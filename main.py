import tkinter as tk

root = tk.Tk()

root.geometry("600x400")

root.grid_columnconfigure(0, weight=1)
frm = tk.Frame(root)
frm.grid()
b = tk.Label(frm, text="Welcome to the EarthQuake DIRECTORY!!", font=("impact", 24) ).grid(column=0, row=0)
a = tk.Button(frm, text="Search")
    
a.place(x=240, y=70)



entry = tk.Entry(root)
entry.place(x=240, y=50)




root.mainloop()





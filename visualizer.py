import tkinter as tk

window = tk.Tk()
window.title("Java O-O Visualizer")
window.geometry("950x550")

step = 0

code_frame = tk.Frame(window, width=450)
code_frame.pack(side="left", fill="both", expand=True)

code_label = tk.Label(
    code_frame,
    text="Java Code",
    font=("Arial", 18, "bold")
)
code_label.pack(pady=20)

code_text = tk.Label(
    code_frame,
    text="Car c1 = new Car();",
    font=("Courier", 16),
)
code_text.pack(pady=50)

diagram_frame = tk.Frame(window, width=500)
diagram_frame.pack(side="right", fill="both", expand=True)

diagram_label = tk.Label(
    diagram_frame,
    text="Memory Diagram",
    font=("Arial", 18, "bold")
)
diagram_label.pack(pady=20)

canvas = tk.Canvas(
    diagram_frame,
    width=450,
    height=380,
    bg="white"
)
canvas.pack()


def next_step():
    global step

    if step == 0:
        canvas.create_text(65, 55, text="c1", font=("Arial", 16))
        canvas.create_rectangle(35, 75, 95, 110, width=2)

        canvas.create_oval(160, 90, 410, 340, width=3)
        canvas.create_text(285, 125, text="Car", font=("Arial", 20))

        canvas.create_text(285, 180, text="speed", font=("Arial", 14))
        canvas.create_rectangle(250, 195, 320, 230, width=2)

        canvas.create_text(285, 270, text="direction", font=("Arial", 14))
        canvas.create_rectangle(250, 285, 320, 320, width=2)

        canvas.create_line(
            95, 92, 185, 130,
            arrow=tk.LAST,
            width=3,
            smooth=True
        )

        step = 1


next_button = tk.Button(
    code_frame,
    text="Next Step",
    font=("Arial", 14),
    command=next_step
)
next_button.pack(pady=20)

window.mainloop()

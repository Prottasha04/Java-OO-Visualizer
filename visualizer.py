import tkinter as tk

CODE = [
    'Car c1 = new Car();',
    'Car c2 = new Car(20, 90, "sedan");',
    'c1.accelerate(50);',
    'Car c3 = c2;',
    'int hello = 3;'
]

class Visualizer:
    def __init__(self, root):
        self.root = root
        root.title('Java O-O Visualizer')
        root.geometry('1270x800')
        root.minsize(1200, 790)
        self.step = 0
        self.animating = False
        self.playing = False
        self.timer = None

        left = tk.Frame(root, padx=18, pady=18)
        left.pack(side='left', fill='both', expand=True)
        right = tk.Frame(root, padx=10, pady=18)
        right.pack(side='right', fill='y')
        tk.Label(left, text='Java Code', font=('Arial', 19, 'bold')).pack(anchor='w')
        self.code_box = tk.Text(left, height=9, width=43, font=('Courier', 14),
                                wrap='none', padx=10, pady=15, bg='#f5f5f5', relief='flat')
        self.code_box.pack(fill='x', pady=(12, 15))
        for line in CODE:
            self.code_box.insert('end', line + '\n')
        self.code_box.tag_configure('active', background='#ffe49a')
        self.code_box.configure(state='disabled')
        self.status = tk.Label(left, text='', font=('Arial', 12),
                               anchor='w', justify='left', wraplength=460)
        self.status.pack(fill='x', pady=8)
        controls = tk.Frame(left)
        controls.pack(anchor='w', pady=10)
        self.next_button = tk.Button(controls, text='Next Step', width=12, command=self.next_step)
        self.next_button.pack(side='left', padx=(0, 8))
        self.play_button = tk.Button(controls, text='Auto Play', width=12, command=self.toggle_play)
        self.play_button.pack(side='left', padx=(0, 8))
        tk.Button(controls, text='Reset', width=9, command=self.reset).pack(side='left')

        tk.Label(right, text='Memory Diagram', font=('Arial', 19, 'bold')).pack()
        self.canvas = tk.Canvas(right, width=660, height=690, bg='white',
                                highlightthickness=1, highlightbackground='#ddd')
        self.canvas.pack(pady=12)
        self.reset()

    def highlight(self, index):
    
        self.code_box.configure(state='normal')
        self.code_box.tag_remove('active', '1.0', 'end')
        self.code_box.tag_add('active', f'{index+1}.0', f'{index+1}.end')
        self.code_box.configure(state='disabled')

    def draw_variable(self, name, x, y, value=None):
       
        self.canvas.create_text(x-53, y, text=name, font=('Arial', 14), anchor='e')
        self.canvas.create_rectangle(x-34, y-17, x+34, y+17, width=2)
        if value is not None:
            self.canvas.create_text(x, y, text=str(value), font=('Arial', 14))

    def draw_car(self, cx, cy, title, speed, direction, tag, with_type=False):
    
        c = self.canvas
        radius = 112
        c.create_oval(cx-radius, cy-radius, cx+radius, cy+radius,
                      width=3, tags=tag)
        c.create_text(cx, cy-76, text=title, font=('Arial', 17, 'bold'), tags=tag)
        for offset, label, value in [(-27, 'speed', speed), (28, 'direction', direction)]:
            c.create_text(cx-42, cy+offset, text=label, font=('Arial', 11), tags=tag)
            c.create_rectangle(cx+17, cy+offset-15, cx+70, cy+offset+15,
                               width=2, tags=tag)
            c.create_text(cx+43, cy+offset, text=str(value), font=('Arial', 12), tags=tag)
        if with_type:
            c.create_text(cx-42, cy+76, text='type', font=('Arial', 11), tags=tag)
            c.create_rectangle(cx+17, cy+62, cx+70, cy+90, width=2, tags=tag)

    def draw_accelerate_callout(self):
       
        c = self.canvas
        c.create_text(245, 320, text='accelerate(50)',
                      font=('Arial', 12, 'bold'), anchor='w', tags='accelerate_note')
        c.create_line(305, 305, 322, 282, 338, 259,
                      fill='black', width=1.5, tags='accelerate_note')

    def draw_string(self):
        c = self.canvas
        c.create_oval(502, 297, 632, 397, width=2, tags='string')
        c.create_text(567, 322, text='String', font=('Arial', 15), tags='string')
        c.create_text(567, 361, text='"sedan"', font=('Arial', 13), tags='string')

    def animate_reverse_arrow(self, start, end, done, bend=-25, arrow_at_start=False):
     
        sx, sy = start
        ex, ey = end
        mx = (sx+ex)/2
        my = (sy+ey)/2 + bend
        points = []
        for i in range(41):
            t = i/40
            x = (1-t)**2*sx + 2*(1-t)*t*mx + t*t*ex
            y = (1-t)**2*sy + 2*(1-t)*t*my + t*t*ey
            points.append((x, y))
       
        arrow_direction = tk.FIRST if arrow_at_start else tk.LAST
        line = self.canvas.create_line(ex, ey, ex, ey, fill='#2475b8',
                                       width=3, arrow=arrow_direction,
                                       arrowshape=(12, 14, 5))
        self.animating = True

        def frame(i):
            # Draw from point i to the endpoint, revealing the path in reverse.
            section = points[40-i:]
            coords = [coord for point in section for coord in point]
            if len(coords) < 4:
                coords = [ex, ey, ex, ey]
            self.canvas.coords(line, *coords)
            if i < 40:
                self.timer = self.root.after(16, lambda: frame(i+1))
            else:
                self.animating = False
                done()
        frame(0)

    def next_step(self):
        if self.animating or self.step >= len(CODE):
            return
        current = self.step
        self.step += 1
        self.highlight(current)
        self.status.config(text=f'Step {self.step}/5: {CODE[current]}')

        if current == 0:
            self.draw_variable('c1', 110, 125)
            self.draw_car(360, 165, 'Car #1', 0, 0, 'car1')
            self.animate_reverse_arrow((110, 125), (253, 131), self.after_step)
        elif current == 1:
            self.draw_variable('c2', 110, 435)
            self.draw_car(360, 465, 'Car #2', 20, 90, 'car2', with_type=True)
            self.draw_string()
            self.animate_reverse_arrow((110, 435), (250, 420),
                lambda: self.animate_reverse_arrow((403, 541), (522, 380), self.after_step, bend=45))
               
                #Problem!!!!!
            
        elif current == 2:
            self.canvas.delete('car1')
            self.draw_car(360, 165, 'Car #1', 50, 0, 'car1')
            self.draw_accelerate_callout()
            self.after_step()
        elif current == 3:
            self.draw_variable('c3', 570, 585)
            self.animate_reverse_arrow((570, 585), (451, 528), self.after_step, bend=30)
        elif current == 4:
            self.draw_variable('hello', 110, 630, value=3)
            self.after_step()

    def after_step(self):
        if self.step == len(CODE):
            self.playing = False
            self.play_button.config(text='Auto Play')
            self.status.config(text='Finished! All five statements have been simulated.')
        elif self.playing:
            self.timer = self.root.after(700, self.next_step)

    def toggle_play(self):
        self.playing = not self.playing
        self.play_button.config(text='Pause' if self.playing else 'Auto Play')
        if self.playing and not self.animating:
            self.next_step()

    def reset(self):
        if self.timer is not None:
            self.root.after_cancel(self.timer)
            self.timer = None
        self.animating = False
        self.playing = False
        self.step = 0
        self.play_button.config(text='Auto Play')
        self.canvas.delete('all')
        self.code_box.configure(state='normal')
        self.code_box.tag_remove('active', '1.0', 'end')
        self.code_box.configure(state='disabled')
        self.status.config(text='Click Next Step to begin.')

if __name__ == '__main__':
    root = tk.Tk()
    Visualizer(root)
    root.mainloop()

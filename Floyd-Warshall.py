import tkinter as tk
import math
import random

class Node():
    def __init__(self, x, y, index, canvas_index, order_index):
        self.x = x
        self.y = y
        self.index = index
        self.canvas_index = canvas_index
        self.order_index = order_index

class Path():
    def calculation(self, values, count):
        path = [[x for x in range(count)] for y in range(count)]

        for o in range(count):
            for y in range(count):
                if y != o:
                    for x in range(count):
                        if y != x and o != x:
                            if values[y][x] > values[y][o] + values[o][x]:
                                values[y][x] = values[y][o] + values[o][x]
                                path[y][x] = path[y][o]
        
        return values, path

class UI(Path):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("플로이드-워셜 알고리즘")
        self.window.geometry("642x900+600+200")
        self.window.resizable(False, False)
        self.window.update_idletasks()

        self.window_top = tk.Toplevel()
        self.window_top.title("분석 툴")
        self.window_top.geometry("400x700+190+200")
        self.window_top.resizable(False, False)

        self.size = 10
        self.nodes = []
        self.values = []
        self.paths = []
        self.selected = []
        self.analyze_widget = []
        self.collision_sizes = [140, 110, 85, 70, 65, 60, 55, 52, 50, 45, 42, 40, 40, 37, 35, 32]
        
        self.double_linked = tk.IntVar()
        self.order_visible = True
        self.value_visible = False

        self.setting()
        self.setting_top()

        self.canvas.bind("<Button-1>", lambda e: self.click(e.x, e.y))
        self.window.mainloop()

    def setting(self):
        frame = tk.Frame(self.window, bd=1, relief="solid")
        frame.place(x=10, y=10, width=622, height=622)

        self.canvas = tk.Canvas(frame, highlightthickness=0, bg="white")
        self.canvas.place(x=0, y=0, width=620, height=620)

        control = tk.Frame(self.window, bd=1, relief="solid")
        control.place(x=10, y=642, width=622, height=250)

        control_detail = tk.Frame(control)
        control_detail.grid(row=0, column=0, columnspan=2, pady=(15, 0))
        
        tk.Button(control_detail, text="노드 재생성", command=self.make_node).grid(row=0, column=0, padx=10)
        tk.Button(control_detail, text="노드 순서 표시", command=self.order_visible_func).grid(row=0, column=1, padx=10)
        tk.Button(control_detail, text="가중치 표시", command=self.value_visible_func).grid(row=0, column=2, padx=10)
        tk.Button(control_detail, text="계산 시작", command=self.start_algorithm).grid(row=0, column=3, padx=10)
        tk.Label(control_detail, text="노드 찾기: ").grid(row=0, column=4, padx=(10, 0))
        self.find_node_entry = tk.Entry(control_detail, validate="all", validatecommand=(control_detail.register(self.find_node_and_mark), '%P'), width=5)
        self.find_node_entry.grid(row=0, column=5, padx=(0, 10))

        check_frame = tk.Frame(control_detail)
        check_frame.grid(row=1, column=0, columnspan=4, pady=(10, 0))

        tk.Radiobutton(check_frame, text="양뱡향 (가중치 동일)", value=0, variable=self.double_linked, command=self.update).grid(row=0, column=1, padx=10)
        tk.Radiobutton(check_frame, text="양뱡향", value=1, variable=self.double_linked, command=self.update).grid(row=0, column=2, padx=10)
        tk.Radiobutton(check_frame, text="단방향 + 양뱡항", value=2, variable=self.double_linked, command=self.update).grid(row=0, column=3, padx=10)
        tk.Radiobutton(check_frame, text="단방향", value=3, variable=self.double_linked, command=self.update).grid(row=0, column=4, padx=10)

        tk.Label(control, text="노드 갯수: ").grid(row=1, column=0, padx=10, pady=(15, 0))
        self.scale = tk.Scale(control, command=lambda e: self.update(), variable=tk.IntVar(value=100), orient="horizontal", from_=25, to=400, tickinterval=25, resolution=25, length=515)
        self.scale.grid(row=1, column=1)

        result_frame = tk.Frame(control)
        result_frame.grid(row=2, column=0, columnspan=2, pady=(15, 0))

        tk.Label(result_frame, text="최단 경로: ").grid(row=0, column=0)
        tk.Label(result_frame, text="최단 길이: ").grid(row=1, column=0)
        tk.Label(result_frame, text="평균 경로 가중치 값: ").grid(row=2, column=0)

        self.path_route = tk.Label(result_frame, wraplength=480)
        self.path_route.grid(row=0, column=1)

        self.min_value = tk.Label(result_frame)
        self.min_value.grid(row=1, column=1)

        self.avg_value = tk.Label(result_frame)
        self.avg_value.grid(row=2, column=1)

        self.make_node()

    def setting_top(self):
        frame = tk.Frame(self.window_top, name="frame", bd=1, relief="solid")
        frame.place(x=10, y=10, width=380, height=680)

        tk.Label(frame, text="차수의 총 갯수").grid(row=0, column=0, sticky="w")
        tk.Label(frame, text="한 노드에 연결된 최대 차수").grid(row=1, column=0, sticky="w")
        tk.Label(frame, text="한 노드에 연결된 최소 차수").grid(row=2, column=0, sticky="w")
        tk.Label(frame, text="한 노드에 연결된 평균 차수").grid(row=3, column=0, sticky="w")
        tk.Label(frame, text="모든 가중치의 총합").grid(row=4, column=0, sticky="w")
        tk.Label(frame, text="모든 경로의 갯수 총합").grid(row=5, column=0, sticky="w")
        tk.Label(frame, text="최대 가중치를 가진 경로").grid(row=6, column=0, sticky="w")
        tk.Label(frame, text="최소 가중치를 가진 경로").grid(row=7, column=0, sticky="w")
        tk.Label(frame, text="많은 경유지를 거친 경로").grid(row=8, column=0, sticky="w")

        for i in range(9):
            tk.Label(frame, text=": ").grid(row=i, column=1, sticky="w")
            self.analyze_widget.append(tk.Label(frame))
            self.analyze_widget[-1].grid(row=i, column=2, sticky="w")

        grid_frame = tk.Frame(frame, name="grid_f", bd=1, relief="solid")
        grid_frame.place(x=42, y=331, width=330, height=340)

        row_frame = tk.Frame(frame, name="row_f", bd=1, relief="solid")
        row_frame.place(x=6, y=331, width=30, height=340)

        column_frame = tk.Frame(frame, name="column_f", bd=1, relief="solid")
        column_frame.place(x=42, y=295, width=330, height=30)

        grid_canvas = tk.Canvas(grid_frame, name="grid", highlightthickness=0, bg="white")
        grid_canvas.place(x=0, y=0, width=328, height=338)

        row_canvas = tk.Canvas(row_frame, name="row", highlightthickness=0, bg="white")
        row_canvas.place(x=0, y=0, width=28, height=338)

        column_canvas = tk.Canvas(column_frame, name="column", highlightthickness=0, bg="white")
        column_canvas.place(x=0, y=0, width=328, height=28)

        value_change_button = tk.Button(frame, name="change", text="수정된 가중치로")
        value_change_button.place(x=10, y=260, width=100)
        value_change_button.configure(command=lambda: change(grid_canvas, value_change_button))

        result_label = tk.Label(frame, text=" =  ")
        result_label.place(x=255, y=262)

        tk.Label(frame, text="시작 노드").place(x=110, y=244, width=80)
        from_entry = tk.Entry(frame, validate="all")
        from_entry.place(x=130, y=264, width=40)

        tk.Label(frame, text="->").place(x=180, y=262)

        tk.Label(frame, text="도착 노드").place(x=190, y=244, width=80)
        to_entry = tk.Entry(frame, validate="all")
        to_entry.place(x=210, y=264, width=40)

        self.grid_coords = [0, 0]

        def click(x, y):
            self.grid_coords[0] = x
            self.grid_coords[1] = y
        
        def drag(x, y, grid_c, row_c, column_c):
            x -= self.grid_coords[0]
            y -= self.grid_coords[1]

            grid_c.scan_dragto(x, y, 1)
            row_c.scan_dragto(0, y, 1)
            column_c.scan_dragto(x, 0, 1)
        
        def release(grid_c, row_c, column_c):
            grid_c.scan_mark(0, 0)
            row_c.scan_mark(0, 0)
            column_c.scan_mark(0, 0)

        def change(grid_c, button):
            flag = button["text"]
            button["text"] = "초기 가중치로" if flag == "수정된 가중치로" else "수정된 가중치로"

            for index in grid_c.find_withtag("before"):
                grid_c.itemconfigure(index, state="hidden" if flag == "수정된 가중치로" else "normal")
            
            for index in grid_c.find_withtag("after"):
                grid_c.itemconfigure(index, state="hidden" if flag == "초기 가중치로" else "normal")
        
        def find_value(start, finish, result_l):
            try:
                try:
                    start = self.window_top.nametowidget(start).get()
                except:
                    pass
                try:
                    finish = self.window_top.nametowidget(finish).get()
                except:
                    pass

                self.window_top.nametowidget(result_l)["text"] = f" =  {self.values[int(start) - 1][int(finish) - 1]}"
            except:
                self.window_top.nametowidget(result_l)["text"] = " =  "

            return True
        
        from_entry.configure(validatecommand=(frame.register(find_value), '%P', to_entry, result_label))
        to_entry.configure(validatecommand=(frame.register(find_value), from_entry, '%P', result_label))

        self.window_top.bind("<Button-3>", lambda e: click(e.x, e.y))
        self.window_top.bind("<B3-Motion>", lambda e: drag(e.x, e.y, grid_canvas, row_canvas, column_canvas))
        self.window_top.bind("<ButtonRelease-3>", lambda e: release(grid_canvas, row_canvas, column_canvas))

    def analyze_before_start(self):
        degree_count = 0
        degree_max = float('-inf')
        degree_min = float('inf')

        for y in range(self.scale.get()):
            degree_connect_count = 0

            for x in range(self.scale.get()):
                degree_connect_count += 1 if self.values[y][x] != float('inf') else 0
                degree_connect_count += 1 if self.values[x][y] != float('inf') else 0

                degree_count += 1 if self.values[y][x] != float('inf') else 0
            
            degree_max = max(degree_max, degree_connect_count)
            degree_min = min(degree_min, degree_connect_count)

        self.analyze_widget[0]["text"] = f"{degree_count} 개"
        self.analyze_widget[1]["text"] = f"{degree_max} 개"
        self.analyze_widget[2]["text"] = f"{degree_min} 개"
        self.analyze_widget[3]["text"] = f"{(degree_count * 2) // self.scale.get()} 개"

        grid_c = self.window_top.nametowidget("frame.grid_f.grid")
        row_c = self.window_top.nametowidget("frame.row_f.row")
        column_c = self.window_top.nametowidget("frame.column_f.column")

        grid_c.delete("all")
        row_c.delete("all")
        column_c.delete("all")

        grid_c.xview_moveto(0)
        grid_c.yview_moveto(0)
        row_c.xview_moveto(0)
        row_c.yview_moveto(0)
        column_c.xview_moveto(0)
        column_c.yview_moveto(0)
        
        grid_c.scan_mark(0, 0)
        row_c.scan_mark(0, 0)
        column_c.scan_mark(0, 0)

        for row in range(self.scale.get()):
            row_c.create_text(3, 3 + 20 * row, text=str(row + 1).rjust(3, ' '), anchor="nw")

        for column in range(self.scale.get()):
            column_c.create_text(2 + 25 * column, 5, text=str(column + 1).rjust(3, ' '), anchor="nw")
        
        for y in range(self.scale.get()):
            for x in range(self.scale.get()):
                if self.values[y][x] != float('inf'):
                    grid_c.create_text(1 + 25 * x, 2 + 20 * y, text=str(self.values[y][x]).rjust(3, ' '), anchor="nw", tags="before")
                
                grid_c.create_line(25 * x - 1, -1, 25 * x - 1, 20 * self.scale.get() - 1, fill="gray")
            grid_c.create_line(-1, 20 * y - 1, 25 * self.scale.get() - 1, 20 * y - 1, fill="gray")

        grid_c.create_line(25 * self.scale.get() - 1, -1, 25 * self.scale.get() - 1, 20 * self.scale.get(), fill="gray")
        grid_c.create_line(-1, 20 * self.scale.get() - 1, 25 * self.scale.get(), 20 * self.scale.get() - 1, fill="gray")

    def analyze_after_start(self, sum_value, avg_count, values):
        self.analyze_widget[4]["text"] = f"{sum_value}"
        self.analyze_widget[5]["text"] = f"{avg_count} 개"

        self.window_top.nametowidget("frame.change")["text"] = "수정된 가중치로"

        for y in range(self.scale.get()):
            for x in range(self.scale.get()):
                if values[y][x] != float('inf'):
                    self.window_top.nametowidget("frame.grid_f.grid").create_text(2 + 25 * x, 3 + 20 * y, text=str(values[y][x]).rjust(3, ' '), fill="red" if self.values[y][x] != values[y][x] and self.values[y][x] != float('inf') else "black", anchor="nw", state="hidden", tags="after")

        max_value = float('-inf')
        min_value = float('inf')
        long_count = float('-inf')
        max_path = ""
        min_path = ""
        long_path = ""

        for y in range(self.scale.get()):
            for x in range(self.scale.get()):
                if values[y][x] != float('inf'):
                    if max_value < values[y][x]:
                        max_value = values[y][x]
                        max_path = f"{y + 1} -> {x + 1}"
                    if min_value > values[y][x]:
                        min_value = values[y][x]
                        min_path = f"{y + 1} -> {x + 1}"

                    next, count = y, 0
                    while next != x:
                        next = self.paths[next][x]
                        count += 1
                    
                    if long_count < count:
                        long_count = count
                        long_path = f"{(y + 1)} -> {x + 1}"

        self.analyze_widget[6]["text"] = f"{max_path} / 가중치: {max_value}"
        self.analyze_widget[7]["text"] = f"{min_path} / 가중치: {min_value}"
        self.analyze_widget[8]["text"] = f"{long_path} / 경유지 갯수: {long_count - 1}"

    def make_node(self):
        self.nodes.clear()
        self.values.clear()
        self.canvas.delete("all")

        overlap_size = 10

        for y in range(20):
            for x in range(20):
                while (True):
                    x, y = random.randint(10, 600), random.randint(10, 600)
                    collisions = self.canvas.find_overlapping(x - overlap_size, y - overlap_size, x + self.size + overlap_size, y + self.size + overlap_size)

                    if len(collisions) <= 0:
                        index = self.canvas.create_oval(x, y, x + self.size, y + self.size, fill="white")
                        order_index = self.canvas.create_text(x + self.size // 2, y - 7, text=f"{len(self.nodes) + 1}", state="hidden", tags="order")
                        self.nodes.append(Node(x, y, len(self.nodes), index, order_index))
                        break
        
        self.update()

    def make_value(self):
        self.canvas.delete("value")
        self.canvas.delete("value_line")
        coll_size = self.collision_sizes[self.scale.get() // 25 - 1]
        self.values = [[float('inf') for i in range(400)] for p in range(400)]

        def circle_coords(x, y, x2, y2):
            radian = math.atan2(y2 - y, x2 - x)
            rx = x + math.cos(radian) * (self.size // 2)
            ry = y + math.sin(radian) * (self.size // 2)

            radian = math.atan2(y - y2, x - x2)
            rx2 = x2 + math.cos(radian) * (self.size // 2)
            ry2 = y2 + math.sin(radian) * (self.size // 2)

            return rx, ry, rx2, ry2

        for node in self.nodes:
            if node.index >= self.scale.get(): break
            collisions = list(self.canvas.find_enclosed(node.x - coll_size, node.y - coll_size, node.x + self.size + coll_size, node.y + self.size + coll_size))
            del collisions[collisions.index(node.canvas_index)]

            for collision in collisions:
                if self.find_node_index(collision) == None:
                    continue

                node_c = self.nodes[self.find_node_index(collision)]
                if len(self.canvas.find_withtag(f"{node_c.index}_{node.index}")) <= 0 and len(self.canvas.find_withtag(f"{node.index}_{node_c.index}")) <= 0:
                    if self.double_linked.get() == 0 or self.double_linked.get() == 1 or (self.double_linked.get() == 2 and random.randint(0, 10) > 5) or (self.double_linked.get() == 3 and random.randint(0, 10) > 5):
                        self.values[node.index][node_c.index] = random.randint(1, 31)
                        self.canvas.create_text(node.x - (node.x - node_c.x) // 2, node.y - (node.y - node_c.y) // 2 - 10, anchor="center", state="hidden" if not self.value_visible else "normal", text=f"{self.values[node.index][node_c.index]}", tags=("value", f"{node.index}_{node_c.index}_value"))
                        rx, ry, rx2, ry2 = circle_coords(node.x + self.size // 2, node.y + self.size // 2, node_c.x + self.size // 2, node_c.y + self.size // 2)
                        self.canvas.create_line(rx, ry, rx2, ry2, arrow="last", arrowshape=(0, 0, 0), tags=("value_line", f"{node.index}_{node_c.index}"))

                    if self.double_linked.get() == 0 or self.double_linked.get() == 1 or (self.double_linked.get() == 2 and random.randint(0, 10) > 5) or (self.double_linked.get() == 3 and len(self.canvas.find_withtag(f"{node.index}_{node_c.index}")) <= 0):
                        self.values[node_c.index][node.index] = random.randint(1, 31) if self.double_linked.get() != 0 else self.values[node.index][node_c.index]
                        self.canvas.create_text(node.x - (node.x - node_c.x) // 2, node.y - (node.y - node_c.y) // 2 - 20, anchor="center", state="hidden" if not self.value_visible else "normal", text=f"{self.values[node_c.index][node.index]}", tags=("value", f"{node_c.index}_{node.index}_value"))
                        rx, ry, rx2, ry2 = circle_coords(node.x + self.size // 2, node.y + self.size // 2, node_c.x + self.size // 2, node_c.y + self.size // 2)
                        self.canvas.create_line(rx2, ry2, rx, ry, arrow="last", arrowshape=(0, 0, 0), tags=("value_line", f"{node_c.index}_{node.index}"))

        for node in self.nodes:
            self.canvas.lift(node.canvas_index)

    def node_visible_count(self):
        for node in self.nodes:
            self.canvas.itemconfigure(node.canvas_index, state="normal" if node.index < self.scale.get() else "hidden", fill="white", width=1)
            self.canvas.itemconfigure(node.order_index, state="normal" if node.index < self.scale.get() and self.order_visible else "hidden")

    def order_visible_func(self):
        self.order_visible = not self.order_visible
        self.node_visible_count()
    
    def value_visible_func(self):
        self.value_visible = not self.value_visible
        for canvas_index in self.canvas.find_withtag("value"):
            self.canvas.itemconfigure(canvas_index, state="hidden" if not self.value_visible else "normal")

    def update(self):
        self.paths.clear()
        self.selected.clear()
        self.path_route["text"] = ""
        self.min_value["text"] = ""
        self.avg_value["text"] = ""
        self.canvas.delete("mark")
        self.find_node_entry.delete(0, "end")
        self.node_visible_count()
        self.make_value()

    def start_algorithm(self):
        if len(self.paths) > 0:
            return

        self.analyze_before_start()

        values, self.paths = self.calculation([y[:] for y in self.values], self.scale.get())
        sum_value = 0
        avg_count = 0
        
        for y in range(self.scale.get()):
            for x in range(self.scale.get()):
                if values[y][x] != float('inf'):
                    if values[y][x] != self.values[y][x]:
                        self.canvas.itemconfigure(f"{y}_{x}_value", text=f"{values[y][x]}", fill="red")

                    sum_value += values[y][x]
                    avg_count += 1

        self.analyze_after_start(sum_value, avg_count, values)

        self.values = values
        self.path_route["text"] = ""
        self.min_value["text"] = ""
        self.avg_value["text"] = f"{sum_value / avg_count}"

    def find_node_index(self, canvas_index):
        for node in self.nodes:
            if node.canvas_index == canvas_index:
                return node.index

    def find_node_and_mark(self, index):
        try:
            self.canvas.delete("mark")
            index = int(index) - 1
            if self.canvas.itemcget(self.nodes[index].canvas_index, "state") == "normal":
                x = self.nodes[index].x
                y = self.nodes[index].y
                self.canvas.create_oval(x - 10, y - 10, x + self.size + 10, y + self.size + 10, width=3, outline="red", tags="mark")
        except:
            pass

        return True

    def click(self, x, y):
        self.canvas.delete("mark")
        if len(self.selected) >= 2:
            self.node_visible_count()
            for index in self.canvas.find_withtag("value_line"):
                self.canvas.itemconfigure(index, fill="black", arrowshape=(0, 0, 0), width=1)

            for node in self.nodes:
                self.canvas.lift(node.canvas_index)

            self.selected.clear()

        for node in self.nodes:
            if node.x <= x and node.x + self.size >= x and node.y <= y and node.y + self.size >= y:
                self.canvas.itemconfigure(node.canvas_index, fill="red", width=2)
                self.selected.append(node)
                break
        
        if len(self.selected) >= 2:
            self.min_value["text"] = f"{self.values[self.selected[0].index][self.selected[1].index]}"
            if self.values[self.selected[0].index][self.selected[1].index] == float('inf'):
                return

            if len(self.paths) > 0:
                start, finish = self.selected[0].index, self.selected[1].index

                if self.paths[start][finish] == -1:
                    self.path_route["text"] = f"{start + 1} - {finish + 1}"
                    index = self.canvas.find_withtag(f"{before_start}_{start}")[0]
                    self.canvas.itemconfigure(index, fill="red", arrowshape=(8, 10, 3), width=3)
                    self.canvas.lift(index)
                    return
                
                temp_path = [start + 1]
                while (start != finish):
                    before_start = start
                    start = self.paths[start][finish]
                    index = self.canvas.find_withtag(f"{before_start}_{start}")[0]
                    self.canvas.itemconfigure(index, fill="red", arrowshape=(8, 10, 3), width=3)
                    self.canvas.lift(index)
                    temp_path.append(start + 1)

                for index in temp_path:
                    self.canvas.lift(self.nodes[index - 1].canvas_index)
                
                self.path_route["text"] = "-".join(str(i) for i in temp_path)

UI()
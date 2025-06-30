from manim import *
import numpy as np
import random

class UABModel(Scene):
    def construct(self):    
        dGrid = NumberPlane(
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"include_ticks": False, "stroke_opacity": 0}
        )
        self.play(FadeIn(dGrid))
        
        # === Part 3: information dissemination simulation ===
        self.total_agents = 500
        self.share_radius = 0.15  
        self.sharing_rate = 0.08  
        self.ignore_rate = 0.05   
        self.speed = 0.04         

        # Setup areas
        self.setup_areas()
        self.create_agents()
        self.setup_chart()

        # Initialize data tracking and simnulation 
        self.time_step = 0
        self.chart_data = []
        self.run_simulation()

    def setup_areas(self):
        self.sim_rect = Rectangle(width=6, height=4.5, color=WHITE).shift(LEFT * 3.75)
        self.chart_rect = Rectangle(width=7, height=4.5, color=WHITE).shift(RIGHT * 3.25)
        sim_label = Text("Agents", font_size=26).next_to(self.sim_rect, UP, buff=0.1)
        chart_label = Text("Information Chart", font_size=26).next_to(self.chart_rect, UP, buff=0.1)
        
        self.play(FadeIn(self.sim_rect), FadeIn(self.chart_rect), FadeIn(sim_label), FadeIn(chart_label), run_time=0.4)

    def create_agents(self):
        self.agents = []

        self.left_bound = -6.5
        self.right_bound = -1
        self.top_bound = 2
        self.bottom_bound = -2

        for i in range(self.total_agents):
            x = random.uniform(self.left_bound + 0.2, self.right_bound - 0.2)
            y = random.uniform(self.bottom_bound + 0.2, self.top_bound - 0.2)

            dot = Dot(radius=0.04).move_to([x, y, 0])

            if i < 5:  
                dot.set_color(RED)
                state = "aware"
                info_time = 0
            else:
                dot.set_color(GREEN)
                state = "unaware"
                info_time = -1

            dot.state = state
            dot.info_time = info_time
            dot.vx = random.uniform(-self.speed, self.speed)
            dot.vy = random.uniform(-self.speed, self.speed)

            self.agents.append(dot)
            self.add(dot)

    def setup_chart(self):
        self.axes = Axes(
            x_range=[0, 825, 200],
            y_range=[0, self.total_agents, 100],
            x_length=6.4,
            y_length=4,
            axis_config={"color": WHITE}
        ).shift(RIGHT * 3.5)
        self.add(self.axes)

        x_label = self.axes.get_x_axis_label("Time").scale(0.7)
        y_label = self.axes.get_y_axis_label("Count").scale(0.7).shift(0.4*DOWN)
        self.add(x_label, y_label)

        legend = VGroup(
            VGroup(Dot(radius=0.08, color=GREEN), Text("Unaware", font_size=14, color=GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Dot(radius=0.08, color=RED), Text("Aware", font_size=14, color=RED)).arrange(RIGHT, buff=0.1),
            VGroup(Dot(radius=0.08, color=BLUE), Text("Bored", font_size=14, color=BLUE)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(self.chart_rect, DOWN, buff=0.3)
        self.add(legend)

        self.stats = VGroup()
        self.unaware_stat = Text("Unaware: 492", font_size=16, color=GREEN_A)
        self.sharing_stat = Text("Aware: 8", font_size=16, color=RED_A)
        self.informed_stat = Text("Bored: 0", font_size=16, color=BLUE_A)

        self.stats.add(self.unaware_stat, self.sharing_stat, self.informed_stat)
        self.stats.arrange(RIGHT, buff=0.5).next_to(self.sim_rect, DOWN, buff=0.3)
        self.add(self.stats)

    def update_agents(self):
        for dot in self.agents:
            pos = dot.get_center()
            new_x = pos[0] + dot.vx
            new_y = pos[1] + dot.vy

            if new_x <= self.left_bound or new_x >= self.right_bound:
                dot.vx *= -1
                new_x = pos[0]
            if new_y <= self.bottom_bound or new_y >= self.top_bound:
                dot.vy *= -1
                new_y = pos[1]

            dot.move_to([new_x, new_y, 0])

            if dot.state == "aware":
                dot.info_time += 1
                if dot.info_time > 40 and random.random() < self.ignore_rate:
                    dot.state = "bored"
                    dot.set_color(BLUE)

        for i, dot1 in enumerate(self.agents):
            if dot1.state == "aware":
                for j, dot2 in enumerate(self.agents):
                    if i != j and dot2.state == "unaware":
                        d = np.linalg.norm(dot1.get_center() - dot2.get_center())
                        if d < self.share_radius and random.random() < self.sharing_rate:
                            dot2.state = "aware"
                            dot2.set_color(RED)
                            dot2.info_time = 0

    def count_states(self):
        counts = {"unaware": 0, "aware": 0, "bored": 0}
        for dot in self.agents:
            counts[dot.state] += 1
        return counts

    def update_chart(self):
        counts = self.count_states()

        self.remove(self.stats)
        self.unaware_stat = Text(f"Unaware: {counts['unaware']}", font_size=16, color=GREEN)
        self.sharing_stat = Text(f"Aware: {counts['aware']}", font_size=16, color=RED)
        self.informed_stat = Text(f"Bored: {counts['bored']}", font_size=16, color=BLUE)

        self.stats = VGroup(self.unaware_stat, self.sharing_stat, self.informed_stat)
        self.stats.arrange(RIGHT, buff=0.5).next_to(self.sim_rect, DOWN, buff=0.3)
        self.add(self.stats)

        self.chart_data.append({
            'time': self.time_step,
            'unaware': counts['unaware'],
            'aware': counts['aware'],
            'bored': counts['bored']
        })

        if len(self.chart_data) > 1:
            self.draw_chart_lines()

    def draw_chart_lines(self):
        if hasattr(self, 'chart_lines'):
            for line in self.chart_lines:
                self.remove(line)

        self.chart_lines = []
        times = [d['time'] for d in self.chart_data]
        sets = [[d[k] for d in self.chart_data] for k in ['unaware', 'aware', 'bored']]
        colors = [GREEN, RED, BLUE]

        for data, color in zip(sets, colors):
            if len(data) > 1:
                points = [self.axes.coords_to_point(t, val) for t, val in zip(times, data)]
                line = VMobject().set_points_as_corners(points).set_stroke(color, width=3)
                self.add(line)
                self.chart_lines.append(line)
    
    def run_simulation(self):
        for step in range(1200):
            self.time_step = step
            
            if step % 3 == 0:
                self.update_agents()
                self.update_chart()
                self.wait(1/60) 
            
            counts = self.count_states()
            if counts['aware'] == 0 and step > 20:
                break
        self.wait(1)
        
# manim -pqh Manim/2_UABmodel_adaptation.py UABModel
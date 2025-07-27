from manim import *
import numpy as np

class LogisticPopulation(Scene):
    def construct(self):
        dGrid = NumberPlane(
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"include_ticks": False, "stroke_opacity": 0}
        )
        
        self.play(FadeIn(dGrid)) 
        self.wait(0.4)
        
        # Simulation
        
        title = Text("Logistic Growth Model", font_size=36, gradient=(BLUE_B, GREEN_B)).shift(UP * 3)
        title.save_state()
        title.shift(DOWN * 0.3).set_opacity(0)
        
        self.play(title.animate.shift(UP * 0.3).set_opacity(1), run_time=1)
        self.wait(0.5)
        
        K = 5  
        r = 0.0405465  
        
        def logistic_func(t):
            return K / (1 + np.exp(-r * (t - 2000)))

        axes = Axes(
            x_range=[1940, 2060, 10],
            y_range=[0, 6, 1],
            x_length=10,
            y_length=6,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=True
        )
        
        x_label = Text("Year", font_size=20, color=WHITE)
        x_label.next_to(axes.get_x_axis(), DOWN, buff=0.5)
        
        y_label = Text("Population (millions)", font_size=20, color=WHITE)
        y_label.next_to(axes.get_y_axis(), LEFT, buff=0.5).shift(RIGHT)
        y_label.rotate(PI/2)
        
        x_ticks = VGroup()
        x_tick_labels = VGroup()
        for year in range(1950, 2061, 10):
            tick_pos = axes.coords_to_point(year, 0)
            tick = Line(tick_pos + DOWN * 0.1, tick_pos + UP * 0.1, color=WHITE)
            x_ticks.add(tick)
            
            label = Text(str(year), font_size=16, color=WHITE)
            label.next_to(tick, DOWN, buff=0.15)
            x_tick_labels.add(label)
        
        y_ticks = VGroup()
        y_tick_labels = VGroup()
        for pop in range(1, 6):
            tick_pos = axes.coords_to_point(1940, pop)
            tick = Line(tick_pos + LEFT * 0.1, tick_pos + RIGHT * 0.1, color=WHITE)
            y_ticks.add(tick)
            
            label = Text(str(pop), font_size=16, color=WHITE)
            label.next_to(tick, LEFT, buff=0.15)
            y_tick_labels.add(label)
        
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=2)
        
        self.play(Create(x_ticks), Create(y_ticks), Write(x_tick_labels), Write(y_tick_labels), run_time=1.5)
        
        info_1 = MathTex(r"P_0 = 2.5 \text{ M (Y: 2000)}", font_size=24)
        info_2 = MathTex(r"P_{10} = 3.0 \text{ M (Y: 2010)}", font_size=24)

        info_1.to_corner(UR, buff=0.6)
        info_2.next_to(info_1, DOWN, aligned_edge=RIGHT, buff=0.3)

        self.play(Write(info_1), Write(info_2), run_time=1.8)
        self.wait(1.75)
        
        k_line = axes.get_horizontal_line(axes.coords_to_point(2060, K), color=YELLOW)
        k_label = Text("K = 5 million", font_size=20, color=YELLOW)
        k_label.next_to(k_line, RIGHT, buff=0.3)
        
        self.play(Create(k_line), Write(k_label), run_time=1.5)
        self.wait(3.5)
        
        curve = axes.plot(
            logistic_func,
            x_range=[1940, 2060],
            color=BLUE_B,
            stroke_width=4
        )
        
        self.play(Create(curve), run_time=4)
        self.wait(1)
        
        years = [1950, 1960, 1970, 2000, 2010, 2020, 2030, 2040, 2050]
        populations = [logistic_func(year) for year in years]
        
        dots = VGroup()
        h_lines = VGroup()
        v_lines = VGroup()
        labels = VGroup()
        
        for i, (year, pop) in enumerate(zip(years, populations)):

            dot = Dot(axes.coords_to_point(year, pop), color=RED, radius=0.08)
            dots.add(dot)

            h_line = DashedLine(
                axes.coords_to_point(1940, pop),
                axes.coords_to_point(year, pop),
                color=GRAY,
                stroke_width=2
            )
            h_lines.add(h_line)
            
            v_line = DashedLine(
                axes.coords_to_point(year, 0),
                axes.coords_to_point(year, pop),
                color=GRAY,
                stroke_width=2
            )
            v_lines.add(v_line)
            
            pop_text = Text(f"{pop:.1f}M", font_size=14, color=WHITE)
            if i < 4:  
                pop_text.next_to(dot, UP, buff=0.1)
            else:  
                pop_text.next_to(dot, DOWN, buff=0.1)
            labels.add(pop_text)
        
        for i in range(len(years)):
            self.play(
                Create(h_lines[i]),
                Create(v_lines[i]),
                FadeIn(dots[i]),
                Write(labels[i]),
                run_time=0.8
            )
            self.wait(0.3)
        

        known_dots = VGroup(dots[3], dots[4])  
        self.play(
            known_dots.animate.set_color(GREEN).scale(1.3),
            run_time=1
        )
        self.wait(1)
        
        self.play(
            known_dots.animate.set_color(RED).scale(1/1.3),
            run_time=1
        )
        
        self.play(
            FadeOut(dGrid), FadeOut(axes), FadeOut(x_label), FadeOut(y_label), FadeOut(info_2),
            FadeOut(x_ticks), FadeOut(y_ticks), FadeOut(x_tick_labels), FadeOut(y_tick_labels),
            FadeOut(k_line), FadeOut(k_label), FadeOut(curve), FadeOut(dots), FadeOut(info_1),
            FadeOut(h_lines), FadeOut(v_lines), FadeOut(labels), FadeOut(title), run_time=2
        )
        
        self.wait(2)
        
# manim -pqh Manim/5_pop_simulation.py
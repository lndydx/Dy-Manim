from manim import *
import random

class population(Scene):
    def construct(self):
        dGrid = NumberPlane(
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"include_ticks": False, "stroke_opacity": 0}
        )
        
        earth = Circle(radius=3, color=BLUE).set_fill(BLUE_E, opacity=0.6)
        self.play(FadeIn(earth, dGrid))

        num_dots = 150
        
        red_dots = VGroup()
        for _ in range(num_dots):
            dot = Dot(radius=0.05, color=RED)
            rand_pos = earth.get_center() + random.uniform(-2.7, 2.7) * RIGHT + random.uniform(-2.7, 2.7) * UP

            if np.linalg.norm(rand_pos - earth.get_center()) <= 2.9:
                dot.move_to(rand_pos)
                red_dots.add(dot)

        self.play(
            LaggedStart(*[FadeIn(dot, scale=0.5) for dot in red_dots], 
                       lag_ratio=0.02,    
                       run_time=11.8)        
        )
        self.wait(1) 

        # === Part 1:how population growth
        earth_group = VGroup(earth, red_dots)
        self.play(earth_group.animate.scale(0.65).to_corner(UL))

        birth_dots = VGroup()
        
        dot1 = Dot(radius=0.08, color=YELLOW).move_to(LEFT * 2 + DOWN * 0.5)
        birth_dots.add(dot1)
        
        for i in range(2):
            dot = Dot(radius=0.08, color=YELLOW).move_to(LEFT * 0.5 + DOWN * (0.5 - i * 0.3))
            birth_dots.add(dot)

        for i in range(4):
            dot = Dot(radius=0.08, color=YELLOW).move_to(RIGHT * 1 + DOWN * (0.5 - i * 0.3))
            birth_dots.add(dot)
        
        for i in range(8):
            dot = Dot(radius=0.08, color=YELLOW).move_to(RIGHT * 2.5 + DOWN * (0.5 - i * 0.3))
            birth_dots.add(dot)
            
        for i in range(16):
            dot = Dot(radius=0.08, color=YELLOW).move_to(RIGHT * 4 + DOWN * (0.5 - i * 0.3))
            birth_dots.add(dot)
        current_index = 0
        
        self.play(FadeIn(birth_dots[current_index]), run_time=0.5)
        current_index += 1
        self.wait(0.5)
        
        self.play(LaggedStart(*[FadeIn(birth_dots[current_index + i]) for i in range(2)], lag_ratio=0.2), run_time=0.6)
        current_index += 2
        self.wait(0.5)
        
        self.play(LaggedStart(*[FadeIn(birth_dots[current_index + i]) for i in range(4)], lag_ratio=0.15), run_time=0.8)
        current_index += 4
        self.wait(0.5)

        self.play(LaggedStart(*[FadeIn(birth_dots[current_index + i]) for i in range(8)], lag_ratio=0.1), run_time=1.0)
        current_index += 8
        self.wait(0.5)

        self.play(LaggedStart(*[FadeIn(birth_dots[current_index + i]) for i in range(16)], lag_ratio=0.05), run_time=1.0)
        self.wait(0.5)

        rate_text = Text("Birth Rate > Death Rate", font_size=36).shift(RIGHT)
        rate_text.shift(DOWN * 1.5 + DOWN * 0.3)  
        rate_text.set_opacity(0)
        self.play(rate_text.animate.shift(UP * 0.3).set_opacity(1), run_time=1)
        self.wait(2.2)
        self.play(FadeOut(birth_dots, earth_group, rate_text, dGrid))
        
        # === Part 2: Intro
        main_text = MathTex(r"\ln \frac{dy}{dx}", font_size=120)
        main_text.set_color_by_gradient(BLUE_B, GREEN_B)
        
        circles = VGroup()
        for i in range(8):
            circle = Circle(radius=0.5 + i * 0.3)
            circle.set_stroke(BLUE, width=2, opacity=0.6 - i * 0.05)
            circle.set_fill(opacity=0)
            circles.add(circle)
        
        floating_symbols = VGroup()
        symbols = [r"\int", r"\sum", r"\pi", r"e", r"\infty", r"\nabla"]
        positions = [
            UP * 2 + LEFT * 3,
            UP * 1.5 + RIGHT * 4,
            DOWN * 2 + LEFT * 4,
            DOWN * 1.5 + RIGHT * 3,
            UP * 3 + RIGHT * 2,
            DOWN * 3 + LEFT * 2
        ]
        
        for symbol, pos in zip(symbols, positions):
            math_symbol = MathTex(symbol, font_size=60)
            math_symbol.set_color(DARK_BLUE)
            math_symbol.move_to(pos)
            math_symbol.set_opacity(0.6)
            floating_symbols.add(math_symbol)
        
        self.play(
            LaggedStart(
                *[FadeIn(symbol) for symbol in floating_symbols],
                lag_ratio=0.2
            ), LaggedStart(
                *[Create(circle) for circle in circles],
                lag_ratio=0.2
            ),
            run_time=1.2
        )

        self.play(
            Write(main_text),
            Rotate(circles, angle=2*PI, about_point=ORIGIN), 
            run_time=1.5,
            rate_func=linear
        )
        self.wait(0.8)
        self.play(
            FadeOut(circles), FadeOut(floating_symbols), FadeOut(main_text),
            run_time=1.2
        )
        self.wait(0.5)
        
         # === Part 3: Formula / Equation ===
         
        logistic_title = Text("The Logistic Model", font_size=44, gradient=(BLUE, GREEN)).to_edge(UP)
        equation = MathTex(r"\frac{dP}{dt} = rP\left(1 - \frac{P}{K} \right)").scale(1.1)
        self.play(FadeIn(logistic_title), Write(equation), FadeIn(dGrid))
        self.wait(3)

        self.play(equation.animate.to_corner(UL).shift(DOWN).set_color_by_gradient(GREEN_B, BLUE_B).scale(0.9))
        self.wait(0.8)
        explanation = VGroup(
            MathTex(r"\frac{dP}{dt} = \text{ Rate of population change}").scale(0.8),
            MathTex(r"rP = \text{ Jumlah populasi sekarang}").scale(0.8),
            MathTex(r"1 - \frac{P}{K} = \text{ Population growth brake}").scale(0.8),
            MathTex(r"K = \text{ Carrying capacity}").scale(0.8),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(equation, DOWN, aligned_edge=LEFT, buff=0.5)

        for line in explanation:
            self.play(FadeIn(line), run_time=0.6)
            self.play(Indicate(line, color=YELLOW, scale_factor=1.06), run_time=1)
            self.wait(6)
        
        how = Text("how does this formula work?", font_size=34).next_to(logistic_title, DOWN).to_corner(UR, buff=1).shift(DOWN * 1.5).set_color_by_gradient(BLUE_B, GREEN_B)
        self.play(Write(how))
        self.wait(4.5)
            
        less = Text("P < K: Fast", font_size=28).next_to(how, DOWN, buff=0.5)
        less.save_state()  
        less.shift(DOWN * 0.3).set_opacity(0)  

        self.play(less.animate.shift(UP * 0.3).set_opacity(1), run_time=1)
        self.wait(4)

        approach = Text("P → K: Start to slow down", font_size=28).next_to(less, DOWN, buff=0.5)
        approach.save_state()
        approach.shift(DOWN * 0.3).set_opacity(0)

        self.play(approach.animate.shift(UP * 0.3).set_opacity(1), run_time=1)
        self.wait(4)

        equal = Text("P = K: Stop", font_size=28).next_to(approach, DOWN, buff=0.5)
        equal.save_state()
        equal.shift(DOWN * 0.3).set_opacity(0)

        self.play(equal.animate.shift(UP * 0.3).set_opacity(1), run_time=1)
        self.wait(4.5)
  
        self.play(FadeOut(dGrid, logistic_title, equation, explanation, less, equal, approach, how))
        self.wait(0.5)
        
# manim -pqh Manim/4_population.py
from manim import *

class infSpread(Scene):
    def construct(self):    
        dGrid = NumberPlane(
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"include_ticks": False, "stroke_opacity": 0}
        )
        
        # === Part 1:how information spreads? ===
        # Create persons and arrows
        def create_person(color, name):
            person = VGroup()
            head = Circle(radius=0.2, fill_opacity=1, color=color)
            body = Rectangle(height=0.5, width=0.25, fill_opacity=1, color=color)
            body.next_to(head, DOWN, buff=0)
            text = Text(name, font_size=24).next_to(body, DOWN)
            person.add(head, body, text)
            return person
        
        first_person = create_person(RED, "Acong").to_edge(UP + LEFT, buff=0.5).scale(1.1)
        self.play(FadeIn(first_person), FadeIn(dGrid), run_time=1.25)
        self.wait(6)
        
        arrow = Arrow(start=LEFT, end=RIGHT, buff=0).next_to(first_person, RIGHT, buff=0.5)
        promotion = Text("Ayo Kuliah Di TI Widyatama!", font_size=27).shift(1.5*UP + 4*LEFT).set_color_by_gradient(GREEN_B, BLUE_B)
        
        persons = VGroup(
            create_person(BLUE_A, "Bagas"), 
            create_person(BLUE, "Roi").shift(RIGHT),
        ).next_to(arrow, RIGHT, buff=0.5).scale(1.1)

        self.play(FadeIn(persons, lag_ratio=0.3))
        self.wait(2)
        
        self.play(Create(arrow))
        self.play(FadeIn(promotion))
        self.wait(5)
        
        # Tree diagram for information spread
        # Origin
        start_point = 2 * UP

        # 1st Branch
        receives_info_point = start_point + 1.5 * DOWN + 2 * LEFT
        no_info_point = start_point + 1.5 * DOWN + 2 * RIGHT

        # 2nd Branch
        believes_given_info = receives_info_point + 1.5 * DOWN + 1.2 * LEFT
        doubts_given_info = receives_info_point + 1.5 * DOWN + 1.2 * RIGHT
        believes_given_no_info = no_info_point + 1.5 * DOWN + 1.2 * LEFT
        doubts_given_no_info = no_info_point + 1.5 * DOWN + 1.2 * RIGHT

        # 3rd Branch
        shares_believes_info = believes_given_info + 1.5 * DOWN + 0.8 * LEFT
        keeps_believes_info = believes_given_info + 1.5 * DOWN + 0.8 * RIGHT
        shares_doubts_info = doubts_given_info + 1.5 * DOWN + 0.8 * LEFT
        keeps_doubts_info = doubts_given_info + 1.5 * DOWN + 0.8 * RIGHT
        shares_believes_no_info = believes_given_no_info + 1.5 * DOWN + 0.8 * LEFT
        keeps_believes_no_info = believes_given_no_info + 1.5 * DOWN + 0.8 * RIGHT
        shares_doubts_no_info = doubts_given_no_info + 1.5 * DOWN + 0.8 * LEFT
        keeps_doubts_no_info = doubts_given_no_info + 1.5 * DOWN + 0.8 * RIGHT

        branches_level1 = VGroup(
            Line(start_point, receives_info_point, color=RED_B),
            Line(start_point, no_info_point, color=RED_C),
        )

        branches_level2 = VGroup(
            Line(receives_info_point, believes_given_info, color=BLUE_B),
            Line(receives_info_point, doubts_given_info, color=BLUE_C),
            Line(no_info_point, believes_given_no_info, color=BLUE_B),
            Line(no_info_point, doubts_given_no_info, color=BLUE_C),
        )

        branches_level3 = VGroup(
            Line(believes_given_info, shares_believes_info, color=GREEN_B),
            Line(believes_given_info, keeps_believes_info, color=GREEN_C),
            Line(doubts_given_info, shares_doubts_info, color=GREEN_B),
            Line(doubts_given_info, keeps_doubts_info, color=GREEN_C),
            Line(believes_given_no_info, shares_believes_no_info, color=GREEN_B),
            Line(believes_given_no_info, keeps_believes_no_info, color=GREEN_C),
            Line(doubts_given_no_info, shares_doubts_no_info, color=GREEN_B),
            Line(doubts_given_no_info, keeps_doubts_no_info, color=GREEN_C)
        )
        branches_level1.shift(2*RIGHT)
        branches_level2.shift(2*RIGHT)
        branches_level3.shift(2*RIGHT)
        
        # Copy and animate persons along the branches
        john_copy = first_person.copy()
        alice_copy = persons[0].copy()   
        duke_copy = persons[1].copy()

        self.play(first_person.animate.set_opacity(0.4), john_copy.animate.move_to(branches_level1).shift(1.5*UP).scale(0.8))
        
        self.play(Indicate(john_copy, scale_factor=1.1, color=YELLOW), FadeIn(branches_level1), run_time=1.2)
        self.wait(0.1)
        
        self.play(
            persons[0].animate.set_opacity(0.4), alice_copy.animate.move_to(branches_level2).shift(1.5*UP + 2.5*LEFT).scale(0.8),
            persons[1].animate.set_opacity(0.4), duke_copy.animate.move_to(branches_level2).shift(1.5*UP + 2.5*RIGHT).scale(0.8)
        )
        self.wait(0.1)
        
        self.play(Indicate(alice_copy, scale_factor=1.1, color=YELLOW), Indicate(duke_copy, scale_factor=1.1, color=YELLOW), FadeIn(branches_level2), run_time=1.2)  
        self.wait(0.1)
        
        self.play(FadeIn(branches_level3), run_time=1.2)
        self.wait(0.1)
        
        branches_level4 = Text("......   ......  ......   ......   ......  ......   .......", font_size=40, color=YELLOW_B).next_to(branches_level3, DOWN, buff=0.5)
        self.play(FadeIn(branches_level4))
        self.wait(2)
        
        explanation = MathTex(r"\text{Information} \rightarrow \infty \,?", font_size=48).to_edge(LEFT).shift(0.7*DOWN)
        self.add(explanation)  
        explanation.save_state()
        
        explanation.generate_target()
        explanation.target.shift(UP)  

        self.play(FadeIn(explanation), MoveToTarget(explanation), run_time=1.25)
        self.wait(1)

        # === Part 2: Intro ===
        self.play(FadeOut(branches_level1), FadeOut(branches_level2), FadeOut(branches_level3), FadeOut(branches_level4), FadeOut(john_copy), FadeOut(alice_copy), FadeOut(duke_copy), FadeOut(explanation), FadeOut(first_person), FadeOut(persons), FadeOut(arrow), FadeOut(dGrid), FadeOut(promotion))   
        self.wait(0.2)
        
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
                lag_ratio=0.1
            ),
            run_time=0.8
        )

        self.play(
            Write(main_text),
            Rotate(circles, angle=2*PI, about_point=ORIGIN), 
            run_time=1.3,
            rate_func=linear
        )
        self.wait(0.8)
        self.play(
            FadeOut(circles), FadeOut(floating_symbols), FadeOut(main_text),
            run_time=0.8
        )
                        
# manim -pqh Manim/1_information_spread.py infSpread
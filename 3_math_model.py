from manim import *
import numpy as np

class mathModel(Scene):
    def construct(self):
        dGrid = NumberPlane(
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"include_ticks": False, "stroke_opacity": 0}
        )

        img = ImageMobject("Picture/UAB_Model_VisualizationEn.png").scale(0.16).shift(UP*2 + LEFT*6.6)
        self.play(FadeIn(dGrid), FadeIn(img))  
        self.wait(1.5)     
        
        # === Part 4: mathematical model and explanation === 
        label1 = MathTex("U : ", font_size=36).set_color_by_gradient(GREEN, GREEN_B).shift(DOWN*0.5 + LEFT*6.4)
        label2 = MathTex("A : ", font_size=36).set_color_by_gradient(RED, YELLOW).shift(DOWN*1.5 + LEFT*6.4)
        label3 = MathTex("B : ", font_size=36).set_color_by_gradient(BLUE, TEAL).shift(DOWN*2.5 + LEFT*6.4)
        
        desc1 = Text("Unaware / Who Doesn't Know", font_size=28).next_to(label1, RIGHT, buff=0.2)
        desc2 = Text("Aware / Active Spreader", font_size=28).next_to(label2, RIGHT, buff=0.2)
        desc3 = Text("Bored / Passive Spreader", font_size=28).next_to(label3, RIGHT, buff=0.2)
        
        self.play(FadeIn(label1), FadeIn(desc1), run_time=1)
        self.play(FadeIn(label2), FadeIn(desc2), run_time=1)
        self.play(FadeIn(label3), FadeIn(desc3), run_time=1)
        self.wait(6)
        
        # System differential eq
        eq1 = MathTex(r"\frac{dU}{dt} = -\delta UA \:...(1)").set_color_by_gradient(GREEN, GREEN_B)
        eq2 = MathTex(r"\frac{dA}{dt} = \delta UA - \epsilon A \:...(2)").set_color_by_gradient(RED, YELLOW)
        eq3 = MathTex(r"\frac{dB}{dt} = \epsilon A \:...(3)").set_color_by_gradient(BLUE, TEAL)

        sir_group = VGroup(eq1, eq2, eq3).arrange(DOWN, aligned_edge=LEFT).scale(0.8)
        sir_group.to_edge(RIGHT).shift(UP*2 + LEFT*3.9)
        self.play(Write(eq1), Write(eq2), Write(eq3))
        self.wait(2)
        
        # Highlight the equations
        highlight1 = SurroundingRectangle(eq1, color=GREEN_B, fill_opacity=0.1, stroke_width=2, buff=0.1)
        highlight2 = SurroundingRectangle(eq2, color=RED_B, fill_opacity=0.1, stroke_width=2, buff=0.1)
        highlight3 = SurroundingRectangle(eq3, color=BLUE_B, fill_opacity=0.1, stroke_width=2, buff=0.1)
        
        self.play(Create(highlight1), Create(highlight2), Create(highlight3))
        self.wait(0.3)
        
        self.play(
            highlight1.animate.set_stroke(width=4),
            highlight2.animate.set_stroke(width=4),
            highlight3.animate.set_stroke(width=4),
            run_time=0.5
        )
        self.play(
            highlight1.animate.set_stroke(width=2),
            highlight2.animate.set_stroke(width=2),
            highlight3.animate.set_stroke(width=2),
            run_time=0.5
        )
        self.wait(1)
        
        # === Part 5: Index of Virality ===
        Vo = MathTex(r"V_o = \frac{Rate \,of \,Spread}{Stop \,Speed}", font_size=45).to_edge(UP).shift(LEFT * 4.5 + DOWN)
        self.add(Vo)  
        Vo.save_state()
        
        Vo.generate_target()
        Vo.target.shift(0.5*UP)  
        self.play(
            FadeOut(highlight1), FadeOut(highlight2), FadeOut(highlight3), FadeOut(sir_group), FadeOut(img), FadeOut(label1), FadeOut(desc1), FadeOut(label2), FadeOut(desc2), FadeOut(label3), FadeOut(desc3), FadeIn(Vo), MoveToTarget(Vo), run_time=1.25
            )
        Vo_formula = MathTex(r"V_o = \frac{\delta}{\epsilon}", font_size=40).to_edge(UP).shift(LEFT * 5.5 + DOWN * 0.5)
        
        highlight4 = SurroundingRectangle(Vo_formula, color=BLUE_B, stroke_width=2, buff=0.1)

        self.wait(0.8)
        self.play(Transform(Vo, Vo_formula))
        self.wait(0.1)
        self.play(Create(highlight4))
        self.wait(0.5)
        
        self.create_graph_vo_less_than_1()
        self.create_graph_vo_equals_1()
        self.create_graph_vo_greater_than_1()
        
        self.wait(1)

    def create_graph_vo_less_than_1(self):
        axes1 = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 1, 0.2],
            x_length=3.5,
            y_length=2.5,
            axis_config={"color": WHITE, "stroke_width": 1}
        ).shift(LEFT * 4.5 + DOWN)
        
        x_label1 = axes1.get_x_axis_label("t", direction=LEFT).scale(0.8).shift(RIGHT*0.4)
        y_label1 = axes1.get_y_axis_label("P", direction=UP).scale(0.7)
        
        vo_text1 = MathTex("V_o < 1", font_size=30).next_to(axes1, UP, buff=0.2)
        def u_func1(t):
            return 0.95 - 0.3 * (1 - np.exp(-0.5 * t))    
        def a_func1(t):
            return 0.05 + 0.15 * np.exp(-0.8 * t) * np.sin(1.2 * t) * np.exp(-0.3 * t)
        def b_func1(t):
            return 1 - u_func1(t) - a_func1(t)
        
        u_curve1 = axes1.plot(u_func1, x_range=[0, 20], color=GREEN, stroke_width=3)
        a_curve1 = axes1.plot(a_func1, x_range=[0, 20], color=RED, stroke_width=3)
        b_curve1 = axes1.plot(b_func1, x_range=[0, 20], color=BLUE, stroke_width=3)
        
        graph1 = VGroup(axes1, x_label1, y_label1, vo_text1, u_curve1, a_curve1, b_curve1)
        self.play(FadeIn(graph1), run_time=2)
        self.wait(1.5)

    def create_graph_vo_equals_1(self):
        axes2 = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 1, 0.2],
            x_length=3.5,
            y_length=2.5,
            axis_config={"color": WHITE, "stroke_width": 1}
        ).shift(DOWN)
        
        x_label2 = axes2.get_x_axis_label("t", direction=LEFT).scale(0.8).shift(RIGHT*0.4)
        y_label2 = axes2.get_y_axis_label("P", direction=UP).scale(0.7)
        
        vo_text2 = MathTex("V_o = 1", font_size=30).next_to(axes2, UP, buff=0.2)
        def u_func2(t):
            return 0.95 - 0.6 * (1 - np.exp(-0.3 * t))
        def a_func2(t):
            return 0.05 + 0.25 * np.exp(-0.1 * t) * (1 - np.exp(-0.4 * t))
        def b_func2(t):
            return 1 - u_func2(t) - a_func2(t)
        
        u_curve2 = axes2.plot(u_func2, x_range=[0, 20], color=GREEN, stroke_width=3)
        a_curve2 = axes2.plot(a_func2, x_range=[0, 20], color=RED, stroke_width=3)
        b_curve2 = axes2.plot(b_func2, x_range=[0, 20], color=BLUE, stroke_width=3)
        
        graph2 = VGroup(axes2, x_label2, y_label2, vo_text2, u_curve2, a_curve2, b_curve2)
        self.play(FadeIn(graph2), run_time=2)
        self.wait(1.5)

    def create_graph_vo_greater_than_1(self):
        axes3 = Axes(
            x_range=[0, 20, 5],
            y_range=[0, 1, 0.2],
            x_length=3.5,
            y_length=2.5,
            axis_config={"color": WHITE, "stroke_width": 1},
        ).shift(RIGHT * 4.5 + DOWN)
        
        x_label3 = axes3.get_x_axis_label("t", direction=LEFT).scale(0.8).shift(RIGHT*0.4)
        y_label3 = axes3.get_y_axis_label("P", direction=UP).scale(0.7)
        
        vo_text3 = MathTex("V_o > 1", font_size=30).next_to(axes3, UP, buff=0.2)
        def u_func3(t):
            return 0.95 * np.exp(-0.8 * t) + 0.05
        def a_func3(t):
            return 0.05 + 0.7 * np.exp(-0.3 * t) * (np.exp(0.5 * t) - 1) * np.exp(-0.4 * t)
        def b_func3(t):
            return 1 - u_func3(t) - a_func3(t)
        
        u_curve3 = axes3.plot(u_func3, x_range=[0, 20], color=GREEN, stroke_width=3)
        a_curve3 = axes3.plot(a_func3, x_range=[0, 20], color=RED, stroke_width=3)
        b_curve3 = axes3.plot(b_func3, x_range=[0, 20], color=BLUE, stroke_width=3)
        
        graph3 = VGroup(axes3, x_label3, y_label3, vo_text3, u_curve3, a_curve3, b_curve3)
        self.play(FadeIn(graph3), run_time=2)
        self.wait(1.5)
        
# manim -pqh Manim/3_math_model.py mathModel
from manim import *

class limitVisualization(Scene):
    def construct(self):
        # -------------- Scene 1 ------------------ #
        dGrid = NumberPlane(
            background_line_style={
                "stroke_opacity": 0.4
            },
            axis_config={
                "include_ticks": False,
                "stroke_opacity": 0
            }
        )
        self.play(FadeIn(dGrid))

        intro = Text("Limit Visualization", font_size=64).shift(3.4*UP).set_color_by_gradient(BLUE_B, PINK)
        fn = MathTex("f(x)= \, \\frac{\\sin(x)}{x}", font_size=80).shift(UP).set_color_by_gradient(PINK, BLUE_B)

        self.play(Write(intro, run_time=1))
        self.wait(1.2)

        self.play(Write(fn, run_time=1.5))

        # -------------- Scene 2 ------------------ #
        txt1 = Text("What happens as x approaches 0?", font_size=44).shift(DOWN).set_color_by_gradient(BLUE_B, PINK)
        txt2 = Text("Does it become 1, 0, Undefined, or something else?", font_size=42).shift(2*DOWN).set_color_by_gradient(BLUE_B, PINK)
        txt3 = Text("Let's find out!", font_size=48).shift(3*DOWN).set_color_by_gradient(PINK, BLUE_B)

        self.play(Write(txt1))
        self.wait(1)

        self.play(Write(txt2))
        self.play(Write(txt3, run_time=1.8))
        self.wait(1.7)

        self.play(FadeOut(intro, fn, txt1, txt2, txt3))
        self.wait(0.5)

        # -------------- Scene 3 ------------------ #
        label = MathTex("f(x)= \, \\frac{\\sin(x)}{x}", font_size=64).shift(4.8*LEFT + 2.9*UP)

        ax = Axes(
            x_range=[-5.5, 5.5],
            y_range=[-1.5, 1.5],
            axis_config={"include_numbers": True}
        ).shift(0.67*RIGHT)

        graph = ax.plot(lambda x: np.sin(x)/x, color=BLUE_C, x_range=[-5, 5])

        self.play(Write(label), Create(ax), Create(graph, run_time=1.2))
        self.wait(1)

        # -------------- Scene 4 ------------------ #
        leftLim_tracker = ValueTracker(-0.99)
        rightLim_tracker = ValueTracker(0.99)

        left_dot = always_redraw(
            lambda: 
                Dot(point=ax.c2p(leftLim_tracker.get_value(), np.sin(leftLim_tracker.get_value())/leftLim_tracker.get_value()), color=RED_A)
        )
        right_dot = always_redraw(
            lambda:
                Dot(point=ax.c2p(rightLim_tracker.get_value(), np.sin(rightLim_tracker.get_value())/rightLim_tracker.get_value()), color=GREEN_A)
        )

        leftDec = DecimalNumber(
            0, include_sign=True,
            num_decimal_places=7,
            color=RED_A,
            font_size=30
        ).add_updater(
            lambda m: m.set_value(
                np.sin(leftLim_tracker.get_value()) / leftLim_tracker.get_value()
            ).next_to(left_dot, LEFT)
        )

        rightDec = DecimalNumber(
            0, include_sign=True,
            num_decimal_places=7,
            color=GREEN_A,
            font_size=30
        ).add_updater(
            lambda m: m.set_value(
                np.sin(rightLim_tracker.get_value()) / rightLim_tracker.get_value()
            ).next_to(right_dot, RIGHT)
        )

        leftLim = MathTex("\\lim_{x \\to 0^-} f(x)", font_size=40)
        rightLim = MathTex("\\lim_{x \\to 0^+} f(x)", font_size=40)

        leftLim.add_updater(lambda m: m.next_to(leftDec, UP))
        rightLim.add_updater(lambda m: m.next_to(rightDec, UP))

        self.play(FadeIn(left_dot, right_dot, leftDec, rightDec, leftLim, rightLim))
        self.play(
            leftLim_tracker.animate.set_value(-0.001),
            rightLim_tracker.animate.set_value(0.001),
            run_time=3
        )
        self.wait(0.7)
        self.play(FadeOut(left_dot, right_dot, leftDec, rightDec, graph, label, ax, run_time=0.3))

        # -------------- Scene 5 ------------------ #
        leftLim.clear_updaters()
        rightLim.clear_updaters()

        self.play(
            leftLim.animate.move_to(ORIGIN + 2*LEFT).scale(1.8),
            rightLim.animate.move_to(ORIGIN + 2*RIGHT).scale(1.8),
            run_time=1
        )
        self.wait(1)

        equalTo = MathTex("=", font_size=72).shift(0.1*UP + 0.15*RIGHT)
        self.play(Create(equalTo))

        # -------------- Scene 6 ------------------ #
        limLR = MathTex("\\lim_{x \\to 0^-} \\frac{\\sin(x)}{x} = \\lim_{x \\to 0^+} \\frac{\\sin(x)}{x} = 1", font_size=70)


        self.play(
            leftLim.animate.shift(2*UP),
            rightLim.animate.shift(2*UP),
            equalTo.animate.shift(2*UP)
        )
        self.play(Write(limLR))
        self.wait(0.5)
        self.play(FadeOut(limLR, leftLim, rightLim, equalTo))

        # -------------- Scene 7 ------------------ #
        txt4 = Text("Since the left limit equals the \n      right limit, Therefore :", line_spacing=1.2).set_color_by_gradient(BLUE_B, PINK).shift(1.5*UP)
        limFnResult = MathTex("\\lim_{x \\to 0} \\frac{\\sin(x)}{x} = 1", font_size=70).set_color_by_gradient(PINK, BLUE_B).shift(0.4*DOWN)

        self.play(Write(txt4))
        self.play(Write(limFnResult))
        self.wait(1)

        self.play(FadeOut(txt4, limFnResult, dGrid, run_time=0.5))
        self.wait(1)

# manim -pqm Manim/LimitVisualization.py
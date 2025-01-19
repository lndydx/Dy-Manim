from manim import *

class derivative(Scene):
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

        intro = Text("Defining The Derivative", font_size=64).shift(3.4*UP).set_color_by_gradient(BLUE_B, GREEN_B)
        noteTxt = Text("Remember!").shift(2*UP).set_color_by_gradient(GREEN_B, BLUE_B)
        gradient = MathTex("m= \, \\frac{\\Delta y}{\\Delta x}", font_size=64)
        highlightSq = Rectangle(width=4, height=2, color=BLUE_B).move_to(gradient)

        self.play(Write(intro))
        self.wait(0.8)
        self.play(Write(noteTxt))
        self.wait(0.2)

        self.play(FadeIn(gradient))
        self.play(Create(highlightSq), run_time=0.8, rate_func=smooth)
        self.wait(0.5)

        self.play(FadeOut(intro), FadeOut(noteTxt), FadeOut(highlightSq), FadeOut(gradient))

        # -------------- Scene 2 ------------------ #
        axes = Axes(
            x_range=[0, 8, 1],
            x_length=10,
            y_range=[-2, 7, 1],
            y_length=6,
            axis_config={"include_tip": True, "tick_size": 0}
        ).to_edge(DL).shift(1.4 * RIGHT)

        def dFunction(x):
            return 1/4*x**2 - x + 3/2
        
        dGraph = axes.plot(dFunction, color=BLUE_C, x_range=[0, 7])

        self.play(Write(VGroup(axes, dGraph)), run_time=1)
        self.wait(0.5)

        x = 4
        h = 2
        xh = x + h

        pointQ = axes.coords_to_point(x, dFunction(x))
        pointP = axes.coords_to_point(x + h, dFunction(x + h))

        dotQ = Dot(pointQ)
        dotP = Dot(pointP)

        labelQ = MathTex("Q").next_to(dotQ, DOWN)
        labelQ.next_to(dotP, UP)

        labelP = MathTex("P").next_to(dotP, RIGHT)
        labelP.next_to(dotQ, UP)

        secantLine = axes.get_secant_slope_group(
            x, dGraph, dx=h, secant_line_color=GREEN, secant_line_length=7
        )

        dashedLine_xh = DashedLine(
            start=pointP, end=axes.coords_to_point(xh, 0)
        )
        dashedLine_y = DashedLine(
            start=pointQ, end=axes.coords_to_point(x, 0)
        )

        brace_h = BraceBetweenPoints(axes.coords_to_point(x, -0.8), axes.coords_to_point(xh, 0), direction=DOWN)
        label_h = MathTex("\\Delta x").next_to(brace_h, DOWN)

        brace_f = BraceBetweenPoints(pointQ, pointP, direction=RIGHT)
        label_f = MathTex("\\Delta y").next_to(brace_f, RIGHT)

        label_fx = MathTex("f(x)", font_size=42).move_to(axes.coords_to_point(0.3, dFunction(x))).shift(LEFT)
        label_fxh = MathTex("f(x+h)", font_size=42).move_to(axes.coords_to_point(0.3, dFunction(xh))).shift(1.4*LEFT)
        label_x = MathTex("x").move_to(axes.coords_to_point(x, 0)).shift(0.4*DOWN)
        label_xh = MathTex("x+h").move_to(axes.coords_to_point(xh, 0)).shift(0.4*DOWN)

        self.play(FadeIn(dotQ), FadeIn(dotP))
        self.play(Write(labelQ), Write(labelP))
        self.play(Create(secantLine))

        self.play(Create(dashedLine_xh), Create(dashedLine_y))
        self.play(Write(label_fx), Write(label_fxh), Write(label_x), Write(label_xh))
        self.play(GrowFromCenter(brace_h), Write(label_h), GrowFromCenter(brace_f), Write(label_f))
        self.wait(0.5)

        scene2_group = VGroup(
            axes, dGraph, dotQ, dotP, 
            labelQ, labelP, secantLine,
            dashedLine_xh, dashedLine_y,
            brace_h, label_h, brace_f, label_f,
            label_fx, label_fxh, label_x, label_xh
        )

        self.play(
            scene2_group.animate.scale(0.6)
            .to_edge(UL)
        )

        # -------------- Scene 3 ------------------ #
        delY_eq = MathTex("\\Delta y = f(x+h) - f(x)").to_edge(DL).shift(2 * UP)
        delX_eq = MathTex("\\Delta x = x + h - x = h").to_edge(DL).shift(UP)

        curlyBrace = BraceBetweenPoints(
            delY_eq.get_right(), delX_eq.get_right(), direction=RIGHT
        )
        m = MathTex("m = \\frac{f(x+h) - f(x)}{h}").next_to(curlyBrace, 3.7*RIGHT)

        txt1 = Text("Suppose point P is fixed", font_size=35).shift(DOWN).set_color_by_gradient(GREEN_B, BLUE_B).align_on_border(LEFT)
        txt2 = Text("Now, we need to bring point Q to P as close as possible", font_size=35).shift(1.8*DOWN).set_color_by_gradient(GREEN_B, BLUE_B).align_on_border(LEFT)
        txt3 = Text("But how?", font_size=35).shift(2.6*DOWN).set_color_by_gradient(GREEN_B, BLUE_B).align_on_border(LEFT)

        txt4 = Text("Let's use limit, then make h approaches to zero ", font_size=35).shift(DOWN).set_color_by_gradient(BLUE_B, GREEN_B).align_on_border(LEFT)
        txt5 = MathTex("h \\to 0", font_size=60).shift(1.8*DOWN).set_color_by_gradient(BLUE_B, GREEN_B).align_on_border(LEFT)
        txt6 = MathTex("Note: \\Delta x = h").shift(3.2*DOWN).set_color_by_gradient(BLUE_B, GREEN_B).align_on_border(LEFT)

        self.play(Write(delY_eq), Write(delX_eq), run_time=1.5)
        self.play(GrowFromCenter(curlyBrace.shift(0.5*RIGHT)), Write(m))
        self.wait(0.5)

        self.play(
            FadeOut(delY_eq), FadeOut(delX_eq), FadeOut(curlyBrace),
            m.animate.set_color_by_gradient(BLUE_B, GREEN_B).move_to(3.3*RIGHT + 2.5*UP).scale(1.1)      
        )
        self.play(Write(txt1), Write(txt2))
        self.wait(1.2)
        self.play(Write(txt3))
        self.wait(1)

        self.play(FadeOut(txt1), FadeOut(txt2), FadeOut(txt3))

        self.play(Write(txt4), Write(txt5))
        self.play(FadeIn(txt6))
        self.wait(0.8)
        self.play(
            FadeOut(txt6), FadeOut(m), FadeOut(txt5), FadeOut(txt4),
            scene2_group.animate.scale(1.8).move_to(ORIGIN))

        # -------------- Scene 4 ------------------ #
        h_values = [2, 1.5, 1, 0.5, 0.2, 0.1, 0.00001]
        scaleFactor = 0.6

        for h_val in h_values:
            new_xh = x + h_val
            new_pointP = axes.coords_to_point(new_xh, dFunction(new_xh))
            new_pointQ = axes.coords_to_point(x, dFunction(x))
            new_dotP = Dot(new_pointP)
            
            new_secantLine = axes.get_secant_slope_group(
                x, dGraph, dx=h_val, secant_line_color=GREEN, secant_line_length=7
            )
            
            new_dashedLine_xh = DashedLine(
                start=new_pointP,
                end=axes.coords_to_point(new_xh, 0)
            )
            
            new_brace_h = BraceBetweenPoints(
                axes.coords_to_point(x, -0.8),
                axes.coords_to_point(new_xh, 0),
                direction=DOWN
            )
            new_labelQ = MathTex("Q").next_to(new_pointP, UP).scale(scaleFactor)
            new_label_h = MathTex("\\Delta x").next_to(new_brace_h, DOWN).scale(scaleFactor)
            
            new_brace_f = BraceBetweenPoints(new_pointQ, new_pointP, direction=RIGHT)
            new_label_f = MathTex("\\Delta y").next_to(new_brace_f, RIGHT).scale(scaleFactor)
            
            new_label_fx = MathTex("f(x)").move_to(axes.coords_to_point(0.3, dFunction(x))).shift(1.5*LEFT*scaleFactor).scale(scaleFactor)
            new_label_fxh = MathTex("f(x+h)").move_to(axes.coords_to_point(0.3, dFunction(new_xh))).shift(1.9*LEFT*scaleFactor).scale(scaleFactor)
            
            new_label_x = MathTex("x").move_to(axes.coords_to_point(x, 0)).shift(0.4*DOWN*scaleFactor).scale(scaleFactor)
            new_label_xh = MathTex("x+h").move_to(axes.coords_to_point(new_xh, 0)).shift(0.4*DOWN*scaleFactor).scale(scaleFactor)
            
            self.play(
                Transform(dotP, new_dotP), Transform(secantLine, new_secantLine), Transform(dashedLine_xh, new_dashedLine_xh),
                Transform(brace_h, new_brace_h), Transform(label_h, new_label_h), Transform(brace_f, new_brace_f),
                Transform(label_f, new_label_f), Transform(label_fx, new_label_fx), Transform(label_fxh, new_label_fxh),
                Transform(label_x, new_label_x), Transform(label_xh, new_label_xh), Transform(labelQ, new_labelQ),
                run_time=0.8
            )
            self.wait(0.5)

        tangent_line = axes.get_secant_slope_group(
            x, dGraph, dx=0.0001,
            secant_line_color=RED,
            secant_line_length=8
        )
        
        self.play(
            Transform(secantLine, tangent_line), FadeOut(brace_f), FadeOut(label_f), FadeOut(brace_h), FadeOut(label_h),
            FadeOut(label_x), FadeOut(label_xh), FadeOut(label_fx), FadeOut(label_fxh), FadeOut(dashedLine_xh), FadeOut(dashedLine_y),
            FadeOut(labelQ), FadeOut(labelP), run_time=1
        )

        # -------------- Scene 5 ------------------ #
        derivativeDef = MathTex("m", "=", "\\lim_{h \\to 0}", "\\frac{f(x + h) - f(x)}{h}",
            font_size=64).set_color_by_gradient(BLUE_B, GREEN_B).shift(0.6 * RIGHT)
        
        dFx = MathTex("\\frac{dy}{dx} = ", font_size=64).next_to(derivativeDef, LEFT).set_color_by_gradient(BLUE_B, GREEN_B)

        fullEq = VGroup(dFx, derivativeDef)
        highlight_full = Rectangle(
            width=fullEq.width + 0.5,
            height=fullEq.height + 0.5, 
            color=BLUE_B
        ).move_to(fullEq).set_color_by_gradient(GREEN_B, GREEN_B)

        self.play(FadeOut(axes), FadeOut(dGraph), FadeOut(secantLine), FadeOut(dotP), FadeOut(dotQ), run_time=1.5)

        self.play(Write(derivativeDef), run_time=1.5)
        self.play(FadeIn(dFx), run_time=1.2)
        self.play(Create(highlight_full), run_time=1, rate_func=smooth)
        self.wait(0.6)

        self.play(FadeOut(dGrid), FadeOut(derivativeDef), FadeOut(dFx),
        FadeOut(highlight_full) ,run_time=1
        )

# manim -pqh Manim/DerivativeVisualization.py
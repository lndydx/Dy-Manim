from manim import *

class integral(Scene):
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

        intro = Text("Integral Visualization", font_size=64).shift(3.4*UP).set_color_by_gradient(GREEN_B, BLUE_B)
        
        self.play(Write(intro), run_time=1.2)
        self.wait(0.5)
        self.play(FadeOut(intro))

        # -------------- Scene 2 ------------------ #
        curve = lambda x: x**2
        fx_label = MathTex("f(x) = x^2").shift(2.8*UP + 3.9*RIGHT)
        
        axes = Axes(
            x_range=[0, 3.5, 0.5],
            y_range=[0, 10, 2],
            axis_config={"include_numbers": True},
        ).scale(0.8)

        labels = axes.get_axis_labels(x_label="x", y_label="y")
        graph = axes.plot(curve, x_range=[0, 3], color=(BLUE, GREEN))
        rects = axes.get_riemann_rectangles(
            graph,
            x_range=[0, 3],
            dx=0.5, 
            color=(BLUE, GREEN),
            input_sample_type="right",  
        )

        x = 1.5
        brace_delX = BraceBetweenPoints(
            axes.coords_to_point(x - 0.5, 0), 
            axes.coords_to_point(x, 0), 
            direction=DOWN
        ).shift(0.4*DOWN)
        label_delX = MathTex("\\Delta x").next_to(brace_delX, 0.5*DOWN)
        
        y_val = curve(x)
        point_on_graph = axes.coords_to_point(x, y_val)
        point_on_y_axis = axes.coords_to_point(0, y_val)

        dashed_line_horiz = DashedLine(point_on_graph, point_on_y_axis)
        fxi_label = MathTex(f"f(x_i)").next_to(point_on_y_axis, LEFT, buff=0.2).shift(0.4*LEFT)

        title_sum = Text("Riemann Sum", font_size=48).shift(3.4*UP + 0.6*LEFT)
        title_integral = Text("Integral", font_size=48).shift(3.4*UP + 0.6*LEFT)

        sumIntegralFormula = MathTex(r"\lim_{n \to \infty} \sum_{i=1}^n \Delta x \cdot f(x_i)", font_size=44).shift(2.3*UP + 0.6*LEFT)
        integralFormula = MathTex(r"\int_a^b f(x) \, dx", font_size=44).shift(2.3*UP + 0.6*LEFT)

        self.play(FadeIn(axes), Create(graph))
        self.play(Write(labels), Write(fx_label),
                Create(rects), Write(title_sum), Write(sumIntegralFormula), run_time=1)
        self.wait(0.6)
        self.play(GrowFromCenter(brace_delX), Write(label_delX), Create(dashed_line_horiz), Write(fxi_label),  run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(brace_delX), Unwrite(label_delX), Unwrite(fxi_label), FadeOut(dashed_line_horiz))
        
        # -------------- Scene 3 ------------------ #   
        pointA = MathTex("a", font_size=64).next_to(axes.coords_to_point(0, 0)).shift(0.4*LEFT + 0.9*DOWN)
        pointB = MathTex("b", font_size=64).next_to(axes.coords_to_point(3, 0)).shift(0.4*LEFT + 0.9*DOWN)
        
        for dx in [0.5, 0.2, 0.1, 0.05, 0.01]:
            new_rects = axes.get_riemann_rectangles(
                graph,
                x_range=[0, 3],
                dx=dx,
                color=(BLUE, GREEN),
                input_sample_type="right",
            )
            self.play(Transform(rects, new_rects), run_time=0.9)

        area = axes.get_area(graph, x_range=[0, 3], color=(GREEN, BLUE), opacity=0.6)
        self.play(
            Write(pointA), Write(pointB), FadeOut(rects), FadeIn(area), Transform(title_sum, title_integral), Transform(sumIntegralFormula, integralFormula))
        self.wait(0.9)

        # -------------- Scene 4 ------------------ #
        sceneGroup = VGroup(
            axes, graph, fx_label, labels, area, pointA, pointB)
        self.play(sceneGroup.animate.scale(0.65).to_edge(UL), FadeOut(title_sum), FadeOut(sumIntegralFormula)) 
        
        integralEq = MathTex( r"\lim_{n \to \infty} \sum_{i=1}^n \Delta x \cdot f(x_i) = \int_a^b f(x) \, dx", font_size=40).set_color_by_gradient(BLUE_B, GREEN_B).align_on_border(1.1*LEFT).shift(2*DOWN)
        
        highlightInt = Rectangle(
            width = integralEq.width + 0.2,
            height = integralEq.height + 0.2,
            color = BLUE_C
        ).move_to(integralEq)
        
        self.play(Write(integralEq))
        self.wait(0.6)
        self.play(Write(highlightInt), run_time = 1.2)
        
        txt1 = Text("Riemann sums approximate the area under \na curve by dividing it into rectangles", font_size=24, line_spacing=1.2)
        txt2 = Text("As the number of rectangles increases,\nthe approximation becomes more accurate", font_size=24, line_spacing=1.2) 
        txt3 = Text("But, Doing an infinite sum might \nsound impossible", font_size=24, line_spacing=1.2)
        txt4 = Text(" Let's use integration technique \n for polynomial function", font_size=24, line_spacing=1.2)
        
        polynomial_integral = MathTex(
            r"\int_a^b x^n \, dx = \left[ \frac{x^{n+1}}{n+1} \right]_a^b \quad (n \neq -1)",
            font_size=36
        ).align_on_border(RIGHT).shift(0.5*DOWN + 0.2*LEFT)
        
        txt1.shift(3.2*UP + 3.4*RIGHT)
        txt2.shift(1.6*UP + 3.4*RIGHT)
        txt3.shift(3.2*UP + 3.5*RIGHT)
        txt4.shift(1.5*UP + 3.3*RIGHT)
        
        self.play(Write(txt1))
        self.wait(1)
        self.play(Write(txt2))
        self.wait(1)
        
        self.play(FadeOut(txt1), FadeOut(txt2))
        self.play(Write(txt3))
        self.wait(0.8)
        self.play(Write(txt4))
        self.wait(0.8)
        
        self.play(Write(polynomial_integral), run_time=2)
        self.wait(1)
        
        self.play(
            FadeOut(txt3), FadeOut(txt4), FadeOut(integralEq), FadeOut(highlightInt),
            polynomial_integral.animate.scale(1.2).move_to(UL).shift(2.2*UP + 2.5*LEFT).set_color_by_gradient(BLUE_B, GREEN_B),
            sceneGroup.animate.scale(0.9).move_to(UR).shift(0.9*UP + 2.2*RIGHT)
        )
        self.wait(0.5)
        
        # -------------- Scene 5 ------------------ #
        intFn_St1 = MathTex(
            r"\int_0^3 x^2 \, dx = \left[ \frac{x^{2+1}}{2+1} \right]_0^3 = \left[ \frac{x^{3}}{3} \right]_0^3", font_size=41
        ).align_on_border(LEFT).shift(1.6*UP + 0.1*LEFT).set_color_by_gradient(BLUE_B, GREEN_B)
        intFn_St2 = MathTex(
            r"\frac{3^3}{3} - \frac{0^3}{3} = 9", font_size=41).align_on_border(LEFT).shift(0.1*UP + 0.1*LEFT).set_color_by_gradient(BLUE_B, GREEN_B)
        result = MathTex("Area = 9").move_to(sceneGroup).set_color_by_gradient(GREEN_B, BLUE_B).shift(0.9*RIGHT + 2*DOWN)
    
        self.play(Write(intFn_St1))
        self.wait(0.5)
        self.play(Write(intFn_St2))
        self.wait(1)
        self.play(FadeOut(intFn_St1), FadeOut(intFn_St2), FadeOut(polynomial_integral), FadeIn(result), 
                sceneGroup.animate.scale(1.4).move_to(ORIGIN))
        self.wait(0.7)
        self.play(FadeOut(sceneGroup), FadeOut(result), FadeOut(dGrid), run_time=1.6)
        self.wait(0.4)

# manim -pqh Manim/IntegralVisualization.py
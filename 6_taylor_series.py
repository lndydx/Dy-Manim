from manim import *
import numpy as np
import math

class TaylorSeries(Scene):
    def construct(self):
        dGrid = NumberPlane(
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"include_ticks": False, "stroke_opacity": 0}
        )
        
        # Title & subtitle
        title = Text("Taylor Series", font_size=50).set_color_by_gradient(BLUE_B, GREEN_B).shift(UP)
        subtitle = Text("An infinite polynomials approximating functions", font_size=36).shift(DOWN*0.5)
        
        axes = Axes(
            x_range=[-6.3, 6.23, 1],
            y_range=[-4, 4.4, 1],
            x_length=15,
            y_length=9,
            axis_config={"color": WHITE, "stroke_width": 2},
        ).scale(0.8)
        
        self.play(FadeIn(dGrid))
        self.wait(0.2)
        
        self.play(FadeIn(title, shift=UP), title.animate.shift(DOWN*0.6), run_time=1)
        self.play(Write(subtitle))
        self.wait(0.8)
        
        self.play(Transform(VGroup(title, subtitle), axes), run_time=0.8)
        self.wait(0.2)

        self.play(Create(axes), run_time=1)  
        self.wait(0.5)
        
        # Create a function & their series
        functions = [
            {
                "name": r"\sin(x)",
                "series": r"\sum_{n=0}^{\infty} \frac{(-1)^n x^{2n+1}}{(2n+1)!}",
                "func": lambda x: np.sin(x),
                "color": BLUE_B
            },
            {
                "name": r"\cos(x)",
                "series": r"\sum_{n=0}^{\infty} \frac{(-1)^n x^{2n}}{(2n)!}",
                "func": lambda x: np.cos(x),
                "color": GREEN_B
            },
            {
                "name": r"e^x",
                "series": r"\sum_{n=0}^{\infty} \frac{x^n}{n!}",
                "func": lambda x: np.exp(x),
                "color": YELLOW_B
            },
            {
                "name": r"\ln(1 + x)",
                "series": r"\sum_{n=1}^{\infty} \frac{(-1)^{n+1} x^n}{n}",
                "func": lambda x: np.log(1 + x) if x > -1 else 0,
                "color": BLUE_B
            },
            {
                "name": r"\frac{1}{1-x}",
                "series": r"\sum_{n=0}^{\infty} x^n",
                "func": lambda x: 1/(1-x) if abs(x) < 1 else 0,
                "color": GREEN_B
            },
            {
                "name": r"e^{-x^2}",
                "series": r"\sum_{n=0}^{\infty} \frac{(-1)^n x^{2n}}{n!}",
                "func": lambda x: np.exp(-x**2),
                "color": YELLOW_B
            }
        ]
        
        # Function approximation   
        def sin_taylor(x, n_terms):
            result = 0
            for n in range(n_terms):
                result += (-1)**n * (x**(2*n + 1)) / math.factorial(2*n + 1)
            return result
        
        def cos_taylor(x, n_terms):
            result = 0
            for n in range(n_terms):
                result += (-1)**n * (x**(2*n)) / math.factorial(2*n)
            return result
        
        def exp_taylor(x, n_terms):
            result = 0
            for n in range(n_terms):
                result += (x**n) / math.factorial(n)
            return result
        
        def natural_log_taylor(x, n_terms):
            result = 0
            for n in range(1, n_terms + 1):
                result += (-1)**(n+1) * (x**n) / n
            return result
        
        def geometric_taylor(x, n_terms):
            result = 0
            for n in range(n_terms):
                result += x**n
            return result
        
        def gaussian_taylor(x, n_terms):
            result = 0
            for n in range(n_terms):
                result += ((-1)**n) * (x**(2*n)) / math.factorial(n)
            return result
        
        taylor_function = [
            sin_taylor, cos_taylor, exp_taylor, natural_log_taylor, geometric_taylor, gaussian_taylor
            ]
        
        # Create equations
        eq_group = VGroup()
        
        for i, func_data in enumerate(functions):
            func_eq = MathTex(
                func_data["name"], "=", func_data["series"]
            ).set_color_by_gradient(GREEN_B, BLUE_B).scale(0.8)
            func_eq.to_corner(UL).shift(DOWN * 0.5)
            
            if i == 0:
                self.play(Write(func_eq), run_time=1.4)
                eq_group.add(func_eq)
            else:
                self.play(Transform(eq_group, func_eq), run_time=1)
            
            # Create the actual fn (Graph)
            if func_data["name"] == r"\ln(1 + x)":
                func_graph = axes.plot(func_data["func"], x_range=[-0.9, 5.5, 0.01], color=func_data["color"])
            elif func_data["name"] == r"\frac{1}{1-x}":
                func_graph = axes.plot(func_data["func"], x_range=[-0.8, 0.9, 0.01], color=func_data["color"])
            elif func_data["name"] == r"e^{-x^2}":
                func_graph = axes.plot(func_data["func"], x_range=[-4, 4, 0.01], color=func_data["color"])
            else:
                func_graph = axes.plot(func_data["func"], x_range=[-6, 6, 0.01], color=func_data["color"])
            
            # Create Taylor approximations w/ increasing terms
            approximations = []
            colors = [BLUE_A, GREEN_A, YELLOW_A]
            
            for n_terms in range(1, 6):
                color_index = min(n_terms-1, len(colors)-1)  
                
                if func_data["name"] == r"\ln(1 + x)":
                    approx_graph = axes.plot(
                        lambda x, n=n_terms: taylor_function[i](x, n), 
                        x_range=[-0.9, 6, 0.01], 
                        color=colors[color_index],
                        stroke_width=2
                    )
                elif func_data["name"] == r"\frac{1}{1-x}":
                    approx_graph = axes.plot(
                        lambda x, n=n_terms: taylor_function[i](x, n), 
                        x_range=[-0.9, 0.9, 0.01], 
                        color=colors[color_index],
                        stroke_width=2
                    )
                elif func_data["name"] == r"e^{-x^2}":
                    approx_graph = axes.plot(
                        lambda x, n=n_terms: taylor_function[i](x, n),
                        x_range=[-3, 3, 0.01],
                        color=colors[color_index],
                        stroke_width=2
                    )
                else:
                    x_range_plot = [-6, 6, 0.01]
                    approx_graph = axes.plot(
                        lambda x, n=n_terms: taylor_function[i](x, n), 
                        x_range=x_range_plot, 
                        color=colors[color_index],
                        stroke_width=2
                    )
                approximations.append(approx_graph)
            
            # Show original function
            self.play(Create(func_graph), run_time=1)
            self.wait(0.5)
            
            # Show approximations (Progressively)
            current_approx = None
            for j, approx in enumerate(approximations):
                if current_approx is None:
                    self.play(Create(approx), run_time=0.5)
                    current_approx = approx
                else:
                    self.play(Transform(current_approx, approx), run_time=0.6)
                self.wait(0.2)
            
            self.play(
                current_approx.animate.set_stroke(width=2, opacity=0.7),
                func_graph.animate.set_stroke(width=4),
                run_time=1
            )
            self.wait(0.5)
            
            if i < len(functions) - 1:
                self.play(FadeOut(func_graph), FadeOut(current_approx), run_time=0.5)

# run: manim -pqh Manim/6_taylor_series.py TaylorSeries
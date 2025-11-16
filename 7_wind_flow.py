from manim import *
import numpy as np

class Tornado(Scene):
    def construct(self):
        func = lambda pos: np.array([
            -pos[1]*0.3 + 0.2*np.sin(pos[0]),
            pos[0]*0.3 + 0.2*np.cos(pos[1]),
            0
        ])
        stream_lines = StreamLines(
            func,
            stroke_width=2,
            max_anchors_per_line=50,
            opacity=0.9  
        )

        formula = MathTex(r"\vec{F}(x, y) = \langle -0.3y + 0.2\sin(x),\; 0.3x + 0.2\cos(y) \rangle").shift(3.4*UP + 2.6*LEFT).scale(0.8)

        self.add(stream_lines, formula)
        stream_lines.start_animation(flow_speed=1.2)
        self.wait(3 *stream_lines.virtual_time / stream_lines.flow_speed)

class WindFlow(Scene):
    def construct(self):
        func = lambda pos: 0.5*np.sin(pos[0] / 2) * DR + 2*np.cos(pos[1] / 2) * LEFT
        stream_lines = StreamLines(
            func, stroke_width=2,
            max_anchors_per_line=50
        )

        formula = MathTex(
            r"\vec{F}(x, y) = \langle 0.5\sin(\tfrac{x}{2}) - 2\cos(\tfrac{y}{2}),\; -0.5\sin(\tfrac{x}{2}) \rangle"
        ).shift(3.4*UP + 2.6*LEFT).scale(0.8)
        
        self.add(stream_lines, formula)
        stream_lines.start_animation(warm_up=False, flow_speed=1.1)
        self.wait(3 * stream_lines.virtual_time / stream_lines.flow_speed)
        
class SaddlePoint(Scene):
    def construct(self):
        func = lambda pos: np.array([
            pos[0] * pos[1],
            pos[0]**2 - pos[1]**2,
            0
        ])
        
        stream_lines = StreamLines(
            func, stroke_width=2,
            max_anchors_per_line=50
        )

        formula = MathTex(
            r"\vec{F}(x, y) = \langle xy, \; x^2 - y^2 \rangle"
        ).shift(3.4*UP + 4.5*LEFT).scale(0.8)
        
        self.add(stream_lines, formula)
        stream_lines.start_animation(warm_up=False, flow_speed=1.1)
        self.wait(3 * stream_lines.virtual_time / stream_lines.flow_speed)
        
# run: manim -pqh Manim/7_wind_flow.py 
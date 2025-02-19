from manim import *

class permutation(Scene):
    def construct(self):
        # === Part 1: Grid & Intro ===
        dGrid = NumberPlane(
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"include_ticks": False, "stroke_opacity": 0}
        )
        self.play(FadeIn(dGrid))

        title = Text("Permutation", font_size=48)
        subtitle = Text("Arranging objects where order matters", font_size=32)
        subtitle.next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # === Part 2: Case Example ===
        case_title = Text("Case: Winners Podium Arrangement", font_size=36).to_edge(UP)
        self.play(Write(case_title))

        def create_person(color, label):
            person = VGroup()
            head = Circle(radius=0.2, fill_opacity=1, color=color)
            body = Rectangle(height=0.5, width=0.3, fill_opacity=1, color=color)
            body.next_to(head, DOWN, buff=0)
            text = Text(label, font_size=24).next_to(body, DOWN)
            person.add(head, body, text)
            return person

        persons = VGroup(
            create_person(RED, "Lorem"),
            create_person(GREEN, "Ellen"),
            create_person(BLUE, "John")
        ).arrange(RIGHT, buff=1).next_to(case_title, DOWN, buff=0.5)

        self.play(Create(persons, lag_ratio=0.3))
        self.wait(1)

        # === Part 3: Explanation of Permutation ===
        explanation = VGroup(
            Text("Why use Permutation?", font_size=28),
            Text("• Order affects the result", font_size=24),
            Text("• Each position must be filled", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        explanation.next_to(persons, DOWN, buff=0.5)

        self.play(Write(explanation), run_time=3)
        self.wait(1.5)

        self.play(
            explanation.animate.scale(0.8).to_edge(LEFT).shift(2*UP),
            persons.animate.scale(0.8).to_edge(RIGHT)
        )

        # === Part 4: Podium Visualization ===
        def create_podium():
            podium = VGroup()
            heights = [1.8, 1.4, 1]
            positions = [0, -2, 2]
            colors = [GOLD_E, GOLD_A, GOLD_C]

            for i, (height, pos, color) in enumerate(zip(heights, positions, colors)):
                block = Rectangle(height=height, width=0.5, fill_opacity=1, fill_color=color, stroke_color=WHITE)
                block.move_to([pos, height / 2, 0])
                number = Text(str(i + 1), font_size=24, color=WHITE).move_to(block)
                podium.add(VGroup(block, number))
            return podium

        podium = create_podium().move_to(ORIGIN)
        self.play(Create(podium, lag_ratio=0.5))

        podium_placeholders = VGroup(
            Text("?", font_size=36).move_to(podium[0].get_top() + UP*0.8),
            Text("?", font_size=36).move_to(podium[1].get_top() + UP*0.8),
            Text("?", font_size=36).move_to(podium[2].get_top() + UP*0.8),
        )
        self.play(Write(podium_placeholders))
        self.wait(1)

        # === Part 5: Step-by-Step Selection ===
        # First Position
        step1_text = MathTex("\\text{First position: Any of 3 people (3 choices)}").to_edge(LEFT).shift(1.6*DOWN)
        self.play(Write(step1_text))

        first_person = persons[0].copy()
        self.play(persons[0].animate.set_opacity(0.4), first_person.animate.move_to(podium[0].get_top() + UP*0.8), run_time=0.8)
        self.play(Indicate(first_person, scale_factor=1.2, color=YELLOW))
        self.wait(0.8)

        # Second position
        step2_text = MathTex("\\text{Second position: Any of 2 remaining people (2 choices)}").to_edge(LEFT).shift(2.4*DOWN)
        self.play(Write(step2_text))

        second_person = persons[1].copy()
        self.play(persons[1].animate.set_opacity(0.4), second_person.animate.move_to(podium[1].get_top() + UP*0.8), run_time=0.8)
        self.play(Indicate(second_person, scale_factor=1.2, color=YELLOW))
        self.wait(0.8)

        # Third position
        step3_text = MathTex("\\text{Third position: 1 remaining person (1 choice)}").to_edge(DL)
        self.play(Write(step3_text))

        third_person = persons[2].copy()
        self.play(persons[2].animate.set_opacity(0.4), third_person.animate.move_to(podium[2].get_top() + UP*0.8), run_time=0.8)
        self.play(Indicate(third_person, scale_factor=1.2, color=YELLOW))
        self.wait(0.4)
        self.play(FadeOut(podium_placeholders))
        self.wait(0.4)
        
        # === Part 6: Total Ways & Formula ===
        mobjects = VGroup(podium, first_person, second_person, third_person)
        self.play(
            FadeOut(step1_text), FadeOut(step2_text), FadeOut(step3_text), FadeOut(explanation), FadeOut(case_title), FadeOut(persons),
            mobjects.animate.scale(0.8).to_edge(UL).shift(UP*0.2)
        )
        
        total_ways = MathTex("\\text{Total ways} = n P r = \\frac{n!}{(n-r)!}").to_edge(LEFT)
        desc1 = Tex("n = Total objects (contestants)").to_edge(LEFT).shift(DOWN*0.6)
        desc2 = Tex("r = Chosen objects (podium spots)").to_edge(LEFT).shift(DOWN*1.2)
        result = MathTex("\\frac{3!}{(3-3)!} = \\frac{3!}{0!} = 3.2.1 = 6").to_edge(LEFT).shift(DOWN*2.2)
        
        self.play(Write(total_ways))
        self.wait(0.8)
        self.play(total_ways.animate.shift(UP*0.4))
        self.play(Write(desc1), Write(desc2))
        self.wait(0.8)
        self.play(Write(result))
        self.wait(1)
        self.play(FadeOut(total_ways), FadeOut(desc1), FadeOut(desc2), FadeOut(result), FadeOut(mobjects))
        self.wait(0.8)
        
        permutationEq = MathTex("n P r = \\frac{n!}{(n-r)!}", font_size=64).set_color_by_gradient(BLUE_B, GREEN_B)
        highlight = Rectangle(
            width=permutationEq.width + 0.5,
            height=permutationEq.height + 0.5,
            color=BLUE
        ).move_to(permutationEq)
        
        self.play(Write(permutationEq))
        self.wait(0.8)
        self.play(Create(highlight))
        self.wait(1)
        self.play(FadeOut(highlight), FadeOut(permutationEq), FadeOut(dGrid))

# manim -pqm Manim/Permutation.py
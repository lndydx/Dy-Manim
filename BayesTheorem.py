from manim import *

class BayesTheorem(Scene):
    def construct(self):
        # === Scene 1: Introduction to Bayes Theorem ===
        dGrid = NumberPlane(
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"include_ticks": False, "stroke_opacity": 0}
        )
        self.play(FadeIn(dGrid))

        title = Text("Bayes' Theorem", font_size=60).set_color_by_gradient(BLUE_B, GREEN_B)
        subtitle = Text("Updating beliefs based on new evidence!", font_size=36).set_color_by_gradient(BLUE_B, GREEN_B)
        subtitle.next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.3)
        self.play(FadeOut(title), FadeOut(subtitle))

        # === Scene 2: Bayes Formula ===
        formula_title = Text("Bayes' Theorem Formula", font_size=40).to_edge(UP).set_color_by_gradient(GREEN_B, BLUE_B)
        self.play(Write(formula_title))

        bayes_formula = MathTex(r"P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}", font_size=48).shift(UP)
        self.play(Write(bayes_formula))
        self.wait(1)

        # === Scene 3: Components of Bayes Theorem ===
        self.play(bayes_formula.animate.shift(UP * 0.5))
        
        # Create component explanations
        prior = MathTex(r"P(A)", r"\text{: Prior (Initial probability)}").scale(0.8)
        likelihood = MathTex(r"P(B|A)", r"\text{: Likelihood (Probability of B if A is true)}").scale(0.8)
        evidence = MathTex(r"P(B)", r"\text{: Evidence (Total probability of B)}").scale(0.8)
        posterior = MathTex(r"P(A|B)", r"\text{: Posterior (Probability of A after observing B)}").scale(0.8)

        prior[0].set_color(RED_B)
        likelihood[0].set_color(BLUE_B)
        evidence[0].set_color(GREEN_B)
        posterior[0].set_color(YELLOW_B)
        
        components = VGroup(prior, likelihood, evidence, posterior).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        components.next_to(bayes_formula, DOWN, buff=0.5)
        
        for component in components:
            self.play(FadeIn(component), run_time=0.5)
        self.wait(2.2)

        self.play(FadeOut(components), FadeOut(bayes_formula))
        
        # === Scene 4: Visualization with Venn Diagram ===
        venn_title = Text("Visualization with Venn Diagram", font_size=34).next_to(formula_title, DOWN, buff=0.5)
        self.play(Write(venn_title))

        # Venn diagram
        universe = Rectangle(width=8, height=5.5, color=WHITE, fill_opacity=0.05)
        circle_a = Circle(radius=2.2, color=RED, fill_opacity=0.3).shift(LEFT * 1.2)
        circle_b = Circle(radius=2.2, color=BLUE, fill_opacity=0.3).shift(RIGHT * 1.2)

        a_label = Text("A", font_size=42, color=RED).move_to(circle_a.get_center() + LEFT * 1)
        b_label = Text("B", font_size=42, color=BLUE).move_to(circle_b.get_center() + RIGHT * 1)

        intersection = Intersection(circle_a, circle_b, color=PURPLE, fill_opacity=0.5)

        venn_group = VGroup(universe, circle_a, circle_b, intersection, a_label, b_label)
        venn_group.scale(0.9).next_to(venn_title, DOWN, buff=0.5)

        self.play(FadeIn(universe))
        self.play(FadeIn(circle_a), Write(a_label))
        self.play(FadeIn(circle_b), Write(b_label))
        self.play(FadeIn(intersection))

        # Add probability labels
        p_a = MathTex(r"P(A)", color=RED_B).scale(0.65).next_to(circle_a, DOWN, buff=0.2)
        p_b = MathTex(r"P(B)", color=BLUE_B).scale(0.65).next_to(circle_b, DOWN, buff=0.2)

        arrow_ratio = Arrow(start=circle_b.get_top(), end=intersection.get_top(), buff=0.1, color=YELLOW_B)
        p_a_and_b = MathTex(r"P(A \cap B)", color=PURPLE_A).scale(0.75).move_to(intersection.get_center())
        p_a_given_b = MathTex(r"P(A|B)", color=YELLOW_B).scale(0.8).next_to(intersection, UP, buff=0.2)

        self.play(Write(p_a), Write(p_b))
        self.play(Write(p_a_and_b))
        self.play(GrowArrow(arrow_ratio))
        self.play(Write(p_a_given_b))

        self.wait(2)
        
        self.play(
            FadeOut(venn_group), FadeOut(p_a), FadeOut(p_b), FadeOut(p_a_given_b),
            FadeOut(p_a_and_b), FadeOut(venn_title), FadeOut(arrow_ratio)
        )
        
        # === Scene 5: Medical Test Example ===
        example_title = Text("Example: Medical Test", font_size=36).next_to(formula_title, DOWN, buff=0.5)
        self.play(Write(example_title))
        
        example_setup = VGroup(
            Text("• Rare disease: 1% of population (P(D) = 0.01)", font_size=24, color=RED_B),
            Text("• Test accuracy if sick: 95% (P(+|D) = 0.95)", font_size=24, color=BLUE_B),
            Text("• False positive rate: 5% (P(+|¬D) = 0.05)", font_size=24, color=GREEN_B)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        example_setup.next_to(example_title, DOWN, buff=0.5)
        
        for line in example_setup:
            self.play(FadeIn(line), run_time=0.5)
        
        question = Text("If test result is positive, what's the actual probability of having the disease?", font_size=28)
        question.next_to(example_setup, DOWN, buff=0.5)
        
        self.play(Write(question))
        self.wait(3.25)
        
        # === Scene 6: Bayes Calculation ===
        self.play(
            FadeOut(example_setup),
            FadeOut(question)
        )
        
        cal1 = MathTex(r"P(D|+) = \frac{P(+|D) \cdot P(D)}{P(+)}", font_size=36)
        cal2 = MathTex(r"P(+) = P(+|D) \cdot P(D) + P(+|\neg D) \cdot P(\neg D)", font_size=30)
        cal3 = MathTex(r"= 0.95 \cdot 0.01 + 0.05 \cdot 0.99 = 0.0095 + 0.0495 = 0.059", font_size=30)
        cal4 = MathTex(r"P(D|+) = \frac{0.95 \cdot 0.01}{0.059} \approx 0.16 \text{ or } 16\%", font_size=36)
        
        calculations = VGroup(cal1, cal2, cal3, cal4).arrange(DOWN, buff=0.3)
        
        self.play(Write(cal1))
        self.play(Write(cal2))
        self.play(Write(cal3))
        self.play(Write(cal4))
        
        highlight = SurroundingRectangle(cal4, color=GOLD)
        self.play(Create(highlight))
        self.wait(1)
        
        # === Scene 7: Conclusion ===
        self.play(
            FadeOut(cal1), FadeOut(cal2), FadeOut(cal3), 
            FadeOut(highlight), FadeOut(example_title), FadeOut(formula_title)
        )
        
        conclusion_title = Text("Conclusion", font_size=48).to_edge(UP).set_color_by_gradient(BLUE_B, GREEN_B)
        self.play(ReplacementTransform(cal4, conclusion_title))
        
        conclusion_text = VGroup(
            Text("• Bayes' Theorem updates beliefs with new evidence", font_size=28),
            Text("• Even with 95% test accuracy, true probability is only 16%", font_size=28),
            Text("• Prior probability significantly impacts the result", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        conclusion_text.next_to(conclusion_title, DOWN, buff=0.6)
        
        for line in conclusion_text:
            self.play(FadeIn(line), run_time=0.4)
        
        final_formula = MathTex(r"P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}", font_size=48).set_color_by_gradient(BLUE_B, GREEN_B).shift(DOWN * 1.2)
        final_formula.next_to(conclusion_text, DOWN, buff=0.5)
        
        self.play(Write(final_formula))
        
        box = SurroundingRectangle(final_formula, color=BLUE, buff=0.2)
        self.play(Create(box))
        self.wait(2.4)
        
        self.play(FadeOut(box), FadeOut(final_formula), FadeOut(conclusion_text), 
                  FadeOut(conclusion_title), FadeOut(dGrid))

# manim -pqh Manim/bayesTheorem.py 
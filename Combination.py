from manim import *

class combination(Scene):
    def construct(self):
        # === Scene 1: Combination Intro ===
        dGrid = NumberPlane(
            background_line_style={"stroke_opacity": 0.3},
            axis_config={"include_ticks": False, "stroke_opacity": 0}
        )
        self.play(FadeIn(dGrid))

        title = Text("Combination", font_size=60).set_color_by_gradient(BLUE_B, GREEN_B)
        subtitle = Text("Arranging objects where order doesn't matter!", font_size=36).set_color_by_gradient(BLUE_B, GREEN_B)
        subtitle.next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(0.8)
        self.play(FadeOut(title), FadeOut(subtitle))

        # === Scene 2: Case Example ===
        case_title = Text("Case: Selecting 2 Objects from 5", font_size=36).to_edge(UP).set_color_by_gradient(GREEN_B, BLUE_B)
        self.play(Write(case_title))

        def create_gift(color, symbol, label):
            gift = VGroup()
            box = Square(side_length=0.5, fill_opacity=0.8, color=color, stroke_width=2)
            symbol_text = Text(symbol, font_size=32).move_to(box)
            label_text = Text(label, font_size=20).next_to(box, DOWN, buff=0.2)
            gift.add(box, symbol_text, label_text)
            return gift

        gifts = VGroup(
            create_gift(RED, "B", "Book"),
            create_gift(BLUE_B, "N", "Necklace"),
            create_gift(YELLOW, "V", "Voucher"),
            create_gift(GREEN, "H", "Headphone"),
            create_gift(PURPLE_B, "W", "Watch")
        ).arrange(RIGHT, buff=0.7).scale(0.9).next_to(case_title, DOWN, buff=0.8)

        for gift in gifts:
            self.play(GrowFromCenter(gift), run_time=0.4)
        self.wait(0.8)

        # === Scene 3: Combination Explanation ===
        question = Text("Why Combination?", font_size=40).shift(3.5*LEFT + DOWN*0.8)
        explanation = Text("Selection order doesn't affect the result", font_size=24).shift(3.4*LEFT + 1.6*DOWN)
        self.play(FadeIn(question))
        self.play(Write(explanation))
        
        # Simplified demonstration with just the boxes
        book_copy = gifts[0].copy().scale(0.65)
        bag_copy = gifts[1].copy().scale(0.65)
        
        box1 = Rectangle(height=1.4, width=1.8, fill_opacity=0.2, color=BLUE)
        box1.next_to(explanation, RIGHT, buff=1.5)
        box1_label = Text("Selection 1", font_size=20).next_to(box1, UP, buff=0.2)
        
        self.play(Create(box1), Write(box1_label))
        self.play(
            book_copy.animate.move_to(box1.get_center() + UP * 0.3),
            FadeOut(gifts[0])
        )
        self.play(
            bag_copy.animate.move_to(box1.get_center() + DOWN * 0.3),
            FadeOut(gifts[1])
        )
        
        equals_sign = Text("=", font_size=36).next_to(box1, RIGHT, buff=0.5)
        self.play(Write(equals_sign))
    
        box2 = box1.copy().next_to(equals_sign, RIGHT, buff=0.5)
        box2_label = Text("Selection 2", font_size=20).next_to(box2, UP, buff=0.2)
        bag_copy2 = bag_copy.copy()
        book_copy2 = book_copy.copy()
        
        self.play(Create(box2), Write(box2_label))
        self.play(
            bag_copy2.animate.move_to(box2.get_center() + UP * 0.3),
            book_copy2.animate.move_to(box2.get_center() + DOWN * 0.3)
        )
        
        result_text = Text("Same Result!", font_size=24).next_to(VGroup(box1, box2), DOWN, buff=0.5)
        self.play(Write(result_text))
        
        self.wait(0.6)
        self.play(
            FadeOut(box1), FadeOut(box1_label),
            FadeOut(box2), FadeOut(box2_label),
            FadeOut(equals_sign), FadeOut(result_text),
            FadeOut(book_copy), FadeOut(bag_copy),
            FadeOut(book_copy2), FadeOut(bag_copy2),
            FadeOut(gifts[2:]), FadeOut(explanation), FadeOut(question)
        )

        # === Scene 4: Selection Process ===
        new_gifts = VGroup(
            create_gift(RED, "?", "..."),
            create_gift(BLUE_B, "?", "..."),
            create_gift(YELLOW, "?", "..."),
            create_gift(GREEN, "?", "..."),
            create_gift(PURPLE_B, "?", "...")
        ).arrange(RIGHT, buff=0.7).scale(1.1).to_edge(UP, buff=2)
        
        self.play(FadeIn(new_gifts))
        
        # Step 1: First selection
        step1_text = Text("Step 1: First choice (5 options)", font_size=28).to_edge(LEFT)
        self.play(Write(step1_text))
        
        highlights = VGroup(*[
            SurroundingRectangle(gift, color=YELLOW, buff=0.05) for gift in new_gifts
        ])
        self.play(LaggedStart(*[Create(h) for h in highlights], lag_ratio=0.2))
        self.wait(0.5)
        
        selected_gift1 = new_gifts[0].copy().scale(1.3).move_to(LEFT * 3 + DOWN * 1.8)
        self.play(
            Indicate(new_gifts[0], scale_factor=1.2, color=YELLOW),
            FadeOut(highlights)
        )
        self.play(
            TransformFromCopy(new_gifts[0], selected_gift1),
            new_gifts[0].animate.set_opacity(0.4)
        )
        
        # Step 2: Second selection
        step2_text = Text("Step 2: Second choice (4 remaining options)", font_size=28).to_edge(LEFT).shift(DOWN*0.7 + LEFT*0.4)
        step2_text.scale(0.9)  # Scale down to prevent overflow
        self.play(Write(step2_text))

        highlights = VGroup(*[
            SurroundingRectangle(gift, color=YELLOW, buff=0.05) for gift in new_gifts[1:]
        ])
        self.play(LaggedStart(*[Create(h) for h in highlights], lag_ratio=0.2))
        self.wait(0.5)
        
        selected_gift2 = new_gifts[1].copy().scale(1.3).next_to(selected_gift1, RIGHT, buff=0.8)
        self.play(
            Indicate(new_gifts[1], scale_factor=1.2, color=YELLOW),
            FadeOut(highlights)
        )
        self.play(
            TransformFromCopy(new_gifts[1], selected_gift2),
            new_gifts[1].animate.set_opacity(0.4)
        )
        
        selected_pair = VGroup(selected_gift1, selected_gift2)
        brace = Brace(selected_pair, DOWN)
        order_text = Text("Same as {Blue, Red}", font_size=24).next_to(brace, DOWN)
        
        self.play(
            GrowFromCenter(brace),
            Write(order_text)
        )
        self.wait(0.6)
        
        # Clear screen
        self.play(
            FadeOut(step1_text), FadeOut(step2_text), 
            FadeOut(brace), FadeOut(order_text),
            FadeOut(new_gifts)
        )
        
        # === Scene 5: Formula & Calculation (20 seconds) ===
        formula_title = Text("Combination Formula", font_size=50).to_edge(UP).set_color_by_gradient(GREEN_B, BLUE_B)
        self.play(
            ReplacementTransform(case_title, formula_title),
            selected_pair.animate.scale(0.7).to_edge(UL, buff=1)
        )
        
        formula = MathTex(
            r"C(n,r) = \frac{n!}{r!(n-r)!}", font_size=40
        ).shift(UP*0.6 + LEFT*5)
        
        calculation = MathTex(
            r"C(5,2) = \frac{5!}{2!(5-2)!} = \frac{5 \cdot 4 \cdot 3!}{2 \cdot 1 \cdot 3!} = \frac{20}{2} = 10", font_size=36
        ).shift(DOWN*0.5 + LEFT*3.4)
        
        self.play(Write(formula))
        self.wait(0.5)
        self.play(Write(calculation))
        self.wait(1)
        
        # Create table of all combinations
        combinations_title = Text("10 Object Combinations", font_size=28).to_edge(RIGHT, buff=2).shift(UP * 0.5)
        self.play(Write(combinations_title))
        
        gift_names = ["Blue", "Red", "Yellow", "Green", "Purple"]
        combination_texts = []
        
        # Create table of combinations
        for i in range(5):
            for j in range(i+1, 5):
                combo_text = Text(f"{{{gift_names[i]}, {gift_names[j]}}}", font_size=16)
                combination_texts.append(combo_text)
        
        combinations_table = VGroup(*combination_texts).arrange_in_grid(rows=5, cols=2, buff=0.3).scale(1.5)
        combinations_table.next_to(combinations_title, DOWN, buff=0.5)
        
        self.play(LaggedStart(*[Write(c) for c in combinations_table], lag_ratio=0.1))
        
        highlight_rect = SurroundingRectangle(combinations_table[0], color=YELLOW)
        self.play(Create(highlight_rect))
        self.wait(1)
        
        # === Scene 6: Conclusion (10 seconds) ===
        self.play(
            FadeOut(formula_title), FadeOut(selected_pair), 
            FadeOut(combinations_title), FadeOut(combinations_table),
            FadeOut(highlight_rect), FadeOut(calculation)
        )
        
        final_formula = MathTex("n \\, C \\, r = \\frac{n!}{r!(n-r)!}", font_size=64).set_color_by_gradient(BLUE_B, GREEN_B)
        
        self.play(ReplacementTransform(formula, final_formula))
        
        highlight = SurroundingRectangle(
            final_formula, 
            color=BLUE, 
            buff=0.3,
            stroke_width=3
        )
    
        self.play(Create(highlight))
        self.wait(0.8)
        self.play(FadeOut(highlight), FadeOut(final_formula), FadeOut(dGrid))

# manim -pqh Manim/Combination.py 
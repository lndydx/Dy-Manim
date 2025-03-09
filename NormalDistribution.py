from manim import *
import numpy as np
import random

class NormalDistribution(Scene):
    def construct(self):
        self.normal_distribution_animation()
        self.wait(1)

        self.saved_normal_curve = self.normal_curve.copy()
        self.saved_axes = self.axes.copy()
        
        objects_to_remove = [mob for mob in self.mobjects if mob != self.dGrid]
        self.play(*[FadeOut(mob) for mob in objects_to_remove])
        self.galton_board_animation()
        
        curve = self.saved_normal_curve.copy()
        axes = self.saved_axes.copy()
        
        axes.set_opacity(0)
        curve_group = VGroup(axes, curve)
        
        # Gaussian curve position settings
        curve_group.scale(0.75)
        curve_group.move_to(DOWN*1.5)
        curve_group.shift(LEFT*3)
        
        self.play(Create(curve, run_time=1.5))
        
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def normal_distribution_animation(self):
        # === Part 1: Grid & Intro ===
        self.dGrid = NumberPlane(
            background_line_style={
                "stroke_opacity": 0.4
            },
            axis_config={
                "include_ticks": False,
                "stroke_opacity": 0
            }
        )
        self.play(FadeIn(self.dGrid))
        
        # Configuration parameters
        mean = 0
        std_dev = 1
        x_min, x_max = -4, 4
        y_max = 0.45
        
        title = Tex("Normal Distribution", font_size=64).set_color_by_gradient(GREEN_B, BLUE_B).shift(UP*3.3)
        explanation1 = Tex("Continuous probability distribution that is symmetric around its mean", font_size=36).shift(UP*0.2)        
        explanation2 = Tex("showing that data near the mean is more frequent than data far from the mean", font_size=36).shift(DOWN*0.3)

        self.play(Write(title))
        self.play(FadeIn(explanation1), FadeIn(explanation2))
        self.wait(3.8)
        self.play(FadeOut(explanation1), FadeOut(title), FadeOut(explanation2))

        # === Part 2: Create Normal Distribution Graph ===
        self.create_graph(x_min, x_max, y_max, mean, std_dev)

    def create_graph(self, x_min, x_max, y_max, mean, std_dev):
        self.axes = Axes(
            x_range=(x_min, x_max, 1),
            y_range=(0, y_max, 0.1),
            axis_config={"color": WHITE}
        )

        def normal_pdf(x):
            return np.exp(-0.5 * ((x - mean) / std_dev) ** 2) / (std_dev * np.sqrt(2 * np.pi))

        self.normal_curve = self.axes.plot(
            lambda x: normal_pdf(x),
            x_range=[x_min, x_max],
            color=BLUE
        )

        self.formula = MathTex(r"f(x) = \frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}", font_size=50).shift(UP*3.3 + LEFT*4)

        self.play(Create(self.axes), Write(self.formula))
        self.wait(0.5)
        
        self.play(Create(self.normal_curve), run_time=2)
        self.wait(0.8)

        self.mean_line = DashedLine(self.axes.c2p(mean, 0), self.axes.c2p(mean, normal_pdf(mean)), color=YELLOW)
        sigma_lines = []
        sigma_labels = []
        sigma_values = [1, 2, 3]

        for sigma in sigma_values:
            left_sigma = DashedLine(self.axes.c2p(mean - sigma * std_dev, 0), self.axes.c2p(mean - sigma * std_dev, normal_pdf(mean - sigma * std_dev)), color=GREEN)
            right_sigma = DashedLine(self.axes.c2p(mean + sigma * std_dev, 0), self.axes.c2p(mean + sigma * std_dev, normal_pdf(mean + sigma * std_dev)), color=GREEN)

            sigma_label_left = MathTex(f"\mu - {sigma}\sigma", font_size=24).next_to(left_sigma, DOWN)
            sigma_label_right = MathTex(f"\mu + {sigma}\sigma", font_size=24).next_to(right_sigma, DOWN)
            lowercase_sigma = MathTex("\mu", font_size=30).next_to(self.mean_line, DOWN)

            sigma_lines.extend([left_sigma, right_sigma])
            sigma_labels.extend([sigma_label_left, sigma_label_right])

        self.sigma_lines = VGroup(*sigma_lines)
        self.sigma_labels = VGroup(*sigma_labels)
        self.lowercase_sigma = VGroup(*lowercase_sigma)
        
        self.play(Create(self.mean_line), Write(lowercase_sigma))
        self.play(Create(self.sigma_lines), Write(self.sigma_labels))
        
        self.wait(0.5)

        # Shading Area
        self.shade_area(self.axes, self.normal_curve, mean, std_dev)
        self.move_elements_to_corner()
        
    def shade_area(self, axes, normal_curve, mean, std_dev):
        colors = [BLUE, GREEN, RED]
        percentages = ["68.27\%", "95.45\%", "99.73\%"]
        intervals = [1, 2, 3]

        shaded_regions = []
        percentage_labels = []

        for i in range(3):
            shaded_region = axes.get_area(
                normal_curve, x_range=[mean - intervals[i] * std_dev, mean + intervals[i] * std_dev],
                color=colors[i], opacity=0.3
            )
            label = MathTex(percentages[i], font_size=30).move_to(axes.c2p(mean, 0.05 + (0.05 * i)))
            self.play(FadeIn(shaded_region), Write(label))
            self.wait(0.8)

            shaded_regions.append(shaded_region)
            percentage_labels.append(label)

        self.shaded_regions = VGroup(*shaded_regions)
        self.percentage_labels = VGroup(*percentage_labels)

    def move_elements_to_corner(self):        
        graph_elements = VGroup(self.axes, self.normal_curve, self.mean_line, self.sigma_lines, self.sigma_labels, self.lowercase_sigma)
        self.dGrouping = VGroup(self.shaded_regions, self.percentage_labels, graph_elements)
        self.play(FadeOut(self.formula), self.dGrouping.animate.shift(LEFT*3 + UP*2).scale(0.65))

        self.wait(1)
        self.empirical_rule()

    def empirical_rule(self):
        ER_title = Tex("Empirical Rule", font_size=48).shift(UP*3.4 + RIGHT*2.5)
        explanation3 = Tex("A rule in statistics that describes the distribution", font_size=32).shift(UP*2.5 + RIGHT*2.5)
        explanation4 = Tex("of data in a normal distribution", font_size=32).shift(UP*2 + RIGHT*2.5)
        
        exp5 = Tex("About 68\\% of the data is within 1 standard deviation of the mean", font_size=36).shift(DOWN).to_corner(LEFT)
        exp6 = Tex("About 95\\% of the data is within 2 standard deviations of the mean", font_size=36).shift(DOWN*2).to_corner(LEFT)
        exp7 = Tex("About 99.7\\% of the data is within 3 standard deviations of the mean", font_size=36).shift(DOWN*3).to_corner(LEFT)
        expGroup = VGroup(exp5, exp6, exp7)
        
        self.play(Write(ER_title))
        self.play(FadeIn(explanation3), FadeIn(explanation4))
        self.wait(0.8)
        
        self.play(Write(expGroup), run_time=3)
        self.wait(3.6)
        self.play(FadeOut(explanation3), FadeOut(explanation4), FadeOut(expGroup), FadeOut(self.dGrouping), FadeOut(ER_title))

    def galton_board_animation(self):
        self.config = {
            "runTime": 9,
            "itemsTotal" : 250, 
            "itemDelayFrames" : 1,
            "circleSize" : 0.2,  
            "circleVerticalShift" : 0.6,  
            "circleGorizontalShift" : 0.4,  
            "circleRowsCount" : 7, 
            "firstCircleCenterX" : -3,  
            "firstCircleCenterY" : 3,  
            "durationSeconds" : 2,
            "circleRadius" : 0.05,
            "firstDot" : [-3, 4.3, 0]
        }
        
        self.frameNumber = 0

        # Galton board elements
        table = self.createTable()
        counter = self.createCounter()
        circles = self.createCircles()  
        vertices = self.createVertices()
        items = self.createItems(vertices)

        def updateFrameFunction(table):
            durationSeconds = self.config["durationSeconds"]
            durationFrames = durationSeconds * self.camera.frame_rate
            self.frameNumber += 1

            for item in items:
                if item.isActive and self.frameNumber > item.startFrame:
                    alpha = (self.frameNumber - item.startFrame) / durationFrames
                    if (alpha <= 1.0) :
                        point = item.path.point_from_proportion(rate_functions.linear(alpha))
                        item.circle.move_to(point)     
                    else:
                        updateCounter()
                        updateStackValue(item.stackIndex)
                        item.isActive = False

        def updateCounter():
            val = counter[0].get_value()
            val += 1
            counter[0].set_value(val)

        def updateStackValue(stackValueIndex):
            cell = table.get_entries((1, stackValueIndex + 1))
            val = cell.get_value()
            val += 1
            cell.set_value(val)

        self.play(FadeIn(circles), FadeIn(table), FadeIn(counter), run_time=1) 

        wrapper = VGroup(table, counter)
        for item in items:
            wrapper.add(item.circle)

        runTime = self.config["runTime"]
        self.play(UpdateFromFunc(wrapper, updateFrameFunction), run_time=runTime)

        self.wait(0.2)

    def createTable(self):
        table = IntegerTable(
            [[0, 0, 0, 0, 0, 0, 0, 0],],
            line_config={"stroke_width": 1, "color": YELLOW},
            include_outer_lines=False
            )
        table.scale(0.5)
        table.shift(DOWN * 3.7).shift(LEFT * 3)

        return table
    
    def createCounter(self):
        counter = Integer(0).shift(RIGHT * 4).shift(DOWN * .6)
        text = Text('Items count:', font_size = 28)
        text.next_to(counter, LEFT)

        return VGroup(counter, text)   
    
    def createCircles(self): 
        rows = self.config["circleRowsCount"] 
        circleSize = self.config["circleSize"] 
        circleVerticalShift = self.config["circleVerticalShift"]  
        circleGorizontalShift = self.config["circleGorizontalShift"]  
        firstCircleCenterX = self.config["firstCircleCenterX"] 
        firstCircleCenterY = self.config["firstCircleCenterY"] 

        circles = VGroup() 

        for row in range(rows):
            currentRowShiftUp = (firstCircleCenterY - row * circleVerticalShift)
            currentRowShiftRight = (firstCircleCenterX - row * circleGorizontalShift)
            for elem in range(row + 1):
                elemShiftRight = currentRowShiftRight + (elem * circleGorizontalShift) * 2

                tmp = Circle(radius = circleSize, color=BLUE_A)
                tmp.shift(UP * currentRowShiftUp)
                tmp.shift(RIGHT * elemShiftRight)
                circles.add(tmp)

        return circles
    
    def createVertices(self):
        rows = self.config["circleRowsCount"]  
        circleSize = self.config["circleSize"] 
        circleVerticalShift = self.config["circleVerticalShift"]  
        circleGorizontalShift = self.config["circleGorizontalShift"]  
        firstCircleCenterX = self.config["firstCircleCenterX"]  
        firstCircleCenterY = self.config["firstCircleCenterY"] 

        vertices = [[None for i in range(rows + 1)] for j in range(rows + 1)]

        for row in range(rows + 1):
            currentRowShiftUp = (firstCircleCenterY - row * circleVerticalShift)
            currentRowShiftRight = (firstCircleCenterX - row * circleGorizontalShift)
            for elem in range(row + 1):
                elemShiftRight = currentRowShiftRight + (elem * circleGorizontalShift) * 2
                vertices[row][elem] = [elemShiftRight, currentRowShiftUp + circleSize + .1, 0] 

        return vertices
    
    def createItems(self, vertices):
        itemsTotal = self.config["itemsTotal"]
        circleRadius = self.config["circleRadius"]
        itemDelayFrames = self.config["itemDelayFrames"]
        firstDot = self.config["firstDot"]

        items = []
        startFrame = 0
        stackValues = [0, 0, 0, 0, 0, 0, 0, 0]

        for k in range (itemsTotal):
            item = Item()
            circle = Circle(radius=circleRadius, color=GREEN, fill_opacity=1)
            pathIndex = self.createPathIndex()
            stackIndex = pathIndex.bit_count()
            stackValues[stackIndex] += 1

            path = self.createPath(vertices, pathIndex, stackValues[stackIndex])

            item.path = path
            item.circle = circle
            item.stackIndex = stackIndex
            item.startFrame = startFrame
            
            startFrame += itemDelayFrames

            self.add(circle)
            circle.move_to(firstDot)

            items.append(item)

        return items  

    def createPathIndex(self):
        pathIndex = random.randrange(128)
        return pathIndex
    
    def createPath(self, vertices, pathIndex, itemsCountInStack):
        firstDot = self.config["firstDot"]
        rowCapacity = 3

        lastDotRowIndex = (itemsCountInStack - 1) // rowCapacity
        lastDotColIndex = (itemsCountInStack - 1) % rowCapacity 
        
        path = Line(firstDot, vertices[0][0], stroke_width=1)
        previousDot = vertices[0][0]
        binary = bin(pathIndex)[2:].zfill(7)
        rowIndex = 1
        colIndex = 0
        for digit in binary:
            if digit == '0':
                pathTmp = ArcBetweenPoints(previousDot, vertices[rowIndex][colIndex], angle=PI/2, stroke_width=1)
                previousDot = vertices[rowIndex][colIndex]
            else:
                colIndex += 1
                pathTmp = ArcBetweenPoints(previousDot, vertices[rowIndex][colIndex], angle=-PI/2, stroke_width=1)
                previousDot = vertices[rowIndex][colIndex]
            path.append_vectorized_mobject(pathTmp)
            rowIndex += 1

        lastDotWidth = 0.1
        lastDotHeight = 0.1

        lastDotX = previousDot[0]
        
        if lastDotColIndex == 0:
            lastDotX = lastDotX - lastDotWidth
        elif lastDotColIndex == 2:
            lastDotX = lastDotX + lastDotWidth

        lastDotY = previousDot[1] - 2.4 + lastDotHeight * lastDotRowIndex

        pathLast = Line(previousDot, [lastDotX, lastDotY, 0] , stroke_width=1)
        path.append_vectorized_mobject(pathLast)

        return path    


class Item:
    circle = None
    path = None
    startFrame = 0
    stackIndex = 0  
    isActive = True
    
# manim -pqh Manim/NormalDistribution.py
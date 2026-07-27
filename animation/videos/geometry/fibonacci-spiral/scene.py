from manim import *
import numpy as np
from lnx import *

class FibonacciCurve(MovingCameraScene):
    def construct(self):
        # Background and camera
        #backgroundLnx(self)
        frame = self.camera.frame

        base_stroke = 4  # stroke inicial

        # Recursive Fibonacci function
        def Fibonacci(n):
            if n < 0:
                print("Incorrect input")
                return 0
            if n in (0, 1, 2):
                return 1 if n else 0
            return Fibonacci(n - 1) + Fibonacci(n - 2)

        # Initial square with yellow stroke and fill
        last_square = (
            Square(1)
            .set_stroke(color=YELLOW, width=4)
        )
        # Initial arc in a contrasting bright color (e.g., BLUE)
        arc = ArcBetweenPoints(
            last_square.get_vertices()[2],
            last_square.get_vertices()[0],
            color=BLUE,
            stroke_width=4
        )
        # Label in white for visibility
        tex = Tex("1", font_size=20, color=WHITE).move_to(last_square.get_center())
        squares = VGroup(last_square)

        # Directions for placing subsequent squares
        directions = [UP, LEFT, DOWN, RIGHT] * 12

        # Text scale
        scale_val = 0.5

        # Camera updater: keep a margin around the squares group
        frame.add_updater(lambda f: f.set(width=squares.width * 1.2))

        # Display initial square, arc, and label
        self.play(Create(last_square), Create(arc), Create(tex))

        # Build Fibonacci squares and colorful arcs
        for i in range(2, 21):
            direction = directions[i - 2]
            side = Fibonacci(i)

            # Create and style the square
            square = Square(side).next_to(squares, direction, buff=0)
            square.set_stroke(color=YELLOW, width=4) 
            squares.add(square)

            # Label for the square
            label = MathTex(
                f"{side}",
                font_size=square.side_length * 20 * scale_val,
                color=WHITE
            ).move_to(square.get_center())

            stroke_factor1=base_stroke*square.side_length*0.4/i 

            self.play(
                Create(square, run_time=0.5),
                Create(label, run_time=0.5)
            )

            # Smooth camera pan & zoom
            self.play(
                frame.animate
                     .move_to(squares.get_center())
                     .set(width=squares.width * 1.2),
                run_time=0.5,
                rate_func=smooth
            )

            # Draw arc in a secondary bright color (e.g., TEAL) for contrast
            verts = square.get_vertices()
            if direction is UP:
                arc = ArcBetweenPoints(verts[3], verts[1], color=TEAL, stroke_width=4)
            elif direction is LEFT:
                arc = ArcBetweenPoints(verts[0], verts[2], color=TEAL, stroke_width=4)
            elif direction is DOWN:
                arc = ArcBetweenPoints(verts[1], verts[3], color=TEAL, stroke_width=4)
            else:  # RIGHT
                arc = ArcBetweenPoints(verts[2], verts[0], color=TEAL, stroke_width=4)
            squares.add(arc)
            self.play(Create(arc, run_time=0.3))

            # Moderate stroke growth to maintain visual consistency
            self.play(
                    squares.animate.set_stroke(width=squares.get_stroke_width() + stroke_factor1),
                    run_time=0.3
                )
            """if 10 <= i < 20:
                self.play(
                    squares.animate.set_stroke(width=squares.get_stroke_width() + 15),
                    run_time=0.3
                )
            elif i >= 20:
                self.play(
                    squares.animate.set_stroke(width=squares.get_stroke_width() + 250),
                    run_time=0.3
                )
                """

        # Pause, then reset camera to initial square
        self.wait(2)
        frame.clear_updaters()
        self.play(
            frame.animate
                 .move_to(last_square.get_center())
                 .set(width=last_square.width * 1.5),
            squares.animate.set_stroke(width=base_stroke),
            run_time=3
        ) 
        self.wait(1)

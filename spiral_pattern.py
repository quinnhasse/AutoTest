import turtle
import colorsys

# Set up the Turtle screen
screen = turtle.Screen()
screen.bgcolor("black")
turtle.speed(0)
turtle.pensize(2)

# Function to draw a colorful spiral pattern
def draw_spiral(color):
    angle = 0
    while angle < 720:
        hue = angle / 360.0
        turtle.color(colorsys.hsv_to_rgb(hue, 1, 1))
        turtle.forward(angle / 10)
        turtle.right(30)
        angle += 1

# Draw multiple layers of the spiral pattern
for i in range(10):
    draw_spiral("white")

# Hide the Turtle and display the final pattern
turtle.hideturtle()
screen.mainloop()
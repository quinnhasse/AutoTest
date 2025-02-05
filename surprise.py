import turtle

# Create a screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Surprise Art")

# Create a turtle
artist = turtle.Turtle()
artist.speed(0)
artist.width(2)

# Set color palette
colors = ["red", "yellow", "blue", "green", "orange", "purple"]

# Draw a beautiful spiral design
for i in range(360):
    artist.color(colors[i % 6])
    artist.forward(i * 2)
    artist.right(59)

# Hide the turtle and display the artwork
artist.hideturtle()

# Exit on click
screen.exitonclick()
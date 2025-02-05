import turtle

def fractal_tree(t, branch_length, angle, level):
    if level == 0:
        return
    t.forward(branch_length)
    t.left(angle)
    fractal_tree(t, branch_length * 0.7, angle, level - 1)
    t.right(2 * angle)
    fractal_tree(t, branch_length * 0.7, angle, level - 1)
    t.left(angle)
    t.backward(branch_length)

if __name__ == "__main__":
    t = turtle.Turtle()
    my_screen = turtle.Screen()
    t.left(90)
    t.up()
    t.backward(200)
    t.down()
    t.color("green")
    fractal_tree(t, 100, 30, 7)
    my_screen.exitonclick()
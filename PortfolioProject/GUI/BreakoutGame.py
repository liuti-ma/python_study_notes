import turtle
import random

# Screen setup
screen = turtle.Screen()
screen.title("Breakout Game")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Paddle
paddle = turtle.Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# Ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, -200)
ball.dx = random.choice([-2, 2])
ball.dy = 2

# Bricks
bricks = []
colors = ["red", "orange", "yellow", "green", "blue"]
for row in range(5):
    for col in range(-5, 6):
        brick = turtle.Turtle()
        brick.shape("square")
        brick.color(colors[row])
        brick.shapesize(stretch_wid=1, stretch_len=2)
        brick.penup()
        brick.goto(col * 70, 200 - row * 30)
        bricks.append(brick)


# Paddle movement
def move_left():
    x = paddle.xcor()
    if x > -350:
        paddle.setx(x - 40)


def move_right():
    x = paddle.xcor()
    if x < 350:
        paddle.setx(x + 40)


screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")

# Game loop
while True:
    screen.update()
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Wall collision
    if ball.xcor() > 390 or ball.xcor() < -390:
        ball.dx *= -1
    if ball.ycor() > 290:
        ball.dy *= -1

    # Paddle collision
    if ball.ycor() < -240 and paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50:
        ball.dy *= -1

    # Brick collision
    for brick in bricks:
        if brick.distance(ball) < 30:
            ball.dy *= -1
            brick.goto(1000, 1000)
            bricks.remove(brick)
            break

    # Game over
    if ball.ycor() < -290:
        ball.goto(0, -200)
        ball.dx = random.choice([-2, 2])
        ball.dy = 2
        break

turtle.done()

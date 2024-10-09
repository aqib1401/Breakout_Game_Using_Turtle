from turtle import *
import random
import math

COLORS = ["#003049", "#d62828", "#f77f00", "#fcbf49", "#eae2b7"]

starting_ball_speed = 0.7
STARTING_ANGLE_MIN = 60
STARTING_ANGLE_MAX = 120

#  Set initial score to 0
score = 0

game_over = False
start_var = False

# Variables for paddle movement
move_left = False
move_right = False

paddle = Turtle()
ball = Turtle()
score_turtle = Turtle()
score_turtle.hideturtle()

start_msg = Turtle()
start_msg.penup()
start_msg.hideturtle()
start_msg.goto(x=0, y=-65)

# Create window
s = getscreen()
s.clear()

# Walls
right_wall = s.screensize()[0] / 2
left_wall = right_wall * -1

# Store all created turtles
turtles = []

# 3 dots to show lifelines
life_lines = []

# Turn off animation
tracer(0)


def create_targets():
    # coordinates for drawing target turtles
    x_cor = -280
    y_cor = 220
    for color in COLORS:
        for i in range(6):
            new_turtle = Turtle()
            new_turtle.penup()
            new_turtle.goto(x=x_cor, y=y_cor)
            new_turtle.shape("square")
            new_turtle.color(color)
            new_turtle.shapesize(stretch_len=5, stretch_wid=0.8)

            turtles.append(new_turtle)

            x_cor += 105
            if x_cor > 280:
                y_cor -= 22
                x_cor = -280


def create_lifeline_dots():
    # axis position for 3 dots
    x_axis = 310
    y_axis = 300
    # create 3 dot turtles to show lifelines
    for i in range(3):
        new_turtle = Turtle()
        new_turtle.penup()
        new_turtle.goto(x=x_axis, y=y_axis)
        new_turtle.shape("circle")
        new_turtle.color('Black')
        new_turtle.shapesize(stretch_len=0.5, stretch_wid=0.5)

        life_lines.append(new_turtle)

        x_axis += 20


def create_paddle():
    global paddle
    #  Create Paddle
    paddle = Turtle()
    paddle.penup()
    paddle.goto(x=0, y=-280)
    paddle.shape("square")
    paddle.color("#001f2d")
    paddle.shapesize(stretch_len=5, stretch_wid=0.6)


def create_ball():
    global ball
    #  Create Ball
    ball = Turtle()
    ball.penup()
    ball.goto(0, -250)
    ball.shape("circle")
    ball.color("#a32020")


def create_score():
    global score_turtle
    # Show score
    score_turtle = Turtle()
    score_turtle.penup()
    score_turtle.goto(-365, 290)
    score_turtle.hideturtle()


def move_paddle_right():
    global move_right
    move_right = True


def move_paddle_left():
    global move_left
    move_left = True


def stop_moving_right():
    global move_right
    move_right = False


def stop_moving_left():
    global move_left
    move_left = False


def move_ball():
    ball.forward(starting_ball_speed)


# change the color of targets to gery after game over
def change_color():
    for t in turtles:
        t.color("#adb5bd")


# bound to key 'Space bar' and when clicked, start the ball movement
def start():
    global start_var
    start_var = True


def starting_msg():
    global start_var
    if not start_var:
        start_msg.write("Press 'Space Bar' to play", align="center",
                        font=("Arial", 14, "normal"))


def check_collision(target_turtle):
    # Calculate the horizontal and vertical distances between the centers
    dx = abs(ball.xcor() - target_turtle.xcor())
    dy = abs(ball.ycor() - target_turtle.ycor())

    # Set thresholds based on the shapes' dimensions
    horizontal_threshold = (3.5 * 20) + (3.5 * 20)  # length of both turtles * 20 (turtle units)
    vertical_threshold = (1.3 * 20) + (1.3 * 20)  # width of both turtles * 20 (turtle units)

    if dx < horizontal_threshold / 2 and dy < vertical_threshold / 2:
        return True
    return False


#  Reset the game after a life loss
def re_try():
    to_delete = life_lines[0]  # Deletes the 1st lifeline dot
    to_delete.hideturtle()
    life_lines.remove(to_delete)

    # Starting angle for ball motion
    re_starting_angle = random.randint(STARTING_ANGLE_MIN, STARTING_ANGLE_MAX)

    ball.goto(0, -250)
    paddle.goto(0, -280)
    ball.setheading(re_starting_angle)

    if len(life_lines) == 0:
        global game_over
        game_over = True
        change_color()  # Change the color to remaining targets to grey


#  Updates the score on the screen
def show_score(total_score):
    score_turtle.clear()
    score_turtle.write(f"Score: {total_score}", font=("Arial", 12, "normal"))


#  Start / Re-start the game
def start_game():
    global score, start_var, game_over

    # Hide all the previous elements if exists

    #  if targets exists then hides it
    for t in turtles:
        t.hideturtle()
    turtles.clear()

    # clear screen of "Game Over" message
    hideturtle()
    clear()

    # clear screen of final score message
    score_turtle.clear()
    score_turtle.hideturtle()

    paddle.hideturtle()
    ball.hideturtle()

    starting_msg()

    # Create fresh elements
    create_targets()
    create_lifeline_dots()

    create_score()
    score = 0
    show_score(total_score=score)

    create_paddle()

    create_ball()
    ball.setheading(random.randint(STARTING_ANGLE_MIN, STARTING_ANGLE_MAX))

    onkey(start, "space")


listen()  # Listen for keyboard input
onkeypress(move_paddle_left, "Left")  # Start moving left on key press
onkeyrelease(stop_moving_left, "Left")  # Stop moving left on key release

onkeypress(move_paddle_right, "Right")  # Start moving right on key press
onkeyrelease(stop_moving_right, "Right")  # Stop moving right on key release

start_game()

while True:
    try:
        if move_right and paddle.xcor() < 320:
            paddle.setx(paddle.xcor() + 1)
        elif move_left and paddle.xcor() > -320:
            paddle.setx(paddle.xcor() - 1)

        if start_var and not game_over:
            start_msg.clear()
            # Move the ball
            move_ball()

        # Paddle collision
        if check_collision(paddle):
            # Calculate bounce angle based on where the ball hits the paddle
            relative_x = ball.xcor() - paddle.xcor()
            bounce_angle = math.degrees(math.atan2(ball.ycor() - paddle.ycor(), relative_x))
            ball.setheading(bounce_angle)

        # Wall collisions
        if abs(ball.xcor()) > 365:
            ball.setx(364 * (1 if ball.xcor() > 0 else -1))
            ball.setheading(180 - ball.heading())

        # Ceiling collision
        if ball.ycor() > 300:
            ball.sety(299)
            ball.setheading(-ball.heading())

        # Floor collision re-try / game over
        if ball.ycor() < -320:
            re_try()
            start_var = False

        else:
            # Target collisions
            for target in turtles:

                if check_collision(target_turtle=target):
                    target.hideturtle()
                    turtles.remove(target)
                    ball.setheading(-ball.heading())
                    score += 1
                    show_score(total_score=score)
                    starting_ball_speed += 0.02

                    break

        if game_over:
            # Game over message
            write("Game Over", align="center", font=("Arial", 24, "bold"))
            score_turtle.clear()
            score_turtle.goto(x=0, y=-35)
            score_turtle.write(f"Your final score is {score}", align="center",
                               font=("Arial", 17, "normal"))
            starting_msg()
            onkey(start_game, "space")
            game_over = False

        update()
    except Terminator:
        print("Window Closed. Game Over")
        bye()
        break

from paddle import Paddle
from ball import Ball


def get_output(ball_delta_y_input: float, paddle_velocity_input: float) -> float:
    if ball_delta_y_input < 0:
        return -1.0
    if ball_delta_y_input > 0:
        return 1.0
    else:
        return 0.0

def move_paddle(paddle: Paddle, ball: Ball, delta: float) -> float:
    ball_delta_y_input = ball.y - (paddle.y + paddle.width / 2)
    paddle_velocity_input = paddle.velocity
    paddle_speed_output = get_output(ball_delta_y_input, paddle_velocity_input)
    paddle.move(paddle_speed_output, delta)
    return paddle_speed_output

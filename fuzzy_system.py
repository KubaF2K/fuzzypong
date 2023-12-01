import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class FuzzySystem:
    def __init__(self, screen_height: int, paddle_size: int, max_speed: float, view: bool = False):
        ball_delta_y = ctrl.Antecedent(np.arange(-screen_height, screen_height, 0.5), 'ballDeltaY')
        ball_delta_y['FAR_HIGH'] = fuzz.trapmf(ball_delta_y.universe, [-screen_height, -screen_height, -paddle_size//2, -paddle_size//3])
        ball_delta_y['CLOSE_HIGH'] = fuzz.trapmf(ball_delta_y.universe, [-paddle_size//2, -paddle_size//3, -0.5, -0.5])
        ball_delta_y['ZERO'] = fuzz.trapmf(ball_delta_y.universe, [-0.5, -0.5, 0.5, 0.5])
        ball_delta_y['CLOSE_LOW'] = fuzz.trapmf(ball_delta_y.universe, [0.5, 0.5, paddle_size//3, paddle_size//2])
        ball_delta_y['FAR_LOW'] = fuzz.trapmf(ball_delta_y.universe, [paddle_size//3, paddle_size//2, screen_height, screen_height])
        if view:
            ball_delta_y.view()

        paddle_velocity = ctrl.Antecedent(np.arange(-max_speed, max_speed, 0.1), 'paddleVelocity')
        paddle_velocity['FAST_UP'] = fuzz.trapmf(paddle_velocity.universe,
                                                 [-max_speed, -max_speed, -max_speed // 4, -max_speed // 8])
        paddle_velocity['SLOW_UP'] = fuzz.trapmf(paddle_velocity.universe, [-max_speed // 4, -max_speed // 8, -0.1, -0.1])
        paddle_velocity['ZERO'] = fuzz.trapmf(paddle_velocity.universe, [-0.1, -0.1, 0.1, 0.1])
        paddle_velocity['SLOW_DOWN'] = fuzz.trapmf(paddle_velocity.universe, [0.1, 0.1, max_speed // 8, max_speed // 4])
        paddle_velocity['FAST_DOWN'] = fuzz.trapmf(paddle_velocity.universe,
                                                   [max_speed // 8, max_speed // 4, max_speed, max_speed])
        if view:
            paddle_velocity.view()

        paddle_speed = ctrl.Consequent(np.arange(-2.0, 2.0, 0.1), 'paddleSpeed')
        paddle_speed['FAST_UP'] = fuzz.trapmf(paddle_speed.universe, [-2.0, -2.0, -1.2, -1.0])
        paddle_speed['SLOW_UP'] = fuzz.trapmf(paddle_speed.universe, [-1.2, -1.0, -0.1, -0.1])
        paddle_speed['ZERO'] = fuzz.trapmf(paddle_speed.universe, [-0.1, -0.1, 0.1, 0.1])
        paddle_speed['SLOW_DOWN'] = fuzz.trapmf(paddle_speed.universe, [0.1, 0.1, 1.0, 1.2])
        paddle_speed['FAST_DOWN'] = fuzz.trapmf(paddle_speed.universe, [1.0, 1.2, 2.0, 2.0])
        if view:
            paddle_speed.view()

        self.fuzzy_rules = [ctrl.Rule(ball_delta_y['FAR_HIGH'] & paddle_velocity['FAST_DOWN'], paddle_speed['FAST_UP']),
                            ctrl.Rule(ball_delta_y['FAR_HIGH'] & paddle_velocity['SLOW_DOWN'], paddle_speed['FAST_UP']),
                            ctrl.Rule(ball_delta_y['FAR_HIGH'] & paddle_velocity['ZERO'], paddle_speed['FAST_UP']),
                            ctrl.Rule(ball_delta_y['FAR_HIGH'] & paddle_velocity['SLOW_UP'], paddle_speed['SLOW_UP']),
                            ctrl.Rule(ball_delta_y['FAR_HIGH'] & paddle_velocity['FAST_UP'], paddle_speed['ZERO']),
                            ctrl.Rule(ball_delta_y['CLOSE_HIGH'] & paddle_velocity['FAST_DOWN'], paddle_speed['FAST_UP']),
                            ctrl.Rule(ball_delta_y['CLOSE_HIGH'] & paddle_velocity['SLOW_DOWN'], paddle_speed['FAST_UP']),
                            ctrl.Rule(ball_delta_y['CLOSE_HIGH'] & paddle_velocity['ZERO'], paddle_speed['SLOW_UP']),
                            ctrl.Rule(ball_delta_y['CLOSE_HIGH'] & paddle_velocity['SLOW_UP'], paddle_speed['ZERO']),
                            ctrl.Rule(ball_delta_y['CLOSE_HIGH'] & paddle_velocity['FAST_UP'], paddle_speed['SLOW_DOWN']),
                            ctrl.Rule(ball_delta_y['ZERO'] & paddle_velocity['FAST_DOWN'], paddle_speed['FAST_UP']),
                            ctrl.Rule(ball_delta_y['ZERO'] & paddle_velocity['SLOW_DOWN'], paddle_speed['SLOW_UP']),
                            ctrl.Rule(ball_delta_y['ZERO'] & paddle_velocity['ZERO'], paddle_speed['ZERO']),
                            ctrl.Rule(ball_delta_y['ZERO'] & paddle_velocity['SLOW_UP'], paddle_speed['SLOW_DOWN']),
                            ctrl.Rule(ball_delta_y['ZERO'] & paddle_velocity['FAST_UP'], paddle_speed['FAST_DOWN']),
                            ctrl.Rule(ball_delta_y['CLOSE_LOW'] & paddle_velocity['FAST_DOWN'], paddle_speed['SLOW_UP']),
                            ctrl.Rule(ball_delta_y['CLOSE_LOW'] & paddle_velocity['SLOW_DOWN'], paddle_speed['ZERO']),
                            ctrl.Rule(ball_delta_y['CLOSE_LOW'] & paddle_velocity['ZERO'], paddle_speed['SLOW_DOWN']),
                            ctrl.Rule(ball_delta_y['CLOSE_LOW'] & paddle_velocity['SLOW_UP'], paddle_speed['FAST_DOWN']),
                            ctrl.Rule(ball_delta_y['CLOSE_LOW'] & paddle_velocity['FAST_UP'], paddle_speed['FAST_DOWN']),
                            ctrl.Rule(ball_delta_y['FAR_LOW'] & paddle_velocity['FAST_DOWN'], paddle_speed['ZERO']),
                            ctrl.Rule(ball_delta_y['FAR_LOW'] & paddle_velocity['SLOW_DOWN'], paddle_speed['SLOW_DOWN']),
                            ctrl.Rule(ball_delta_y['FAR_LOW'] & paddle_velocity['ZERO'], paddle_speed['FAST_DOWN']),
                            ctrl.Rule(ball_delta_y['FAR_LOW'] & paddle_velocity['SLOW_UP'], paddle_speed['FAST_DOWN']),
                            ctrl.Rule(ball_delta_y['FAR_LOW'] & paddle_velocity['FAST_UP'], paddle_speed['FAST_DOWN'])]

        paddle_ctrl = ctrl.ControlSystem(self.fuzzy_rules)
        self.paddle_simulation = ctrl.ControlSystemSimulation(paddle_ctrl)

    def get_output(self, ball_delta_y_input: float, paddle_velocity_input: float) -> float:
        self.paddle_simulation.input['ballDeltaY'] = ball_delta_y_input
        self.paddle_simulation.input['paddleVelocity'] = paddle_velocity_input
        self.paddle_simulation.compute()
        return self.paddle_simulation.output['paddleSpeed']

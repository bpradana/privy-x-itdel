import random
from typing import Dict, Tuple, Union, List

import cv2
import pygame
from deepface import DeepFace


class Paddle:
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        velocity: int,
        color: Tuple[int, int, int],
    ) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.color = color
        self.paddle = pygame.Rect(x, y, width, height)
        self.direction_x = 0

    def draw(self) -> None:
        pygame.draw.rect(
            surface=self.screen,
            color=self.color,
            rect=self.paddle,
        )

    def hit_wall(self) -> bool:
        if self.paddle.x <= 0 or self.paddle.x + self.width >= self.screen.get_width():
            return True
        return False

    def move(self, x: Union[int, None] = None) -> None:
        if x is not None:
            self.paddle.x = x
        else:
            self.paddle.x += self.velocity * self.direction_x
            if self.hit_wall():
                self.paddle.x = (
                    0 if self.paddle.x <= 0 else self.screen.get_width() - self.width
                )

    def stop(self) -> None:
        self.direction_x = 0

    def move_left(self) -> None:
        self.direction_x = -1

    def move_right(self) -> None:
        self.direction_x = 1

    def reset(self) -> None:
        self.paddle.x = self.screen.get_width() // 2 - self.width // 2


class Ball:
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        radius: int,
        velocity: int,
        color: Tuple[int, int, int],
    ) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity
        self.color = color
        self.direction_x = 1
        self.direction_y = 1
        self.ball = pygame.Rect(x, y, radius, radius)

    def draw(self) -> None:
        pygame.draw.rect(
            surface=self.screen,
            color=self.color,
            rect=self.ball,
        )

    def hit_wall(self) -> bool:
        if self.ball.x <= 0 or self.ball.x + self.radius >= self.screen.get_width():
            return True
        return False

    def hit_paddle(self, paddle: Paddle) -> bool:
        if self.ball.colliderect(paddle.paddle):
            return True
        return False

    def hit_top(self) -> bool:
        if self.ball.y <= 0:
            return True
        return False

    def hit_bottom(self) -> bool:
        if self.ball.y + self.radius >= self.screen.get_height():
            return True
        return False

    def bounce(self, axis: str) -> None:
        if axis == "x":
            self.direction_x *= -1
        elif axis == "y":
            self.direction_y *= -1

    def move(self) -> None:
        self.ball.x += self.velocity * self.direction_x
        self.ball.y += self.velocity * self.direction_y
        if self.hit_wall():
            self.bounce("x")

    def reset(self, direction) -> None:
        self.ball.x = self.screen.get_width() // 2 - self.radius // 2
        self.ball.y = self.screen.get_height() // 2 - self.radius // 2

        self.direction_x = random.choice([-1, 1])
        if direction == "top":
            self.direction_y = -1
        elif direction == "bottom":
            self.direction_y = 1


class Score:
    def __init__(
        self,
        screen: pygame.Surface,
        position: str,
        color: Tuple[int, int, int],
    ):
        self.screen = screen
        self.position = position
        self.color = color
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)

    def _get_position(self) -> Tuple[int, int]:
        if self.position == "top":
            return (50, self.screen.get_height() // 4)
        elif self.position == "bottom":
            return (50, self.screen.get_height() // 4 * 3)
        else:
            raise ValueError("Invalid position")

    def draw(self) -> None:
        text = self.font.render(
            str(self.score),
            True,
            self.color,
        )
        self.screen.blit(text, self._get_position())

    def increment(self) -> None:
        self.score += 1


class Game:
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        paddle_width: int,
        paddle_height: int,
        paddle_color: Tuple[int, int, int],
        paddle_velocity: int,
        ball_radius: int,
        ball_color: Tuple[int, int, int],
        ball_velocity: int,
        score_color: Tuple[int, int, int],
    ) -> None:
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height
        self.paddle_color = paddle_color
        self.paddle_velocity = paddle_velocity
        self.ball_radius = ball_radius
        self.ball_color = ball_color
        self.ball_velocity = ball_velocity
        self.score_color = score_color

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.paddle_top = Paddle(
            screen=self.screen,
            x=self.screen_width // 2 - self.paddle_width // 2,
            y=0,
            width=self.paddle_width,
            height=self.paddle_height,
            velocity=self.paddle_velocity,
            color=self.paddle_color,
        )
        self.paddle_bottom = Paddle(
            screen=self.screen,
            x=self.screen_width // 2 - self.paddle_width // 2,
            y=self.screen_height - self.paddle_height,
            width=self.paddle_width,
            height=self.paddle_height,
            velocity=self.paddle_velocity,
            color=self.paddle_color,
        )
        self.ball = Ball(
            screen=self.screen,
            x=self.screen_width // 2 - self.ball_radius // 2,
            y=self.screen_height // 2 - self.ball_radius // 2,
            radius=self.ball_radius,
            velocity=self.ball_velocity,
            color=self.ball_color,
        )
        self.score_top = Score(
            screen=self.screen,
            position="top",
            color=self.score_color,
        )
        self.score_bottom = Score(
            screen=self.screen,
            position="bottom",
            color=self.score_color,
        )

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.paddle_top.draw()
        self.paddle_bottom.draw()
        self.ball.draw()
        self.score_top.draw()
        self.score_bottom.draw()

    def update(self) -> None:
        self.ball.move()
        self.paddle_top.move()
        self.paddle_bottom.move()
        if self.ball.hit_paddle(self.paddle_top):
            self.ball.bounce("y")
        if self.ball.hit_paddle(self.paddle_bottom):
            self.ball.bounce("y")
        if self.ball.hit_bottom():
            self.score_top.increment()
            self.ball.reset("bottom")
            self.paddle_bottom.reset()
            self.paddle_top.reset()
        if self.ball.hit_top():
            self.score_bottom.increment()
            self.ball.reset("top")
            self.paddle_bottom.reset()
            self.paddle_top.reset()

    def control(
        self,
        mode: str = "key",
        event: Union[pygame.event.Event, None] = None,
        face_coordinate: Union[Dict[str, float], None] = None,
    ) -> None:
        if mode == "key" and event is not None:
            self._control_key(event)
        elif mode == "face" and face_coordinate is not None:
            self._control_face(face_coordinate)
        else:
            raise ValueError("Invalid mode")

    def _control_key(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.paddle_top.move_left()
            if event.key == pygame.K_RIGHT:
                self.paddle_top.move_right()
            if event.key == pygame.K_a:
                self.paddle_bottom.move_left()
            if event.key == pygame.K_d:
                self.paddle_bottom.move_right()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.paddle_top.stop()
            if event.key == pygame.K_a or event.key == pygame.K_d:
                self.paddle_bottom.stop()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    def _control_face(self, face_coordinate: Dict[str, float]) -> None:
        self.paddle_top.move(int(self.screen_width * face_coordinate["top"]))
        self.paddle_bottom.move(int(self.screen_width * face_coordinate["bottom"]))


class FaceDetection:
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        left_color: Tuple[int, int, int],
        right_color: Tuple[int, int, int],
    ) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.left_color = left_color
        self.right_color = right_color
        self.cap = cv2.VideoCapture(0)
        self.left_roi = {
            "x": 0,
            "y": 0,
            "w": self.screen_width // 2,
            "h": self.screen_height,
        }
        self.right_roi = {
            "x": self.screen_width // 2,
            "y": 0,
            "w": self.screen_width // 2,
            "h": self.screen_height,
        }
        self.left_face = None
        self.right_face = None

    def draw(self) -> None:
        _, self.frame = self.cap.read()
        self.frame = cv2.flip(self.frame, 1)
        self.frame = cv2.resize(self.frame, (self.screen_width, self.screen_height))

        self.draw_roi()

        self.results = DeepFace.extract_faces(
            self.frame, detector_backend="yolov8", enforce_detection=False
        )

        self.left_face = self.largest_face_in_roi(self.left_roi)
        self.right_face = self.largest_face_in_roi(self.right_roi)
        self.draw_player()

        cv2.imshow("frame", self.frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            self.close()

    def close(self) -> None:
        self.cap.release()
        cv2.destroyAllWindows()

    def draw_roi(self) -> None:
        cv2.rectangle(
            img=self.frame,
            pt1=(self.left_roi["x"], self.left_roi["y"]),
            pt2=(
                self.left_roi["x"] + self.left_roi["w"],
                self.left_roi["y"] + self.left_roi["h"],
            ),
            color=self.left_color,
            thickness=2,
        )
        cv2.rectangle(
            img=self.frame,
            pt1=(self.right_roi["x"], self.right_roi["y"]),
            pt2=(
                self.right_roi["x"] + self.right_roi["w"],
                self.right_roi["y"] + self.right_roi["h"],
            ),
            color=self.right_color,
            thickness=2,
        )

    def draw_bbox(
        self, bbox: Dict[str, int], text: str, color: Tuple[int, int, int]
    ) -> None:
        cv2.rectangle(
            img=self.frame,
            pt1=(bbox["x"], bbox["y"]),
            pt2=(bbox["x"] + bbox["w"], bbox["y"] + bbox["h"]),
            color=color,
            thickness=2,
        )
        cv2.putText(
            img=self.frame,
            text=text,
            org=(bbox["x"], bbox["y"]),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=color,
            thickness=2,
            lineType=cv2.LINE_AA,
        )

    def draw_player(self):
        if self.left_face is not None:
            self.draw_bbox(
                bbox=self.left_face["facial_area"],
                text="Player 1",
                color=self.left_color,
            )
        if self.right_face is not None:
            self.draw_bbox(
                bbox=self.right_face["facial_area"],
                text="Player 2",
                color=self.right_color,
            )

    def face_in_roi(
        self,
        facial_area: Dict[str, int],
        roi: Dict[str, int],
    ) -> bool:
        if (
            facial_area["x"] >= roi["x"]
            and facial_area["x"] + facial_area["w"] <= roi["x"] + roi["w"]
            and facial_area["y"] >= roi["y"]
            and facial_area["y"] + facial_area["h"] <= roi["y"] + roi["h"]
        ):
            return True
        return False

    def largest_face_in_roi(self, roi: Dict[str, int]):
        largest_face = None
        largest_face_area = 0
        for result in self.results:
            if self.face_in_roi(result["facial_area"], roi):
                face_area = result["facial_area"]["w"] * result["facial_area"]["h"]
                if face_area > largest_face_area:
                    largest_face = result
                    largest_face_area = face_area
        return largest_face

    def to_float(self, facial_area: Dict[str, int], roi: Dict[str, int]) -> float:
        return (facial_area["x"] - roi["x"] + facial_area["w"] // 2) / (
            self.screen_width // 2
        )

    def map_control(self) -> Dict[str, float]:
        control = {"top": 0.5, "bottom": 0.5}
        if self.left_face is not None:
            control["top"] = self.to_float(self.left_face["facial_area"], self.left_roi)
        if self.right_face is not None:
            control["bottom"] = self.to_float(
                self.right_face["facial_area"], self.right_roi
            )
        return control


if __name__ == "__main__":
    COLOR_WHITE = (255, 255, 255)
    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (0, 0, 255)

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 800
    PADDLE_WIDTH = 100
    PADDLE_HEIGHT = 20
    PADDLE_COLOR = COLOR_WHITE
    PADDLE_VELOCITY = 5
    BALL_RADIUS = 10
    BALL_COLOR = COLOR_WHITE
    BALL_VELOCITY = 13
    SCORE_COLOR = COLOR_WHITE

    FD_SCREEN_WIDTH = 1280
    FD_SCREEN_HEIGHT = 720
    FD_LEFT_COLOR = COLOR_BLUE
    FD_RIGHT_COLOR = COLOR_GREEN

    game = Game(
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT,
        paddle_width=PADDLE_WIDTH,
        paddle_height=PADDLE_HEIGHT,
        paddle_color=PADDLE_COLOR,
        paddle_velocity=PADDLE_VELOCITY,
        ball_radius=BALL_RADIUS,
        ball_color=BALL_COLOR,
        ball_velocity=BALL_VELOCITY,
        score_color=SCORE_COLOR,
    )
    face_detection = FaceDetection(
        screen_width=FD_SCREEN_WIDTH,
        screen_height=FD_SCREEN_HEIGHT,
        left_color=FD_LEFT_COLOR,
        right_color=FD_RIGHT_COLOR,
    )

    while True:
        game.draw()
        face_detection.draw()

        # key control mode
        # for event in pygame.event.get():
        #     game.control(mode="key", event=event)

        # face control mode
        face_coordinate = face_detection.map_control()
        game.control(mode="face", face_coordinate=face_coordinate)

        game.update()
        pygame.display.update()
        game.clock.tick(30)

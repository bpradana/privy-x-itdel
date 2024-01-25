import cv2
import mediapipe as mp
import pygame
import random
from typing import Union, Dict, List


class HandEvent:
    def __init__(self, click: bool, x: float, y: float) -> None:
        self.click = click
        self.x = x
        self.y = y


class HandEventMotion(HandEvent):
    def __init__(self, click: bool, x: float, y: float) -> None:
        super().__init__(click, x, y)


class HandEventDown(HandEvent):
    def __init__(self, click: bool, x: float, y: float) -> None:
        super().__init__(click, x, y)


class HandEventUp(HandEvent):
    def __init__(self, click: bool, x: float, y: float) -> None:
        super().__init__(click, x, y)


class Block:
    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
    ):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        self.block = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self) -> None:
        pygame.draw.rect(
            surface=self.screen,
            color=self.color,
            rect=self.block,
        )

    def move(self, x: int, y: int) -> None:
        self.block.x = x
        self.block.y = y


class BlockController:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.blocks = []

        self.dragging = False
        self.selected_block = None
        self.offset_x = 0
        self.offset_y = 0

    def add_block(self, block: Block) -> None:
        self.blocks.append(block)

    def remove_block(self, block: Block) -> None:
        self.blocks.remove(block)

    def start_drag(self, block: Block, cursor_x: int, cursor_y: int) -> None:
        self.dragging = True
        self.selected_block = block
        self.offset_x = block.block.x - cursor_x
        self.offset_y = block.block.y - cursor_y

    def stop_drag(self) -> None:
        self.dragging = False
        self.selected_block = None

    def drag(self, cursor_x: int, cursor_y: int) -> None:
        if self.dragging and self.selected_block is not None:
            self.selected_block.move(cursor_x + self.offset_x, cursor_y + self.offset_y)

    def collide(self, cursor_x: int, cursor_y: int) -> Union[Block, None]:
        for block in self.blocks:
            if block.block.collidepoint(cursor_x, cursor_y):
                return block
        return None

    def draw(self) -> None:
        for block in self.blocks:
            block.draw()


class Cursor:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.size = 10
        self.cursor = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self):
        pygame.draw.rect(
            surface=self.screen,
            color=self.color,
            rect=self.cursor,
        )

    def move(self, x, y):
        self.cursor.x = x
        self.cursor.y = y


class Playground:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.block_controller = BlockController(self.screen)
        self.cursor = Cursor(self.screen, 0, 0)

    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.block_controller.draw()
        self.cursor.draw()

    def control(
        self,
        mode: str = "key",
        event: Union[pygame.event.Event, None] = None,
        hand_event: Union[
            Union[HandEventMotion, HandEventDown, HandEventUp], None
        ] = None,
    ) -> None:
        if mode == "mouse" and event is not None:
            self._control_mouse(event)
        elif mode == "hand" and hand_event is not None:
            self._control_hand(hand_event)
        else:
            raise ValueError("mode must be 'mouse' or 'hand'")

    def _control_mouse(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if block := self.block_controller.collide(*event.pos):
                    self.block_controller.start_drag(block, *event.pos)
                else:
                    self.block_controller.add_block(
                        Block(
                            self.screen,
                            event.pos[0],
                            event.pos[1],
                            random.randint(10, 100),
                            random.randint(10, 100),
                        )
                    )
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.block_controller.stop_drag()
        elif event.type == pygame.MOUSEMOTION:
            self.cursor.move(*event.pos)
            self.block_controller.drag(*event.pos)

    def _control_hand(
        self, event: Union[HandEventMotion, HandEventDown, HandEventUp]
    ) -> None:
        cursor_x = int(event.x * self.screen_width)
        cursor_y = int(event.y * self.screen_height)

        if type(event) == HandEventDown:
            if block := self.block_controller.collide(cursor_x, cursor_y):
                self.block_controller.start_drag(block, cursor_x, cursor_y)
            else:
                self.block_controller.add_block(
                    Block(
                        self.screen,
                        cursor_x,
                        cursor_y,
                        random.randint(10, 100),
                        random.randint(10, 100),
                    )
                )
        elif type(event) == HandEventUp:
            self.block_controller.stop_drag()
        elif type(event) == HandEventMotion:
            self.cursor.move(cursor_x, cursor_y)
            self.block_controller.drag(cursor_x, cursor_y)


class HandTracking:
    def __init__(self, screen_width: int, screen_height: int) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands  # type: ignore
        self.mp_draw = mp.solutions.drawing_utils  # type: ignore
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75,
        )
        self.click = False
        self.cursor_x = 0
        self.cursor_y = 0

    def draw(self, hands) -> None:
        _, self.frame = self.cap.read()
        self.frame = cv2.cvtColor(cv2.flip(self.frame, 1), cv2.COLOR_BGR2RGB)
        self.frame = cv2.resize(self.frame, (self.screen_width, self.screen_height))

        self.results = hands.process(self.frame)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)

        self._draw_annotation()
        self.multi_hand_landmarks_processed = self._preprocess_landmarks()
        self.palm_coordinates = self._get_palm_coordinates(
            self.multi_hand_landmarks_processed
        )
        self._draw_cursor(self.palm_coordinates, self.multi_hand_landmarks_processed)

        cv2.imshow("frame", self.frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            self.close()

    def close(self) -> None:
        self.cap.release()
        cv2.destroyAllWindows()

    def _draw_annotation(self) -> None:
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    self.frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

    def _draw_cursor(
        self,
        palm_coordinates: List[Dict[str, int]],
        multi_hand_landmarks_processed: List[List[Dict[str, Union[int, float]]]],
    ) -> None:
        if palm_coordinates and multi_hand_landmarks_processed:
            for palm_coordinate, hand_landmarks in zip(
                palm_coordinates, multi_hand_landmarks_processed
            ):
                cv2.circle(
                    self.frame,
                    (palm_coordinate["x"], palm_coordinate["y"]),
                    10,
                    (255, 0, 0),
                    cv2.FILLED,
                )
                if self._is_pinch(hand_landmarks):
                    cv2.circle(
                        self.frame,
                        (palm_coordinate["x"], palm_coordinate["y"]),
                        20,
                        (0, 255, 0),
                        cv2.FILLED,
                    )

    def _preprocess_landmarks(self) -> List[List[Dict[str, Union[int, float]]]]:
        if not self.results.multi_hand_landmarks:
            return []

        multi_hand_landmarks_processed = []

        for hand_landmarks in self.results.multi_hand_landmarks:
            landmarks_processed = []
            for id, landmark in enumerate(hand_landmarks.landmark):
                landmarks_processed.append(
                    {
                        "id": id,
                        "x": landmark.x,
                        "y": landmark.y,
                    }
                )
            multi_hand_landmarks_processed.append(landmarks_processed)

        return multi_hand_landmarks_processed

    def _get_palm_coordinates(
        self,
        multi_hand_landmarks_processed: List[List[Dict[str, Union[int, float]]]],
    ) -> List[Dict[str, int]]:
        if not multi_hand_landmarks_processed:
            return [{"x": self.screen_width // 2, "y": self.screen_height // 2}]

        palm_coordinates = []
        palm_ids = [0, 5, 9, 13, 17]

        for hand_landmarks in multi_hand_landmarks_processed:
            x_sum = 0
            y_sum = 0
            for landmark in hand_landmarks:
                if landmark["id"] in palm_ids:
                    x_sum += landmark["x"]
                    y_sum += landmark["y"]
            palm_coordinates.append(
                {
                    "x": int(x_sum / len(palm_ids) * self.screen_width),
                    "y": int(y_sum / len(palm_ids) * self.screen_height),
                }
            )

        return palm_coordinates

    def _is_pinch(
        self,
        hand_landmarks_processed: List[Dict[str, Union[int, float]]],
        threshold: float = 0.08,
    ) -> bool:
        thumb_tip = hand_landmarks_processed[4]
        index_tip = hand_landmarks_processed[8]
        distance = (
            (thumb_tip["x"] - index_tip["x"]) ** 2
            + (thumb_tip["y"] - index_tip["y"]) ** 2
        ) ** 0.5
        if distance < threshold:
            return True
        return False

    def _cursor_easing(
        self, cursor_x: int, cursor_y: int, easing: float = 0.05
    ) -> None:
        self.cursor_x += (cursor_x - self.cursor_x) * easing
        self.cursor_y += (cursor_y - self.cursor_y) * easing

    def event(self) -> List[Union[HandEventMotion, HandEventDown, HandEventUp]]:
        hand_events = []

        for palm_coordinate, hand_landmarks in zip(
            self.palm_coordinates, self.multi_hand_landmarks_processed
        ):
            cursor_x = palm_coordinate["x"] / self.screen_width
            cursor_y = palm_coordinate["y"] / self.screen_height

            if self.click == self._is_pinch(hand_landmarks):
                hand_events.append(
                    HandEventMotion(click=self.click, x=cursor_x, y=cursor_y)
                )
            elif not self.click:
                self.click = self._is_pinch(hand_landmarks)
                hand_events.append(
                    HandEventDown(click=self.click, x=cursor_x, y=cursor_y)
                )
            elif self.click:
                self.click = self._is_pinch(hand_landmarks)
                hand_events.append(
                    HandEventUp(click=self.click, x=cursor_x, y=cursor_y)
                )

        return hand_events


if __name__ == "__main__":
    playground = Playground(1280, 720)
    hand_tracking = HandTracking(playground.screen_width, playground.screen_height)

    with hand_tracking.hands as hands:
        while True:
            playground.draw()
            hand_tracking.draw(hands)

            # for event in pygame.event.get():
            #     playground.control(mode="mouse", event=event)

            for event in hand_tracking.event():
                playground.control(mode="hand", hand_event=event)

            pygame.display.update()
            playground.clock.tick(20)

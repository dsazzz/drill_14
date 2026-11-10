from math import sin, tau

from pico2d import get_canvas_width, get_time, load_image

#커밋용

class Bird:
    WIDTH = 90
    HEIGHT = 83
    FRAME_COUNT = 14
    FRAMES_PER_SECOND = 14

    def __init__(self, image, offset_x, offset_y, phase):
        self.image = image
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.phase = phase

    def draw(self, flock_x, direction, elapsed):
        frame = int(elapsed * self.FRAMES_PER_SECOND + self.phase) % self.FRAME_COUNT
        column, row = frame % 5, frame // 5

        # The 918 x 506 sheet is not evenly divisible into its 5 x 3 grid.
        left = column * self.image.w // 5
        right = (column + 1) * self.image.w // 5
        top = row * self.image.h // 3
        bottom = (row + 1) * self.image.h // 3

        bob = 4 * sin(tau * (elapsed * 0.8 + self.phase / self.FRAME_COUNT))
        self.image.clip_composite_draw(
            left, self.image.h - bottom, right - left, bottom - top,
            0, '' if direction == 1 else 'h',
            flock_x + self.offset_x, self.offset_y + bob,
            self.WIDTH, self.HEIGHT
        )


class BirdFlock:
    SPEED = 150  # pixels per second
    SPACING = 100

    def __init__(self):
        image = load_image('bird_animation.png')
        self.birds = [
            Bird(image, (i % 5 - 2) * self.SPACING,
                 425 + (i // 5) * 90, i * 1.4)
            for i in range(10)
        ]
        self.elapsed = 0.0
        self.last_time = get_time()
        self.distance = 0.0
        self.x = 0.0
        self.direction = 1
        self.update_position()

    def reset_clock(self):
        self.last_time = get_time()

    def update_position(self):
        margin = 2 * self.SPACING + Bird.WIDTH / 2
        left = margin
        right = max(left, get_canvas_width() - margin)
        width = right - left
        if width == 0:
            self.x = get_canvas_width() / 2
            return

        # A triangular path preserves overshoot even after a long frame.
        position = self.distance % (2 * width)
        if position < width:
            self.x = left + position
            self.direction = 1
        else:
            self.x = right - (position - width)
            self.direction = -1

    def update(self):
        now = get_time()
        dt = max(0.0, now - self.last_time)
        self.last_time = now
        self.elapsed += dt
        self.distance += self.SPEED * dt
        self.update_position()

    def draw(self):
        for bird in self.birds:
            bird.draw(self.x, self.direction, self.elapsed)

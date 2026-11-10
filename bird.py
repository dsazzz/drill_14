from pico2d import get_canvas_width, load_image


class Bird:
    image = None
    WIDTH = 90
    HEIGHT = 83
    SPEED = 3

    def __init__(self, x, y):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.direction = 1

    def update(self):
        self.x += self.direction * self.SPEED
        left = self.WIDTH / 2
        right = get_canvas_width() - self.WIDTH / 2

        if self.x >= right:
            self.x = right
            self.direction = -1
        elif self.x <= left:
            self.x = left
            self.direction = 1

    def draw(self):
        # Step 1: use the top-left pose; wing animation comes in step 2.
        self.image.clip_composite_draw(
            0, self.image.h - 168, 183, 168,
            0, '' if self.direction == 1 else 'h',
            self.x, self.y, self.WIDTH, self.HEIGHT
        )

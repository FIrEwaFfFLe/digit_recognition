from math import *
from pygame import *
import constants
import tester
import mnist_data
import qwe


def wab(x):
    return x * 255, x * 255, x * 255


def generate(x):
    ans = [[0] * int(2 * x - 1) for _ in range(int(2 * x - 1))]
    for i in range(int(2 * x - 1)):
        for j in range(int(2 * x - 1)):
            x1, y1 = j - x + 1, i - x + 1
            ans[i][j] = 1 - sqrt((x1 * x1 + y1 * y1) / (x * x))
    return ans


def paint(x, y):
    global canvas, pattern
    for i in range(y - constants.thickness + 1, y + constants.thickness):
        for j in range(x - constants.thickness + 1, x + constants.thickness):
            if 0 <= i <= 27 and 0 <= j <= 27:
                canvas[i * 28 + j] = max(canvas[i * 28 + j], pattern[i - y + constants.thickness - 1][j - x + constants.thickness - 1])


def run():
    global canvas
    init()
    running = True
    # mode 1 - simulation playing, 2 - paused
    ticks = 0
    screen = display.set_mode((constants.width, constants.height))
    display.set_caption("Digit guesser")
    brush = False
    eraser = False
    mnist_cur = 0

    while running:
        clock = time.Clock()
        clock.tick(constants.FPS)

        # key
        for q in event.get():
            if q.type == QUIT:
                running = False
            if q.type == MOUSEBUTTONDOWN and q.button == 1:
                brush = True
            if q.type == MOUSEBUTTONUP and q.button == 1:
                brush = False
            if q.type == MOUSEBUTTONDOWN and q.button == 3:
                eraser = True
            if q.type == MOUSEBUTTONUP and q.button == 3:
                eraser = False
            if q.type == KEYDOWN and q.key == 114:
                tester.call(canvas)
            if q.type == KEYDOWN and q.key == 113:
                canvas = [0] * 784
            if q.type == KEYDOWN and q.key == 120:
                canvas = [mnist_data.end[mnist_cur][0][i] for i in range(784)]
            if q.type == KEYDOWN and q.key == 1073741903:
                mnist_cur += 1
            if q.type == KEYDOWN and q.key == 1073741904:
                mnist_cur = (mnist_cur - 1 + len(mnist_data.end)) % len(mnist_data.end)

        if brush and not eraser:
            pos = mouse.get_pos()
            x, y = pos[0] // constants.one, pos[1] // constants.one
            if y <= 27:
                paint(x, y)
        if eraser and not brush:
            pos = mouse.get_pos()
            x, y = pos[0] // constants.one, pos[1] // constants.one
            if y <= 27:
                canvas[y * 28 + x] = 0

        # drawing
        screen.fill(constants.BLACK)
        for i in range(784):
            x, y = i % 28, i // 28
            draw.rect(screen, wab(canvas[i]), Rect(x * constants.one, y * constants.one, constants.one, constants.one))
        draw.line(screen, wab(1), (0, constants.one * 28), (constants.one * 28, constants.one * 28), 1)
        display.update()
        ticks += 1


canvas = [0] * 784
pattern = generate(constants.thickness)

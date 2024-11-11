# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font
from state_machine import *
from ball import Ball
import game_world
import game_framework

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)#meter per min
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)#meter per sec
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)#픽셀 per sec

TIME_PER_ACTION = 0.2 # 다음 액션프레임으로 넘어가는데 걸리는 시간 정의
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5
#A/T * AF/A = AF/T


class Run:
    @staticmethod
    def enter(bird, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            bird.dir, bird.face_dir, bird.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            bird.dir, bird.face_dir, bird.action = -1, -1, 0

    @staticmethod
    def exit(bird, e):
        pass


    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        if bird.x>1500:
            bird.flip = 'h'
            bird.dir = -1
        elif bird.x<25:
            bird.flip = ''
            bird.dir = 1

    @staticmethod
    def draw(bird):
        bird.image.clip_composite_draw(int(bird.frame) * 183, bird.action * 169, 183, 169, 0, bird.flip,bird.x, bird.y,64,64)
        if int(bird.frame) == 4 and bird.action == 1:
            bird.action = 2
        elif int(bird.frame) == 4 and bird.action == 2:
            bird.action = 3
        elif int(bird.frame) == 3 and bird.action == 3:
            bird.action = 1
            bird.frame = 0





class Bird:

    def __init__(self):
        self.font = load_font('ENCR10B.TTF',16)
        self.x, self.y = 400, 300
        self.action = 1
        self.dir = 1
        self.frame = 0
        self.flip = ''
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Run)
        self.state_machine.set_transitions(
            {

            })

    def update(self):
        self.state_machine.update()


    def draw(self):
        self.font.draw(self.x - 60, self.y + 50, f'(Time: {get_time():.2f})',(255,255,0))
        self.state_machine.draw()

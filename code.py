from game import Game
from sprite import Sprite
from hiibot_iots2 import IoTs2
from random import randint
class MyGame(Game):
    def __init__(self):
        super().__init__(rotation=270)
    # override    
    def on_player_collision_with_enemy(self,player,enemy):
        player.life-=1
        enemy.life-=1
    # override
    def on_short_click(self):
        if self.player.vy==0 and game.gameover==False:
            self.player.vy=-5
    # override
    def on_long_click(self):
        self.restart()

game = MyGame()

class Cactus(Sprite):
    def __init__(self):
        super().__init__(img="/imgs/cactus24x50.bmp",x=240,y=76,w=24,h=50,vx=-6,vy=0)
    # override
    def update(self):
        if self.x<=-1*self.w:
            self.life=0
            game.change_score_by(1)
        super().update()

class Mario(Sprite):
    def __init__(self):
        super().__init__(img="/imgs/mario.bmp",x=240,y=78,w=25,h=50,vx=-5,vy=0)
        self.time=0
    # override
    def update(self):
        if self.x<=-1*self.w:
            self.life=0
            game.change_score_by(1)
        self.time+=1
        if self.time % 5==0:
            self.setframe(0)
        if self.time % 10==0:
            self.setframe(1)
        if self.time % 15==0:
            self.setframe(2)
        super().update()

class Player(Sprite):
    def __init__(self):
        super().__init__(img="/imgs/player.bmp",x=0,y=90,w=34,h=40,vx=0,vy=0)
        self.time=0
    # override
    def update(self):
        # jump
        if self.y<=0:
            self.vy=5
        if self.y>90:
            self.vy=0
            self.y=90
        super().update()
        self.time+=1
        if self.time % 10==0:
            self.setframe(0)
        if self.time % 20==0:
            self.setframe(1)
        if self.time % 80==0:
            if randint(1,10)>3:
                game.add_enemy_sprite(Mario())
            else:
                game.add_enemy_sprite(Cactus())

player = Player()
game.set_player_sprite(player)
game.add_gameover_sprite(Sprite(img="/imgs/game_over190x10.bmp",x=30,y=60,w=190,h=10,vx=0,vy=0))
game.start()

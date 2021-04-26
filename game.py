from hiibot_iots2 import IoTs2
import displayio
from time import sleep
import displayio
import adafruit_imageload
iots2 = IoTs2()
screen = iots2.screen
class Game:
    def __init__(self,rotation=0,max_size=8):
        if rotation==0:
            self.width=240
            self.height=135
        if rotation==90:
            self.width=240
            self.height=135
        if rotation==180:
            self.width=240
            self.height=135
        if rotation==270:# button on the left-hand
            self.width=240
            self.height=135
        screen.rotation = rotation
        self.player={}
        self.enemys=[]
        self.foods=[]
        self.bullets=[]
        self.bgs=[]
        self.gameovers=[]
        self.gameover=False
        self.group = displayio.Group(max_size=max_size)
        self.load_score()
    def load_score(self):
        digital_bmp, palette = adafruit_imageload.load("/imgs/digital200x25.bmp",bitmap=displayio.Bitmap,palette=displayio.Palette)
        palette.make_transparent(1)
        palette[0] = 0xffffff
        score = displayio.TileGrid(digital_bmp, pixel_shader=palette,
                                width=3, height=1,
                                tile_width=20, tile_height=25)
        score.x = 176
        score.y = 4
        self.score=score
        self.score_num=0
        self.group.append(score)
    def change_score_by(self,num):
        self.score_num+=num
        self.score[2] = self.score_num % 10
        self.score[1] = (self.score_num // 10) % 10
        self.score[0] = (self.score_num // 100) % 10
    def set_player_sprite(self,sprite):
        self.player=sprite
        self.group.append(sprite.gird)
    def add_bullets_sprite(self,sprite):
        self.bullets.append(sprite)
        self.group.append(sprite.gird)
    def add_foods_sprite(self,sprite):
        self.foods.append(sprite)
        self.group.append(sprite.gird)
    def add_enemy_sprite(self,sprite):
        self.enemys.append(sprite)
        self.group.append(sprite.gird)
    def add_bg_sprite(self,sprite):
        self.bgs.append(sprite)
        self.group.append(sprite.gird)
    def add_gameover_sprite(self,sprite):
        self.gameovers.append(sprite)
        sprite.gird.hidden=True
        self.group.append(sprite.gird)

    def on_player_collision_with_food(self,player,food):
        pass
    def on_player_collision_with_enemy(self,player,enemy):
        pass
    def on_enemy_collision_with_food(self,enemy,food):
        pass
    def on_bullet_collision_with_enemy(self,bullet,enemy):
        pass
    def horizontal_overlap(self,char, obj):
        return char.x + char.w > obj.x and char.x < obj.x + obj.w
    def vertical_overlap(self,char, obj):
        return obj.y + obj.h > char.y and obj.y < char.y + char.h
    def collision(self):
        # player vs enemy
        for enemy in self.enemys:
            if self.horizontal_overlap(self.player, enemy) and self.vertical_overlap(self.player, enemy):
                self.on_player_collision_with_enemy(self.player,enemy)
        
        # player vs food
        for food in self.foods:
            if self.horizontal_overlap(self.player, food) and self.vertical_overlap(self.player, food):
                self.on_player_collision_with_food(self.player,food)
        
        # bullet vs enemy
        for bullet in self.bullets:
            for enemy in self.enemys:
                if self.horizontal_overlap(bullet, enemy) and self.vertical_overlap(bullet, enemy):
                    self.on_bullet_collision_with_enemy(bullet,enemy)
        
        # enemy vs food
        for food in self.foods:
            for enemy in self.enemys:
                if self.horizontal_overlap(enemy,food) and self.vertical_overlap(enemy,food):
                    self.on_enemy_collision_with_food(enemy,food)
    def on_short_click(self):
        pass
    def on_long_click(self):
        pass
    def update(self):
        for enemy in self.enemys:
            enemy.update()
            if enemy.life==0:
                self.group.remove(enemy.gird)
                self.enemys.remove(enemy)
        for food in self.foods:
            food.update()
            if food.life==0:
                self.group.remove(food.gird)
                self.foods.remove(food)
        for bullet in self.bullets:
            bullet.update()
            if bullet.life==0:
                self.group.remove(bullet.gird)
                self.bullets.remove(bullet)
        for bg in self.bgs:
            bg.update()
        self.player.update()
        self.collision()
        if self.player.life==0:
            self.show_gameovers_sprite()
            self.gameover=True
        
    def show_gameovers_sprite(self):
        for x in self.gameovers:
            x.gird.hidden=False
    def hide_gameovers_sprite(self):
        for x in self.gameovers:
            x.gird.hidden=True
    def start(self):
        screen.show(self.group)
        while True:
            sleep(0.02)
            iots2.button_update()
            if iots2.button_wasPressed:
                self.on_short_click()
            if iots2.button_pressedFor(1.0):
                self.on_long_click()
            if self.gameover==False:
                self.update()
    def restart(self):
        print('restart')
        self.score_num=0
        self.player.reset()
        self.hide_gameovers_sprite()
        for x in self.enemys:
            self.group.remove(x.gird)
            self.enemys.remove(x)
        for x in self.foods:
            self.group.remove(x.gird)
            self.foods.remove(x)
        for x in self.bullets:
            self.group.remove(x.gird)
            self.bullets.remove(x)
        self.update()
        sleep(1)
        self.gameover=False

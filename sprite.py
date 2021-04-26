import displayio
import adafruit_imageload
class Sprite:
    def __init__(self,img,x,y,w,h,vx=0,vy=0,life=1):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.vx=vx
        self.vy=vy
        self.life=life
        bmp, palette = adafruit_imageload.load(img,bitmap=displayio.Bitmap,palette=displayio.Palette)
        #palette.make_transparent(1)
        palette[0] = 0x000000
        self.gird = displayio.TileGrid(bmp, pixel_shader=palette,width=1, height=1,tile_width=w, tile_height=h, default_tile=0)
        self.gird.x=x
        self.gird.y=y
        #for reset
        self._x=x
        self._y=y
        self._vx=vx
        self._vy=vy
        self._life=life
    def reset(self):
        self.x=self._x
        self.y=self._y
        self.vx=self._vx
        self.vy=self._vy
        self.life=self._life
    def setframe(self,index):
        self.gird[0, 0]=index
    def update(self):
        self.x+=self.vx
        self.y+=self.vy
        self.gird.x=self.x
        self.gird.y=self.y

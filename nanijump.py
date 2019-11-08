from pygame import *
from random import *
display.init()
display.set_caption("Nani Jump")
window = display.set_mode([700, 200])



def addText(bushDone, caseDone):
    font.init()
    textFont = font.SysFont('arial', 20)
    totalScore = bushDone * 2 + caseDone * 3
    text = 'SCORE:  ' + str(totalScore)
    return textFont.render(text, True, (20, 20, 20))



def getEvent():
    eventList = event.get()
    for eve in eventList:
        if eve.type == QUIT:
            exit()
        if eve.type == KEYDOWN:
            if eve.key == K_SPACE:
                return 'SPACE_down'

class Figure:
    def __init__(self):
        self.imgs = {
            '0': image.load("img/right_0.png"),
            '1': image.load("img/right_1.png"),
            '2': image.load("img/right_2.png"),
            's': image.load("img/right_1s.png"),
            'j': image.load("img/right_1j.png"),
        }
        self.walk = [self.imgs['0'], self.imgs['1'], self.imgs['2'], self.imgs['1']]
        self.stand = [self.imgs['1'], self.imgs['s'], self.imgs['1'], self.imgs['s']]

    def display(self, pos, ori, frame):
        if pos == 2: return transform.flip(self.imgs['j'], not ori, 0)
        if pos:return transform.flip(self.stand[frame], not ori, 0)
        else:return transform.flip(self.walk[frame], not ori, 0)


class Bush:
    def __init__(self, startTime):
        self.surface = image.load("img/bush.png")
        self.startTime = startTime

    def move(self, time, speed):
        self.time = time
        self.x = 800- (self.time - self.startTime) / speed
        return self.x

    def display(self):
        return transform.scale(self.surface, (20, 30))

    def getEdge(self):
        return self.x


class Case:
    def __init__(self, startTime):
        self.surface = image.load("img/case.png")
        self.startTime = startTime

    def move(self, time, speed):
        self.time = time
        self.x = 800 - (self.time - self.startTime) / speed
        return self.x

    def display(self):
        return transform.scale(self.surface, (20, 50))

    def getEdge(self):
        return self.x

def jump(pos):
    if pos == 0:
        return 0
    if pos == 120:
        return 0
    pos += 1
    return pos



bg = transform.scale(image.load("img/bg.png"), (500, 140))
window.fill((240, 240, 240))
end = True
while True:
    if end:
        while True:
            font.init()
            textFont = font.SysFont('arial', 20)
            text = 'PRESS SPACE TO START'
            window.blit(textFont.render(text, False, (20, 20, 20)), (20, 5))
            display.update()
            eve = getEvent()
            if eve == 'SPACE_down' :
                init()
                timeFlag = time.get_ticks()
                girl = Figure()
                speed = 2
                x = 0
                y = 0
                moveleft = 0
                moveright = 0
                frame = 0
                frame2 = 0
                facingRight = 1
                stand = 1
                pos = 0
                end = False
                bush = [Bush(time.get_ticks())]
                case = [Case(time.get_ticks())]
                bushNum = 1
                caseNum = 1
                bushDone = 0
                caseDone = 0
                break
    if time.get_ticks() - timeFlag < 5:
        continue
    frame2 = (frame2+1)%1000
    window.fill((233, 233, 233))
    window.blit(bg, (-200-frame2/2, 0))
    window.blit(bg, (300-frame2/2, 0))
    window.blit(bg, (800 - frame2/2, 0))
    bushRan = randint(1, 10000)
    if bushRan >9980:
        bush.append(Bush(time.get_ticks()))
        bushNum += 1
    caseRan = randint(1, 10000)
    if caseRan >9985:
        if caseNum < 2:
            case.append(Case(time.get_ticks()))
            caseNum += 1

    #window.blit(image.load('img/background.png'), (0,0))
    for i in range(bushNum):
        window.blit(bush[len(bush)-i-1].display(), (bush[len(bush)-i-1].move(time.get_ticks(), 7.0), 150))
        draw.ellipse(window, (220, 220, 220), (bush[len(bush)-i-1].move(time.get_ticks(), 7.0), 178, 25, 7), 0)
        if bush[len(bush)-i-1].getEdge() <= -10: bushNum -= 1; bushDone+=1
        if y > -20 and bush[len(bush)-i-1].getEdge() < x < bush[len(bush)-i-1].getEdge() + 20:
            print("End!")
            end = True


    for i in range(caseNum):
        window.blit(case[len(case)-i-1].display(), (case[len(case)-i-1].move(time.get_ticks(), 4.0), 130))
        draw.ellipse(window, (220, 220, 220), (case[len(case) - i - 1].move(time.get_ticks(), 4.0), 178, 30, 8), 0)
        if case[len(case) - i - 1].getEdge() <= -10: caseNum -= 1; caseDone+=1
        if y > -30 and case[len(case)-i-1].getEdge() < x < case[len(case)-i-1].getEdge() + 10:
            print("End!")
            end = True

    eventList = event.get()
    for eve in eventList:
        if eve.type == QUIT:
            exit()
        if eve.type == KEYDOWN:
            if eve.key == K_RIGHT:
                moveright = 1
            if eve.key == K_LEFT:
                moveleft = 1
            if eve.key == K_SPACE and pos == 0:
                pos = 1
        if eve.type == KEYUP:
            if eve.key == K_RIGHT:
                moveright = 0
            if eve.key == K_LEFT:
                moveleft = 0
    if moveleft and x > 0:
        x -= speed
        facingRight = 0
        stand = 0
    if moveright and x < 650:
        x += speed
        facingRight = 1
        stand = 0
    if moveleft == 0 and moveright == 0:
        stand = 1

    pos = jump(pos)
    if pos:
        stand = 2
        if pos <60:
            y = - pos
        else: y = pos - 120

    frame = (frame+1) % 100
    draw.ellipse(window, (220, 220, 220), (x+6, 178, 35+y/6, 8+y/10), 0)
    window.blit(transform.scale(girl.display(stand, facingRight, int(frame/25)), (50, 80)), (x, 100+y))
    window.blit(addText(bushDone, caseDone),(580,5))

    display.update()
    timeFlag = time.get_ticks()



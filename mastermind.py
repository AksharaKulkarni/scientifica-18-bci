import pygame
import random
import sys
import mindpy
import time

pygame.init()
pygame.font.init()

display_width=1000
display_height=600
clock=pygame.time.Clock()
WHITE=(255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN= (0,255,0)
BLUE=(0,0,255)
guess = 1

global screen

## BACK END
#correct colour wrong or right place
def digitsMatched(anum,gnum):
    m=0
    newGuess = []
    newAnswer = []
    for x,y in zip(gnum,anum):
        if x != y:
            newGuess.append(x)
            newAnswer.append(y)
    for letter in "123":
        for i in range(min(newAnswer.count(letter),newGuess.count(letter))):
            m+=1
    return m
##    m=0
##    for i in gnum:
##            if anum.count(i)>0:
##                m=m+1
##    return m
#correct place correct colour
def find_fully_correct(answer, guess):
    res= 0
    for x, y in  zip(guess, answer):
        if x == y:
            res+=1
    return res 
#create adminno/answer
def create_code():
    characters = '123123123123123'
    length = 3 
    l = list(random.sample(characters,length))
    return l



##FRONT END
validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
class TextBox(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.text = ""
    self.font = pygame.font.Font(None, 25)
    self.image = self.font.render(" ", False, [0, 0, 0])
    self.rect = self.image.get_rect()
  def add_chr(self, char):
    if char in validChars:
        self.text += char
    self.update()
  def update(self):
    old_rect_pos = self.rect.center
    self.image = self.font.render(self.text, False, [0, 0, 0])
    self.rect = self.image.get_rect()
    self.rect.center = old_rect_pos
def textb(cordinate):
    textBox = TextBox()
    textBox.rect.center = cordinate
    running = True
    while running:
      #screen.fill([255, 255, 255])
      screen.blit(textBox.image, textBox.rect)
      pygame.display.flip()
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYUP:
            if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                pass
        if e.type == pygame.KEYDOWN:
            textBox.add_chr(pygame.key.name(e.key))
            if e.key == pygame.K_SPACE:
                textBox.text += " "
                textBox.update()
            if e.key == pygame.K_BACKSPACE:
                textBox.text = textBox.text[:-1]
                textBox.update()
            if e.key == pygame.K_RETURN:
                if len(textBox.text) > 0:
                    #print (textBox.text)
                    running = False
    return textBox.text
def read_test_blinks(c):
    global avg_bs
    screen.fill((240,128,128))
    t4 = endfont.render("Lets try some blinks !!",1,(0,0,0))
    screen.blit(t4,(200,225))
    pygame.display.update()

    blinks = []
    for i in range(5):
       insta = (0,0)
       while insta == (0,0):
           insta = c.recv(30,False)
       if insta[1] == 's':
          blinks.append(int(insta[0]))
       print (blinks)
    avg_bs = int(sum(blinks)/len(blinks))
    t4 = endfont.render("Blink Strength = "+str(avg_bs),1,(0,0,0))
    screen.blit(t4,(200,325))
    t5 = urgefont.render("Now dont blink! Press any key to start",1,(0,0,0))
    screen.blit(t5,(200,425))
    pygame.display.update()

    mastermind_wait()
    screen.fill(BLACK)
def play_screen():
    text1=myfont.render("Enter your Guess: ", 1, (211, 229, 219))
    screen.blit(text1, (275,25))
    t2 = myfont.render("Correct colour",1,(254,0,230))
    screen.blit(t2,(700,100-35))
    t3 = myfont.render("Correct place",1,(254,0,230))
    screen.blit(t3,(600,150-35))
    t4 = myfont.render("Wrong place",1,(254,0,230))
    screen.blit(t4,(800,150-35))
    pygame.draw.line(screen,(255,255,255),(770,100),(770,600),1)
    pygame.draw.line(screen,(255,255,255),(590,100),(940,100),1)
    pygame.draw.line(screen,(255,255,255),(590,60),(590,600),1)
    pygame.draw.line(screen,(255,255,255),(940,60),(940,600),1)
    pygame.draw.line(screen,(255,255,255),(590,60),(940,60),1)
    pygame.draw.line(screen,(255,255,255),(590,150),(940,150),1)

    g1=pygame.draw.circle(screen,WHITE,(300-25,100),30,2)
    g2=pygame.draw.circle(screen,WHITE,(400-25,100),30,2)
    g3=pygame.draw.circle(screen,WHITE,(500-25,100),30,2)
    pygame.display.update()

def input_guess(c):
    global avg_bs
    #insta = textb([700,10])
    insta = 0 
    toreturn = ''
    choosefrom = ['r', 'g', 'b']

    for i in range(3):
       x = 0
       insta = 0 
       while insta != 'd':
           insta = 0
           while insta == 0:
               insta = c.recv(avg_bs,False)[1]
           if insta == 's':
              if choosefrom[x%3] == 'r': col = RED;
              elif choosefrom[x%3] == 'g': col = GREEN;
              elif choosefrom[x%3] == 'b': col = BLUE;
              pygame.draw.circle(screen,col,(300+100*i-25,100),30,0)
              pygame.display.flip()
              x += 1

       if x > 0: x -= 1
       toreturn += choosefrom[x%3]

    for i in range(3):
        pygame.draw.circle(screen,BLACK,(300+100*i-25,100),30,0)
        pygame.draw.circle(screen,WHITE,(300+100*i-25,100),30,2)
    pygame.display.flip()

    print (toreturn)
    return toreturn

def mastermind_wait():
    waiting = True
    pygame.event.clear()
    while waiting:
      e = pygame.event.wait()
      if e.type == pygame.KEYDOWN:
         if e.key == pygame.K_SPACE:
            waiting = False

def output_guess(insta):
    global guess
    done = False
    #guess colours
    textsurface = myfont.render(("Guess #"+str(guess+1)), 1, (255, 255, 255))
    screen.blit(textsurface,(75,180+guess*75))
    colours ={
      "r":RED,
      "g":GREEN,
      "b":BLUE
      }
    col = []
    for letter in insta:
      col.append(colours[letter])
    for g in range(3):  
      op1=pygame.draw.circle(screen,col[g],((g+3)*100-25,185+guess*75),30,0)
    pygame.display.update()
    #clues
    numbers = {
        "r":"1",
        "g":"2",
        "b":"3"
        }
    guesss = []
    for letter in insta:
        guesss.append(numbers[letter])
    print("GUESS",guesss)
    
    match=digitsMatched(answer,guesss)
    print("Correct colour (wrong place  )",match)
    t4 = myfont.render(str(match),1,(255,255,255
                                     ))
    screen.blit(t4,(800,185+guess*75))
    
    count = find_fully_correct(answer,guesss)
    print("Correct colour (right place)   ",count)
    t4 = myfont.render(str(count),1,(255,255,255))
    screen.blit(t4,(600,185+guess*75))
    
    if count == 3:
        game_over_screen("win")
        done = True
    elif guess == 4:
        game_over_screen("lose")
        done = True
    pygame.display.update()
    return done
    

def game_over_screen(result):
    if result =="win":
        screen.fill((240,128,128))
        t4 = endfont.render(" YOU WIN!",1,(0,0,0))
        screen.blit(t4,(275,225))
        print("GAME OVER")
    elif result == "lose":
        screen.fill((240,128,128))
        t4 = endfont.render(" YOU LOSE!",1,(0,0,0))
        screen.blit(t4,(275,225))
        t5 = urgefont.render("Thanks for trying!",1,(0,0,0))
        screen.blit(t5,(300,325))
        print("GAME OVER")
        
    pass


    
def main():
    global myfont, screen, guess, endfont, urgefont
    global answer

    client = mindpy.Client()

    pygame.init()

    answer = create_code()
    print("ANSWER",answer)

    screen= pygame.display.set_mode((display_width,display_height))

    myfont=pygame.font.SysFont("Times New Roman", 25)
    urgefont=pygame.font.SysFont("Times New Roman", 50)
    endfont=pygame.font.SysFont("Times New Roman", 75)
    pygame.display.set_caption('MASTERMIND')

    read_test_blinks(client)
    play_screen()

    for guess in range(5):
        insta = input_guess(client)
        pygame.display.flip()
        done = output_guess(insta)
        if done: break
        #mastermind_wait()
        
    done = False
    while not done:
       # --- Event Processing
       for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()

main()

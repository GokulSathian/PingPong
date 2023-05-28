import pygame
pygame.init()   #Need to initialize

WIDTH,HEIGHT = 700,500  #in caps to show the constants
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PingPong")

FPS=60

WHITE =(255,255,255)
BLACK =(0,0,0)

PADDLE_WIDTH,PADDLE_HEIGHT = 20,100
BALL_RADIUS =7

SCORE_FONT= pygame.font.SysFont("comicsans",50 )

class Paddle:
    COLOR =WHITE
    VELOCITY = 4  #Number of pixels moving in Y direction that is height
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
    
    def draw(self,win): # Drawing rectangle
        pygame.draw.rect(win,self.COLOR,(self.x,self.y,self.width,self.height))

    def move(self,up):
        self.up=up
        if self.up and self.y+self.VELOCITY>=0: #it runs only one time as its not in active main loop
            self.y-=self.VELOCITY
        else:
            self.y+=self.VELOCITY

class Ball:
    COLOR = WHITE
    MAX_VEL=5

    def __init__(self,x,y,radius):
        self.x=self.original_x=x #Keeps the initial value in instance variable original
        self.y=self.original_y=y
        self.radius=radius
        self.x_vel=self.MAX_VEL
        self.y_vel=0
    
    def draw(self,win):
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.radius)
    
    def move(self):
        self.x+=self.x_vel
        self.y+=self.y_vel
    
    def reset(self):
        self.x=self.original_x
        self.y=self.original_y
        self.y_vel=0
        self.x_vel*=-1

def draw(win,paddles,left_score,right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}",1,WHITE)#Whatever drawn first will be on top so that ball can pass over it 
    right_score_text = SCORE_FONT.render(f"{right_score}",1,WHITE)#Always Anti ALiasing 1
    win.blit(left_score_text,(WIDTH//4-left_score_text.get_width()//2,20))
    win.blit(right_score_text,(WIDTH*3//4-right_score_text.get_width()//2,20))

    for paddle in paddles:
        paddle.draw(win) #Calling method draw
    

    
    for i in range(10,HEIGHT,HEIGHT//20): #Height//20 so that the height divided equally and loop runs that much time
        if i%2 ==1: #Alternatively doesn't draws rectangle
            continue
        pygame.draw.rect(win,WHITE,(WIDTH//2,i,5,HEIGHT//20))
    pygame.display.update() # Should mannually update the display takes time so do it only minimal amount of time

def movements(keys,left_paddle,right_paddle):
    if keys[pygame.K_w]:    #All letter keys are small letter
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y+left_paddle.height+left_paddle.VELOCITY <=HEIGHT: #Y always referenced from top to bottom
        left_paddle.move(up=False)
    if keys[pygame.K_UP]:   #All functional keys are caps
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y+right_paddle.height+right_paddle.VELOCITY <=HEIGHT:
        right_paddle.move(up=False)

def collision(ball,left_paddle,right_paddle):
    if ball.y-ball.radius<=0:  #Collision with ceilings
        ball.y_vel*=-1    #reversing the ball direction
    elif ball.y+ball.radius>=HEIGHT:
        ball.y_vel*=-1

    if ball.x_vel<0:
        if ball.y <=left_paddle.y+left_paddle.height and  ball.y>=left_paddle.y: #y of ball within y of paddle 
            if ball.x-ball.radius<=left_paddle.x+left_paddle.width:  
                ball.x_vel*=-1  
                middle_y = left_paddle.y+left_paddle.height/2
                diff=ball.y-middle_y
                reduction_factor=(left_paddle.height/2)/ball.MAX_VEL
                ball.y_vel= diff/reduction_factor
    else:
        if ball.y <=right_paddle.y+right_paddle.height and  ball.y>=right_paddle.y:
            if ball.x+ball.radius >= right_paddle.x:
                ball.x_vel*=-1
                middle_y = right_paddle.y+right_paddle.height/2
                diff=middle_y-ball.y
                reduction_factor=(right_paddle.height//2)/ball.MAX_VEL
                ball.y_vel= diff/reduction_factor

def main(): 
    run = True
    clock =pygame.time.Clock()
    left_score,right_score=0,0
    #Creating Objects        
    Left_Paddle=Paddle(10,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)  #x axis from left to right only Always referencing top left
    Right_Paddle=Paddle(WIDTH-PADDLE_WIDTH-10,HEIGHT//2-PADDLE_HEIGHT//2,PADDLE_WIDTH,PADDLE_HEIGHT)   
#    dot1=Paddle(10,450,5,5)
    ball =Ball(WIDTH//2,HEIGHT//2,BALL_RADIUS)
    while run:
        clock.tick(FPS) #to make sure the frames per second stay constant in every computer that is run loop runs 60/sec
        
        draw(WIN,[Left_Paddle,Right_Paddle,ball],left_score,right_score)
        for event in pygame.event.get():  #to get all the events clicking,moving ,closing etc
            if event.type == pygame.QUIT:  #Check if we hit right top close button
                run=False
                break
        keys =pygame.key.get_pressed()   #to get the keys that are pressed
        movements(keys,Left_Paddle,Right_Paddle)
        
        ball.move()
        collision(ball,Left_Paddle,Right_Paddle)

        if ball.x<0:
            right_score+=1
            ball.reset()
        elif ball.x>WIDTH:
            left_score+=1
            ball.reset()

    pygame.quit() # to quit the program


if __name__== '__main__':
    main()
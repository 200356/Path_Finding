from tkinter import *
import tkinter.messagebox
import pygame
import sys

root = tkinter.Tk()
root.geometry('0x0')

window_width=500
window_height=500

window=pygame.display.set_mode((window_width,window_height))
columns=25
rows=25

box_width=window_width //columns
box_height=window_height // rows

grid=[]
queue=[]
path=[]

class Box:
    def __init__(self,i,j):
        self.x=i
        self.y=j
        self.start=False
        self.target=False
        self.wall = False
        self.queued=False
        self.visited=False
        self.neighbours=[]
        self.prior=None

    #Method to draw each box
    def draw(self,win,color):
        pygame.draw.rect(win,color,(self.x * box_width, self.y * box_height,box_width-2,box_height-2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x-1][self.y])
        if self.x < columns-1:
            self.neighbours.append(grid[self.x+1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y-1])
        if self.y < rows-1:
            self.neighbours.append(grid[self.x][self.y+1])

#Creating the grid
for i in range(columns):
    arr=[]
    for j in range(rows):
        arr.append(Box(i,j))
    grid.append(arr)

for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

start_box=grid[0][0]
start_box.start=True
start_box.visited=True
queue.append(start_box)



def main():
 begin_search=False
 target_box_set=False
 searching=True
 target_box=None

 while True:
     # Quitting the game
     for event in pygame.event.get() :
         if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
         elif event.type == pygame.MOUSEMOTION:
             x=pygame.mouse.get_pos()[0]
             y=pygame.mouse.get_pos()[1]
             #draw wall
             if event.buttons[0]:
                 i=x//box_width
                 j=y//box_height
                 grid[i][j].wall = True

             # set target
             if event.buttons[2] and target_box_set==False:
                 i=x//box_width
                 j=y//box_height
                 target_box=grid[i][j]
                 grid[i][j].target = True
                 target_box_set = True

         # Start Algorithm Keydown on keyboard
         if event.type == pygame.KEYDOWN and target_box_set:
             begin_search=True

     if begin_search:
         if len(queue)>0 and searching:
             current_box=queue.pop(0)
             current_box.visited=True
             if current_box==target_box:
                 searching=False
                 while current_box.prior != start_box:
                     path.append(current_box.prior)
                     current_box = current_box.prior
             else:
                 for neighbour in current_box.neighbours:
                     if not neighbour.queued and not neighbour.wall and not neighbour.visited:
                         neighbour.queued=True
                         neighbour.prior = current_box
                         queue.append(neighbour)
         else:
             if searching:
                 tkinter.messagebox.showinfo("Attention!", "No path is possible")
                 searching=False

     window.fill((0,0,0)) #fills screen with black


     for i in range(columns):
         for j in range(rows):
             box=grid[i][j]
             box.draw(window,(50,50,50))
             if box.queued:
                 box.draw(window,(200,0,0))
             if box.visited:
                 box.draw(window,(0,200,0))
             if box in path:
                 box.draw(window,(0,0,200))
             if box.start:
                 box.draw(window,(0,200,200))
             if box.wall:
                 box.draw(window,(90,90,90))
             if box.target:
                 box.draw(window,(200,200,0))

     pygame.display.flip() #updates the display

main()




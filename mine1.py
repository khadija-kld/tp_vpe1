import pygame
from cube import Cube
from text import Texture
import random

class MainGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.texture = Texture('grass_carried.png')
        #self.texture2 = Texture('grass_path_side.png')
        self.camera_vertical_position = 400 
        self.jump_sound = pygame.mixer.Sound('cartoon-penguin.wav')
        self.creat_sound = pygame.mixer.Sound('ihitokage__block.ogg')

        self.cubes = [
            Cube(position=(0, 0, 0), texture=self.texture),    
            Cube(position=(2, 0, 0), texture=self.texture),    
            
            Cube(position=(4, 0, 0), texture=self.texture),
            Cube(position=(6, 0, 0), texture=self.texture),
            Cube(position=(-2, 0, 0), texture=self.texture),   
            Cube(position=(0, 0, 2), texture=self.texture), 
            Cube(position=(0, 0, 4), texture=self.texture),   
            #Cube(position=(0, 2, 2), texture=self.texture),
            Cube(position=(0, 0, -2), texture=self.texture),   
            Cube(position=(2, 0, 2), texture=self.texture),    
            Cube(position=(-2, 0, 2), texture=self.texture),   
            Cube(position=(2, 0, -2), texture=self.texture),   
            Cube(position=(-2, 0, -2), texture=self.texture), 
            #sCube(position=(0, 2, 0), texture=self.texture),    
            #Cube(position=(2, 4, 0), texture=self.texture),    
        
            ]

        
        self.running = True
        self.clock = pygame.time.Clock() 
        

    def add_block(self):
         
        x = random.randint(0, 5)  
        z = random.randint(-5, 5)

       
        new_cube = Cube(position=(x, 0, z), texture=self.texture)
        self.cubes.append(new_cube)
        self.creat_sound.play()
        print(f"Nouveau cube ajouté a la position {x, 0, z}")

    def run(self):
        jumping = False
        jump_height = 70  
        jump_speed = 40  
        current_jump_position = 0  
        ground = -2  
        zoom_limit = -5 
        max_cube_y = max(cube.position[1] for cube in self.cubes)  #valeur max de y


        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
            
                    if event.key == pygame.K_SPACE:
                        
                        if self.cubes[0].zoom < 2 :
                            self.camera_vertical_position += 860
                            self.jump_sound.play()
            
                            ground += 2
                            if ground > max_cube_y or self.cubes[0].zoom < zoom_limit:
                                self.camera_vertical_position = 400
                                ground = -2
                                
                                #self.cubes[0].zoom = 5
                        elif not jumping: 
                            jumping = True
                            self.jump_sound.play()

                if event.type == pygame.MOUSEBUTTONDOWN: 
                        self.add_block()            
            if jumping:
                
                if current_jump_position < jump_height:
                    self.camera_vertical_position += jump_speed
                    current_jump_position += jump_speed
                elif current_jump_position >= jump_height and current_jump_position < 2 * jump_height:
                    # Descendre
                    self.camera_vertical_position -= jump_speed
                    current_jump_position += jump_speed
                else:
                    
                    jumping = False
                    current_jump_position = 0


            self.screen.fill((135, 206, 235))  
            
            
            for cube in self.cubes:
                cube.v0 = self.camera_vertical_position  
                cube.update(events)
                cube.draw(self.screen)
                
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    game = MainGame()
    game.run()


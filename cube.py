import pygame
import math
import numpy as np

class Cube:
    def __init__(self, position, texture):
        self.position = position
        self.texture = texture
        self.f = 900
        self.alpha = 1
        self.beta = 1
        self.u0, self.v0 = 400, 400
        self.angle_x, self.angle_y = 0, 0
        self.deplacement_x = 0
        self.vitesse_deplacement = 1.5
        self.rotation_speed = 0.2   
        self.zoom = 5 
        self.zoom_speed = 2.5 
        #self.walking_sound = pygame.mixer.Sound('step-on-dirt.wav') 

        self.cube_3d = [
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1)
        ]

        self.faces = [
            [1, 2, 6, 5],
 
            [4, 5, 6, 7],  
            [0, 1, 5, 4],  
            [2, 3, 7, 6],  
            [0, 3, 7, 4],  
            [0, 1, 2, 3],  
        ]

        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

    def project_3d_to_2d(self, x, y, z):
        
        u = self.u0 + (self.alpha * self.f * x / z)
        v = self.v0 + (self.beta * self.f * y / z)  
        return u, v
    
    def rotation_matrix_x(self, angle):
        return np.array([
            [1, 0, 0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)]
        ])

    def rotation_matrix_y(self, angle):
        return np.array([
            [math.cos(angle), 0, math.sin(angle)],
            [0, 1, 0],
            [-math.sin(angle), 0, math.cos(angle)]
        ])

    def update(self, events):
        

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: 
                    self.deplacement_x += self.vitesse_deplacement
        
                elif event.key == pygame.K_RIGHT:
                    self.deplacement_x -= self.vitesse_deplacement                    
                    
                elif event.key == pygame.K_UP:
                    self.zoom -= self.zoom_speed
                
                    
                elif event.key == pygame.K_w:    
                    self.angle_x -= self.rotation_speed
                elif event.key == pygame.K_DOWN:
                    self.zoom += self.zoom_speed
                    
                elif event.key == pygame.K_x:
                    self.angle_x += self.rotation_speed
                elif event.key == pygame.K_a:  
                    self.angle_y -= self.rotation_speed
                elif event.key == pygame.K_d:  
                    self.angle_y += self.rotation_speed

    def draw(self, screen):
        if self.zoom < 0 or self.zoom >30 :
            return
        
        cube_2d = []
        for point in self.cube_3d:
            
            point = np.add(point, self.position)
            point_deplace = np.array(point) + np.array([self.deplacement_x, 0, 0])
            rotated_point = np.dot(self.rotation_matrix_x(self.angle_x), point_deplace)
            rotated_point = np.dot(self.rotation_matrix_y(self.angle_y), rotated_point)
            rotated_point[-1] += 5  
            rotated_point[-1] += self.zoom
            u, v = self.project_3d_to_2d(*rotated_point)
            cube_2d.append((u, v))

        for face in self.faces:
            face_points_2d = []
            for vertex in face:
                face_points_2d.append(cube_2d[vertex])
            self.texture.map_texture_to_face(screen, face_points_2d)


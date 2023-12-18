import pygame as pg
import numpy as np


def interpolate(p1, p2, t):
    return p1[0] * (1 - t) + p2[0] * t, p1[1] * (1 - t) + p2[1] * t

def subdivide_face(corners, divisions=8):
    subdivided = []
    for i in range(divisions):
        for j in range(divisions):
            
            frac_i = i / divisions
            frac_j = j / divisions
            frac_i_plus_1 = (i + 1) / divisions
            frac_j_plus_1 = (j + 1) / divisions
            
            top_left = interpolate(interpolate(corners[0], corners[1], frac_i),
                                   interpolate(corners[3], corners[2], frac_i),
                                   frac_j)
            top_right = interpolate(interpolate(corners[0], corners[1], frac_i_plus_1),
                                    interpolate(corners[3], corners[2], frac_i_plus_1),
                                    frac_j)
            bottom_left = interpolate(interpolate(corners[0], corners[1], frac_i),
                                      interpolate(corners[3], corners[2], frac_i),
                                      frac_j_plus_1)
            bottom_right = interpolate(interpolate(corners[0], corners[1], frac_i_plus_1),
                                       interpolate(corners[3], corners[2], frac_i_plus_1),
                                       frac_j_plus_1)
            
            subdivided.append([top_left, top_right, bottom_right, bottom_left])
    return subdivided

class Texture:
    def __init__(self, filepath):
        self.texture_image = pg.image.load(filepath)
        self.texture_size = 8
        self.texture_data = pg.surfarray.array3d(self.texture_image)

    def map_texture_to_face(self, screen, face_points_2d):
        blocks = subdivide_face(face_points_2d, self.texture_size)
        for block in blocks:
            x, y = int(block[0][0]), int(block[0][1])
            color = self.texture_data[x % self.texture_image.get_width(), 
                                      y % self.texture_image.get_height()]
            pg.draw.polygon(screen, color, block)

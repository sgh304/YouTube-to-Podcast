import pygame

def get_smallest_rect(rects):
    '''Gets the smallest rect that contains all passed in rects'''
    left = min([rect.left for rect in rects])
    top = min([rect.top for rect in rects])
    right = max([rect.right for rect in rects])
    bottom = max([rect.bottom for rect in rects])
    return pygame.Rect(left, top, right - left, bottom - top)
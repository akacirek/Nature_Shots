import sys
import pygame
import csv
import json

# Fuction
def process_coordinates(file_name = "via_project_7Apr2024_7h56m_csv (3).csv", file_loaded = "Nature_Shots_Level_1.png"):
    entities=[]
    with open(file_name, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            region_shape_attributes = row['region_shape_attributes']
            if row['filename'] == file_loaded:
                region_shape_attributes=json.loads(region_shape_attributes)
                x_points = region_shape_attributes['all_points_x']
                y_points = region_shape_attributes['all_points_y']
                final_tuple=[]
                for coordinate in range(len(x_points)):
                    coordinate_tuple = (x_points[coordinate],y_points[coordinate])
                    final_tuple.append(coordinate_tuple)
                entities.append(tuple(final_tuple))
    return entities
level_1_coordinates = process_coordinates("via_project_16Apr2024_18h3m_csv (1).csv")
level_2_coordinates = process_coordinates("via_project_25Apr2024_17h1m_csv (4).csv", "Nature_Shots_Level_2.png")
level_3_coordinates = process_coordinates("via_project_25Apr2024_17h1m_csv (4).csv", "Nature_Shots_Level_3.png")
level_4_coordinates = process_coordinates("via_project_25Apr2024_17h1m_csv (4).csv", "Nature_Shots_Level_4.png")


# Initialize Pygame
pygame.init()
image_path = 'Nature_Shots_Level_1.png'
loaded_image = pygame.image.load(image_path)

def draw_polygon_alpha(surface, color, points):
    lx, ly = zip(*points)
    min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)

    polygon=pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points],1)

    surface.blit(shape_surf, target_rect)
    return polygon

# Set up the display window
window_size = (756, 756)
window_surface = pygame.display.set_mode(window_size)
pygame.display.set_caption("Move Object")
my_surface = pygame.Surface((756, 756))
rect_x1, rect_y1 = 347, 114
rect_width1, rect_height1 = 91, 209

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create a rectangle (our movable object)
rect_width, rect_height = 100, 50
rect_x, rect_y = 200, 150
rect_speed = 5

used = []

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the keys pressed
    keys = pygame.key.get_pressed()

    # Update the position based on arrow keys
    if keys[pygame.K_LEFT]:
        rect_x -= rect_speed
    if keys[pygame.K_RIGHT]:
        rect_x += rect_speed
    if keys[pygame.K_UP]:
        rect_y -= rect_speed
    if keys[pygame.K_DOWN]:
        rect_y += rect_speed

    window_surface.blit(loaded_image,(0, 0))  # Adjust the position as needed
    
    index = 0
    rect1=pygame.draw.rect(window_surface, BLACK, (rect_x, rect_y, rect_width, rect_height),1)
    for coordinates in level_1_coordinates:
        tree1=draw_polygon_alpha(window_surface, (255, 255, 0, 127), coordinates)
        index += 1
        print(index)
        if rect1.colliderect(tree1):
            if index in used:
                print("Already seen")
                print(used)
                print(index)
            else:
                used.append(index)
                print("Added")
                print(used)
                print(index)
            
    # Update the display
    pygame.display.update()
#https://www.robots.ox.ac.uk/~vgg/software/via/via_demo.html
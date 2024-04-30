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
    return target_rect

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
scoring = 0
clock = pygame.time.Clock()
scoring_dict = {'tree':[0,1,2,3,4,5,6],"rock":[7,8,9],'fish':[10,11,12,13],"cave":[14]}
font = pygame.font.Font(None, 36)

# Main game loop
while True:
    clock.tick(60)
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
    score_text = font.render(f'Score: {scoring}', True, (255, 255, 255))
    window_surface.blit(score_text, (10, 10))
    
    index = 0
    rect1=pygame.draw.rect(window_surface, BLACK, (rect_x, rect_y, rect_width, rect_height),1)
    all_polygons = []
    for coordinates in level_1_coordinates:
        tree1=draw_polygon_alpha(window_surface, (255, 255, 0, 127), coordinates)
        all_polygons.append(tree1)
    pygame.display.update()
    for polygon in all_polygons:
        collide = pygame.Rect.colliderect(rect1, polygon)
        if collide:
            for key, value in scoring_dict.items():

        #if rect1.colliderect(polygon):
                if index in used:
                    print("Already seen")
                    print(index)
                else:
                    used.append(index)
                    if index in value:
                        if key == "tree":
                            scoring += 1
                        if key == "rock":
                            scoring += 2
                        if key == "fish":
                            scoring += 3
                        if key == "cave":
                            scoring += 5
                    print("Added")
                    print(index)
        index += 1
            
    # Update the display
    pygame.display.update()
#https://www.robots.ox.ac.uk/~vgg/software/via/via_demo.html
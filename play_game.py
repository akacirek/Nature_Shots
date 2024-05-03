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
lvl_1_background = "Nature_Shots_Level_1.png"
lvl_2_background = "Nature_Shots_Level_2.png"
lvl_3_background = "Nature_Shots_Level_3.png"
lvl_4_background = "Nature_Shots_Level_4.png"
lvl_5_background = "Nature_Shots_Level_5.png"



# Initialize Pygame
pygame.init()

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

lvl_coordinates = level_1_coordinates
used = []
scoring = 0
lvl = 1
clock = pygame.time.Clock()
lvl_1_scoring_dict = {'tree':[0,1,2,3,4,5,6],"rock":[7,8,9],'fish':[10,11,12,13],"cave":[14]}
lvl_2_scoring_dict = {'parrot':[0,1,2,3,4],'palm_tree':[5,6,7],'turtle':[8]}
lvl_3_scoring_dict = {'seaweed':[0,1,2,3,4,5,6],'seashells':[7,8],'seahorse':[9,10],'fish':[11,12],'crab':[13],'octopus':[14],'starfish':[15]}
lvl_4_scoring_dict = {'pine_tree':[0,1,2,3,4,5],'log':[6,7,8],'igloo':[9]}
font = pygame.font.Font(None, 36)

# Main game loop
while True:
    if lvl == 1:
        lvl_background = lvl_1_background
        lvl_scoring_dict = lvl_1_scoring_dict
    if scoring >= 7 and lvl == 1:
        scoring = 0
        lvl = 2
        used = []
        lvl_background = lvl_2_background
        lvl_scoring_dict = lvl_2_scoring_dict
        lvl_coordinates = level_2_coordinates
    if scoring >= 7 and lvl == 2:
        scoring = 0
        lvl = 3
        used = []
        lvl_background = lvl_3_background
        lvl_scoring_dict = lvl_3_scoring_dict
        lvl_coordinates = level_3_coordinates
    if scoring >= 7 and lvl == 3:
        scoring = 0
        lvl = 4
        used = []
        lvl_background = lvl_4_background
        lvl_scoring_dict = lvl_4_scoring_dict
        lvl_coordinates = level_4_coordinates
    if scoring >= 7 and lvl == 4:
        lvl = 5
        lvl_background = lvl_5_background
        lvl_coordinates = []
    image_path = lvl_background
    loaded_image = pygame.image.load(image_path)
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
    score_text = font.render(f'Score: {scoring}', True, (128, 128, 128))
    window_surface.blit(score_text, (10, 10))
    
    index = 0
    rect1=pygame.draw.rect(window_surface, BLACK, (rect_x, rect_y, rect_width, rect_height),1)
    all_polygons = []
    for coordinates in lvl_coordinates:
        tree1=draw_polygon_alpha(window_surface, (255, 255, 0, 127), coordinates)
        all_polygons.append(tree1)
    pygame.display.update()
    for polygon in all_polygons:
        collide = pygame.Rect.colliderect(rect1, polygon)
        if collide:
            for key, value in lvl_scoring_dict.items():

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
                        if key == 'parrot':
                            scoring += 2
                        if key == 'palm_tree':
                            scoring += 3
                        if key == 'turtle':
                            scoring += 5
                        if key == 'seaweed':
                            scoring += 2
                        if key == 'seashell':
                            scoring += 2
                        if key == 'seahorse':
                            scoring += 2
                        if key == 'fish':
                            scoring += 2
                        if key == 'crab':
                            scoring += 3
                        if key == 'octopus':
                            scoring += 5
                        if key == 'starfish':
                            scoring += 3
                        if key == 'pine_tree':
                            scoring += 2
                        if key == 'log':
                            scoring += 3
                        if key == 'igloo':
                            scoring += 5
                    print("Added")
                    print(index)
        index += 1
            
    # Update the display
    pygame.display.update()
#https://www.robots.ox.ac.uk/~vgg/software/via/via_demo.html
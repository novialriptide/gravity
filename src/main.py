##############################################
# GRAVITY, DEVELOPED BY GITHUB.COM/ANBDREW   #
BUILD_VERSION = 1
##############################################
import os

os.system("pip install -r requirements.txt")
import sys
import json

import assets.gamedenRE as gamedenRE

import pygame
import pymunk

from pathlib import Path

MAIN_DIRECTORY_PATH = f"{os.getcwd()}/assets/"

# rendering constants
SCREEN_SIZE = (500, 500)
RENDER_SIZE = 10

# image constants
NOISE_TEXTURE_IMAGE_PATH = MAIN_DIRECTORY_PATH + "textures/parallax/noise.png"
NOISE_TEXTURE_IMAGE = pygame.image.load(NOISE_TEXTURE_IMAGE_PATH)
NOISE_TEXTURE_IMAGE.set_alpha(40)

LOGO_IMAGE_PATH = MAIN_DIRECTORY_PATH + "textures/logos/logo_trans.png"
LOGO_IMAGE = pygame.image.load(LOGO_IMAGE_PATH)

# tile constants
UNTOUCHABLE_TILE_ID = 2
GOAL_TILE_ID = 3
START_TILE_ID = 4

# vars
OFFICIAL_LEVELS = os.listdir(MAIN_DIRECTORY_PATH + "levels")
OFFICIAL_LEVELS.remove("title.json")
attempt_number = 0
camera_movement = True

title_screen = True
level_selector = False
game_over = False
game_won = False
display_console = False
display_hud = False

DEFAULT_FONT = MAIN_DIRECTORY_PATH + "textures/pixel.ttf"

# pygame setup
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("GRAVITY: BETA")
pygame.display.set_icon(LOGO_IMAGE)
dt = 1

# camera
camera_pos = [0, 0]
camera_lag_speed = 20

# parallax objects
front_objects = [
    {
        "image": NOISE_TEXTURE_IMAGE,
        "rect": NOISE_TEXTURE_IMAGE.get_rect(),
        "scroll_speed": 0.25,
        "position": [0, 0],
    }
]
back_objects = []

# pymunk setup
space = pymunk.Space()

# player entity setup
player_pos = None
player = None


def load_player_entity():
    global player_pos
    global player

    player_pos = 0, 0
    body = pymunk.Body(10, 1666)
    body.position = player_pos
    player = gamedenRE.entity(body, [5 * RENDER_SIZE, 5 * RENDER_SIZE])
    player.poly.friction = 1
    player.poly.elasticity = 0
    space.add(player.body, player.poly)


load_player_entity()

# tile map setup
default_tileset = gamedenRE.tileset(
    MAIN_DIRECTORY_PATH + "textures/tilesets/1.png", (10, 10)
)
map_pos = [0, 0]
loaded_tileset = None
loaded_tilemap = None
loaded_tilemap_image = None
loaded_tilemap_file_name = None


def execute_data_points(tilemap: gamedenRE.tilemap, layer: int):
    """currently just marks the spawn point"""
    global player_pos
    m_width, m_height = tilemap.map_size
    t_width, t_height = tilemap.tile_size
    for row in range(m_height):
        for column in range(m_width):
            tile_id = tilemap.map_data["contents"][layer][row][column]

            # sets the player's spawn position
            if tile_id == 1:
                player.body.position = (
                    t_width * column * RENDER_SIZE + (t_width * RENDER_SIZE) / 2,
                    t_height * row * RENDER_SIZE + (t_height * RENDER_SIZE) / 2,
                )


def load_tilemap(tileset: gamedenRE.tileset, tilemap_path: str):
    global loaded_tileset
    global loaded_tilemap
    global loaded_tilemap_image
    global loaded_tilemap_file_name

    loaded_tileset = tileset
    loaded_tilemap = gamedenRE.convert_tiledjson(tilemap_path)
    loaded_tilemap["invisible_layers"] = [0]
    loaded_tilemap = gamedenRE.tilemap(loaded_tilemap, loaded_tileset)
    loaded_tilemap_image = loaded_tilemap.get_image_map()
    loaded_tilemap_file_name = tilemap_path.replace(
        MAIN_DIRECTORY_PATH + "levels/", ""
    ).replace(".json", "")
    t_w, t_h = (
        loaded_tilemap_image.get_rect().width,
        loaded_tilemap_image.get_rect().height,
    )
    loaded_tilemap_image = pygame.transform.scale(
        loaded_tilemap_image, (int(t_w * RENDER_SIZE), int(t_h * RENDER_SIZE))
    )
    execute_data_points(loaded_tilemap, 0)


# gravity settings
gravity_speed = 5000
space.gravity = 0, 0

# collisions
def coll_post(arbiter, space, data):
    for shape in arbiter.shapes:
        try:

            def two():
                global game_over
                game_over = True

            def three():
                global game_won
                game_won = True

            def test_tile_id(argument):
                switcher = {2: two, 3: three}
                func = switcher.get(argument, lambda: "invalid tile id")
                func()

            test_tile_id(shape.gameden["tile_id"])
        except AttributeError:
            pass
    return True


collision_handler = space.add_default_collision_handler()
collision_handler.post_solve = coll_post

# game functions
polys = None


def load_tilemap_collisions():
    global polys
    polys = gamedenRE.add_rects_to_space(
        space, loaded_tilemap.get_collision_rects((0, 0), 1, render_size=RENDER_SIZE)
    )


def unload_tilemap_collisions():
    for body in space.bodies:
        space.remove(body)

    for shape in space.shapes:
        space.remove(shape)


def game_reset():
    space.gravity = 0, 0
    player.body.velocity = 0, 0
    execute_data_points(loaded_tilemap, 0)


def camera_focus_on_goal(layer: int):
    global camera_pos
    m_width, m_height = loaded_tilemap.map_size
    t_width, t_height = loaded_tilemap.tile_size
    for row in range(m_height):
        for column in range(m_width):
            tile_id = loaded_tilemap.map_data["contents"][layer][row][column]

            # sets the player's spawn position
            if tile_id == 3:
                camera_pos = [
                    t_width * column * RENDER_SIZE + (t_width * RENDER_SIZE) / 2,
                    t_height * row * RENDER_SIZE + (t_height * RENDER_SIZE) / 2,
                ]


# main game
load_tilemap(default_tileset, MAIN_DIRECTORY_PATH + "levels/title.json")
load_tilemap_collisions()
logo_resized = pygame.transform.scale(
    LOGO_IMAGE,
    (
        int(LOGO_IMAGE.get_rect().width * RENDER_SIZE * 1 / 25),
        int(LOGO_IMAGE.get_rect().height * RENDER_SIZE * 1 / 25),
    ),
)
while True:
    if clock.get_fps() != 0:
        dt = clock.get_fps() / 1000
    else:
        dt = 0

    left_mouse_click_up = False
    right_mouse_click = False
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            SCREEN_SIZE = event.w, event.h
            screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            # changing gravity keys
            if event.key == pygame.K_s:
                space.gravity = 0, dt * gravity_speed
            if event.key == pygame.K_w:
                space.gravity = 0, dt * -gravity_speed
            if event.key == pygame.K_a:
                space.gravity = dt * -gravity_speed, 0
            if event.key == pygame.K_d:
                space.gravity = dt * gravity_speed, 0

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                left_mouse_click_up = True

    # camera movements
    if camera_movement:
        _m = int(SCREEN_SIZE[0] / 2)
        camera_pos[0] += (
            player.body.position[0] - camera_pos[0] - _m
        ) / camera_lag_speed
        _m = int(SCREEN_SIZE[1] / 2)
        camera_pos[1] += (
            player.body.position[1] - camera_pos[1] - _m
        ) / camera_lag_speed

    # map + background
    screen.fill((115, 115, 115))
    screen.blit(
        loaded_tilemap_image,
        (map_pos[0] - int(camera_pos[0]), map_pos[1] - int(camera_pos[1])),
    )

    # draw main object
    x, y = player.body.position
    local_vertices = player.poly.get_vertices()
    player_vertices = []
    for vertice in local_vertices:
        vx, vy = vertice
        player_vertices.append(
            [vx + x - int(camera_pos[0]), vy + y - int(camera_pos[1])]
        )
    pygame.draw.polygon(screen, (61, 143, 166), player_vertices)

    if title_screen:
        # buttons
        game_credits = gamedenRE.text2(
            f"developed by github.com/anbdrew",
            1.5 * RENDER_SIZE,
            DEFAULT_FONT,
            (0, 0, 0),
        )
        button_text = gamedenRE.text2(
            "click on me to start!", 2 * RENDER_SIZE, DEFAULT_FONT, (0, 0, 0)
        )
        b_rect = button_text.get_rect()
        b_x, b_y = (
            SCREEN_SIZE[0] / 2 - b_rect.width / 2,
            SCREEN_SIZE[1] * 3 / 5 - b_rect.height / 2,
        )
        start_button = gamedenRE.button(
            pygame.Rect(b_x, b_y, b_rect.width, b_rect.height)
        )

        t_x, t_y = (
            SCREEN_SIZE[0] / 2 - logo_resized.get_rect().width / 2,
            SCREEN_SIZE[1] * 2 / 5 - logo_resized.get_rect().height / 2,
        )
        c_x, c_y = (
            SCREEN_SIZE[0] / 2 - game_credits.get_rect().width / 2,
            SCREEN_SIZE[1] * 2.6 / 5 - game_credits.get_rect().height / 2,
        )
        screen.blit(logo_resized, (t_x, t_y))
        screen.blit(button_text, (b_x, b_y))
        screen.blit(game_credits, (c_x, c_y))

        if start_button.is_hovering(mouse_pos) and left_mouse_click_up:
            title_screen = False
            unload_tilemap_collisions()
            load_player_entity()
            load_tilemap(default_tileset, MAIN_DIRECTORY_PATH + "levels/1.json")
            load_tilemap_collisions()
            camera_focus_on_goal(1)
            level_selector = False
            display_hud = True
            left_mouse_click_up = False

    if level_selector:
        # buttons
        y_margin = 0
        for level in OFFICIAL_LEVELS:
            # rendering
            w_width, w_height = SCREEN_SIZE
            button_text = gamedenRE.text2(
                level, 1.5 * RENDER_SIZE, DEFAULT_FONT, (0, 0, 0)
            )
            button_pos = (
                int(w_width / 20),
                int(w_height / 2 - button_text.get_rect().height / 2) + y_margin,
            )
            button = gamedenRE.button(
                pygame.Rect(
                    button_pos[0],
                    button_pos[1],
                    button_text.get_rect().width,
                    button_text.get_rect().height,
                )
            )

            if button.is_hovering(mouse_pos) and left_mouse_click_up:
                unload_tilemap_collisions()
                load_player_entity()
                load_tilemap(default_tileset, MAIN_DIRECTORY_PATH + f"levels/{level}")
                load_tilemap_collisions()
                level_selector = False
                display_hud = True
                left_mouse_click_up = False

            elif button.is_hovering(mouse_pos):
                pygame.draw.rect(screen, (0, 255, 0), button.rect)

            else:
                pygame.draw.rect(screen, (255, 0, 0), button.rect)
            screen.blit(button_text, button_pos)
            y_margin += button_text.get_rect().height + RENDER_SIZE

    if game_over:
        # display
        screen.fill((255, 25, 25))
        w_width, w_height = SCREEN_SIZE
        text = gamedenRE.text2(
            f"click on me to retry...", 1.5 * RENDER_SIZE, DEFAULT_FONT, (0, 0, 0)
        )

        # button
        button_pos = [
            int(w_width / 2 - text.get_rect().width / 2),
            int(w_height / 2 - text.get_rect().height / 2),
        ]
        button_rect = pygame.Rect(
            button_pos[0], button_pos[1], text.get_rect().width, text.get_rect().height
        )
        button = gamedenRE.button(button_rect)
        if left_mouse_click_up and button.is_hovering(mouse_pos):
            game_reset()
            camera_focus_on_goal(1)
            game_over = False
            attempt_number += 1

        screen.blit(text, button_pos)

    if game_won:
        # display
        screen.fill((25, 255, 25))
        w_width, w_height = SCREEN_SIZE
        text = gamedenRE.text2(
            f"you passed the level! click on me to move on!",
            1.5 * RENDER_SIZE,
            DEFAULT_FONT,
            (0, 0, 0),
        )

        # button
        button_pos = [
            int(w_width / 2 - text.get_rect().width / 2),
            int(w_height / 2 - text.get_rect().height / 2),
        ]
        button_rect = pygame.Rect(
            button_pos[0], button_pos[1], text.get_rect().width, text.get_rect().height
        )
        button = gamedenRE.button(button_rect)
        if left_mouse_click_up and button.is_hovering(mouse_pos):
            load_tilemap(
                default_tileset,
                MAIN_DIRECTORY_PATH + f"levels/{int(loaded_tilemap_file_name)+1}.json",
            )
            unload_tilemap_collisions()
            load_player_entity()
            load_tilemap_collisions()
            game_reset()
            attempt_number = 0
            camera_focus_on_goal(1)
            game_won = False

        screen.blit(text, button_pos)

    # HUD
    if display_hud:
        w_width, w_height = SCREEN_SIZE

        # fps
        fps_text = gamedenRE.text2(
            f"FPS: {int(clock.get_fps())}", 1.5 * RENDER_SIZE, DEFAULT_FONT, (0, 0, 0)
        )
        screen.blit(
            fps_text,
            (
                int(w_width - w_width / 75 - fps_text.get_rect().width),
                int(w_height / 75),
            ),
        )

        # number of attempts
        attempt_text = gamedenRE.text2(
            f"attempt #{attempt_number}", 1.5 * RENDER_SIZE, DEFAULT_FONT, (0, 0, 0)
        )
        screen.blit(
            attempt_text,
            (
                int(w_width - w_width / 75 - attempt_text.get_rect().width),
                fps_text.get_rect().height + int(w_height / 75),
            ),
        )

        # level
        level_text = gamedenRE.text2(
            f"level #{loaded_tilemap_file_name}",
            1.5 * RENDER_SIZE,
            DEFAULT_FONT,
            (0, 0, 0),
        )
        screen.blit(
            level_text,
            (
                int(w_width - w_width / 75 - level_text.get_rect().width),
                fps_text.get_rect().height
                + attempt_text.get_rect().height
                + int(w_height / 75),
            ),
        )

    pygame.display.flip()
    space.step(0.02)
    clock.tick(60)

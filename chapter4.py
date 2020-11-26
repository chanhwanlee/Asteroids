import arcade
import os
import random
import math

SPRITE_SCALING = 0.5

WIDTH = 1200
HEIGHT = 600


class Chapter4View(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        centerx_of_screen = WIDTH/2
        centery_of_screen = HEIGHT/2

        self.MOVEMENT_SPEED = 5

        self.STARTING_ENEMY_COUNT = 15

        self.sprite1 = arcade.Sprite(
                                    center_x=centerx_of_screen,
                                    center_y=centery_of_screen)

        self.sprite1.texture = arcade.make_soft_square_texture(30,
                                                               arcade.color.WHITE,
                                                               outer_alpha=255)
        self.player1 = arcade.SpriteList()
        self.player1.append(self.sprite1)

        self.lives = 3

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.enemy_texture = arcade.make_soft_square_texture(30,
                                                             arcade.color.RED,
                                                             outer_alpha=255)
        self.enemies = arcade.SpriteList()

        for i in range(self.STARTING_ENEMY_COUNT):
            enemy = arcade.Sprite()
            enemy.center_x = random.randrange(0, WIDTH-15)
            enemy.center_y = random.randrange(0, HEIGHT-15)
            enemy.texture = self.enemy_texture
            enemy.change_x = random.random() * 3
            enemy.change_y = random.random() * 3
            enemy.change_angle = random.random() * 0
            self.enemies.append(enemy)

        self.laser_texture = arcade.make_soft_square_texture(5,
                                                             arcade.color.BLUE,
                                                             outer_alpha=255)
        self.lasers = arcade.SpriteList()

    def setup(self):
        # Create sprite lists here
        None

    def on_draw(self):
        arcade.start_render()

        self.sprite1.draw()
        self.enemies.draw()
        self.lasers.draw()

        virus_count = (f"Viruses Remaining: {len(self.enemies)}")
        arcade.draw_text(virus_count, (WIDTH - 260), (HEIGHT - 40),
                         arcade.color.WHITE, 20)

        life_count = (f"Lives: {self.lives}")
        arcade.draw_text(life_count, 30, (HEIGHT - 40), arcade.color.WHITE, 20)

        if len(self.enemies) == 0 and self.lives > 0:
            win_text = "You have received these items to obtain the key! "
            win_text2 = "Press 'P' to get to the key"
            arcade.draw_text(win_text, (WIDTH/3-100), (HEIGHT-100), arcade.color.WHITE, 25)
            arcade.draw_text(win_text2, (WIDTH/3-100), (HEIGHT-200), arcade.color.WHITE, 25)
            arcade.draw_circle_filled(WIDTH/2, HEIGHT/2, 50, arcade.color.YELLOW, 128)
            arcade.draw_lrtb_rectangle_filled((WIDTH/3-50), (WIDTH/3 + 50),
                                              (HEIGHT/2 + 50), (HEIGHT/2-50),
                                              arcade.color.BLUE)
            arcade.draw_line((WIDTH*2/3), (HEIGHT/2-50), (WIDTH*2/3), (HEIGHT/2 +50),
                             arcade.color.BABY_BLUE, 25)
        
        if self.lives <= 0 and len(self.enemies) > 0:
            lose_text = "You failed in curing the viruses."
            arcade.draw_text(lose_text, (WIDTH/3-50), (HEIGHT-200), arcade.color.WHITE, 25)

    def update(self, delta_time):
        self.sprite1.update()

        self.sprite1.change_x = 0
        self.sprite1.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.sprite1.change_y = self.MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.sprite1.change_y = -self.MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.sprite1.change_x = -self.MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.sprite1.change_x = self.MOVEMENT_SPEED

        if self.sprite1.left < 0:
            self.sprite1.left = 0
        elif self.sprite1.right > WIDTH - 1:
            self.sprite1.right = WIDTH - 1

        if self.sprite1.bottom < 0:
            self.sprite1.bottom = 0
        elif self.sprite1.top > HEIGHT - 1:
            self.sprite1.top = HEIGHT - 1

        self.lasers.update()

        self.enemies.update()

        for enemy in self.enemies:
            if enemy.center_x < 0:
                enemy.center_x = WIDTH
            elif enemy.center_x > WIDTH:
                enemy.center_x = 0
            if enemy.center_y < 0:
                enemy.center_y = HEIGHT
            elif enemy.center_y > HEIGHT:
                enemy.center_y = 0

        for enemy in self.enemies:
            lasers_in_contact = enemy.collides_with_list(self.lasers)
            if lasers_in_contact:
                enemy.kill()
                for laser in lasers_in_contact:
                    laser.kill()
            if len(self.enemies) == 0:
                print("You won")

        for enemy in self.enemies:
            user_in_contact = enemy.collides_with_list(self.player1)
            if user_in_contact:
                enemy.kill()
                if self.lives == 1:
                    self.lives -= 1
                    print("game over")

                else:
                    self.lives -= 1
                    enemy.center_x = random.randrange(0, WIDTH-15)
                    enemy.center_y = random.randrange(0, HEIGHT-15)
                    enemy.texture = self.enemy_texture
                    enemy.change_x = random.random() * 3
                    enemy.change_y = random.random() * 3
                    enemy.change_angle = random.random() * 0
                    self.enemies.append(enemy)


    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True
        
        if key == arcade.key.P:
            self.director.next_view()

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        laser = arcade.Sprite()
        laser_speed = 10

        start_x = self.sprite1.center_x
        start_y = self.sprite1.center_y
        laser.center_x = start_x
        laser.center_y = start_y

        end_x = x
        end_y = y

        x_diff = end_x - start_x
        y_diff = end_y - start_y
        angle = math.atan2(y_diff, x_diff)

        laser.angle = math.degrees(angle)

        laser.change_x = math.cos(angle) * laser_speed
        laser.change_y = math.sin(angle) * laser_speed

        laser.texture = self.laser_texture
        laser.width = 15

        self.lasers.append(laser)

        if laser.center_x > WIDTH or laser.center_x < 0:
            laser.kill()
        elif laser.center_y > HEIGHT or laser.center_y < 0:
            laser.kill()


def main():
    game = Chapter4View(WIDTH, HEIGHT, "Cure the Virus")
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

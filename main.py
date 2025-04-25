import random
import sys

WIDTH = 800
HEIGHT = 600

# Game states
game_state = "menu"  # 'menu' or 'playing'

# Sound status
sound_on = True

# Player
player = Actor('player_action1.png') 
player.pos = (WIDTH // 2, HEIGHT - 50)

# Player image paths
player_images = [
    'player_action1.png',
    'player_action2.png'
]

# Current image index
current_image_index = 0

def switch_player_image():
    global current_image_index
    current_image_index = (current_image_index + 1) % len(player_images)
    player.image = player_images[current_image_index]

# Switch player image every 0.5 seconds
clock.schedule_interval(switch_player_image, 0.5)

# Lists for stars and stones
stars = []
stones = []

# Score and stones hit
score = 0
stones_hit = 0

class Button:
    def __init__(self, text, pos, action):
        self.text = text
        self.pos = pos
        self.action = action
        self.width = 200
        self.height = 50
        self.rect = Rect((self.pos[0], self.pos[1]), (self.width, self.height))

    def draw(self):
        screen.draw.filled_rect(self.rect, "blue")
        screen.draw.text(self.text, center=self.rect.center, fontsize=30, color="white")

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()

# Menu buttons
buttons = []

def play_game():
    global game_state, score, stones_hit, stars, stones
    game_state = "playing"
    score = 0
    stones_hit = 0
    stars = []
    stones = []

def toggle_sound():
    global sound_on
    sound_on = not sound_on

def exit_game():
    sys.exit()

def create_buttons():
    global buttons
    buttons = [
        Button("Play", (300, 150), play_game),
        Button("Sound On/Off", (300, 230), toggle_sound),
        Button("Exit", (300, 310), exit_game),
    ]

create_buttons()

def spawn_star():
    star = Actor('star_gold.png')
    star.x = random.randint(20, WIDTH - 20)
    star.y = 0
    stars.append(star)

def spawn_stone():
    stone = Actor('meteorbrown_big1.png')
    stone.x = random.randint(20, WIDTH - 20)
    stone.y = 0
    stones.append(stone)

music_playing = False  # Başlangıçta müzik çalmıyor

def update():
    global music_playing
    if game_state == "playing":
        game_update()

    if game_state == "menu":
        if sound_on and not music_playing:
            sounds.menu_music.play(-1)  # Sonsuz döngüde çal
            music_playing = True
        elif not sound_on and music_playing:
            sounds.menu_music.stop()  # Ses kapalıysa müzik durdur
            music_playing = False

def game_update():
    global score, stones_hit

    # Player movement
    if keyboard.left and player.left > 0:
        player.x -= 5
    if keyboard.right and player.right < WIDTH:
        player.x += 5

    # Move stars
    for star in stars[:]:  # Listeyi kopyalayarak döngü yapıyoruz
        star.y += 4
        if star.colliderect(player):
            stars.remove(star)
            score += 1
            sounds.notification.play()  # Star sound
        elif star.y > HEIGHT:
            stars.remove(star)

    # Move stones
    for stone in stones[:]:  # Listeyi kopyalayarak döngü yapıyoruz
        stone.y += 5
        if stone.colliderect(player):
            stones.remove(stone)
            stones_hit += 1
            sounds.bomb.play()  # Stone sound
        elif stone.y > HEIGHT:
            stones.remove(stone)

    # If 3 stones are hit, reset the game
    if stones_hit >= 3:
        sounds.lose.play()  # Lose sound
        reset_game()

def draw():
    screen.clear()

    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()

def draw_menu():
    if stones_hit >= 3:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, 150), fontsize=80, color="red")

    screen.draw.text("Star Catcher", center=(WIDTH // 2, 70), fontsize=60, color="white")

    for button in buttons:
        button.draw()

    sound_status = "Sound: ON" if sound_on else "Sound: OFF"
    screen.draw.text(sound_status, center=(WIDTH // 2, 400), fontsize=30, color="yellow")

def draw_game():
    player.draw()

    for star in stars:
        star.draw()

    for stone in stones:
        stone.draw()

    screen.draw.text(f"Score: {score}", (10, 10), color="white", fontsize=40)
    screen.draw.text(f"Stones: {stones_hit}", (10, 60), color="red", fontsize=40)

def reset_game():
    global game_state
    game_state = "menu"

def on_mouse_down(pos):
    if game_state == "menu":
        for button in buttons:
            button.check_click(pos)

def update_falling_objects():
    if game_state == "playing":
        if random.randint(0, 8) < 5:
            spawn_star()
        if random.randint(0, 4) < 2:
            spawn_stone()

clock.schedule_interval(update_falling_objects, 0.5)

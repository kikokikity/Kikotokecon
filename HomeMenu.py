import pygame
import sys
import time
import sqlite3

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
pygame.font.init()
FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pixel Art Game Main Menu')

# Menu options
main_menu_options = ['Start Game', 'Task Entry', 'Settings']
settings_menu_options = ['Option 1', 'Option 2', 'Back']
selected_option = 0
in_settings_menu = False
in_task_entry_menu = False
tasks = []

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            points INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Database functions
def add_task(name, points):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (name, points) VALUES (?, ?)', (name, points))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, points FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Pygame functions
def draw_time():
    current_time = time.strftime("%H:%M:%S")
    time_text = FONT.render(current_time, True, WHITE)
    time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(time_text, time_rect)

def draw_menu(options):
    screen.fill(BLACK)
    draw_time()
    for i, option in enumerate(options):
        if i == selected_option:
            color = WHITE
        else:
            color = GRAY
        text = FONT.render(option, True, color)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
        screen.blit(text, text_rect)

def draw_task_entry_menu(tasks):
    screen.fill(BLACK)
    draw_time()
    for i, task in enumerate(tasks):
        task_text = f"{task[1]} - {task[2]} points"
        text = SMALL_FONT.render(task_text, True, WHITE)
        text_rect = text.get_rect(topleft=(100, 100 + i * 30))
        screen.blit(text, text_rect)
        delete_text = SMALL_FONT.render('Delete', True, RED)
        delete_rect = delete_text.get_rect(topleft=(SCREEN_WIDTH - 150, 100 + i * 30))
        screen.blit(delete_text, delete_rect)
        pygame.draw.rect(screen, RED, delete_rect, 2)

    add_task_text = SMALL_FONT.render('Add Task', True, GREEN)
    add_task_rect = add_task_text.get_rect(topleft=(100, SCREEN_HEIGHT - 100))
    screen.blit(add_task_text, add_task_rect)
    pygame.draw.rect(screen, GREEN, add_task_rect, 2)

def handle_task_entry_menu(event):
    global tasks
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
        for i, task in enumerate(tasks):
            delete_text = SMALL_FONT.render('Delete', True, RED)
            delete_rect = delete_text.get_rect(topleft=(SCREEN_WIDTH - 150, 100 + i * 30))
            if delete_rect.collidepoint(mouse_x, mouse_y):
                delete_task(task[0])
                tasks = get_tasks()
        add_task_text = SMALL_FONT.render('Add Task', True, GREEN)
        add_task_rect = add_task_text.get_rect(topleft=(100, SCREEN_HEIGHT - 100))
        if add_task_rect.collidepoint(mouse_x, mouse_y):
            task_name = input("Enter task name: ")
            task_points = int(input("Enter task points: "))
            add_task(task_name, task_points)
            tasks = get_tasks()

def main():
    global selected_option, in_settings_menu, in_task_entry_menu, tasks
    running = True
    clock = pygame.time.Clock()
    tasks = get_tasks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if in_task_entry_menu:
                    pass  # Handle task entry specific key events if needed
                elif in_settings_menu:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(settings_menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(settings_menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == len(settings_menu_options) - 1:  # 'Back' option
                            in_settings_menu = False
                            selected_option = 0
                else:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(main_menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(main_menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            print("Start Game selected")
                            # Start the game
                        elif selected_option == 1:
                            print("Task Entry selected")
                            in_task_entry_menu = True
                            selected_option = 0
                        elif selected_option == 2:
                            print("Settings selected")
                            in_settings_menu = True
                            selected_option = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if in_task_entry_menu:
                    handle_task_entry_menu(event)
                else:
                    mouse_x, mouse_y = event.pos
                    for i, option in enumerate(settings_menu_options if in_settings_menu else main_menu_options):
                        text_rect = FONT.render(option, True, WHITE).get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
                        if text_rect.collidepoint(mouse_x, mouse_y):
                            selected_option = i
                            if in_settings_menu:
                                if selected_option == len(settings_menu_options) - 1:  # 'Back' option
                                    in_settings_menu = False
                                    selected_option = 0
                            else:
                                if selected_option == 0:
                                    print("Start Game selected")
                                    # Start the game
                                elif selected_option == 1:
                                    print("Task Entry selected")
                                    in_task_entry_menu = True
                                    selected_option = 0
                                elif selected_option == 2:
                                    print("Settings selected")
                                    in_settings_menu = True
                                    selected_option = 0

        if in_task_entry_menu:
            draw_task_entry_menu(tasks)
        elif in_settings_menu:
            draw_menu(settings_menu_options)
        else:
            draw_menu(main_menu_options)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()

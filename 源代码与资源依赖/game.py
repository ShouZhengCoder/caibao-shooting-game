import pygame
import random
import time
import os
import sys

pygame.init()
def resource_path(relative_path):
    """获取资源文件的绝对路径"""
    if getattr(sys, 'frozen', False):  # 是否为打包后的文件
        base_path = sys._MEIPASS  # 打包后的临时目录
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 屏幕设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("财宝的进击")

# 颜色定义
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# 加载图片
background_image = pygame.image.load(resource_path("background1.jpg"))
player_image = pygame.image.load(resource_path("player_normal.jpg"))
boss_image = pygame.image.load(resource_path("boss.jpg"))

# 缩放背景图片
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# 图片缩放
player_width, player_height = 50, 70
player_image = pygame.transform.scale(player_image, (player_width, player_height))

boss_width, boss_height = 100, 100
boss_image = pygame.transform.scale(boss_image, (boss_width, boss_height))

# 加载障碍物图片
obstacle_images = []
obstacle_folder = resource_path("obstacles")  # 障碍物图片文件夹

for filename in os.listdir(obstacle_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(obstacle_folder, filename)
        img = pygame.image.load(image_path)
        obstacle_images.append(pygame.transform.scale(img, (70, 50)))

# 初始化音效
pygame.mixer.init()
pygame.mixer.music.load(resource_path("background_music.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
shoot_sound = pygame.mixer.Sound(resource_path("shoot_sound.mp3"))
hit_boss_sound = pygame.mixer.Sound(resource_path("hit_boss_sound.mp3"))
hit_player_sound = pygame.mixer.Sound(resource_path("hit_player_sound.mp3"))
# 初始化游戏时钟和帧率
clock = pygame.time.Clock()
FPS = 60

# 新增变量
#half_health_triggered = False  # 是否已经触发过50%血量事件
new_background_image = pygame.image.load(resource_path("background2.jpg")) # 新背景图像
new_background_image = pygame.transform.scale(new_background_image, (WIDTH, HEIGHT))
# 新音乐
new_music_path = resource_path("intense_music.mp3")

def run_game():
    """游戏主循环"""
    # 玩家设置
    player_x = 10
    player_y = HEIGHT // 2 - player_height // 2
    player_speed = 5
    player_health = 100
    max_player_health = 100
    # 子弹设置
    bullets = []
    bullet_width, bullet_height = 10, 5
    bullet_speed = 7
    # Boss 设置
    boss_x = WIDTH - boss_width - 10
    boss_y = HEIGHT // 2 - boss_height // 2
    boss_speed = 3
    boss_health = 20
    # Boss 子弹设置
    boss_bullets = []
    boss_bullet_speed = 5
    boss_attack_cooldown = 2  # Boss 每 2 秒发射一颗子弹
    last_boss_attack_time = time.time()
    # 障碍物设置
    obstacles = []
    obstacle_speed = 5
    damage_per_hit = 20  # 每次碰撞的伤害
    # 冷却计数
    shoot_count = 0
    last_shoot_time = time.time()
    cooldown_time = 2
    max_shoots_before_cooldown = 5
    half_health_triggered = False
    running = True
    game_over = False
    while running:
        obstacle_spawn_rate = 30
        if not half_health_triggered:
            screen.blit(background_image, (0, 0))
        else:
            screen.blit(new_background_image, (0, 0))
        # 检测Boss血量
        if boss_health <= 10 and not half_health_triggered:  # Boss血量低于50%时触发
            half_health_triggered = True
            # 更换背景图像
            #background_image = new_background_image
            # 更换背景音乐
            pygame.mixer.music.stop()
            pygame.mixer.music.load(new_music_path)
            pygame.mixer.music.play(-1)
            # 提高障碍物生成频率
            obstacle_spawn_rate = max(10, obstacle_spawn_rate - 15)  # 增加障碍物生成概率
        # 绘制玩家血量条
        pygame.draw.rect(screen, RED, (10, 10, 200, 20))  # 背景条
        pygame.draw.rect(screen, GREEN, (10, 10, 200 * (player_health / max_player_health), 20))  # 当前血量条
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # 获取按键状态
        keys = pygame.key.get_pressed()
        if not game_over:
            # 玩家移动
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed
            if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height:
                player_y += player_speed
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
                player_x += player_speed
            # 玩家射击
            if keys[pygame.K_SPACE]:
                if shoot_count < max_shoots_before_cooldown:
                    bullets.append([player_x + player_width, player_y + player_height // 2])
                    shoot_count += 1
                    shoot_sound.play()
                elif time.time() - last_shoot_time > cooldown_time:
                    last_shoot_time = time.time()
                    shoot_count = 0
                    bullets.append([player_x + player_width, player_y + player_height // 2])
                    shoot_sound.play()
            # 子弹移动和绘制
            for bullet in bullets[:]:
                bullet[0] += bullet_speed
                pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_width, bullet_height))
                if bullet[0] > WIDTH:
                    bullets.remove(bullet)
                # 子弹击中 Boss
                if boss_x < bullet[0] < boss_x + boss_width and boss_y < bullet[1] < boss_y + boss_height:
                    bullets.remove(bullet)
                    boss_health -= 1
                    hit_boss_sound.play()
            # 绘制玩家
            screen.blit(player_image, (player_x, player_y))
            # 绘制 Boss
            screen.blit(boss_image, (boss_x, boss_y))
            pygame.draw.rect(screen, RED, (boss_x, boss_y - 10, boss_width, 5))
            pygame.draw.rect(screen, BLUE, (boss_x, boss_y - 10, boss_width * (boss_health / 20), 5))
            # Boss 攻击
            if time.time() - last_boss_attack_time > boss_attack_cooldown:
                boss_bullets.append([boss_x, boss_y + boss_height // 2])
                last_boss_attack_time = time.time()
            # Boss 子弹移动和绘制
            for boss_bullet in boss_bullets[:]:
                boss_bullet[0] -= boss_bullet_speed
                pygame.draw.rect(screen, BLUE, (boss_bullet[0], boss_bullet[1], 10, 5))
                # 检测 Boss 子弹是否击中玩家
                if (
                    player_x < boss_bullet[0] < player_x + player_width
                    and player_y < boss_bullet[1] < player_y + player_height
                ):
                    boss_bullets.remove(boss_bullet)
                    player_health -= damage_per_hit
                    if player_health <= 0:
                        game_over = True
                    hit_player_sound.play()
                # 移除超出屏幕的子弹
                if boss_bullet[0] < 0:
                    boss_bullets.remove(boss_bullet)
            # 随机生成障碍物
            if random.randint(1, obstacle_spawn_rate) == 1 and obstacle_images:
                obstacles.append([WIDTH, random.randint(0, HEIGHT - 50), random.choice(obstacle_images)])
            # 移动和绘制障碍物
            for obstacle in obstacles[:]:
                obstacle[0] -= obstacle_speed
                screen.blit(obstacle[2], (obstacle[0], obstacle[1]))
                # 玩家碰到障碍物
                if (
                    player_x < obstacle[0] + 50
                    and player_x + player_width > obstacle[0]
                    and player_y < obstacle[1] + 50
                    and player_y + player_height > obstacle[1]
                ):
                    obstacles.remove(obstacle)
                    player_health -= damage_per_hit
                    if player_health <= 0:
                        game_over = True
                    hit_player_sound.play()
                if obstacle[0] < -50:
                    obstacles.remove(obstacle)
            # Boss 移动
            boss_y += boss_speed
            if boss_y <= 0 or boss_y >= HEIGHT - boss_height:
                boss_speed *= -1
            # 胜利检测
            if boss_health <= 0:
                game_over = True
        # 游戏结束逻辑
        if game_over:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(resource_path("background_music.mp3"))
            pygame.mixer.music.play(-1)
            font = pygame.font.SysFont("Arial", 50)
            message = "You Win!" if boss_health <= 0 else "You Lose!"
            text = font.render(message, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
            restart_text = font.render("Press R to retry, Q quit(Caps)", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r :
                            return True
                        elif event.key == pygame.K_q :
                            return False
        pygame.display.flip()
        clock.tick(FPS)
# 主循环
while run_game():
    pass
pygame.quit()

import pygame

pygame.init()

WIDTH, HEIGHT = 1300,800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ========== 1. 加载图片（替换成你自己的png路径）==========
# 底层地图

map_img_3 = pygame.image.load("room3.png").convert_alpha()
map_img_4 = pygame.image.load("room4.png").convert_alpha()
map_img_5 = pygame.image.load("room5.png").convert_alpha()
map_img_6 = pygame.image.load("room6.png").convert_alpha()
map_img_7 = pygame.image.load("room7.png").convert_alpha()
map_img_8 = pygame.image.load("room8.png").convert_alpha()
map_img_9 = pygame.image.load("room9.png").convert_alpha()
map_img_10 = pygame.image.load("room10.png").convert_alpha()
# 家具物体
#table_img = pygame.image.load("table.png").convert_alpha()
#chair_img = pygame.image.load("chair.png").convert_alpha()
box_img = pygame.image.load("box.png").convert_alpha()

# ========== 2. 定义所有物体列表：存图片、坐标 ==========
# 格式：[ (图片, x坐标, y坐标), ... ]
objects = [
    #(table_img, 200, 300),   # 桌子放在(200,300)
    #(chair_img, 150, 320),   # 椅子在桌子左边
    #(chair_img, 280, 320),
    (box_img, 600, 450),     # 箱子在右侧
    (box_img, 680, 460),
]

running = True
while running:
    # 退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ========== 3. 分层绘制（顺序绝对不能乱！）==========
    # 第一层：画整张地图（底层）
    screen.blit(map_img_3, (0, 0))
    screen.blit(map_img_4, (0, 0))
    screen.blit(map_img_5, (0, 0))  # 地图左上角贴窗口原点
    screen.blit(map_img_6, (0, 0))
    screen.blit(map_img_7, (0, 0))
    screen.blit(map_img_8, (0, 0))
    screen.blit(map_img_9, (0, 0))
    screen.blit(map_img_10, (0, 0))


    # 第二层：遍历绘制所有家具、箱子
    for obj_img, x, y in objects:
        screen.blit(obj_img, (x, y))

    # 刷新画面
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
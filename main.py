import os
import uiautomator2 as u2
import math
import cv2
import numpy as np
import colorama
def init(adb_url):
    ## init uiautomator2
    msg = os.system("toolkit\\adb connect %s" % adb_url)
    print(msg)
    msg = os.system("python -m  uiautomator2 init")
    # print(msg)
    # print("???")
    # print(msg.read())
    colorama.init(strip=True)
    d = u2.connect(adb_url)
    return d
def rnd_click(d, left, top, right, bottom):
    # 定义矩阵区域 (left, top, right, bottom)
    # left, top, right, bottom = 504, 1468, 579, 1502

    # 生成随机点的数量
    num_points = 10  # 你可以根据需要调整这个值

    # 在指定区域内生成随机点的 x 坐标
    x_coords = np.random.randint(left, right, num_points)

    # 在指定区域内生成随机点的 y 坐标
    y_coords = np.random.randint(top, bottom, num_points)

    # 打印生成的随机点的坐标并点击
    points = list(zip(x_coords, y_coords))
    print("生成的随机点坐标:")
    for point in points:
        x, y = point
        print(f"点击坐标: ({x}, {y})")
        d.click(int(x), int(y))

def element_click(d, boss_element, player_element, button_element):
    if boss_element == 'None':
        return 
    if player_element == 'None':
        return
    
    to_element = None

    if boss_element == 'fire':
        if player_element == 'bonfire':
            to_element = 'wooden'
        if player_element == 'steam':
            to_element = 'water'
    if boss_element == 'wooden':
        if player_element == 'bonfire':
            to_element = 'fire'
        if player_element == 'bloom':
            to_element = 'water'
    if boss_element == 'water':
        if player_element == 'bloom':
            to_element = 'wooden'
        if player_element == 'steam':
            to_element = 'fire'

    if button_element == 'fire_button':
        if to_element == 'fire':
            rnd_click(d, 81, 1001, 119, 1036)
        if to_element == 'water':
            rnd_click(d, 197, 999, 234, 1038)
        if to_element == 'wooden':
            rnd_click(d, 141, 1104, 178, 1147)
    if button_element == 'water_button':
        if to_element == 'fire':
            rnd_click(d, 141, 1104, 178, 1147)
        if to_element == 'water':
            rnd_click(d, 81, 1001, 119, 1036)
        if to_element == 'wooden':
            rnd_click(d, 197, 999, 234, 1038)
    if button_element == 'wooden_button':
        if to_element == 'fire':
            rnd_click(d, 197, 999, 234, 1038)
        if to_element == 'water':
            rnd_click(d, 141, 1104, 178, 1147)
        if to_element == 'wooden':
            rnd_click(d, 81, 1001, 119, 1036)
    return to_element

def screen(d):
    full_screen = d.screenshot()
    boss_element = boss_color_judge(full_screen)
    player_element = player_template_judge(full_screen.crop((238,1068,841,1390)))
    button_element = button_color_judge(full_screen)
    
    print("boss_element: ", boss_element)
    print("player_element: ", player_element)
    print("button_element: ", button_element)

    to_element = element_click(d, boss_element, player_element, button_element)
    print("to_element: ", to_element)
    msg = {
        'boss_element' : boss_element,
        'player_element' : player_element,
        'button_element' : button_element,
        'to_element': to_element
    }
    return msg
    # while True:
    #     full_screen = d.screenshot()
    #     boss_element = boss_color_judge(full_screen)
    #     player_element = player_template_judge(full_screen.crop((238,1068,841,1390)))
    #     button_element = button_color_judge(full_screen)
        
    #     print("boss_element: ", boss_element)
    #     print("player_element: ", player_element)
    #     print("button_element: ", button_element)

    #     to_element = element_click(d, boss_element, player_element, button_element)
    #     print("to_element: ", to_element)
    #     msg = {
    #         'boss_element' : boss_element,
    #         'player_element' : player_element,
    #         'button_element' : button_element,
    #         'to_element': to_element
    #     }
    #     # return msg

def similar(rgb1, rgb2):
    return math.sqrt((rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2)

def fire_sim(rgb1, rgb2, rgb3, thr = 30):
    fire_rgb1 = (254, 181, 113)
    fire_rgb2 = (254, 184, 90)
    fire_rgb3 = (254, 153, 99)
    thorld1 = similar(rgb1, fire_rgb1)
    thorld2 = similar(rgb2, fire_rgb2)
    thorld3 = similar(rgb3, fire_rgb3)

    if thorld1 + thorld2 + thorld3 < thr:
        return True
    return False
    
def wooden_sim(rgb1, rgb2, rgb3, thr = 30):
    fire_rgb1 = (167, 224, 109)
    fire_rgb2 = (181, 227, 120)
    fire_rgb3 = (145, 219, 105)
    thorld1 = similar(rgb1, fire_rgb1)
    thorld2 = similar(rgb2, fire_rgb2)
    thorld3 = similar(rgb3, fire_rgb3)

    if thorld1 + thorld2 + thorld3 < thr:
        return True
    return False

def water_sim(rgb1, rgb2, rgb3, thr = 30):
    fire_rgb1 = (196, 237, 243)
    fire_rgb2 = (163, 228, 237)
    fire_rgb3 = (219, 245, 249)
    thorld1 = similar(rgb1, fire_rgb1)
    thorld2 = similar(rgb2, fire_rgb2)
    thorld3 = similar(rgb3, fire_rgb3)

    if thorld1 + thorld2 + thorld3 < thr:
        return True
    return False

def boss_color_judge(img):
    rgb1 = img.getpixel((522,542))
    rgb2 = img.getpixel((557,536))
    rgb3 = img.getpixel((542,581))

    if fire_sim(rgb1, rgb2, rgb3, thr = 50):
        return 'fire'
    if wooden_sim(rgb1, rgb2, rgb3, thr = 50):
        return 'wooden'
    if water_sim(rgb1, rgb2, rgb3, thr = 50):
        return 'water'
    return 'None'

def water_button_sim(rgb1, rgb2, rgb3, thr = 30):
    fire_rgb1 = (149, 207, 207)
    fire_rgb2 = (147, 204, 206)
    fire_rgb3 = (62, 79, 98)
    thorld1 = similar(rgb1, fire_rgb1)
    thorld2 = similar(rgb2, fire_rgb2)
    thorld3 = similar(rgb3, fire_rgb3)

    if thorld1 + thorld2 + thorld3 < thr:
        return True
    return False

def wooden_button_sim(rgb1, rgb2, rgb3, thr = 30):
    fire_rgb1 = (189, 214, 172)
    fire_rgb2 = (188, 214, 172)
    fire_rgb3 = (152, 217, 156)
    thorld1 = similar(rgb1, fire_rgb1)
    thorld2 = similar(rgb2, fire_rgb2)
    thorld3 = similar(rgb3, fire_rgb3)

    if thorld1 + thorld2 + thorld3 < thr:
        return True
    return False

def fire_button_sim(rgb1, rgb2, rgb3, thr = 30):
    fire_rgb1 = (226, 176, 138)
    fire_rgb2 = (226, 170, 136)
    fire_rgb3 = (65, 66, 75)
    thorld1 = similar(rgb1, fire_rgb1)
    thorld2 = similar(rgb2, fire_rgb2)
    thorld3 = similar(rgb3, fire_rgb3)

    if thorld1 + thorld2 + thorld3 < thr:
        return True
    return False

def button_color_judge(img):
    rgb1 = img.getpixel((94,1008))
    rgb2 = img.getpixel((111,1009))
    rgb3 = img.getpixel((106,1023))

    if fire_button_sim(rgb1, rgb2, rgb3, thr = 50):
        return 'fire_button'
    if wooden_button_sim(rgb1, rgb2, rgb3, thr = 50):
        return 'wooden_button'
    if water_button_sim(rgb1, rgb2, rgb3, thr = 50):
        return 'water_button'
    return 'None_button'


def steam_sim(rgb1, rgb2, rgb3, thr = 30):
    fire_rgb1 = (158, 91, 161)
    fire_rgb2 = (153, 104, 182)
    fire_rgb3 = (171, 116, 196)
    thorld1 = similar(rgb1, fire_rgb1)
    thorld2 = similar(rgb2, fire_rgb2)
    thorld3 = similar(rgb3, fire_rgb3)

    if thorld1 + thorld2 + thorld3 < thr:
        return True
    return False

def bonfire_sim(rgb1, rgb2, rgb3, thr = 30):
    fire_rgb1 = (221, 142, 75)
    fire_rgb2 = (239, 169, 124)
    fire_rgb3 = (242, 188, 150)
    thorld1 = similar(rgb1, fire_rgb1)
    thorld2 = similar(rgb2, fire_rgb2)
    thorld3 = similar(rgb3, fire_rgb3)

    if thorld1 + thorld2 + thorld3 < thr:
        return True
    return False

def bloom_sim(rgb1, rgb2, rgb3, thr = 30):
    fire_rgb1 = (235, 242, 242)
    fire_rgb2 = (135, 224, 185)
    fire_rgb3 = (97, 175, 124)
    thorld1 = similar(rgb1, fire_rgb1)
    thorld2 = similar(rgb2, fire_rgb2)
    thorld3 = similar(rgb3, fire_rgb3)

    if thorld1 + thorld2 + thorld3 < thr:
        return True
    return False

def player_color_judge(img):
    rgb1 = img.getpixel((555,1219))
    rgb2 = img.getpixel((562,1218))
    rgb3 = img.getpixel((577,1215))

    if steam_sim(rgb1, rgb2, rgb3, thr = 50):
        return 'steam'
    if bonfire_sim(rgb1, rgb2, rgb3, thr = 50):
        return 'bonfire'
    if bloom_sim(rgb1, rgb2, rgb3, thr = 50):
        return 'bloom'
    return 'None'

def match_template(main_image, template_image, threshold=0.8):
    
    # 将 PIL 图像转换为 NumPy 数组
    main_image = np.array(main_image)

    # OpenCV 使用 BGR 格式，而 PIL 使用 RGB 格式，所以需要转换颜色通道
    main_image = cv2.cvtColor(main_image, cv2.COLOR_RGB2BGR)
    # 使用 cv2.matchTemplate 进行模板匹配
    result = cv2.matchTemplate(main_image, template_image, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    if len(locations[0]) > 0:
        return True, result
    else:
        return False, result

def player_template_judge(main_image, template_image_paths=['bloom.png', 'bonfire.png', 'steam.png']):
    # 设置匹配的阈值
    dir = "template"
    
    threshold = 0.8

    # 初始化变量以存储最佳匹配结果
    best_match_template = None
    best_match_value = -1
    best_match_location = None
    best_match_template_path = None

    # 遍历每个模板图像
    for template_image_path in template_image_paths:
        template_image_path = os.path.join(dir, template_image_path)
        
        template_image = cv2.imread(template_image_path)
        matched, result = match_template(main_image, template_image, threshold)
        
        if matched:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > best_match_value:
                best_match_value = max_val
                best_match_location = max_loc
                best_match_template = template_image
                best_match_template_path = template_image_path
    if best_match_location==None:
        return 'None'
    return best_match_template_path.split('.')[0].split('\\')[-1]

def get_rgb(img):
    rgb1 = img.getpixel((555,1219))
    rgb2 = img.getpixel((562,1218))
    rgb3 = img.getpixel((577,1215))

    print(rgb1)
    print(rgb2)
    print(rgb3)

if __name__ == '__main__':
    adb_url = "127.0.0.1:16384"
    d = u2.connect(adb_url)
    screen(d)
# adb_url = "127.0.0.1:16384"
# init(adb_url=adb_url)
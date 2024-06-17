import cv2
import numpy as np
import matplotlib.pyplot as plt

def match_template(main_image, template_image, threshold=0.8):
    # 使用 cv2.matchTemplate 进行模板匹配
    result = cv2.matchTemplate(main_image, template_image, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    if len(locations[0]) > 0:
        return True, result
    else:
        return False, result

# 读取主图像
main_image_path = 'slm_6.png'
main_image = cv2.imread(main_image_path)

# 模板图像路径列表
template_image_paths = [
    'template/bloom.png',
    'template/bonfire.png',
    'template/steam.png'
]

# 设置匹配的阈值
threshold = 0.8

# 初始化变量以存储最佳匹配结果
best_match_template = None
best_match_value = -1
best_match_location = None
best_match_template_path = None

# 遍历每个模板图像
for template_image_path in template_image_paths:
    template_image = cv2.imread(template_image_path)
    matched, result = match_template(main_image, template_image, threshold)
    
    if matched:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > best_match_value:
            best_match_value = max_val
            best_match_location = max_loc
            best_match_template = template_image
            best_match_template_path = template_image_path

# 检查是否找到匹配
if best_match_template is not None:
    # 获取模板图像的尺寸
    template_height, template_width, _ = best_match_template.shape

    # 在主图像上绘制匹配结果的矩形
    cv2.rectangle(main_image, best_match_location, 
                  (best_match_location[0] + template_width, best_match_location[1] + template_height), 
                  (0, 0, 255), 2)
    
    # 将 BGR 图像转换为 RGB 以显示正确的颜色
    main_image_rgb = cv2.cvtColor(main_image, cv2.COLOR_BGR2RGB)

    # 显示结果图像
    plt.figure(figsize=(10, 8))
    plt.imshow(main_image_rgb)
    plt.title(f'Matched Template: {best_match_template_path}')
    plt.axis('off')
    plt.show()
else:
    print("No template matched.")

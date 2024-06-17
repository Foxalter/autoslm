import cv2
import numpy as np
from matplotlib import pyplot as plt

def match_template(main_image, template, threshold=0.5):
    """
    Function to perform template matching and return the match result.
    """
    result = cv2.matchTemplate(main_image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(max_val)
    
    if max_val >= threshold:
        return max_val, max_loc
    else:
        return None, None

# 读取主图像
main_image = cv2.imread('slm_5.png', cv2.IMREAD_GRAYSCALE)

# 模板图像文件列表
template_files = ['template//bloom.png', 'template//bonfire.png', 'template//steam.png']

best_match_val = 0
best_match_loc = None
best_template = None
w, h = 0, 0

# 遍历模板图像进行匹配
for template_file in template_files:
    template = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]
    match_val, match_loc = match_template(main_image, template)
    
    if match_val is not None and match_val > best_match_val:
        best_match_val = match_val
        best_match_loc = match_loc
        best_template = template_file

# 绘制最佳匹配结果
if best_match_loc is not None:
    cv2.rectangle(main_image, best_match_loc, (best_match_loc[0] + w, best_match_loc[1] + h), (0, 0, 255), 2)
    plt.imshow(main_image, cmap='gray')
    plt.title(f'Best Match: {best_template} with Score: {best_match_val}')
    plt.show()

    # 保存匹配结果图像
    cv2.imwrite('best_match_result.jpg', main_image)
else:
    print('No match found with the given threshold.')

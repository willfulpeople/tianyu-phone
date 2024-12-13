from fastapi import APIRouter, Response, HTTPException, status
from PIL import Image, ImageDraw, ImageFont
import random
import io
import string
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# 生成随机验证码字符串
def generate_code():
    # 只使用容易辨认的字符
    chars = '34578ABCDEFGHJKLMNPQRSTUVWXYZ'
    return ''.join(random.choices(chars, k=4))

# 生成验证码图片
def generate_captcha_image(code):
    # 创建图片对象
    width = 120
    height = 50
    # 创建一个更大的基础图片，后面会缩放到目标大小
    base_width = width * 2
    base_height = height * 2
    image = Image.new('RGB', (base_width, base_height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 生成干扰线
    for i in range(8):
        x1 = random.randint(0, base_width)
        y1 = random.randint(0, base_height)
        x2 = random.randint(0, base_width)
        y2 = random.randint(0, base_height)
        draw.line([(x1, y1), (x2, y2)], fill=(200, 200, 200), width=2)

    # 创建很大的单个字符图片，然后缩小到合适大小
    try:
        font = ImageFont.load_default()
        char_spacing = base_width // 6  # 字符间距
        start_x = char_spacing  # 起始位置

        for i, char in enumerate(code):
            # 为每个字符创建一个更大的图片
            char_img = Image.new('RGBA', (60, 60), (255, 255, 255, 0))
            char_draw = ImageDraw.Draw(char_img)
            
            # 在更大的范围内绘制字符，这样缩放后仍然清晰
            for thickness in range(2):  # 增加笔画粗细
                char_draw.text((15+thickness, 15), char, font=font, fill=(0, 0, 0))
                char_draw.text((15, 15+thickness), char, font=font, fill=(0, 0, 0))
                char_draw.text((15-thickness, 15), char, font=font, fill=(0, 0, 0))
                char_draw.text((15, 15-thickness), char, font=font, fill=(0, 0, 0))

            # 随机旋转
            angle = random.randint(-30, 30)
            rotated = char_img.rotate(angle, expand=1, fillcolor=(255, 255, 255, 0))
            
            # 计算字符位置
            x = start_x + i * char_spacing
            y = random.randint(base_height//4, base_height//2)
            
            # 将字符图片粘贴到主图片
            image.paste(rotated, (x, y), rotated)

        # 生成颜色干扰
        for _ in range(30):
            x = random.randint(0, base_width)
            y = random.randint(0, base_height)
            draw.point((x, y), fill=(random.randint(0, 255), 
                                   random.randint(0, 255), 
                                   random.randint(0, 255)))

        # 将图片缩放到目标大小
        image = image.resize((width, height), Image.Resampling.LANCZOS)

    except Exception as e:
        logger.error(f"Error drawing text: {str(e)}")
        raise

    # 转换图片为bytes
    try:
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr
    except Exception as e:
        logger.error(f"Error converting image to bytes: {str(e)}")
        raise

@router.get("")
async def get_captcha():
    logger.info("Captcha request received")
    try:
        # 生成验证码
        code = generate_code()
        logger.info(f"Generated captcha code: {code}")

        # 生成验证码图片
        image = generate_captcha_image(code)
        logger.info("Captcha image generated successfully")
        
        # 返回图片
        return Response(content=image, media_type="image/png")
    except Exception as e:
        logger.error(f"Error generating captcha: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
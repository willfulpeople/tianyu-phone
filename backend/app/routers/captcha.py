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
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

# 生成验证码图片
def generate_captcha_image(code):
    # 创建图片对象 - 增加高度以便于放置更大的字体
    width = 120
    height = 50  # 增加高度
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 生成干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(200, 200, 200))

    # 生成干扰点
    for i in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(200, 200, 200))

    # 使用默认字体但增大字号
    try:
        font = ImageFont.load_default()
        # 计算每个字符的位置并单独绘制，增大间距
        for i, char in enumerate(code):
            # 为每个字符计算x位置，平均分布
            x = 20 + i * 25  # 增加字符间距
            # 随机调整y位置制造不规则效果
            y = random.randint(10, 20)
            # 随机旋转角度
            angle = random.randint(-30, 30)
            # 创建一个新的图片用于旋转文字
            char_img = Image.new('RGBA', (30, 30), (255, 255, 255, 0))
            char_draw = ImageDraw.Draw(char_img)
            # 使用更大的字号绘制字符
            char_draw.text((10, 10), char, font=font, fill=(0, 0, 0))
            # 旋转并粘贴到主图片
            rotated = char_img.rotate(angle, expand=1)
            image.paste(rotated, (x, y), rotated)
            
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
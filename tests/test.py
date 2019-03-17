from PIL import Image


def IsValidImage(img_path):
    """
    判断文件是否为有效（完整）的图片
    :param img_path:图片路径
    :return:True：有效 False：无效
    """
    bValid = True
    try:
        Image.open(img_path).verify()
    except:
        bValid = False
    return bValid


def transimg(img_path):
    """
    转换图片格式
    :param img_path:图片路径
    :return: True：成功 False：失败
    """
    if IsValidImage(img_path):
        try:
            str = img_path.rsplit(".", 1)
            output_img_path = str[0] + "a.jpg"
            print(output_img_path)
            im = Image.open(img_path)
            im = im.transpose(Image.ROTATE_270)
            im.save(output_img_path)
            return True
        except:
            return False
    else:
        return False


if __name__ == '__main__':
    img_path = r"C:\Users\lucycore\Desktop\3.jpg"
    print(transimg(img_path))

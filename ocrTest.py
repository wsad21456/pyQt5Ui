
# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
# --use_angle_cls true设置使用方向分类器识别180度旋转文字
import paddleOCR.paddleocr
def pic_ocr(img_path):
    if (img_path is not None) and (not ''.__eq__(img_path)) and (os.path.exists(img_path)):
        ocr = paddleOCR.paddleocr.PaddleOCR(use_angle_cls=True, lang="ch",
                                            use_gpu=True)  # need to run only once to download and load model into memory
        result = ocr.ocr(img_path)
        str_result = []
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                # print(line) # 全部内容
                str_result.append(line[1][0])
                # print(line[1][0]) # 识别结果内容
        return (','.join(str_result))
    else:
        return ''

import requests
import os.path
def download_url(url):
    if url is None or "".__eq__(url) or "nan".__eq__(url) or "NaT".__eq__(url):
        print('地址为空')
        return ''
    file_name = url.split('/')[-1]
    print(file_name)
    if not os.path.exists("./download_imgs"):
        os.makedirs("./download_imgs")
        print('创建文件夹成功')
    # 写入图片
    if os.path.exists("./download_imgs/" + file_name):
        print('文件已存在')
    else:
        # 下载图片
        try:
            r = requests.get(url)
        except Exception:
            return ''
        with open("./download_imgs/" + file_name, "wb") as f:
            f.write(r.content)
            print("下载完成")
    return "./download_imgs/" + file_name


# 显示结果(转成图片结果)
# from PIL import Image
# result = result[0]
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = paddleOCR.paddleocr.draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')

#PDF识别结果
# ocr = paddleOCR.paddleocr.PaddleOCR(use_angle_cls=True, lang="ch", page_num=2)  # need to run only once to download and load model into memory
# img_path = './xxx.pdf'
# result = ocr.ocr(img_path, cls=True)
# for idx in range(len(result)):
#     res = result[idx]
#     for line in res:
#         print(line)

# 程序入口
if __name__ == '__main__':
    path = download_url('http://antpython.net/static/pubdatas/webspider/goodimgs/1.jpeg')
    result_str = pic_ocr(path)
    print(result_str)
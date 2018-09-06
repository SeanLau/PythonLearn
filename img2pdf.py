# !/usr/bin/env python
# _*_ encoding:utf-8_*_

import os
import time

from PIL import Image
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from reportlab.pdfgen import canvas


def get_sub_img(imgs, page_size=(0, 1440)):
    """
    # 用PIL模块分割图片，只做纵向裁切
    :param imgs: image urls to be cropped.
    :param page_size 图片裁切尺寸
    :return: urls of sub images.
    """
    if not imgs:
        return
    crop_image_urls = []
    for img in imgs:
        image_file = os.path.basename(img)
        im = Image.open(img)
        size = im.size
        print(size)
        page_count = size[1] // page_size[1]
        if size[1] % page_size[1]:
            page_count += 1
        for i in range(page_count):
            y_coordinate = (i + 1) * page_size[1]
            if y_coordinate > size[1]:
                y_coordinate = size[1]
            crop_image_url = img.replace(image_file, "") + "%s_crop_" % i + image_file
            im.crop((0, i * page_size[1], size[0], y_coordinate)).save(crop_image_url, "jpeg")
            crop_image_urls.append(crop_image_url)
            # im.crop((0, i * page_size[1], size[0], y_coordinate)).save(
            #     "C:\\Users\\sean\\PycharmProjects\\new_start\\%s.jpg" % i, "jpeg")
    print("切分图片完成！")
    return crop_image_urls


def img2pdf(img_path):
    im = Image.open(img_path)
    w, h = im.size
    pdf_path = img_path.replace("jpg", "pdf")
    c = canvas.Canvas(pdf_path, pagesize=(w, h))
    c.drawImage(img_path, 0, 0, w, h)
    c.showPage()
    c.save()


def merge_pdf(pdfs, outFile):
    # filepath = "C:\\Users\\sean\\PycharmProjects\\new_start\\%s.pdf"
    # outFile = "C:\\Users\\sean\\PycharmProjects\\new_start\\test.pdf"
    pdf_writer = PdfFileWriter()
    for i in pdfs:
        pdf_reader = PdfFileReader(open(i.replace("jpg", "pdf"), "rb"))
        numPages = pdf_reader.getNumPages()
        for j in range(numPages):
            pageObj = pdf_reader.getPage(j)
            pdf_writer.addPage(pageObj)
        pdf_writer.write(open(outFile, "wb"))


def clear_images(image_urls):
    """
    删除临时文件
    :param image:
    :return: None
    """
    for image in image_urls:
        if os.path.exists(image):
            os.remove(image)
            print("正在删除", image)
    time.sleep(2)
    # 面临的问题，合并完pdf文件后，临时的pdf文件无法清除
    # for image in image_urls:
    #     pdf = image.replace("jpg", "pdf")
    #     if os.path.exists(pdf):
    #         os.remove(pdf)
    #         print("正在删除", pdf)


if __name__ == '__main__':
    image_file = ["C:\\Users\\sean\\PycharmProjects\\new_start\\01.jpg",
                  "C:\\Users\\sean\\PycharmProjects\\new_start\\02.jpg"]
    sub_images = get_sub_img(image_file)
    for img in sub_images:
        img2pdf(img)
        print("生成pdf:%s", img)
    print("生成pdf完成")

    # 合并, sub_images' filename just have different extends name 'pdf'
    merge_pdf(sub_images, "技术本质.pdf")
    clear_images(sub_images)  # 清理中间文件

# -*- coding:utf-8 -*-
import numpy as np
import os
from pyheatmap.heatmap import HeatMap
from PIL import Image


def save_heatmap(density_map, blob, imgs_dir, output_dir, down_sample=True):
    """
    生成热力图并保存
    :param density_map: 2d-array, 密度图
    :param blob: dict
    :param imgs_dir: 图片目录
    :param output_dir: 结果保存目录
    :param down_sample: bool, 是否有下采样
    :return:
    """
    img = blob['data']  # 图片数组, shape(h, w, 1)
    img_name = blob['fname']  # 图片文件名
    print('generating heatmap for', img_name)

    # 如果密度图进行下采样4倍, 则需要还原到原始大小
    if down_sample:
        den_resized = np.zeros((density_map.shape[0] * 4, density_map.shape[1] * 4))
        for i in range(den_resized.shape[0]):
            for j in range(den_resized.shape[1]):
                den_resized[i][j] = density_map[int(i / 4)][int(j / 4)] / 16
        density_map = den_resized

    h, w = img.shape[:2]
    density_map = density_map * 1000
    data = []
    for row in range(h):
        for col in range(w):
            for k in range(int(density_map[row][col])):
                data.append([col + 1, row + 1])
    # 生成heatmap
    hm = HeatMap(data)
    # 保存heatmap
    hm_name = 'heatmap_'+img_name.split('.')[0]+'.png'
    hm.heatmap(save_as=os.path.join(output_dir, hm_name))

    # 使用蓝色填充heatmap背景
    im = Image.open(os.path.join(output_dir, hm_name))
    x, y = im.size
    bg = Image.new('RGBA', im.size, (0, 0, 139))
    bg.paste(im, (0, 0, x, y), im)
    bg.save(os.path.join(output_dir, hm_name))

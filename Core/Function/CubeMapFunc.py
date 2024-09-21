import math

import os
import moderngl as mgl
import numpy

import Core as core
import Core.Utils.texture_utils as tu
import Core.Utils.comput_shader_utils as csu
import Core.Utils.image_utils as iu


def pic_list_to_cube(context: mgl.Context, file_list: [str]):
    if len(file_list) >= 1:
        img_list = []
        size = 0
        for i in range(0, 6):
            idx = min(len(file_list) - 1, i)
            file = file_list[idx]
            if not os.path.exists(file) and not os.path.isfile(file):
                raise Exception("Image Path Error")
            img = iu.read_img(file)
            w, h, _ = img.shape
            if w != h:
                raise Exception('Image Size Error: width={} height = {}'.format(w, h))
            if size == 0:
                size = w
            else:
                if size != w:
                    raise Exception('Image Size Error: width={} height = {}'.format(w, h))
            img_list.append(img)
        tex_cube = context.texture_cube(size=(size, size), components=4, dtype='f4')
        for idx, img in enumerate(img_list):
            data = tu.any_to_rgba32(img)
            tex_cube.write(idx, data.tobytes())
        return tex_cube
    return None


def one_pic_to_cube(context: mgl.Context, file: str):
    if os.path.exists(file) and os.path.isfile(file):
        img = iu.read_img(file)
        w, h, _ = img.shape
        if w != h:
            raise Exception('Image Size Error: width={} height = {}'.format(w, h))
        tex_cube = context.texture_cube(size=(w, h), components=4, dtype='f4')
        for i in range(0, 6):
            data = tu.any_to_rgba32(img)
            tex_cube.write(i, data.tobytes())
        return tex_cube
    return None


def cube_to_panorama(context: mgl.Context, tex_cube, save_path):
    tex_cube.use(0)
    shader_path = os.getcwd() + "\\Shader\\CubeToPanorama.glsl"
    cs = csu.create_compute_shader(context, shader_path)
    tex_out = tu.create_texture_with_color(context, width=tex_cube.size[0] * 4, height=tex_cube.size[1] * 2)
    tex_out.bind_to_image(1)
    cs.run(math.ceil(tex_out.size[0] / 16), math.ceil(tex_out.size[1] / 16), 1)
    img = tu.texture_to_img(tex_out)
    iu.save_img(save_path, img)
    cs.release()
    tex_cube.release()
    tex_out.release()


def renderdoc_grid_to_texture_cube(context: mgl.Context, file: str):
    grid_img = iu.read_img(file)

    row, column, _ = grid_img.shape
    if row / column != 6:
        raise Exception('Image Size Error')
    data_list = numpy.split(grid_img, row / column)
    tex_cube = context.texture_cube(size=(column, column), components=4, dtype='f4')
    for i in range(0, len(data_list)):
        data = data_list[i]
        data = numpy.flipud(data)
        data = tu.any_to_rgba32(data)
        tex_cube.write(i, data.tobytes())
    return tex_cube


def renderdoc_grid_to_panorama(src: str, dst: str):
    context = core.create_contex_standalone()
    tex_cube = renderdoc_grid_to_texture_cube(context, src)
    tex_cube.use(0)
    shader_path = os.getcwd() + "\\Shader\\CubeToPanorama.glsl"
    cs = csu.create_compute_shader(context, shader_path)
    tex_out = tu.create_texture_with_color(context, width=tex_cube.size[0] * 2, height=tex_cube.size[1] * 1)
    tex_out.bind_to_image(1)
    cs.run(math.ceil(tex_out.size[0] / 16), math.ceil(tex_out.size[1] / 16), 1)
    img = tu.texture_to_img(tex_out)
    iu.save_img(dst, img)
    cs.release()
    tex_cube.release()
    tex_out.release()
    context.release()

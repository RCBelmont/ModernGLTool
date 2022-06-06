import math

from Utils.graphic_utils import *


def renderdoc_grid_to_texture_cube(context: mgl.Context, file: str):
    grid_img = read_img(file)
    row, column, _ = grid_img.shape
    if row / column != 6:
        raise Exception('Image Size Error')
    data_list = numpy.split(grid_img, row / column)
    tex_cube = context.texture_cube(size=(column, column), components=4, dtype='f4')
    for i in range(0, len(data_list)):
        data = data_list[i]
        data = any_to_rgba32(data)
        tex_cube.write(i, data.tobytes())
    return tex_cube


def renderdoc_grid_to_panorama(src: str, dst: str):
    context = create_contex_standalone()
    tex_cube = renderdoc_grid_to_texture_cube(context, src)
    tex_cube.use(0)
    shader_path = os.getcwd() + "\\Shader\\CubeToPanorama.glsl"
    cs = create_compute_shader(context, shader_path)
    tex_out = create_texture_with_color(context, width=tex_cube.size[0] * 4, height=tex_cube.size[1] * 2)
    tex_out.bind_to_image(1)
    cs.run(math.ceil(tex_out.size[0] / 16), math.ceil(tex_out.size[1] / 16), 1)
    img = texture_to_img(tex_out)
    save_img(dst, img)
    cs.release()
    tex_cube.release()
    tex_out.release()
    context.release()

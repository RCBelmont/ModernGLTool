import math

from Utils.graphic_utils import *


def gen_initial_data():
    for i in range(5):
        yield 1
        yield 2
        yield 3
        yield 4
        yield 5


def gen_blender_film_data():
    context = create_contex_standalone()

    shader_path = os.getcwd() + "\\Shader\\UEFilmToBlender.glsl"
    cs = create_compute_shader(context, shader_path)
    data_count = 2 * 2 * 2
    compute_data = numpy.empty([data_count * 9], dtype='float32', order='C')
    buffer = context.buffer(compute_data)
    buffer.bind_to_storage_buffer(0)
    cs.run(math.ceil(data_count / 256), 1, 1)

    cs.release()
    context.release()

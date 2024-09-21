"""
FILE_NAME: GenerateColorBoard.py
AUTHOR: RCB
CREATED: 2024/8/5-11:49
DESC: 
"""
import os
import Core as core
import Core.Utils.comput_shader_utils as csu
import Core.Utils.image_utils as iu
import Core.Utils.texture_utils as tu
import numpy as np

if __name__ == '__main__':
    sh_list_use = [0] * 4 * 6 * 6
    colors = []
    colors.append((0, 0, 0))
    colors.append((0.1, 0.1, 0.1))
    colors.append((0.28, 0.28, 0.28))
    colors.append((0.5, 0.5, 0.5))
    colors.append((0.75, 0.75, 0.75))
    colors.append((1, 1, 1))

    colors.append((0.2, 0.5, 0.1))
    colors.append((0.0, 0.5, 0.8))
    colors.append((0.1, 0.2, 0.7))
    colors.append((0.5, 0.2, 0.5))
    colors.append((0.75, 0.1, 0.2))
    colors.append((0.5, 0.5, 0))

    colors.append((0.0, 0.5, 0.45))
    colors.append((0.2, 0.2, 0.4))
    colors.append((0.25, 0.07, 0.04))
    colors.append((0.2, 0.8, 0.3))
    colors.append((0.75, 0.5, 0.1))
    colors.append((0.0, 0.5, 0))

    colors.append((0.2, 0.0, 0.0))
    colors.append((0.8, 0.0, 0.0))
    colors.append((0.0, 0.0, 0.28))
    colors.append((0.1, 0.2, 0.1))
    colors.append((0.6, 0.2, 0.1))
    colors.append((0.8, 0.8, 0))

    colors.append((0.53906, 0.26953, 0.21484))
    colors.append((0.8125, 0.40234, 0.33594))
    colors.append((0.97656, 0.67969, 0.5625))
    colors.append((0.22656, 0.08105, 0.07227))
    colors.append((0.875, 0.63281, 0.5))
    colors.append((0.33984, 0.16797, 0.14063))

    colors.append((0.28125, 0.18555, 0.19141))
    colors.append((0.91406, 0.46484, 0.3125))
    colors.append((0.99219, 0.70313, 0.60938))
    colors.append((0.77344, 0.60156, 0.75))
    colors.append((0.57031, 0.44141, 0.53125))
    colors.append((0.48047, 0.52344, 0.76563))

    for i in range(0, 36):
        sh_list_use[i * 4 + 0] = colors[i][0]
        sh_list_use[i * 4 + 1] = colors[i][1]
        sh_list_use[i * 4 + 2] = colors[i][2]
        sh_list_use[i * 4 + 3] = 1

    context = core.create_contex_standalone()
    cs = csu.create_compute_shader(context, os.path.dirname(__file__) + '\\GenerateColorBoard.glsl')

    dst_texture = tu.create_texture_with_color(context, width=64*6, height=64*6)
    dst_texture.bind_to_image(0)

    sh_buffer = context.buffer(np.array(sh_list_use, dtype=np.float32))
    sh_buffer.bind_to_storage_buffer(0)

    cs.run(int(dst_texture.width / 16), int(dst_texture.height / 16), 1)

    save_img = tu.texture_to_img(dst_texture)

    iu.show_img([save_img])

    iu.save_img(r"D:\User\Downloads\ColorBoard.TGA", save_img)

    idx = 0
    for c in colors:
        print("//SV_Target0.rgb = vec3(%f, %f, %f);//%f" % (c[0], c[1], c[2], int(idx)))
        idx += 1


"""
FILE_NAME: RGB_LabConvert.py
AUTHOR: RCB
CREATED: 2024/8/26-14:40
DESC: 
"""

import os

import numpy as np

import Core as core
import Core.Utils.comput_shader_utils as csu
import Core.Utils.image_utils as iu
import Core.Utils.texture_utils as tu

if __name__ == '__main__':
    context = core.create_contex_standalone()
    cs = csu.create_compute_shader(context, os.path.dirname(__file__) + '\\RGB_LabConvert.glsl')
    dst_texture = tu.create_texture_with_color(context, width=64, height=64)
    dst_texture.bind_to_image(1, read=True, write=True)
    cs["srcColor"] = (1,1,1,0)
    ##cs["srcColor"] = (0.65,0,1,0)

    out_array = np.zeros(4*2, dtype=np.float32)
    out_buffer = context.buffer(out_array)
    out_buffer.bind_to_storage_buffer(1)
    cs.run(int(1), 1, 1)

    out_buffer.read_into(out_array)
    ##TODO:DELETE
    print(out_array[0:4])
    print("({:.2f},{:.2f},{:.2f})".format(out_array[1],out_array[2],out_array[0]))


    ##print(out_array[4:8])
    ##TODO:DELETE
    print((0.22*255,0.36*255,0.2*255,0) )
    

    #cs.run(int(dst_texture.width / 16), int(dst_texture.height / 16), 1)
    # save_img = tu.texture_to_img(dst_texture)
    # iu.show_img([save_img])


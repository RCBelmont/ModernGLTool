import os
from PIL import Image
import moderngl as mgl


from Utils.graphic_utils import *


def main():
    shader_path = './Shader/Test.glsl'

    context = create_contex_standalone()
    #cs = create_compute_shader(context, shader_path)
    img_path = "D:\\PC\\Pictures\\belfast_sunset_1k.hdr"
    img_path = "D:\\PC\\Pictures\\Test.jpg"
    create_texture(context, img_path)
    # f = open("./Shader/Test.glsl")
    # shaderCode = f.read()
    #
    # ctx = mgl.create_context(require=430, standalone=True)
    # print(ctx)
    # cs = ctx.compute_shader(shaderCode)
    # cs['destTex'] = 0
    # texDist = ctx.texture((256, 256), 4)
    # texDist.filter = mgl.NEAREST, mgl.NEAREST
    # texDist.bind_to_image(0, read=False, write=True)
    # Image.open("")
    # texSource = ctx.texture()
    # cs.run(int(256 / 16), int(256 / 16))



if __name__ == '__main__':
    main()

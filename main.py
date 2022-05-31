import math
import os
import moderngl as mgl
import numpy

from Utils.graphic_utils import *


def main():
    shader_path = './Shader/Test.glsl'

    context = create_contex_standalone()
    cs = create_compute_shader(context, shader_path)
    texSource = create_texture_with_img(context, "./TestImage/Test.exr")
    texSource.bind_to_image(0)
    texDist = create_texture_with_color(context, texSource.size[0], texSource.size[1], init_color=(1,0,0,1))
    texDist.bind_to_image(1)
    cs.run(math.ceil(texSource.size[0] / 16), math.ceil(texSource.size[1] / 16), 1)
    img = texture_to_img(texDist)
    save_img("./OutPut/AFAF.png", img)
    cs.release()
    texDist.release()
    texSource.release()
    context.release()

    
    # texDist = create_texture_with_color(context, width=512, height=128, init_color=(1, 0, 0, 1))
    # texDist.bind_to_image(0, read=True, write=True)
    # texDist.filter = mgl.NEAREST, mgl.NEAREST

    #cs.run(math.ceil(texDist.size[0] / 1), math.ceil(texDist.size[1] / 1), 1)
    
    ##screate_texture(context, img_path)
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


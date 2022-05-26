import os
from PIL import Image
import moderngl as mgl


def main():
    f = open("./Shader/Test.glsl")
    shaderCode = f.read()

    ctx = mgl.create_context(require=430, standalone=True)
    print(ctx)
    cs = ctx.compute_shader(shaderCode)
    cs['destTex'] = 0
    texDist = ctx.texture((256, 256), 4)
    texDist.filter = mgl.NEAREST, mgl.NEAREST
    texDist.bind_to_image(0, read=False, write=True)
    Image.open("")
    texSource = ctx.texture()
    cs.run(int(256 / 16), int(256 / 16))



if __name__ == '__main__':
    main()

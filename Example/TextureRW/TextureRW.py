"""
FILE_NAME: TextureRW.py
AUTHOR: RCB
CREATED: 2024/4/29-10:20
DESC: 
"""
import os.path

import Core as core
import Core.Utils.comput_shader_utils as csu

if __name__ == "__main__":
    context = core.create_contex_standalone()
    shader_path = os.path.dirname(__file__) + '\\TextureRW.glsl'
    cs = csu.create_compute_shader(context, shader_path)


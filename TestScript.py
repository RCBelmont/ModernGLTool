"""
FILE_NAME: TestScript.py
AUTHOR: RCB
CREATED: 2024/4/28-18:07
DESC: 用来测试的脚本
"""
import os

import Core as core
import Core.Utils.texture_utils as tu
import Core.Utils.comput_shader_utils as csu
import Core.Utils.config_utils as cu
if __name__ == '__main__':
    context = core.create_contex_standalone()
    cmgr = cu.get_config_utils_mgr()
    shader_path = cmgr.get_shader_path('Test\\TextureBindTest.glsl')
    cs = csu.create_compute_shader(context, shader_path)




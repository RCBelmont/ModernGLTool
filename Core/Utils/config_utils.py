"""
FILE_NAME: config_utils.py
AUTHOR: RCB
CREATED: 2024/4/28-18:11
DESC:管理一些默认配置
"""

import sys
import os


class ConfigUtilsMgr:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigUtilsMgr, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.DEFAULT_SHADER_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Shaders')

    def get_shader_root(self) -> str:
        return self.DEFAULT_SHADER_ROOT

    def get_shader_path(self, shader_name: str) -> str:
        if not shader_name.endswith('.glsl'):
            raise Exception('Shader文件名必须以.glsl结尾 {} 不正确'.format(shader_name))
        shader_path = os.path.join(self.DEFAULT_SHADER_ROOT, shader_name)
        if not os.path.exists(shader_path):
            raise Exception('Shader文件不存在：{}'.format(shader_path))
        return os.path.join(self.DEFAULT_SHADER_ROOT, shader_name)

def get_config_utils_mgr() -> ConfigUtilsMgr:
    return ConfigUtilsMgr()
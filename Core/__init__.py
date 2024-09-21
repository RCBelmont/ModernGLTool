"""
FILE_NAME: __init__.py.py
AUTHOR: RCB
CREATED: 2024/4/28-14:26
DESC: 
"""
import sys
import os
import moderngl as mgl

os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '1'
root_path = os.path.dirname(__file__)
if os.path.exists(root_path):
    sys.path.append(root_path)
    for d in os.listdir(root_path):
        full_path = os.path.join(root_path, d)
        if os.path.isdir(full_path):
            sys.path.append(full_path)


def create_contex_standalone(gl_version=430) -> mgl.Context:
    '''
    创建一个独立的ModernGL上下文
    :return: ModernGL上下文
    '''
    return mgl.create_context(require=gl_version, standalone=True)

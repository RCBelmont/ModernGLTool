"""
FILE_NAME: SHToCurve.py
AUTHOR: RCB
CREATED: 2024/7/16-12:24
DESC: 
"""
import os
import Core as core
import Core.Utils.comput_shader_utils as csu
import numpy as np

if __name__ == '__main__':
    slice = 5
    sh_param = "(0.921877,-0.328396,-0.542527,0.009874,-0.005833,0.381935,0.650007,-0.019262,0.085069,0.979919,-0.319365,-0.492302,0.024662,0.001779,0.371323,0.669136,-0.016486,0.051657,1.065387,-0.304428,-0.403395,0.059226,0.009017,0.361971,0.668756,0.012858,0.077494)"
    sh_list = [float(i) for i in sh_param[1:-1].split(",")]

    sqrtPI = 1.77245385091
    c0 = 1.0 / (2 * sqrtPI)
    c1 = 1.73205080757 / (3 * sqrtPI)
    c2 = 3.87298334621 / (8 * sqrtPI)
    c3 = 2.2360679775 / (16 * sqrtPI)
    c4 = 0.5 * c2

    context = core.create_contex_standalone()
    cs = csu.create_compute_shader(context, os.path.dirname(__file__) + '\\SHToCurve.glsl')

    sh_list_use = [0] * 4 * 7

    sh_list_use[int(0 * 4 + 0)] = -c1 * sh_list[3]
    sh_list_use[int(0 * 4 + 1)] = -c1 * sh_list[1]
    sh_list_use[int(0 * 4 + 2)] = c1 * sh_list[2]
    sh_list_use[int(0 * 4 + 3)] = c0 * sh_list[0] - c3 * sh_list[6]

    sh_list_use[int(1 * 4 + 0)] = sh_list[9 + 3] * -c1
    sh_list_use[int(1 * 4 + 1)] = sh_list[9 + 1] * -c1
    sh_list_use[int(1 * 4 + 2)] = sh_list[9 + 2] * c1
    sh_list_use[int(1 * 4 + 3)] = sh_list[9 + 0] * c0 - sh_list[9 + 6] * c3

    sh_list_use[int(2 * 4 + 0)] = sh_list[9 * 2 + 3] * -c1
    sh_list_use[int(2 * 4 + 1)] = sh_list[9 * 2 + 1] * -c1
    sh_list_use[int(2 * 4 + 2)] = sh_list[9 * 2 + 2] * c1
    sh_list_use[int(2 * 4 + 3)] = sh_list[9 * 2 + 0] * c0 - sh_list[9 * 2 + 6] * c3

    sh_list_use[int(3 * 4 + 0)] = sh_list[4] * c2
    sh_list_use[int(3 * 4 + 1)] = sh_list[5] * -c2
    sh_list_use[int(3 * 4 + 2)] = sh_list[6] * 3 * c3
    sh_list_use[int(3 * 4 + 3)] = sh_list[7] * -c2

    sh_list_use[int(4 * 4 + 0)] = sh_list[9 + 4] * c2
    sh_list_use[int(4 * 4 + 1)] = sh_list[9 + 5] * -c2
    sh_list_use[int(4 * 4 + 2)] = sh_list[9 + 6] * 3 * c3
    sh_list_use[int(4 * 4 + 3)] = sh_list[9 + 7] * -c2

    sh_list_use[int(5 * 4 + 0)] = sh_list[9 * 2 + 4] * c2
    sh_list_use[int(5 * 4 + 1)] = sh_list[9 * 2 + 5] * -c2
    sh_list_use[int(5 * 4 + 2)] = sh_list[9 * 2 + 6] * 3 * c3
    sh_list_use[int(5 * 4 + 3)] = sh_list[9 * 2 + 7] * -c2

    sh_list_use[int(6 * 4 + 0)] = sh_list[8] * c4
    sh_list_use[int(6 * 4 + 1)] = sh_list[9 + 8] * c4
    sh_list_use[int(6 * 4 + 2)] = sh_list[9 * 2 + 8] * c4
    sh_list_use[int(6 * 4 + 3)] = 1
    
    sh_buffer = context.buffer(np.array(sh_list_use, dtype=np.float32))
    sh_buffer.bind_to_storage_buffer(0)

    

    out_array = np.zeros(slice * 4, dtype=np.float32)
    out_buffer = context.buffer(out_array)
    out_buffer.bind_to_storage_buffer(1)
    cs.run(int(1), 1, 1)
    out_buffer.read_into(out_array)

    str = ""
    for i in range(0, slice):
        str += f"{out_array[i * 4 + 3]},{out_array[i * 4 + 0]},{out_array[i * 4 + 1]},{out_array[i * 4 + 2]}, 1.0\n"

    with open(r"D:\User\Downloads\shCurve\shCurve.csv", "w") as f:
        f.write(str)
    

"""
FILE_NAME: GenOpacityAvatar.py
AUTHOR: RCB
CREATED: 2024/9/18-17:45
DESC: 
"""

import tkinter as tk
from tkinter import ttk
import os
from lib2to3.fixes.fix_input import context
from tkinter import filedialog

import Core as core
import Core.Utils.comput_shader_utils as csu
import Core.Utils.image_utils as iu
import Core.Utils.texture_utils as tu

context = None
com_shader = None
src_path = None
mask_path = None
out_path = None
progress_bar = None
ui_root = None
progress_label = None

def run():
    src_p = src_path.get()
    dst_p = out_path.get()
    if src_p and dst_p:
        if os.path.exists(src_p) and os.path.isdir(src_p):
            file_list = []
            for root, dirs, files in os.walk(src_p):
                for file in files:
                    if file.lower().endswith(('.jpg', '.png', '.tga')) and '_mask' not in file:
                        src_file = os.path.join(root, file)
                        mask_file = os.path.join(root, file.split('.')[0] + '_mask.' + file.split('.')[1])
                        if os.path.exists(mask_file):
                            file_list.append((src_file, mask_file))
            os.makedirs(dst_p, exist_ok=True)
            total_files = len(file_list)
            for idx, (src_file, mask_file) in enumerate(file_list):
                src_texture = tu.create_texture_with_img(context, src_file)
                mask_texture = tu.create_texture_with_img(context, mask_file)
                dst_texture = tu.create_texture_with_color(context, width=src_texture.width, height=src_texture.height)
                if 'srcTex' in com_shader:
                    com_shader['srcTex'] = 0
                if 'maskTex' in com_shader:
                    com_shader['maskTex'] = 1
                src_texture.use(location=0)
                mask_texture.use(location=1)
                dst_texture.bind_to_image(1, read=True, write=True)
                com_shader.run(int(dst_texture.width / 16), int(dst_texture.height / 16), 1)
                save_img = tu.texture_to_img(dst_texture)
                iu.save_img(os.path.join(dst_p, os.path.basename(src_file)), save_img)
                progress = (idx + 1.0) / total_files * 100.0
                progress_bar['value'] = progress
                progress_label.config(text=f"Progress: {progress:.2f}%")
                ui_root.update_idletasks()

    pass


def select_dir(entry):
    file_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def create_window():
    global progress_label, ui_root, src_path, mask_path, out_path, submit_button, context, com_shader,progress_bar
    ui_root = tk.Tk()
    ui_root.title("Create Opacity Avatar")
    ui_root.geometry("900x200")

    frame = tk.Frame(ui_root)
    frame.pack(anchor='w')

    label1 = tk.Label(frame, text="原始路径")
    label1.pack(side=tk.LEFT)
    src_path = tk.Entry(frame, width=30)
    src_path.pack(side=tk.LEFT)
    button1 = tk.Button(frame, text="选择文件", command=lambda: select_dir(src_path))
    button1.pack(side=tk.LEFT)

    frame = tk.Frame(ui_root)
    frame.pack(anchor='w')
    # 创建标签和输入框以获取路径2，以及一个选择文件的按钮
    label2 = tk.Label(frame, text="输出路径")
    label2.pack(side=tk.LEFT)
    out_path = tk.Entry(frame, width=30)
    out_path.pack(side=tk.LEFT)
    button2 = tk.Button(frame, text="选择文件", command=lambda: select_dir(out_path))
    button2.pack(side=tk.LEFT)

    submit_button = tk.Button(ui_root, text="生成", command=run, width=30)
    submit_button.pack()

    progress_bar = ttk.Progressbar(ui_root, orient='horizontal', length=300, mode='determinate')
    progress_bar.pack(pady=10)
    progress_label = tk.Label(ui_root, text="Progress: 0.00%")
    progress_label.pack()

    context = core.create_contex_standalone()
    ##com_shader = csu.create_compute_shader(context, os.path.dirname(__file__) + '\\Shaders\\OpacityAvatar.glsl')
    label_test = tk.Label(ui_root, text=os.getcwd() + "   " + __file__)
    label_test.pack(side=tk.LEFT)
    # Run the main event loop
    ui_root.mainloop()


if __name__ == '__main__':
    create_window()
    pass

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

# 初始化窗口
root = tk.Tk()
root.title("功能选择界面")
root.geometry("800x600")

# ----------- 工具函数 -----------

def switch_frame(to_show):
    """切换显示的界面"""
    for frame in [menu_frame, style_transfer_frame]:
        frame.pack_forget()
    to_show.pack(fill="both", expand=True)

# ----------- 主菜单 Frame -----------

def create_menu_frame():
    """创建主菜单界面"""
    menu_frame = tk.Frame(root)
    tk.Label(menu_frame, text="请选择功能", font=("Arial", 24)).pack(pady=50)
    tk.Button(menu_frame, text="风格转换功能", font=("Arial", 16), command=lambda: switch_frame(style_transfer_frame)).pack()
    return menu_frame

# ----------- 风格转换 Frame -----------

def create_style_transfer_frame():
    """创建风格转换功能界面"""
    style_transfer_frame = tk.Frame(root)

    # 返回按钮
    tk.Button(style_transfer_frame, text="← 返回主菜单", font=("Arial", 12), command=lambda: switch_frame(menu_frame)).pack(anchor="nw", padx=10, pady=10)

    # 中部区域容器
    middle_frame = tk.Frame(style_transfer_frame)
    middle_frame.pack(pady=10)

    # 左侧：源图像选择
    left_panel = tk.Frame(middle_frame)
    tk.Label(left_panel, text="选择源图像", font=("Arial", 14)).pack(pady=5)
    tk.OptionMenu(left_panel, source_label_var, *label_options).pack(pady=5)
    tk.Entry(left_panel, textvariable=transfer_source_image_path, width=40).pack(pady=5)

    # 新建并挂载预览框
    source_preview_label = tk.Label(left_panel)
    source_preview_label.pack(pady=5)
    tk.Button(left_panel, text="浏览",
              command=lambda: browse_image(transfer_source_image_path, source_preview_label)).pack(pady=5)
    left_panel.pack(side="left", padx=20)

    # 右侧：参考图像选择
    right_panel = tk.Frame(middle_frame)
    tk.Label(right_panel, text="选择参考图像", font=("Arial", 14)).pack(pady=5)
    tk.OptionMenu(right_panel, reference_label_var, *label_options).pack(pady=5)
    tk.Entry(right_panel, textvariable=transfer_reference_image_path, width=40).pack(pady=5)

    reference_preview_label = tk.Label(right_panel)
    reference_preview_label.pack(pady=5)
    tk.Button(right_panel, text="浏览",
              command=lambda: browse_image(transfer_reference_image_path, reference_preview_label)).pack(pady=5)
    right_panel.pack(side="left", padx=20)

    # 上传按钮
    tk.Button(style_transfer_frame, text="上传并执行", font=("Arial", 14), command=lambda: upload_images()).pack(pady=20)

    # 状态提示
    transfer_status_label = tk.Label(style_transfer_frame, text="", font=("Arial", 12))
    transfer_status_label.pack(pady=10)

    return style_transfer_frame, transfer_status_label

def create_image_selection_panel(parent, label_text, path_var, preview_label):
    """创建图像选择的左侧或右侧面板"""
    panel = tk.Frame(parent)
    tk.Label(panel, text=label_text, font=("Arial", 14)).pack(pady=5)
    tk.Entry(panel, textvariable=path_var, width=40).pack(pady=5)
    tk.Button(panel, text="浏览", command=lambda: browse_image(path_var, preview_label)).pack(pady=5)
    preview_label = tk.Label(panel)
    preview_label.pack(pady=5)
    return panel

# ----------- 功能函数 -----------

def browse_image(path_var, preview_label):
    """浏览并选择图像文件"""
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        path_var.set(file_path)
        show_image_preview(file_path, preview_label)

def show_image_preview(file_path, label):
    """显示图像预览"""
    try:
        img = Image.open(file_path)
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        label.configure(image=img_tk)
        label.image = img_tk
    except Exception as e:
        messagebox.showerror("错误", f"图像加载失败：{e}")

def upload_images():
    """上传图像并执行风格转换"""
    transfer_status_label.config(text="风格转换中...", fg="blue")
    root.update_idletasks()

    try:
        # TODO 实验室局域网
        url = "http://192.168.1.117:8000/style-transfer"  # 修改为你的实际 API 地址
        files = {
            "source": open(transfer_source_image_path.get(), "rb"),
            "reference": open(transfer_reference_image_path.get(), "rb")
        }
        data = {
            "source_label": source_label_var.get(),
            "reference_label": reference_label_var.get()
        }
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            transfer_status_label.config(text="转换完成 ✔", fg="green")
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img.show()  # 弹出图片查看器
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if save_path:
                img.save(save_path)
        else:
            transfer_status_label.config(text="转换失败 ❌", fg="red")
    except Exception as e:
        transfer_status_label.config(text=f"请求失败：{e}", fg="red")

# ----------- 初始化界面 -----------

# 在这里定义保存图像路径的 StringVar
transfer_source_image_path = tk.StringVar()
transfer_reference_image_path = tk.StringVar()

# 定义预览标签
transfer_source_preview = tk.Label()
transfer_reference_preview = tk.Label()

# 标签选项
label_options = ["dress", "pant", "short"]

# 存储标签选择
source_label_var = tk.StringVar(value=label_options[0])
reference_label_var = tk.StringVar(value=label_options[0])

# 初始化功能界面
menu_frame = create_menu_frame()
style_transfer_frame, transfer_status_label = create_style_transfer_frame()

# 启动主循环
switch_frame(menu_frame)
root.mainloop()

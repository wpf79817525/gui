#1.环境配置
##（1）创建Conda环境：
```
conda env create -f gui_env.yml
```
##（2）激活环境：
```
conda activate gui_env
```
#2.启动UI应用
```
python main.py
```
#3.添加自定义UI（扩展UI）
##（1）添加功能入口按钮
在 create_menu_frame() 函数中添加按钮，点击后切换到你的功能界面：
```
tk.Button(menu_frame, text="你的功能名", font=("Arial", 16), command=lambda: switch_frame(你的功能_frame)).pack()
```
##（2）创建你的功能 Frame
参考 create_style_transfer_frame() 函数，创建一个新的 Frame：
```
def create_my_feature_frame():
    frame = tk.Frame(root)
    tk.Button(frame, text="← 返回主菜单", command=lambda: switch_frame(menu_frame)).pack(anchor="nw")
    # 添加你的控件
    return frame
```
##（3）在主程序中初始化你的 Frame
在主程序中初始化你的功能界面：
```
my_feature_frame = create_my_feature_frame()
```
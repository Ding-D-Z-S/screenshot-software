import os
import time
import tkinter as tk
from tkinter import filedialog
import threading
from PIL import ImageGrab

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows截屏@叮当在上制作")
        self.root.geometry("640x350") # 设置窗口大小为640x300像素
        self.root.resizable(width=False, height=False)  # 禁止调整窗口大小

        # 提示标签
        self.prompt_label = tk.Label(self.root, text="注意设置间隔时间太短有高概率会吞图！（≥0.05）", fg="red", font=("Arial", 20, "bold"))
        self.prompt_label.pack(pady=5)
        self.prompt_label = tk.Label(self.root, text="请按下开始截图按钮开始截图。", fg="blue", font=("Arial", 15, "bold"))
        self.prompt_label.pack(pady=0)
        self.prompt_label = tk.Label(self.root, text="@叮当在上制作", fg="orange", font=("Arial", 10, "bold"))
        self.prompt_label.pack(pady=0)

        self.save_dir = tk.StringVar()
        self.save_dir.set(r"请选择你的储存位置")  # 默认保存目录

        self.interval_var = tk.DoubleVar()
        self.interval_var.set(1)  # 默认截图间隔（秒）

        self.total_screenshots_var = tk.IntVar()
        self.total_screenshots_var.set(5)  # 默认总截图次数

        self.is_screenshotting = False  # 增加标志，表示是否正在截图

        self.create_widgets()#初始化 ScreenshotApp 类的对象


        
    def create_widgets(self):
        # 左侧部分
        left_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, padx=10)

        # 保存目录
        tk.Label(left_frame, text="保存目录:").pack()
        self.save_dir_entry = tk.Entry(left_frame, textvariable=self.save_dir, width=40)
        self.save_dir_entry.pack()
        tk.Button(left_frame, text="浏览", command=self.browse_save_directory).pack()

        # 截图间隔
        tk.Label(left_frame, text="截图间隔（秒）:").pack()
        self.interval_entry = tk.Entry(left_frame, textvariable=self.interval_var, width=40)
        self.interval_entry.pack()

        # 总截图次数
        tk.Label(left_frame, text="总截图次数:").pack()
        self.total_screenshots_entry = tk.Entry(left_frame, textvariable=self.total_screenshots_var, width=40)
        self.total_screenshots_entry.pack()

        # 开始按钮
        tk.Button(left_frame, text="开始截图", command=self.start_screenshots_thread).pack()

        # 右侧部分（输出栏和滑动栏）
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, padx=10)

        # 输出栏
        self.output_text = tk.Text(right_frame, width=43, height=15, state=tk.DISABLED)
        self.output_text.pack(side=tk.LEFT)
        
        # 添加滑动栏
        self.scrollbar = tk.Scrollbar(right_frame, command=self.output_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=self.scrollbar.set)

        # 在输出栏初始化时插入默认信息
        initial_output = "*******************************************\n您好我是叮当在上！\n欢迎使用Windows截屏。\n注意设置间隔时间（≥0.05秒）\n别给我卡BUG！！！（破音）\n*******************************************\n"
        self.update_output(initial_output)

    def browse_save_directory(self):
        # 通过文件对话框选择保存目录
        self.save_dir.set(filedialog.askdirectory())

    def capture_screen(self, file_path):
        # 使用ImageGrab模块截取整个屏幕并保存图片
        screen = ImageGrab.grab()
        screen.save(file_path)

    def take_screenshots(self, total_screenshots, interval):
        # 截图线程
        save_dir = self.save_dir.get()

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for i in range(total_screenshots):
            if not self.is_screenshotting:
                break

            timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            file_name = f"{timestamp}.png"
            file_path = os.path.join(save_dir, file_name)
            self.capture_screen(file_path)

            # 输出保存目录和“开始截屏”的信息
            self.update_output(f"截屏保存至 {file_path}\n开始截屏\n")

            if i < total_screenshots - 1:
                time.sleep(interval)

        # 截图结束后输出“截屏结束”的信息，并启用按钮
        self.update_output("截屏结束\n")
        self.total_screenshots_entry.config(state=tk.NORMAL)

    def start_screenshots_thread(self):
        # 启动截图线程
        total_screenshots = self.total_screenshots_var.get()
        interval = self.interval_var.get()
        self.total_screenshots_entry.config(state=tk.DISABLED)  # 禁用按钮，防止截图过程中改变总截图次数
        threading.Thread(target=self.take_screenshots_thread, args=(total_screenshots, interval)).start()

    def take_screenshots_thread(self, total_screenshots, interval):
        # 截图线程
        self.is_screenshotting = True
        self.take_screenshots(total_screenshots, interval)
        self.is_screenshotting = False

    def update_output(self, message):
        # 更新输出栏
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, message)
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()

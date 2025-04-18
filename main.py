import os
import sys
import time
import subprocess
import multiprocessing
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout,
    QHBoxLayout, QWidget, QTextEdit, QLabel, QComboBox, QProgressBar
)
from PyQt5.QtCore import Qt, QRunnable, QThreadPool, QObject, pyqtSignal
try:
    import pynvml
except ImportError:
    pynvml = None


class FileProcessor(QRunnable):
    class Signals(QObject):
        log_signal = pyqtSignal(str, str)
        cmd_signal = pyqtSignal(str)
        finished_signal = pyqtSignal(str)

    def __init__(self, file_path, tool_path, model):
        super().__init__()
        self.file_path = file_path
        self.tool_path = tool_path
        self.model = model
        self.signals = self.Signals()

    def run(self):
        try:
            if not os.path.exists(self.tool_path):
                self.signals.log_signal.emit("超分辨率工具不存在，请检查路径", "red")
                self.signals.finished_signal.emit(self.file_path)
                return

            self.signals.log_signal.emit(f"开始处理文件: {self.file_path}", "yellow")
            dir_path = os.path.dirname(self.file_path)
            result_dir = os.path.join(dir_path, "超分辨率输出结果")
            os.makedirs(result_dir, exist_ok=True)
            name_only = os.path.splitext(os.path.basename(self.file_path))[0]
            result_name = f"{name_only}_4K".replace(" ", "_")
            output_path = os.path.join(result_dir, f"{result_name}.png")

            cmd = (
                f'"{self.tool_path}" '
                f'-i "{self.file_path}" '
                f'-o "{output_path}" '
                f'-n {self.model}'
            )
            self.signals.log_signal.emit(f"执行命令: {cmd}", "blue")

            process = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding="utf-8", errors="replace"
            )

            stdout_lines = []
            stderr_lines = []
            while process.poll() is None:
                stdout_line = process.stdout.readline()
                if stdout_line:
                    stdout_lines.append(stdout_line.strip())
                    self.signals.cmd_signal.emit(stdout_line.strip())
                stderr_line = process.stderr.readline()
                if stderr_line:
                    stderr_lines.append(stderr_line.strip())
                    self.signals.cmd_signal.emit(stderr_line.strip())
                time.sleep(0.01)

            stdout_remain, stderr_remain = process.communicate()
            if stdout_remain:
                stdout_lines.append(stdout_remain.strip())
                self.signals.cmd_signal.emit(stdout_remain.strip())
            if stderr_remain:
                stderr_lines.append(stderr_remain.strip())
                self.signals.cmd_signal.emit(stderr_remain.strip())

            if process.returncode == 0:
                self.signals.log_signal.emit(f"生成完毕，文件目录: {output_path}", "green")
            else:
                self.signals.log_signal.emit(f"命令失败，返回码: {process.returncode}", "red")
                if stderr_lines:
                    self.signals.log_signal.emit(f"错误输出: {''.join(stderr_lines)}", "red")
        except Exception as e:
            self.signals.log_signal.emit(f"处理文件 {self.file_path} 时出错: {e}", "red")

        self.signals.finished_signal.emit(self.file_path)


class FileDialogDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = '多文件并行超分辨率处理'
        self.thread_pool = QThreadPool()
        self.active_tasks = 0
        self.processed_files = set()
        self.total_tasks = 0
        self.tool_path = "G:/Greensoftware/NcNN超分/realesrgan-ncnn-vulkan.exe"  # 默认工具路径
        self.gpu_initialized = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.resize(800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 工具路径选择
        tool_layout = QHBoxLayout()
        self.btn_tool_path = QPushButton("选择超分辨率工具")
        self.btn_tool_path.clicked.connect(self.select_tool_path)
        tool_layout.addWidget(self.btn_tool_path)
        self.tool_path_label = QLabel(self.tool_path)
        tool_layout.addWidget(self.tool_path_label)
        main_layout.addLayout(tool_layout)

        # 线程数和模型选择
        settings_layout = QHBoxLayout()
        self.thread_combo = QComboBox()
        max_threads = multiprocessing.cpu_count()
        for i in range(1, max_threads + 1):
            self.thread_combo.addItem(str(i))
        self.thread_combo.setCurrentText("4")  # 默认 4 个线程
        self.thread_combo.currentTextChanged.connect(self.update_thread_count)
        settings_layout.addWidget(QLabel("并行线程数:"))
        settings_layout.addWidget(self.thread_combo)

        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "realesrgan-x4plus-anime",
            "realesrgan-x4plus",
            "realsr-animevideov3-x2",
            "realsr-animevideov3-x3"
        ])  # 可根据需要扩展模型列表
        settings_layout.addWidget(QLabel("模型:"))
        settings_layout.addWidget(self.model_combo)
        settings_layout.addStretch()
        main_layout.addLayout(settings_layout)

        # 文件选择按钮
        self.btn_multi = QPushButton('选择多个文件')
        self.btn_multi.clicked.connect(self.get_multi_files)
        main_layout.addWidget(self.btn_multi)

        # 取消按钮
        self.btn_cancel = QPushButton("取消处理")
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self.cancel_tasks)
        main_layout.addWidget(self.btn_cancel)

        # 状态标签
        self.status_label = QLabel('状态: 待机')
        main_layout.addWidget(self.status_label)

        # GPU 负载标签
        self.gpu_label = QLabel('GPU负载: 未初始化')
        main_layout.addWidget(self.gpu_label)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        main_layout.addWidget(self.progress_bar)

        # 日志区域
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        main_layout.addWidget(self.log_area)

        # CMD 输出区域
        self.cmd_area = QTextEdit()
        self.cmd_area.setReadOnly(True)
        main_layout.addWidget(self.cmd_area)

        # 初始化线程池
        self.update_thread_count(self.thread_combo.currentText())

        # 初始化 GPU 监控
        self.init_gpu_monitoring()
        if self.gpu_initialized:
            self.start_gpu_monitoring()

    def select_tool_path(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择 realesrgan-ncnn-vulkan.exe", "", "可执行文件 (*.exe)")
        if path:
            self.tool_path = path
            self.tool_path_label.setText(path)
            self.append_log(f"已选择工具路径: {path}", "cyan")

    def update_thread_count(self, thread_count):
        self.thread_pool.setMaxThreadCount(int(thread_count))
        self.append_log(f"设置并行线程数为: {thread_count}", "cyan")

    def init_gpu_monitoring(self):
        if pynvml is None:
            self.gpu_label.setText("GPU负载: 未安装pynvml，请运行 'pip install pynvml'")
            return
        try:
            pynvml.nvmlInit()
            self.gpu_initialized = True
        except pynvml.NVMLError:
            self.gpu_label.setText("GPU负载: 初始化失败")
            self.gpu_initialized = False

    def start_gpu_monitoring(self):
        def update_gpu_usage():
            while True:
                if not self.gpu_initialized:
                    break
                try:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                    util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                    self.gpu_label.setText(f"GPU负载: {util.gpu}%")
                except pynvml.NVMLError:
                    self.gpu_label.setText("GPU负载: 检测失败")
                time.sleep(1)
        from threading import Thread
        gpu_thread = Thread(target=update_gpu_usage, daemon=True)
        gpu_thread.start()

    def get_multi_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择多个文件", "", "Images (*.png *.jpg *.jpeg)"
        )
        if files:
            self.btn_multi.setEnabled(False)
            self.btn_cancel.setEnabled(True)
            self.processed_files.clear()
            self.total_tasks = len(files)
            self.active_tasks = 0
            self.progress_bar.setValue(0)
            self.append_log(f"选择了 {self.total_tasks} 个文件", "cyan")
            for file_path in files:
                self.active_tasks += 1
                self.update_status()
                processor = FileProcessor(file_path, self.tool_path, self.model_combo.currentText())
                processor.signals.log_signal.connect(self.append_log)
                processor.signals.cmd_signal.connect(self.append_cmd)
                processor.signals.finished_signal.connect(self.on_task_finished)
                self.thread_pool.start(processor)

    def cancel_tasks(self):
        self.thread_pool.clear()
        self.active_tasks = 0
        self.update_status()
        self.append_log("已取消所有任务", "red")
        self.btn_multi.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        self.progress_bar.setValue(0)

    def append_log(self, message, color="black"):
        colors = {
            "red": "#FF0000", "green": "#008000", "blue": "#0000FF",
            "yellow": "#FFA500", "cyan": "#00FFFF", "black": "#000000"
        }
        color_code = colors.get(color, "#000000")
        self.log_area.append(f'<span style="color:{color_code};">{message}</span>')
        self.log_area.ensureCursorVisible()
        with open("process_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} [{color}] {message}\n")

    def append_cmd(self, message):
        self.cmd_area.append(message)
        self.cmd_area.ensureCursorVisible()

    def on_task_finished(self, file_path):
        self.processed_files.add(file_path)
        self.active_tasks -= 1
        self.update_status()
        self.append_log(f"文件 {file_path} 处理完成", "green")
        progress = int((len(self.processed_files) / self.total_tasks) * 100)
        self.progress_bar.setValue(progress)
        if self.active_tasks == 0:
            self.append_log(f"所有 {self.total_tasks} 个文件处理完成", "cyan")
            self.btn_multi.setEnabled(True)
            self.btn_cancel.setEnabled(False)

    def update_status(self):
        self.status_label.setText(f"状态: 处理中 ({self.active_tasks}/{self.total_tasks})")

    def closeEvent(self, event):
        if pynvml is not None and self.gpu_initialized:
            pynvml.nvmlShutdown()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileDialogDemo()
    ex.show()
    sys.exit(app.exec_())

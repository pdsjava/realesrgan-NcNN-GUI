# Super Resolution Processing Tool

A PyQt5-based GUI application for batch processing images using the `realesrgan-ncnn-vulkan` tool to perform super-resolution enhancement. This tool allows users to select multiple image files, process them with customizable thread counts, monitor GPU usage, and view real-time command-line output.

## Features

- **Batch Image Processing**: Process multiple images concurrently using a thread pool.
- **GPU Monitoring**: Real-time display of GPU utilization and memory usage (requires NVIDIA GPU and `nvidia-smi`).
- **Real-Time CMD Output**: Displays `realesrgan-ncnn-vulkan` command-line output in the GUI.
- **Customizable Threads**: Adjust the number of processing threads (1-4) for optimal performance.
- **User-Friendly Interface**: Select files, view logs, and monitor processing status via a PyQt5 GUI.
- **Error Handling**: Detailed logging of processing errors and file issues.

## Requirements

- **Operating System**: Windows (tested on Windows 10/11)
- **Python**: Python 3.7 or higher
- **Dependencies**:
  - PyQt5
  - psutil
- **External Tools**:
  - `realesrgan-ncnn-vulkan.exe` (download from the [Real-ESRGAN-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan) repository)
  - NVIDIA GPU with `nvidia-smi` for GPU monitoring (optional)
- **Model Files**: Real-ESRGAN models (e.g., `realesrgan-x4plus-anime.param` and `.bin`)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/super-resolution-tool.git
   cd super-resolution-tool
   ```

2. **Install Python Dependencies**:
   ```bash
   pip install pyqt5 psutil
   ```

3. **Download `realesrgan-ncnn-vulkan`**:
   - Download the latest `realesrgan-ncnn-vulkan` executable from the [Real-ESRGAN-ncnn-vulkan releases page](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases).
   - Place `realesrgan-ncnn-vulkan.exe` in the project root directory.

4. **Download Model Files**:
   - Download the required model files (e.g., `realesrgan-x4plus-anime.param` and `realesrgan-x4plus-anime.bin`) from the [Real-ESRGAN model zoo](https://github.com/xinntao/Real-ESRGAN#models).
   - Place the model files in the same directory as `realesrgan-ncnn-vulkan.exe`.

5. **Verify NVIDIA Drivers** (Optional):
   - Ensure NVIDIA drivers are installed and `nvidia-smi` is accessible in the command line for GPU monitoring.

## Usage

1. **Run the Application**:
   ```bash
   python main.py
   ```

2. **Select Files**:
   - Click the "选择文件" (Select Files) button to choose image files (`.png`, `.jpg`, `.jpeg`, `.bmp`).

3. **Configure Threads**:
   - Use the thread dropdown to select the number of concurrent processing threads (1-4, default: 4).

4. **Start Processing**:
   - Click the "开始处理" (Start Processing) button to begin super-resolution processing.
   - The processed images will be saved in the `超分辨率输出结果` (Super Resolution Output) directory.

5. **Monitor Progress**:
   - View processing logs in the "日志输出" (Log Output) section.
   - Monitor real-time `realesrgan-ncnn-vulkan` output in the "CMD 输出" (CMD Output) section.
   - Check GPU usage in the "GPU负载" (GPU Load) label (if NVIDIA GPU is available).

## Project Structure

```
super-resolution-tool/
├── main.py                   # Main application script
├── realesrgan-ncnn-vulkan.exe # Real-ESRGAN executable (must be downloaded)
├── realesrgan-x4plus-anime.param # Model file (must be downloaded)
├── realesrgan-x4plus-anime.bin   # Model file (must be downloaded)
├── 超分辨率输出结果/         # Output directory for processed images
└── README.md                # This file
```

## Troubleshooting

- **Error: `[WinError 2] 系统找不到指定的文件`**
  - Ensure `realesrgan-ncnn-vulkan.exe` is in the project root directory.
  - Verify that the input image files exist and their paths are correct.
  - Check that model files (e.g., `realesrgan-x4plus-anime.param` and `.bin`) are in the same directory as the executable.

- **CMD Output Not Displaying**:
  - Ensure the input files and model files are valid.
  - Run `realesrgan-ncnn-vulkan.exe` manually in the command line to verify output:
    ```bash
    .\realesrgan-ncnn-vulkan.exe -i input.png -o output.png -n realesrgan-x4plus-anime -s 4 -f png
    ```

- **GPU Monitoring Not Working**:
  - Confirm that `nvidia-smi` is accessible in the command line.
  - Install or update NVIDIA drivers if necessary.

- **Processing Fails or Crashes**:
  - Reduce the number of threads (e.g., set to 1) to test stability.
  - Use smaller image files to rule out memory issues.
  - Check the log output for specific error messages.

## License

This project is licensed under the **BSD 3-Clause License**, as it is based on the `realesrgan-ncnn-vulkan` tool, which follows the same license. See the [LICENSE](LICENSE) file for details.

```
BSD 3-Clause License

Copyright (c) 2025, Your Name
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

## Acknowledgments

- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) for the `realesrgan-ncnn-vulkan` tool and models.
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework.
- [psutil](https://github.com/giampaolo/psutil) for system monitoring.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for bug fixes, feature additions, or improvements.

---

### Notes for Customization

- **Repository URL**: Replace `https://github.com/your-username/super-resolution-tool.git` with your actual repository URL.
- **Author Name**: Replace `Your Name` in the license section with your name or organization.
- **Additional Sections**: If you want to add sections like "Screenshots," "Performance Tips," or "Future Plans," let me know, and I can expand the README.
- **License File**: Create a `LICENSE` file in the project root with the BSD-3-Clause text provided above.

If you need further refinements (e.g., adding screenshots, specific installation steps for other platforms, or translations), please let me know! Additionally, if you encounter issues like the `[WinError 2]` error mentioned in the `message.txt`, refer to the troubleshooting section or provide more details for targeted assistance.

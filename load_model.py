import subprocess
import shutil
import sys
import os

def clone_with_lfs(repo_url, repo_dir_name, target_dir):
    # Clone repo
    subprocess.run(["git", "clone", repo_url], check=True)

    # Chạy lfs pull trong thư mục repo vừa clone
    subprocess.run(["git", "lfs", "pull"], cwd=repo_dir_name, check=True)

    # Move thư mục Models trong repo về thư mục đích
    shutil.move(os.path.join(repo_dir_name, "Models"), target_dir)

# Clone StyleTTS2-LibriTTS
clone_with_lfs(
    "https://huggingface.co/yl4579/StyleTTS2-LibriTTS",
    "StyleTTS2-LibriTTS",
    "./Models"
)

# Clone StyleTTS2-LJSpeech (nếu muốn ghi đè Models)
clone_with_lfs(
    "https://huggingface.co/yl4579/StyleTTS2-LJSpeech",
    "StyleTTS2-LJSpeech",
    "./Models"
)

def install_espeak():
    try:
        # Kiểm tra xem espeak đã cài chưa
        subprocess.run(['espeak', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("espeak đã được cài đặt.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Đang cài đặt espeak...")
        if sys.platform.startswith('linux'):
            # Với Linux (Ubuntu/Debian)
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'espeak-ng'], check=True)
        elif sys.platform == 'darwin':
            # Với macOS (bạn cần cài Homebrew trước)
            subprocess.run(['brew', 'install', 'espeak'], check=True)
        else:
            raise RuntimeError("Chưa hỗ trợ cài espeak tự động trên hệ điều hành này.")

install_espeak()
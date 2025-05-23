import subprocess
import shutil
import sys
import os

def install_git_lfs():
    try:
        # Kiểm tra git-lfs đã được cài chưa
        subprocess.run(['git', 'lfs', 'version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("git-lfs đã được cài đặt.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Đang cài đặt git-lfs...")
        if sys.platform.startswith('linux'):
            subprocess.run(['apt-get', 'update'], check=True)
            subprocess.run(['apt-get', 'install', '-y', 'git-lfs'], check=True)
            subprocess.run(['git', 'lfs', 'install'], check=True)
        elif sys.platform == 'darwin':
            subprocess.run(['brew', 'install', 'git-lfs'], check=True)
            subprocess.run(['git', 'lfs', 'install'], check=True)

install_git_lfs()

def clone_with_lfs(repo_url, repo_dir_name, target_dir):
    # Clone repo
    subprocess.run(["git", "clone", repo_url], check=True)

    # Chạy lfs pull trong thư mục repo vừa clone
    subprocess.run(["git", "lfs", "pull"], cwd=repo_dir_name, check=True)

    # Đường dẫn thư mục Models trong repo
    models_src = os.path.join(repo_dir_name, "Models")

    # Kiểm tra thư mục Models có tồn tại không
    if os.path.exists(models_src):
        # Nếu thư mục đích đã tồn tại, xóa đi để tránh lỗi move
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

        shutil.move(models_src, target_dir)
        print(f"Đã move {models_src} => {target_dir}")
    else:
        print(f"[!] Không tìm thấy thư mục 'Models' trong repo {repo_dir_name}")

# Sử dụng
clone_with_lfs(
    "https://huggingface.co/yl4579/StyleTTS2-LibriTTS",
    "StyleTTS2-LibriTTS",
    "Models"
)

clone_with_lfs(
    "https://huggingface.co/yl4579/StyleTTS2-LJSpeech",
    "StyleTTS2-LJSpeech",
    "Models"
)
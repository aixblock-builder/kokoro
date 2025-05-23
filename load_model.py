import os
import shutil
import subprocess
import sys

def install_git_lfs():
    try:
        subprocess.run(['git', 'lfs', 'version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ git-lfs đã được cài đặt.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("🛠️ Đang cài đặt git-lfs...")
        if sys.platform.startswith('linux'):
            subprocess.run(['apt-get', 'update'], check=True)
            subprocess.run(['apt-get', 'install', '-y', 'git-lfs'], check=True)
            subprocess.run(['git', 'lfs', 'install'], check=True)
        elif sys.platform == 'darwin':
            subprocess.run(['brew', 'install', 'git-lfs'], check=True)
            subprocess.run(['git', 'lfs', 'install'], check=True)
        else:
            raise EnvironmentError("⚠️ Chưa hỗ trợ cài đặt git-lfs trên hệ điều hành này.")

def clone_with_lfs(repo_url, repo_dir_name, target_dir):
    # Dọn thư mục repo nếu tồn tại
    if os.path.exists(repo_dir_name):
        print(f"🧹 Đang xóa thư mục cũ: {repo_dir_name}")
        shutil.rmtree(repo_dir_name)

    # Clone repo
    print(f"🔄 Cloning {repo_url}...")
    subprocess.run(["git", "clone", repo_url], check=True)

    # LFS pull
    print(f"📦 Đang pull LFS trong {repo_dir_name}...")
    subprocess.run(["git", "lfs", "pull"], cwd=repo_dir_name, check=True)

    # Move Models
    models_src = os.path.join(repo_dir_name, "Models")
    if os.path.exists(models_src):
        if os.path.exists(target_dir):
            print(f"🧹 Xóa thư mục đích cũ: {target_dir}")
            shutil.rmtree(target_dir)
        shutil.move(models_src, target_dir)
        print(f"✅ Đã move {models_src} ➜ {target_dir}")

        # ✅ Liệt kê nội dung thư mục
        print(f"📂 Nội dung thư mục {target_dir}:")
        for f in os.listdir(target_dir):
            print("  -", f)
    else:
        print(f"[!] ❌ Không tìm thấy thư mục 'Models' trong repo {repo_dir_name}")

# Gọi hàm
install_git_lfs()

clone_with_lfs(
    "https://huggingface.co/yl4579/StyleTTS2-LibriTTS",
    "StyleTTS2-LibriTTS",
    "Models"
)

# Nếu muốn ghi đè Models bằng bộ khác:
clone_with_lfs(
    "https://huggingface.co/yl4579/StyleTTS2-LJSpeech",
    "StyleTTS2-LJSpeech",
    "Models"
)

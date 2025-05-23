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
            raise EnvironmentError("⚠️ Không hỗ trợ OS này.")

def clone_with_lfs(repo_url, repo_dir_name, models_base_dir):
    if os.path.exists(repo_dir_name):
        print(f"🧹 Xóa repo cũ: {repo_dir_name}")
        shutil.rmtree(repo_dir_name)

    print(f"🔄 Cloning {repo_url}...")
    subprocess.run(["git", "clone", repo_url], check=True)

    print(f"📦 Pull LFS trong {repo_dir_name}...")
    subprocess.run(["git", "lfs", "pull"], cwd=repo_dir_name, check=True)

    models_src = os.path.join(repo_dir_name, "Models")
    target_subdir = os.path.join(models_base_dir, repo_dir_name)

    if os.path.exists(models_src):
        shutil.move(models_src, target_subdir)
        print(f"✅ Moved {models_src} ➜ {target_subdir}")
    else:
        print(f"[!] ❌ Không có thư mục 'Models' trong repo {repo_dir_name}")

def print_models_tree(models_dir):
    print(f"\n📂 Nội dung thư mục {models_dir}:")
    for root, dirs, files in os.walk(models_dir):
        level = root.replace(models_dir, '').count(os.sep)
        indent = '    ' * level
        print(f"{indent}- 📁 {os.path.basename(root)}")
        sub_indent = '    ' * (level + 1)
        for f in files:
            print(f"{sub_indent}- 📄 {f}")

# ---------- Main script ----------
install_git_lfs()

MODELS_DIR = "Models"

# Xoá toàn bộ Models nếu đã tồn tại
if os.path.exists(MODELS_DIR):
    print(f"🧹 Xóa thư mục cũ: {MODELS_DIR}")
    shutil.rmtree(MODELS_DIR)

os.makedirs(MODELS_DIR, exist_ok=True)

# Clone & move
clone_with_lfs(
    "https://huggingface.co/yl4579/StyleTTS2-LibriTTS",
    "StyleTTS2-LibriTTS",
    MODELS_DIR
)

clone_with_lfs(
    "https://huggingface.co/yl4579/StyleTTS2-LJSpeech",
    "StyleTTS2-LJSpeech",
    MODELS_DIR
)

# In toàn bộ nội dung Models
print_models_tree(MODELS_DIR)

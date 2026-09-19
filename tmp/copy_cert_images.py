import shutil
import os

# 源目录和目标目录
src_dir = r"C:\Users\ADMIN\Desktop\坤德素材"
dst_dir = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website\images\certifications"

# 创建目标目录
os.makedirs(dst_dir, exist_ok=True)

# 文件名映射
file_mapping = {
    "微信图片_20260918125149_242_61.jpg": "factory-warehouse-crane.jpg",
    "微信图片_20260918125149_243_61.jpg": "production-line-heavy-equipment.jpg",
    "微信图片_20260918125149_246_61.jpg": "automated-production-line.jpg",
    "微信图片_20260918125149_247_61.jpg": "raw-material-storage.jpg",
    "微信图片_20260918125149_248_61.jpg": "brinell-hardness-tester.jpg",
    "微信图片_20260918125149_249_61.jpg": "mechanical-testing-equipment.jpg",
}

# 复制文件
for src_name, dst_name in file_mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dst_path = os.path.join(dst_dir, dst_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"已复制: {src_name} -> {dst_name}")
    else:
        print(f"未找到: {src_name}")

print("\n所有图片复制完成")

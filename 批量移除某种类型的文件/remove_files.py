import os
import shutil
 
def is_image(file):
    return file.endswith('jpg') or file.endswith('png') or file.endswith('jpeg') or file.endswith('JPG') or file.endswith('JPEG')
 
def check_files(data_dir, label, backup_dir, delete, backup):
 
    count_error = 0     # 非图片文件数量
    label_dir = os.path.join(data_dir, label)   # 当前遍历 label 文件夹目录
    for parent, dirs, files in os.walk(label_dir):
        if files == []: # 跳过无文件的文件夹
            continue
 
        for file in files:  # 遍历当前 parent 下的文件
            cur_file = os.path.join(parent, file)   # 当前遍历的文件路径
            if not is_image(cur_file):  # 判断是否为图片文件
                count_error += 1    # 更新非图片文件数量
 
                if backup:  # 备份文件
                    cur_backup_dir = parent.replace(data_dir, backup_dir)
                    if not os.path.exists(cur_backup_dir):
                        os.makedirs(cur_backup_dir)
                    dst_file = os.path.join(cur_backup_dir, file)  # 备份文件路径
                    shutil.copy(cur_file, dst_file)  # 文件备份
 
                if delete:  # 文件删除
                    os.remove(cur_file)
    return count_error
 
 
def count_images(data_dir, backup_dir, delete=False, backup=True):
 
    labels = []     # data_dir 下19类数据的文件夹名
    for dir in os.listdir(data_dir): # os.listdir返回文件夹和文件，只筛选 data_dir 下的文件夹
        cur_dir = os.path.join(data_dir, dir)
        if os.path.isdir(cur_dir):
            labels.append(dir)
 
    print("文件夹\t问题文件数量")
    # 遍历 19 类数据的文件夹
    for label in labels:
        count_error = check_files(data_dir, label, backup_dir, delete, backup)
        print("{}\t{}".format(label, count_error))
 
 
def main():
    delete = False      # 是否删除问题文件
    backup = True       # 是否备份问题文件
    data_dir = r'D:/test/'    # 待检测的数据集目录
    backup_dir = r'D:/test/bk'  # 备份路径
    count_images(data_dir, backup_dir, delete, backup)   # 统计问题文件数量
 
if __name__ == '__main__':
    main()
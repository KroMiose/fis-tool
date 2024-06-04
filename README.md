# FIS: File Interaction Script

## 简介

FIS (File Interaction Script) 是一种用于描述项目文件结构的文本格式，旨在简化与大型语言模型 (LLM) 的交互，实现更高效的代码变更。它提供了一种结构化的方式，让您能够：

- **生成项目结构描述文件:** 从一个已存在的项目目录生成 FIS 描述文件，其中包含项目的完整文件结构和内容。
- **从 FIS 描述文件创建项目:** 使用 FIS 描述文件来创建一个新的项目，包含所有的文件和文件夹结构。
- **应用 FIS 描述文件中的变更:** 读取 FIS 文件中的变更描述，并应用到现有的项目中，包括添加、修改和删除文件。

## 功能

- **生成 FIS 描述文件:** 根据项目目录生成包含所有文件和文件夹结构的 FIS 描述文件。
- **读取 FIS 描述文件:** 解析 FIS 描述文件内容，提取文件结构和内容信息。
- **从 FIS 描述文件创建项目:** 使用 FIS 描述文件来创建一个新的项目文件夹结构和文件。
- **应用 FIS 描述文件中的变更:** 读取 FIS 描述文件中的变更描述，并应用到现有的项目中，包括添加、修改和删除文件。

## 使用方法

1. **安装:** 使用 `pip install fis-tool` 安装 FIS 工具。
2. **交互式终端:** 直接使用 `fis-tool` 命令启动交互式终端。
3. **生成 FIS 描述文件:**
   - 使用 `fis-tool generate` 命令生成 FIS 描述文件。
   - 使用 `-o` 或 `--output` 参数指定输出文件路径。
   - 使用 `-e` 或 `--explanation` 参数选择添加 FIS 结构说明提示词（可选，默认不添加）。
   - 使用 `-g` 或 `--gitignore` 参数使用 `.gitignore` 文件忽略项目文件（可选，默认不使用）。
4. **从 FIS 描述文件创建项目:**
   - 使用 `fis-tool create` 命令从 FIS 描述文件创建项目。
   - 使用 `-f` 或 `--file` 参数指定 FIS 描述文件路径。
   - 使用 `-o` 或 `--output` 参数指定输出项目路径。
5. **应用 FIS 描述文件中的变更:**
   - 使用 `fis-tool apply` 命令将 FIS 描述文件中的变更应用到项目。
   - 使用 `-p` 或 `--project` 参数指定项目根目录路径。
   - 使用 `-f` 或 `--file` 参数指定 FIS 描述文件路径。

## 示例

```bash
# 生成 FIS 描述文件
fis-tool generate -p my_project -o my_project.fis -e zh -g

# 从 FIS 描述文件创建项目
fis-tool create -f my_project.fis -o new_project

# 应用 FIS 描述文件中的变更
fis-tool apply -p my_project -f changes.fis
```

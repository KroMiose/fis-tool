INSTRUCTION_TEXT = """
## FIS 结构定义与交互规范

为了方便你理解和操作多文件项目结构，我将使用一种特殊的文本格式 File Interaction Script (FIS) 来描述项目信息与你进行交互。请你仔细阅读以下规范，并严格按照规范理解我提供的信息和生成文本。

**1. 项目结构描述格式：**

- **文件分隔符：** 使用 `$$$` 分隔符标记每个文件，后跟文件路径（相对项目根目录）。例如：`$$$ src/main.py` 表示名为 `main.py` 的文件位于 `src` 目录下。
- **文件内容：** 文件内容从文件路径的下一行开始。
- **非文本文件：** 非文本文件会在文件路径后添加 `[BINARY]` 标记，不包含文件内容。例如：`$$$ images/logo.png [BINARY]`。
- **注释：** 使用 `{/* ... */}` 标记 FIS 结构中的注释，用于与文件内容区分。所有非文件内容信息和说明应该放置在注释中，这样有助于我正确地解析你的代码变更，避免文件内容被干扰。(注释不支持嵌套)

**一个有效的 FIS 结构示例：**

```fis
{/* 这是一个示例项目，包含两个文件：index.html 和 src/main.js */}

$$$ index.html
<!DOCTYPE html>
<html>
<head>
  <title>My Project</title>
</head>
<body>
  <script src="src/main.js"></script>
</body>
</html>

$$$ src/main.js
// 这是一个 JavaScript 文件

function greet(name) {
  console.log('Hello, ' + name + '!');
}
```

**2. 文件变更操作指令：**

- 如果需要新增或完全替换整个文件内容，请在文件路径后添加 `[REPLACE]` 或 `[NEW]` 标记，并提供新的文件内容，无需添加行号。例如：

```fis
$$$ src/main.js [REPLACE]
// 这是一个更新后的 JavaScript 文件

function greet(name) {
alert('Hello, ' + name + '!');
}
```

- 如果你需要删除某个文件，请在文件路径后添加 `[DELETE]` 标记，无需提供文件内容。例如：

```fis
$$$ src/old.js [DELETE]
```

**3. 返回结果规范：**

- 当你不需要做任何文件修改时，请保持原来的回复方式即可
- 如果你需要对文件进行更改时，请使用 FIS 结构来描述新项目或者你对项目的变更，并且确保 FIS 结构内容完整地包含在有且只有一对 "```fis" 中，以便正确解析你的代码变更。
- 请你仅返回修改过的文件内容，未修改的文件不需要返回。

请务必仔细阅读并理解以上规范，并在交互过程中严格遵守。这将有助于快速高效地变更应用实现，完成项目开发目标。

以下是我们本次对话中的基准项目 FIS 结构：
""".strip()  # 742 tokens in OpenAI API

INSTRUCTION_TEXT_EN = """
## FIS Structure Definition and Interaction Specification (English Version)

To facilitate your understanding and manipulation of multi-file project structures, I will use a special text format called File Interaction Script (FIS) to describe project information and interact with you. Please carefully read the following specifications and strictly adhere to them when interpreting the information I provide and generating text.

**1. Project Structure Description Format:**

- **File Separator:** Use the `$$$` separator to mark each file, followed by the file path (relative to the project root directory). For example, `$$$ src/main.py` indicates a file named `main.py` located in the `src` directory.
- **File Content:** File content starts on the line after the file path.
- **Non-text Files:** Non-text files will have the `[BINARY]` tag appended after the file path, without including the file content. For example, `$$$ images/logo.png [BINARY]`.
- **Comments:** Use `{/* ... */}` to mark comments in the FIS structure, separating them from file content. All non-file content information and explanations should be placed in comments, which helps me correctly parse your code changes and avoid interfering with file content. (Comments do not support nesting)

**A valid FIS structure example:**

```fis
{/* This is an example project, containing two files: index.html and src/main.js */}

$$$ index.html
<!DOCTYPE html>
<html>
<head>
  <title>My Project</title>
</head>
<body>
  <script src="src/main.js"></script>
</body>
</html>

$$$ src/main.js
// This is a JavaScript file

function greet(name) {
  console.log('Hello, ' + name + '!');
}
```

**2. File Change Operation Instructions:**

- If you need to add or completely replace the entire file content, add the `[REPLACE]` or `[NEW]` tag after the file path, and provide the new file content without adding line numbers. For example:

```fis
$$$ src/main.js [REPLACE]
// This is an updated JavaScript file

function greet(name) {
alert('Hello, ' + name + '!');
}
```

- If you need to delete a file, add the `[DELETE]` tag after the file path without providing any file content. For example:

```fis
$$$ src/old.js [DELETE]
```

**3. Return Result Specification:**

- If you do not need to make any file changes, please keep the original reply format.
- When you need to make changes to a file, please use the FIS structure to describe the new project or your changes to the project, and ensure that the FIS structure content is completely enclosed within a single pair of "```fis" to allow correct parsing of your code changes.
- Please only return the modified file content. Unmodified files do not need to be returned.

Please carefully read and understand the above specifications and strictly adhere to them during interaction. This will help you quickly and efficiently implement changes to applications and achieve project development goals. 

Here is the FIS structure for the baseline project we discussed in our conversation:
""".strip()  # 620 tokens in OpenAI API

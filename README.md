# Codet

codet is a command-line tool for analyzing Git commit history. It helps users profile project change hotspots, analyze code changes, and leverage AI for deeper insights.
In particular, the generated git diff files can be conveniently integrated with Cursor for collaborative development.

- Analyze recent commit records, defaulting to the past 7 days.
- Search for keywords in commit diffs.
- Search for author email in commit diffs.
- Support for optional AI analysis via tools.
- Code hotspot analysis to identify frequently modified areas.


## Installation

### Install from PyPI
If you want to quickly install Codet, you can use the following command to install it from PyPI:
```bash
pip install codet
```

### Install from source code
If you want to participate in development or use the latest development version, you can install it from the source code:
```bash
# Clone the repository
git clone https://github.com/yourusername/codet.git
cd codet

# Install dependencies
pip install -e .
```

### Install development dependencies
If you are going to do development work, you can install development dependencies:
```bash
pip install -e ".[dev]"
```

## Usage

### Display help information
If you need to know the detailed usage of Codet, you can use the following command to display the help information:
```bash
codet --help

===========================================================================
---------------------------------codet-------------------------------------
 ██████╗ ██████╗ ██████╗ ███████╗    ████████╗██████╗  █████╗ ██╗██╗     
██╔════╝██╔═══██╗██╔══██╗██╔════╝    ╚══██╔══╝██╔══██╗██╔══██╗██║██║     
██║     ██║   ██║██║  ██║█████╗         ██║   ██████╔╝███████║██║██║     
██║     ██║   ██║██║  ██║██╔══╝         ██║   ██╔══██╗██╔══██║██║██║     
╚██████╗╚██████╔╝██████╔╝███████╗       ██║   ██║  ██║██║  ██║██║███████╗
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
 --------------------------------codet-------------------------------------
===========================================================================

usage: codet [-h] [--version] [-d DAYS] [-e EMAIL] [-u USER] [-k KEYWORD] [-g] [-r] [-p PATH] [-s] [-m {union,intersection}]

codet is a CLI tool for analyzing git commit history.
1. quickly understand commit records, analyze code changes, and identify commit hotspots.
2. filter commits based on time range, search for specific keywords in commit diffs, or filter by author email.
3. as an optional feature, codet integrates AI through API tokens to provide deeper analysis.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d DAYS, --days DAYS  [Optional] Look back for git commits in the past N days (default: 30 days) (default: 30)
  -e EMAIL, --email EMAIL
                        [Optional] Filter commits by git commit author email, can be used multiple times (e.g., -e user1@example.com -e user2@example.com) (default: [])
  -u USER, --user USER  [Optional] Filter commits by git commit author name, can be used multiple times (e.g., -u 'John Doe' -u 'Jane Smith') (default: [])
  -k KEYWORD, --keyword KEYWORD
                        [Optional] Search for keywords in commit diffs, can be used multiple times (e.g., -k keyword1 -k keyword2) (default: [])
  -g, --debug           [Optional] Enable debug mode (default: False) (default: False)
  -r, --recursive       [Optional] Recursively search for git projects in subdirectories (default: True) (default: True)
  -p PATH, --path PATH  [Optional] Specify the path to analyze (default: current directory) (default: /Users/joejiang/Desktop/codet)
  -s, --hotspot         [Optional] Count changes in files and directories within search scope to identify active areas (default: False) (default: False)
  -m {union,intersection}, --mode {union,intersection}
                        [Optional] Search mode: union (match any condition) or intersection (match all conditions) (default: union) (default: union)

Additional:
        For more details, visit the documentation or contact clemente0620@gmail.com 

```

### Usage examples
The following are basic usage examples of Codet. You can combine different parameters according to your needs:
```bash
# View commit records that contain the keyword "feature" and are authored by "John Doe" in the past 7 days
codet -d 7 -k feature -u "John Doe"

# Perform code hotspot analysis on the current directory and its subdirectories
codet -s -r
```

### Command - line parameter description
```
usage: codet [-h] [--version] [-d DAYS] [-e EMAIL] [-u USER] [-k KEYWORD] [-g] [-r] [-p PATH] [-s] [-m {union,intersection}]

codet is a CLI tool for analyzing git commit history.
1. quickly understand commit records, analyze code changes, and identify commit hotspots.
2. filter commits based on time range, search for specific keywords in commit diffs, or filter by author email.
3. as an optional feature, codet integrates AI through API tokens to provide deeper analysis.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d DAYS, --days DAYS  [Optional] Look back for git commits in the past N days (default: 30 days)
  -e EMAIL, --email EMAIL
                        [Optional] Filter commits by git commit author email, can be used multiple times (e.g., -e user1@example.com -e user2@example.com)
  -u USER, --user USER  [Optional] Filter commits by git commit author name, can be used multiple times (e.g., -u 'John Doe' -u 'Jane Smith')
  -k KEYWORD, --keyword KEYWORD
                        [Optional] Search for keywords in commit diffs, can be used multiple times (e.g., -k keyword1 -k keyword2)
  -g, --debug           [Optional] Enable debug mode (default: False)
  -r, --recursive       [Optional] Recursively search for git projects in subdirectories (default: True)
  -p PATH, --path PATH  [Optional] Specify the path to analyze (default: current directory)
  -s, --hotspot         [Optional] Count changes in files and directories within search scope to identify active areas (default: False)
  -m {union,intersection}, --mode {union,intersection}
                        [Optional] Search mode: union (match any condition) or intersection (match all conditions) (default: union)

Additional:
        For more details, visit the documentation or contact clemente0620@gmail.com 
```

## Features
1. **Commit record analysis**: Quickly view and analyze recent commit records. By default, it views commits from the past 30 days.
2. **Keyword search**: Support searching for specific keywords in commit diffs to accurately locate relevant commits.
3. **Author and email filtering**: Filter commit records based on the author's name or email.
4. **Code hotspot analysis**: Identify frequently modified areas in the project by counting the number of changes in files and directories.
5. **Flexible search modes**: Provide two search modes, union (match any condition) and intersection (match all conditions), to meet different search needs.
6. **File processing functionality**: It has functions related to file processing, facilitating operations on project files.
7. **Cross - platform support**: Can be used on multiple operating systems, with good compatibility.
8. **Simple and easy - to - use command - line interface**: Provide a clear and concise command - line operation method, reducing the usage threshold.

## Development

### Clone the repository
If you want to participate in the development of Codet, you can clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/codet.git
cd codet
```

### Install development dependencies
Install development dependencies to perform operations such as code testing, formatting, and packaging:
```bash
pip install -e ".[dev]"
```

## License
Codet is licensed under the MIT License. For detailed information, please refer to the [LICENSE](https://opensource.org/licenses/MIT) file.

## More Information
If you need more detailed information, you can view the documentation or contact the developer: clemente0620@gmail.com.


# Codet

codet 是一个强大的跨平台命令行工具，专门用于分析 Git 提交历史。它能够帮助用户快速了解项目的变更热点、分析代码更改情况，还可以通过集成 AI 提供更深入的洞察。

## 功能特性
1. **提交记录分析**：可快速查看并分析最近的提交记录，默认查看过去 30 天的提交。
2. **关键词搜索**：支持在提交差异中搜索特定关键词，精准定位相关提交。
3. **作者与邮箱过滤**：能够根据提交作者姓名或邮箱对提交记录进行过滤。
4. **代码热点分析**：通过统计文件和目录的变更次数，找出项目中频繁修改的区域。
5. **灵活的搜索模式**：提供并集（匹配任意条件）和交集（匹配所有条件）两种搜索模式，满足不同的搜索需求。
6. **文件处理功能**：具备文件处理相关的功能，方便对项目文件进行操作。
7. **跨平台支持**：可在多种操作系统上使用，具有良好的兼容性。
8. **简单易用的命令行界面**：提供清晰简洁的命令行操作方式，降低使用门槛。

## 安装

### 从 PyPI 安装
如果你想快速安装 Codet，可以使用以下命令从 PyPI 进行安装：
```bash
pip install codet
```

### 从源代码安装
如果你想参与开发或者使用最新的开发版本，可以从源代码进行安装：
```bash
# 克隆仓库
git clone https://github.com/yourusername/codet.git
cd codet

# 安装依赖
pip install -e .
```

### 安装开发依赖
如果你要进行开发工作，可以安装开发依赖：
```bash
pip install -e ".[dev]"
```

## 使用方法

### 显示帮助信息
如果你需要了解 Codet 的详细使用方法，可以使用以下命令显示帮助信息：
```bash
codet --help
```

### 使用示例
以下是 Codet 的基本使用示例，你可以根据需要组合不同的参数：
```bash
# 查看过去 7 天内包含关键词 "feature" 且作者为 "John Doe" 的提交记录
codet -d 7 -k feature -u "John Doe"

# 对当前目录及其子目录进行代码热点分析
codet -s -r
```

### 命令行参数说明
```
===========================================================================
---------------------------------codet-------------------------------------
 ██████╗ ██████╗ ██████╗ ███████╗    ████████╗██████╗  █████╗ ██╗██╗     
██╔════╝██╔═══██╗██╔══██╗██╔════╝    ╚══██╔══╝██╔══██╗██╔══██╗██║██║     
██║     ██║   ██║██║  ██║█████╗         ██║   ██████╔╝███████║██║██║     
██║     ██║   ██║██║  ██║██╔══╝         ██║   ██╔══██╗██╔══██║██║██║     
╚██████╗╚██████╔╝██████╔╝███████╗       ██║   ██║  ██║██║  ██║██║███████╗
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
 --------------------------------codet-------------------------------------
===========================================================================

usage: codet [-h] [--version] [-d DAYS] [-e EMAIL] [-u USER] [-k KEYWORD] [-g] [-r] [-p PATH] [-s] [-m {union,intersection}]

codet is a CLI tool for analyzing git commit history.
1. quickly understand commit records, analyze code changes, and identify commit hotspots.
2. filter commits based on time range, search for specific keywords in commit diffs, or filter by author email.
3. as an optional feature, codet integrates AI through API tokens to provide deeper analysis.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d DAYS, --days DAYS  [Optional] Look back for git commits in the past N days (default: 30 days) (default: 30)
  -e EMAIL, --email EMAIL
                        [Optional] Filter commits by git commit author email, can be used multiple times (e.g., -e user1@example.com -e user2@example.com) (default: [])
  -u USER, --user USER  [Optional] Filter commits by git commit author name, can be used multiple times (e.g., -u 'John Doe' -u 'Jane Smith') (default: [])
  -k KEYWORD, --keyword KEYWORD
                        [Optional] Search for keywords in commit diffs, can be used multiple times (e.g., -k keyword1 -k keyword2) (default: [])
  -g, --debug           [Optional] Enable debug mode (default: False) (default: False)
  -r, --recursive       [Optional] Recursively search for git projects in subdirectories (default: True) (default: True)
  -p PATH, --path PATH  [Optional] Specify the path to analyze (default: current directory) (default: /Users/joejiang/Desktop/codet)
  -s, --hotspot         [Optional] Count changes in files and directories within search scope to identify active areas (default: False) (default: False)
  -m {union,intersection}, --mode {union,intersection}
                        [Optional] Search mode: union (match any condition) or intersection (match all conditions) (default: union) (default: union)

Additional:
        For more details, visit the documentation or contact clemente0620@gmail.com 
```

## 开发

### 克隆仓库
如果你想参与 Codet 的开发，可以克隆仓库到本地：
```bash
git clone https://github.com/yourusername/codet.git
cd codet
```

### 安装开发依赖
安装开发依赖，以便进行代码的测试、格式化和打包等操作：
```bash
pip install -e ".[dev]"
```

## 许可证
Codet 采用 MIT 许可证，详细信息请参考 [LICENSE](https://opensource.org/licenses/MIT) 文件。

## 更多信息
如果你需要更多详细信息，可以查看文档或者联系开发者：clemente0620@gmail.com。
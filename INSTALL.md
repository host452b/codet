# 安装指南

## 从PyPI安装

```bash
pip install codet
```

## 从源代码安装

1. 克隆仓库

```bash
git clone https://github.com/yourusername/codet.git
cd codet
```

2. 安装依赖

```bash
pip install -e .
```

或者安装开发依赖：

```bash
pip install -e ".[dev]"
```

## 验证安装

安装完成后，可以运行以下命令验证安装是否成功：

```bash
codet --version
```

## 打包发布

如果你想自己打包发布，可以按照以下步骤操作：

1. 安装打包工具

```bash
pip install build twine
```

2. 构建包

```bash
python -m build
```

3. 上传到PyPI

```bash
python -m twine upload dist/*
```

## 支持的平台

- Windows
- macOS
- Linux 
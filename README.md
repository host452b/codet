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
  -p PATH, --path PATH  [Optional] Specify the path to analyze (default: current directory) (default: codet)
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

git clone https://github.com/pytorch/pytorch.git
cd pytorch

# # View commit records that contain the keywords "Triton" and "cuda" in the past 7 days
codet -d 7 -k Triton -k cuda  -s -r

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

2025-03-09 10:32:50 [INFO] Initializing CodeTrail executor
2025-03-09 10:32:50 [INFO] Analyzing path: pytorch
2025-03-09 10:32:50 [INFO] Recursive mode enabled, scanning all subdirectories
2025-03-09 10:32:50 [INFO]      Found Git repo at pytorch
2025-03-09 10:32:50 [INFO] Initializing GitWrapper, processing 1 repositories
2025-03-09 10:32:50 [INFO]      Loaded repository: pytorch, path: pytorch
2025-03-09 10:32:50 [INFO]      Successfully loaded 1 Git repositories
2025-03-09 10:32:50 [INFO] Starting to collect raw commit data
2025-03-09 10:32:50 [INFO] Collecting commits since 2025-03-02
Processing pytorch commit records: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 286/286 [00:34<00:00,  8.26it/s]
Processing repositories progress: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:34<00:00, 34.73s/it]
2025-03-09 10:33:25 [INFO] Starting to process commit data
2025-03-09 10:33:25 [INFO] Union mode: match any condition
2025-03-09 10:33:25 [INFO] Intersection mode: must match all conditions
2025-03-09 10:33:25 [INFO] [Search Mode] Using Union Mode - Match any condition
2025-03-09 10:33:25 [INFO]   Union mode: commit included if it matches any email, username or keyword condition
2025-03-09 10:33:25 [INFO]   - Email conditions: none
2025-03-09 10:33:25 [INFO]   - User conditions: none
2025-03-09 10:33:25 [INFO]   - Keyword conditions: Triton, cuda
2025-03-09 10:33:25 [INFO] Processing complete, found 165 matching commits
2025-03-09 10:33:25 [INFO] 
+-----+------------+-----------+------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------------------------------------+---------------------------+
|   # | Repository | Commit ID | Commit Summary                                                                                                               | Email                                             | URL                                                 |                      Date |
+-----+------------+-----------+------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------------------------------------+---------------------------+
|   1 | pytorch    | 17dbeb1   | [PGNCCL] Launch kernel on current stream & remove `record_stream` entirely (#148590)                                         | kw2501@meta.com                                   | https://github.com/pytorch/pytorch/-/commit/17dbeb1 | 2025-03-07 23:33:08-08:00 |
|   2 | pytorch    | 148eb73   | Change nvcc arch flags for sm100 (#148774)                                                                                   | danvm@meta.com                                    | https://github.com/pytorch/pytorch/-/commit/148eb73 | 2025-03-08 19:05:51+00:00 |
|   3 | pytorch    | 7ffadff   | c10d/ProcessGroup: cleanup abort and shutdown (#148798)                                                                      | rice@fn.lc                                        | https://github.com/pytorch/pytorch/-/commit/7ffadff | 2025-03-08 18:33:14+00:00 |
|   4 | pytorch    | 9841f0d   | Add support for non functional collectives under FakeTensorMode and fake_pg for memory tracking (#147566)                    | sanketpurandare@gmail.com                         | https://github.com/pytorch/pytorch/-/commit/9841f0d | 2025-03-08 18:00:49+00:00 |
|   5 | pytorch    | 849cc05   | [CUDA][TF32] Account for tf32 in `test_efficient_conv_bn_eval` (#148802)                                                     | eddiey@nvidia.com                                 | https://github.com/pytorch/pytorch/-/commit/849cc05 | 2025-03-08 16:17:04+00:00 |
|   6 | pytorch    | c3b05c4   | [triton 3.3] support both specialize_impl and create_specialize_impl (#148806)                                               | dberard@fb.com                                    | https://github.com/pytorch/pytorch/-/commit/c3b05c4 | 2025-03-07 18:12:00-08:00 |
|   7 | pytorch    | 3745da1   | [AOTI] Swith to local cpp compile for fbcode (#148592)                                                                       | zhuoran@meta.com                                  | https://github.com/pytorch/pytorch/-/commit/3745da1 | 2025-03-08 08:38:26+00:00 |
|   8 | pytorch    | 5f1c79b   | [CD] Enable triton xpu windows build (#147637)                                                                               | chuanqi.wang@intel.com                            | https://github.com/pytorch/pytorch/-/commit/5f1c79b | 2025-03-08 05:28:42+00:00 |
|   9 | pytorch    | f7c0c23   | Fix compile errors (#148758)                                                                                                 | cyyever@outlook.com                               | https://github.com/pytorch/pytorch/-/commit/f7c0c23 | 2025-03-08 04:56:42+00:00 |
|  10 | pytorch    | 75179fd   | [Codemod][AddExplicitStrictExportArg] caffe2/test/inductor (#148781)                                                         | ycao@meta.com                                     | https://github.com/pytorch/pytorch/-/commit/75179fd | 2025-03-08 04:43:29+00:00 |
|  11 | pytorch    | 8f71d45   | Fix rms_norm in fp16/bf16 (#147203)                                                                                          | 11768013+riccardofelluga@users.noreply.github.com | https://github.com/pytorch/pytorch/-/commit/8f71d45 | 2025-03-08 04:43:15+00:00 |
|  12 | pytorch    | 85467ed   | Fix for AOTI + CUDAGraphs when calling from Python (#148601)                                                                 | jbschlosser@meta.com                              | https://github.com/pytorch/pytorch/-/commit/85467ed | 2025-03-07 15:58:33-05:00 |
|  13 | pytorch    | 9f170d9   | [Triton 3.3] Remove ROCm specific mm gemm template (#148662)                                                                 | sampsa.riikonen@amd.com                           | https://github.com/pytorch/pytorch/-/commit/9f170d9 | 2025-03-08 01:24:36+00:00 |
|  14 | pytorch    | a89e7c2   | [Upstream] Wrap log_2_e in tl.constexpr for new 3.3 bump (#148785)                                                           | drisspguessous@gmail.com                          | https://github.com/pytorch/pytorch/-/commit/a89e7c2 | 2025-03-07 16:22:42-08:00 |
|  15 | pytorch    | 179b7a0   | Do not crash when compiling quantized LORA models (#148435)                                                                  | lukas.pfahler@udo.edu                             | https://github.com/pytorch/pytorch/-/commit/179b7a0 | 2025-03-08 00:02:08+00:00 |
|  16 | pytorch    | 24085db   | Don't clear feedback_saver_fns after cache clear (#148723)                                                                   | gabeferns@meta.com                                | https://github.com/pytorch/pytorch/-/commit/24085db | 2025-03-07 23:43:55+00:00 |
|  17 | pytorch    | 187d5c0   | [logging] Log cudagraphify timings to dynamo_timed (#143220)                                                                 | slarsen@meta.com                                  | https://github.com/pytorch/pytorch/-/commit/187d5c0 | 2025-03-07 09:58:43-08:00 |
|  18 | pytorch    | f2dfe2d   | [Triton 3.3] [ROCm] Enabled split_scan support for ROCm builds (#147619)                                                     | Iurii.Paikov@amd.com                              | https://github.com/pytorch/pytorch/-/commit/f2dfe2d | 2025-03-07 23:06:17+00:00 |
|  19 | pytorch    | 0f85264   | Revert "[cutlass backend] Forward fix for less aligned gemm shapes (#148521)"                                                | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/0f85264 | 2025-03-07 22:42:13+00:00 |
|  20 | pytorch    | 755965d   | [inductor] fix matmul w/ torch.bucketize epilogue (#148769)                                                                  | dberard@fb.com                                    | https://github.com/pytorch/pytorch/-/commit/755965d | 2025-03-07 10:29:47-08:00 |
|  21 | pytorch    | 6774212   | [ROCm] Bump AOTriton to 0.9.2b (#148433)                                                                                     | Xinya.Zhang@amd.com                               | https://github.com/pytorch/pytorch/-/commit/6774212 | 2025-03-07 22:10:07+00:00 |
|  22 | pytorch    | 7b79e17   | [BE] Move cuda12.6 builds to gcc11 (#148740)                                                                                 | nshulga@meta.com                                  | https://github.com/pytorch/pytorch/-/commit/7b79e17 | 2025-03-07 12:58:17-08:00 |
|  23 | pytorch    | 08baaa7   | [Docs][TunableOp] TunableOp documentation update (#148384)                                                                   | 165712832+naromero77amd@users.noreply.github.com  | https://github.com/pytorch/pytorch/-/commit/08baaa7 | 2025-03-07 21:02:44+00:00 |
|  24 | pytorch    | bb94b65   | Revert "[cutlass backend] fix assertion that prevent self multiplication  (#148233)"                                         | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/bb94b65 | 2025-03-07 20:58:28+00:00 |
|  25 | pytorch    | d8dc700   | Delete duplicate entry from `docker-builds.yml` (#148782)                                                                    | 2453524+malfet@users.noreply.github.com           | https://github.com/pytorch/pytorch/-/commit/d8dc700 | 2025-03-07 20:55:46+00:00 |
|  26 | pytorch    | 99da439   | Revert "Remove Cuda 12.4 from nightly Binaries  (#148625)"                                                                   | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/99da439 | 2025-03-07 20:47:45+00:00 |
|  27 | pytorch    | b246cd7   | Revert "Move get accelerator to use build time flags when possible (#146098)"                                                | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/b246cd7 | 2025-03-07 18:59:58+00:00 |
|  28 | pytorch    | 1239176   | Remove Cuda 12.4 from nightly Binaries  (#148625)                                                                            | tingl@nvidia.com                                  | https://github.com/pytorch/pytorch/-/commit/1239176 | 2025-03-07 18:56:04+00:00 |
|  29 | pytorch    | 61c4074   | Add Windows Arm64 Nightly Builds (#139760)                                                                                   | 113098562+iremyux@users.noreply.github.com        | https://github.com/pytorch/pytorch/-/commit/61c4074 | 2025-03-07 18:53:56+00:00 |
|  30 | pytorch    | e839e4f   | Fix Wc++98-compat-extra-semi (#148757)                                                                                       | cyyever@outlook.com                               | https://github.com/pytorch/pytorch/-/commit/e839e4f | 2025-03-07 18:49:08+00:00 |
|  31 | pytorch    | 0a7ccee   | [ROCm][Windows] Disable Composable Kernels and Triton for Windows builds (#147334)                                           | Michal.Gallus@amd.com                             | https://github.com/pytorch/pytorch/-/commit/0a7ccee | 2025-03-07 18:40:49+00:00 |
|  32 | pytorch    | 18c6e00   | [CUDA Graphs][NCCL] Set event queries to happen under thread-local mode in `ProcessGroupNCCL.cpp` (#148594)                  | eddiey@nvidia.com                                 | https://github.com/pytorch/pytorch/-/commit/18c6e00 | 2025-03-07 18:39:02+00:00 |
|  33 | pytorch    | 9769618   | [CI] [inductor] Add cu126 inductor jobs and move away cu124 (#148612)                                                        | tingl@nvidia.com                                  | https://github.com/pytorch/pytorch/-/commit/9769618 | 2025-03-07 18:30:11+00:00 |
|  34 | pytorch    | 8059ead   | [ROCm] Incorporate ROCm triton specific tuning parameters (#148437)                                                          | 108682042+jataylo@users.noreply.github.com        | https://github.com/pytorch/pytorch/-/commit/8059ead | 2025-03-07 18:09:42+00:00 |
|  35 | pytorch    | a3b77d4   | Subprocess compile (attempt 2) (#148635)                                                                                     | aorenste@meta.com                                 | https://github.com/pytorch/pytorch/-/commit/a3b77d4 | 2025-03-06 19:53:54-08:00 |
|  36 | pytorch    | 50c9f6d   | [Windows][Inductor][XPU] Unload triton pyd files to be able to remove them on Windows. (#148323)                             | xinan.lin@intel.com                               | https://github.com/pytorch/pytorch/-/commit/50c9f6d | 2025-03-06 18:55:32-08:00 |
|  37 | pytorch    | d056948   | [XPU][Inductor] Update Intel triton for release 2.7. (#147727)                                                               | xinan.lin@intel.com                               | https://github.com/pytorch/pytorch/-/commit/d056948 | 2025-03-06 18:55:32-08:00 |
|  38 | pytorch    | abcca2f   | Revert "Fix `torch.nn.functional.hardswish` gradients corner case (#148049)"                                                 | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/abcca2f | 2025-03-07 16:05:56+00:00 |
|  39 | pytorch    | 17302b4   | Move get accelerator to use build time flags when possible (#146098)                                                         | desmaison.alban@gmail.com                         | https://github.com/pytorch/pytorch/-/commit/17302b4 | 2025-03-07 15:19:34+00:00 |
|  40 | pytorch    | d54b2b7   | [BE] Delete split builds (#148739)                                                                                           | nshulga@meta.com                                  | https://github.com/pytorch/pytorch/-/commit/d54b2b7 | 2025-03-06 22:42:20-08:00 |
|  41 | pytorch    | 372ad7b   | Enable FSDP2 on HPU device (#148667)                                                                                         | agulati@habana.ai                                 | https://github.com/pytorch/pytorch/-/commit/372ad7b | 2025-03-07 14:33:43+00:00 |
|  42 | pytorch    | bb84a23   | [ROCm] [TunableOp] Enable logging of BLAS parameters (#147034)                                                               | nick.romero@amd.com                               | https://github.com/pytorch/pytorch/-/commit/bb84a23 | 2025-03-07 09:32:56+00:00 |
|  43 | pytorch    | 3f069e7   | [mm_logs] enhance the printing for overview info (#148716)                                                                   | guorachel@meta.com                                | https://github.com/pytorch/pytorch/-/commit/3f069e7 | 2025-03-07 05:23:45+00:00 |
|  44 | pytorch    | 5f392ae   | Throws error when using torch.cuda.MemPool with expandable segments (#148378)                                                | syeahmed@nvidia.com                               | https://github.com/pytorch/pytorch/-/commit/5f392ae | 2025-03-06 15:22:21-08:00 |
|  45 | pytorch    | fe4b88f   | [HPU] Add hpu to fused kernels supported devices (#148666)                                                                   | singh.nitin512@gmail.com                          | https://github.com/pytorch/pytorch/-/commit/fe4b88f | 2025-03-07 04:28:30+00:00 |
|  46 | pytorch    | 33f8ab2   | [ROCm][TunableOp] Add support for rowwise scaling on scaled GEMM. (#148238)                                                  | nick.romero@amd.com                               | https://github.com/pytorch/pytorch/-/commit/33f8ab2 | 2025-03-07 04:12:44+00:00 |
|  47 | pytorch    | cdb4fd0   | Update win-vs2022-cuda12.1-py3 -> win-vs2022-cuda12.6-py3 (#148717)                                                          | atalman@fb.com                                    | https://github.com/pytorch/pytorch/-/commit/cdb4fd0 | 2025-03-07 03:21:24+00:00 |
|  48 | pytorch    | 127bd5a   | Add sparsity (#148513)                                                                                                       | drisspguessous@gmail.com                          | https://github.com/pytorch/pytorch/-/commit/127bd5a | 2025-03-05 19:42:11-08:00 |
|  49 | pytorch    | c8cd8f6   | [dynamo] Properly account for non-list instances in list comparison (#148470)                                                | ryanguo99@meta.com                                | https://github.com/pytorch/pytorch/-/commit/c8cd8f6 | 2025-03-04 11:33:46-08:00 |
|  50 | pytorch    | a7fe685   | Add cpp wrapper skip to cudagraph logs (#148700)                                                                             | elias.ellison@gmail.com                           | https://github.com/pytorch/pytorch/-/commit/a7fe685 | 2025-03-06 12:51:33-08:00 |
|  51 | pytorch    | 50eb4f3   | Enable UBSAN test (#147511)                                                                                                  | cyyever@outlook.com                               | https://github.com/pytorch/pytorch/-/commit/50eb4f3 | 2025-03-07 00:35:30+00:00 |
|  52 | pytorch    | 33a2853   | [codemod] Remove unused-variable in caffe2/torch/csrc/distributed/c10d/cuda/AsyncMM.cu (#148501)                             | rbarnes@meta.com                                  | https://github.com/pytorch/pytorch/-/commit/33a2853 | 2025-03-07 00:33:39+00:00 |
|  53 | pytorch    | a0bc6d8   | [CI][CUDA] Move away from cuda12.4, Add cuda12.6 eager CI tests (#148602)                                                    | tingl@nvidia.com                                  | https://github.com/pytorch/pytorch/-/commit/a0bc6d8 | 2025-03-07 00:15:04+00:00 |
|  54 | pytorch    | e2a0296   | [dtensor] add CuDNN SDPA op support to DTensor (#148537)                                                                     | 12968408+XilunWu@users.noreply.github.com         | https://github.com/pytorch/pytorch/-/commit/e2a0296 | 2025-03-05 16:19:10-08:00 |
|  55 | pytorch    | 3960f97   | Documents torch.cuda.MemPool API (#148374)                                                                                   | syeahmed@nvidia.com                               | https://github.com/pytorch/pytorch/-/commit/3960f97 | 2025-03-05 11:29:07-08:00 |
|  56 | pytorch    | ed9c8a5   | ROCm: Disable torch check for Multiplication of two Float8_e5m2 matrices (#148228)                                           | jagadish.krishnamoorthy@amd.com                   | https://github.com/pytorch/pytorch/-/commit/ed9c8a5 | 2025-03-06 22:12:41+00:00 |
|  57 | pytorch    | e6800bd   | [Test][Linalg][CUDA] Increase niter in test_svd_lowrank_cuda_float64 (#145930)                                               | aidyn.b.aitzhan@gmail.com                         | https://github.com/pytorch/pytorch/-/commit/e6800bd | 2025-03-06 22:10:49+00:00 |
|  58 | pytorch    | 2fb6546   | [cutlass backend] fix assertion that prevent self multiplication  (#148233)                                                  | henrylhtsang@meta.com                             | https://github.com/pytorch/pytorch/-/commit/2fb6546 | 2025-03-04 16:35:06-08:00 |
|  59 | pytorch    | d35a4dd   | [cutlass backend] Forward fix for less aligned gemm shapes (#148521)                                                         | henrylhtsang@meta.com                             | https://github.com/pytorch/pytorch/-/commit/d35a4dd | 2025-03-06 09:51:17-08:00 |
|  60 | pytorch    | 5a5ac98   | [aarch64] add libcufile for cu126 and cu128 (#148465)                                                                        | tingl@nvidia.com                                  | https://github.com/pytorch/pytorch/-/commit/5a5ac98 | 2025-03-06 21:39:39+00:00 |
|  61 | pytorch    | 3d62e81   | [DCP] fix dcp gather_object/scatter_object_list (#147675)                                                                    | i@soullan.com                                     | https://github.com/pytorch/pytorch/-/commit/3d62e81 | 2025-03-06 21:20:34+00:00 |
|  62 | pytorch    | 262411e   | [inductor] online softmax (#127011)                                                                                          | shunting@fb.com                                   | https://github.com/pytorch/pytorch/-/commit/262411e | 2025-03-03 16:05:15-08:00 |
|  63 | pytorch    | edd640a   | [BE][Ez]: Use itertools.chain.from_iterable when possible (#148190)                                                          | aaronGokaslan@gmail.com                           | https://github.com/pytorch/pytorch/-/commit/edd640a | 2025-03-06 20:37:01+00:00 |
|  64 | pytorch    | 29b28e9   | Fix `torch.nn.functional.hardswish` gradients corner case (#148049)                                                          | zesheng.zong@outlook.com                          | https://github.com/pytorch/pytorch/-/commit/29b28e9 | 2025-03-06 19:04:49+00:00 |
|  65 | pytorch    | 96176e3   | Revert "[ROCm] Bump AOTriton to 0.9.1b (#148433)"                                                                            | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/96176e3 | 2025-03-06 18:32:48+00:00 |
|  66 | pytorch    | b85ae06   | Update CPU tolerance for f16 triplet margin loss (#147742)                                                                   | georgewi@graphcore.ai                             | https://github.com/pytorch/pytorch/-/commit/b85ae06 | 2025-03-06 18:09:40+00:00 |
|  67 | pytorch    | d10bacd   | [AOTI][dashboard] Skip torchbench models not supported by export (#148359)                                                   | binbao@meta.com                                   | https://github.com/pytorch/pytorch/-/commit/d10bacd | 2025-03-03 12:14:01-08:00 |
|  68 | pytorch    | 28b68b4   | Revert "[cutlass backend] fix assertion that prevent self multiplication  (#148233)"                                         | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/28b68b4 | 2025-03-06 17:45:49+00:00 |
|  69 | pytorch    | 3cde4c3   | [BE] Remove `onlyCPU` decorator from test_local_scalar_dense (#148559)                                                       | 2453524+malfet@users.noreply.github.com           | https://github.com/pytorch/pytorch/-/commit/3cde4c3 | 2025-03-06 17:43:02+00:00 |
|  70 | pytorch    | 841451a   | Revert "[Inductor] Avoid tensor slice overflow for large step (#147433)"                                                     | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/841451a | 2025-03-06 17:33:08+00:00 |
|  71 | pytorch    | 679e7d2   | [mm_logs] follow up to add count info based on shape for inductor `aten.mm`s (#148623)                                       | guorachel@meta.com                                | https://github.com/pytorch/pytorch/-/commit/679e7d2 | 2025-03-06 16:20:04+00:00 |
|  72 | pytorch    | b160dda   | cpp_wrapper: reduce memory usage by removing unneeded temporaries (#147403)                                                  | bglass@quansight.com                              | https://github.com/pytorch/pytorch/-/commit/b160dda | 2025-03-05 22:30:24+00:00 |
|  73 | pytorch    | 5fb0f45   | [triton 3.3] test_triton_kernel_constants fix (#148626)                                                                      | dberard@fb.com                                    | https://github.com/pytorch/pytorch/-/commit/5fb0f45 | 2025-03-06 01:14:12+00:00 |
|  74 | pytorch    | d518490   | Make torch.serialization.skip_data work with torch.load (#148018)                                                            | mikaylagawarecki@gmail.com                        | https://github.com/pytorch/pytorch/-/commit/d518490 | 2025-03-06 08:50:56+00:00 |
|  75 | pytorch    | 209977e   | Add information about checkpoint offset to untyped storages when torch.load under FakeTensorMode (#147787)                   | mikaylagawarecki@gmail.com                        | https://github.com/pytorch/pytorch/-/commit/209977e | 2025-03-06 08:50:55+00:00 |
|  76 | pytorch    | bdcc1b5   | Allow torch.load under FakeTensorMode to load FakeTensors with correct devices (for plain Tensors) (#147786)                 | mikaylagawarecki@gmail.com                        | https://github.com/pytorch/pytorch/-/commit/bdcc1b5 | 2025-03-06 08:50:55+00:00 |
|  77 | pytorch    | 79aa174   | [dynamo] ctx_manager.py: replace unimplemented with unimplemented_v2 (#148570)                                               | zou3519@gmail.com                                 | https://github.com/pytorch/pytorch/-/commit/79aa174 | 2025-03-05 08:52:57-08:00 |
|  78 | pytorch    | ae6bb58   | Revert "[cutlass backend] Forward fix for less aligned gemm shapes (#148521)"                                                | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/ae6bb58 | 2025-03-06 06:59:39+00:00 |
|  79 | pytorch    | 4dc956a   | [Inductor][Triton] Fix test_autotune_inplace_kernel to work with newer Triton version (#148595)                              | paulzhan@fb.com                                   | https://github.com/pytorch/pytorch/-/commit/4dc956a | 2025-03-06 05:37:04+00:00 |
|  80 | pytorch    | 1fac477   | [Break XPU][Inductor UT] Generalize device-bias code introduced by #146866. (#148534)                                        | xinan.lin@intel.com                               | https://github.com/pytorch/pytorch/-/commit/1fac477 | 2025-03-04 22:14:09-08:00 |
|  81 | pytorch    | ad49cfc   | [cutlass backend] Forward fix for less aligned gemm shapes (#148521)                                                         | henrylhtsang@meta.com                             | https://github.com/pytorch/pytorch/-/commit/ad49cfc | 2025-03-05 10:51:22-08:00 |
|  82 | pytorch    | 8728d4b   | Clear triton kernels after parent make_launcher (#148604)                                                                    | jjwu@meta.com                                     | https://github.com/pytorch/pytorch/-/commit/8728d4b | 2025-03-05 14:05:48-08:00 |
|  83 | pytorch    | 1433bc1   | Remove CAFFE2_USE_EXCEPTION_PTR (#147247)                                                                                    | cyyever@outlook.com                               | https://github.com/pytorch/pytorch/-/commit/1433bc1 | 2025-03-06 02:56:23+00:00 |
|  84 | pytorch    | 43e1284   | Fix empty matrix handling of addmv in inductor (#143792)                                                                     | 32777264+maybeLee@users.noreply.github.com        | https://github.com/pytorch/pytorch/-/commit/43e1284 | 2025-03-06 02:09:22+00:00 |
|  85 | pytorch    | 32715a2   | [inductor][ck] add kBatch_sweep to config.rocm (#148223)                                                                     | coconutruben@meta.com                             | https://github.com/pytorch/pytorch/-/commit/32715a2 | 2025-03-06 01:14:31+00:00 |
|  86 | pytorch    | 2344149   | [scan] Refactoring of input checking and dynamo invocation (#142125)                                                         | boh@zurich.ibm.com                                | https://github.com/pytorch/pytorch/-/commit/2344149 | 2025-03-06 01:06:51+00:00 |
|  87 | pytorch    | 6cc3e69   | [inductor] use eager stride for custom op if no tags (#148367)                                                               | shunting@fb.com                                   | https://github.com/pytorch/pytorch/-/commit/6cc3e69 | 2025-03-04 14:19:43-08:00 |
|  88 | pytorch    | 703176e   | [ROCm] Fix sort for non-standard bool (#147459)                                                                              | prachi.gupta@amd.com                              | https://github.com/pytorch/pytorch/-/commit/703176e | 2025-03-06 00:23:02+00:00 |
|  89 | pytorch    | d6d670a   | [AOTI] build CPU CPP kernels at O3, and all other code at O1 (#148587)                                                       | bglass@quansight.com                              | https://github.com/pytorch/pytorch/-/commit/d6d670a | 2025-03-05 18:45:19+00:00 |
|  90 | pytorch    | 897fd9b   | Revert "Subprocess compile (#146134)"                                                                                        | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/897fd9b | 2025-03-05 22:41:19+00:00 |
|  91 | pytorch    | 5ccd659   | Fix decomp for linspace (#147997)                                                                                            | tmanlaibaatar@fb.com                              | https://github.com/pytorch/pytorch/-/commit/5ccd659 | 2025-03-04 10:47:43-08:00 |
|  92 | pytorch    | 9e755a1   | [ROCm] add gfx12 to nightly wheels (#148562)                                                                                 | Andy.LugoReyes@amd.com                            | https://github.com/pytorch/pytorch/-/commit/9e755a1 | 2025-03-05 21:56:22+00:00 |
|  93 | pytorch    | 10354e1   | Re-enable test_torchinductor:test_buffer_batch_norm (#148573)                                                                | slarsen@meta.com                                  | https://github.com/pytorch/pytorch/-/commit/10354e1 | 2025-03-05 09:47:19-08:00 |
|  94 | pytorch    | 87bd347   | [c10d] Move record param for init to the right place (#148571)                                                               | fduwjj@gmail.com                                  | https://github.com/pytorch/pytorch/-/commit/87bd347 | 2025-03-05 09:13:35-08:00 |
|  95 | pytorch    | 4aeca28   | [cutlass backend] fix assertion that prevent self multiplication  (#148233)                                                  | henrylhtsang@meta.com                             | https://github.com/pytorch/pytorch/-/commit/4aeca28 | 2025-03-04 16:35:06-08:00 |
|  96 | pytorch    | dd6ec87   | [BE] Relax sympy dependency to 1.13.3 or newer (#148575)                                                                     | 2453524+malfet@users.noreply.github.com           | https://github.com/pytorch/pytorch/-/commit/dd6ec87 | 2025-03-05 20:51:16+00:00 |
|  97 | pytorch    | c9edd37   | Revert "[dtensor] add aten._scaled_dot_product_cudnn_attention.default op support (#148377)"                                 | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/c9edd37 | 2025-03-05 19:45:16+00:00 |
|  98 | pytorch    | 8af79b7   | [ROCm] Bump AOTriton to 0.9.1b (#148433)                                                                                     | Xinya.Zhang@amd.com                               | https://github.com/pytorch/pytorch/-/commit/8af79b7 | 2025-03-05 19:11:53+00:00 |
|  99 | pytorch    | 9eef457   | [dtensor] add aten._scaled_dot_product_cudnn_attention.default op support (#148377)                                          | 12968408+XilunWu@users.noreply.github.com         | https://github.com/pytorch/pytorch/-/commit/9eef457 | 2025-03-05 00:05:42-08:00 |
| 100 | pytorch    | 9dd46a9   | Deprecate sm70 for cuda 12.8 binary (#147607)                                                                                | tingl@nvidia.com                                  | https://github.com/pytorch/pytorch/-/commit/9dd46a9 | 2025-03-05 18:54:13+00:00 |
| 101 | pytorch    | 3f4311d   | [CD] Upgrade xpu runtime pypi packages version and enable windows kineto again (#148319)                                     | chuanqi.wang@intel.com                            | https://github.com/pytorch/pytorch/-/commit/3f4311d | 2025-03-05 18:39:52+00:00 |
| 102 | pytorch    | c65ee72   | Initial implementation of host memory stats (#147660)                                                                        | mradmila@meta.com                                 | https://github.com/pytorch/pytorch/-/commit/c65ee72 | 2025-03-05 16:13:16+00:00 |
| 103 | pytorch    | 8274da9   | [c10d][PGNCCL] Fix capturability of isend and irecv (#148462)                                                                | 31858918+Aidyn-A@users.noreply.github.com         | https://github.com/pytorch/pytorch/-/commit/8274da9 | 2025-03-05 15:49:53+00:00 |
| 104 | pytorch    | 96afa8a   | [TEST][SPARSE] Simplify branching in test_cusparselt_backend (#148318)                                                       | aidyn.b.aitzhan@gmail.com                         | https://github.com/pytorch/pytorch/-/commit/96afa8a | 2025-03-05 10:16:56+00:00 |
| 105 | pytorch    | 0ef2e93   | [ROCm] [TunableOp] Track top solutions during tuning process (#147243)                                                       | nick.romero@amd.com                               | https://github.com/pytorch/pytorch/-/commit/0ef2e93 | 2025-03-05 09:34:59+00:00 |
| 106 | pytorch    | 6c3492b   | [ROCm] Enable mi300-specific workflows to be triggered on PRs (#147904)                                                      | 37884920+jithunnair-amd@users.noreply.github.com  | https://github.com/pytorch/pytorch/-/commit/6c3492b | 2025-03-05 06:00:37+00:00 |
| 107 | pytorch    | 2295efa   | Fix only logging ir_post_fusion with torch_compile_debug enabled (#148499)                                                   | elias.ellison@gmail.com                           | https://github.com/pytorch/pytorch/-/commit/2295efa | 2025-03-04 14:42:41-08:00 |
| 108 | pytorch    | df7e43e   | [AOTI] Fix aot_inductor_package test errors (#148279)                                                                        | binbao@meta.com                                   | https://github.com/pytorch/pytorch/-/commit/df7e43e | 2025-03-05 05:22:44+00:00 |
| 109 | pytorch    | b020d16   | stage 1 of depreate silent fallback of tuning gemm (#147798)                                                                 | henrylhtsang@meta.com                             | https://github.com/pytorch/pytorch/-/commit/b020d16 | 2025-03-04 23:42:44+00:00 |
| 110 | pytorch    | ed8ec0c   | [cutlass backend][BE] Fix two small things in cutlass backend standalone debugger (#148493)                                  | henrylhtsang@meta.com                             | https://github.com/pytorch/pytorch/-/commit/ed8ec0c | 2025-03-04 15:43:51-08:00 |
| 111 | pytorch    | 1673bc7   | [mm_logs][ez] dump tuned mm info at lowering stage (#148363)                                                                 | guorachel@meta.com                                | https://github.com/pytorch/pytorch/-/commit/1673bc7 | 2025-03-05 02:21:27+00:00 |
| 112 | pytorch    | edc3ca5   | [Profiler] Add profiler activity for HPU devices (#148182)                                                                   | witold.dziurdz@intel.com                          | https://github.com/pytorch/pytorch/-/commit/edc3ca5 | 2025-03-05 01:37:45+00:00 |
| 113 | pytorch    | b28cbe5   | [dynamo] remove internal stack trace for fullgraph=True graph breaks (#148205)                                               | williamwen@meta.com                               | https://github.com/pytorch/pytorch/-/commit/b28cbe5 | 2025-03-04 11:46:46-08:00 |
| 114 | pytorch    | b587329   | Add overload names to profiler trace (#143114)                                                                               | mwizak@graphcore.ai                               | https://github.com/pytorch/pytorch/-/commit/b587329 | 2025-03-05 01:00:26+00:00 |
| 115 | pytorch    | cf5e3f3   | Add cutlass kernel for rowwise scaled mm on sm100 (#148421)                                                                  | danvm@meta.com                                    | https://github.com/pytorch/pytorch/-/commit/cf5e3f3 | 2025-03-05 00:45:57+00:00 |
| 116 | pytorch    | 84b58bd   | Enable FSDP tests on XPU device (#147518)                                                                                    | cherry.zhang@intel.com                            | https://github.com/pytorch/pytorch/-/commit/84b58bd | 2025-03-04 23:49:33+00:00 |
| 117 | pytorch    | 93e9dae   | [cuDNN][SDPA][Nested Tensor] Experimental cuDNN Nested Tensor SDPA Support (forward only) (#141178)                          | eddiey@nvidia.com                                 | https://github.com/pytorch/pytorch/-/commit/93e9dae | 2025-03-04 23:09:09+00:00 |
| 118 | pytorch    | 5f47b7e   | [ROCm][TunableOp] Unit test for offline tuning of GEMM with bias (#148371)                                                   | nick.romero@amd.com                               | https://github.com/pytorch/pytorch/-/commit/5f47b7e | 2025-03-04 22:24:24+00:00 |
| 119 | pytorch    | 84961a0   | ci: Add workflow dispatch for commit hash update (#148486)                                                                   | eliuriegas@meta.com                               | https://github.com/pytorch/pytorch/-/commit/84961a0 | 2025-03-04 13:08:09-08:00 |
| 120 | pytorch    | d290186   | ci: Add triton to update hash workflow (#148472)                                                                             | eliuriegas@meta.com                               | https://github.com/pytorch/pytorch/-/commit/d290186 | 2025-03-04 13:08:08-08:00 |
| 121 | pytorch    | f30776c   | [BE] Upgrade to mypy 1.14 (#145966)                                                                                          | ZainR@meta.com                                    | https://github.com/pytorch/pytorch/-/commit/f30776c | 2025-03-04 20:58:22+00:00 |
| 122 | pytorch    | 439395c   | [MPS] add slogdet and logdet implementations to mps (#148287)                                                                | irakli.salia854@gmail.com                         | https://github.com/pytorch/pytorch/-/commit/439395c | 2025-03-04 19:49:23+00:00 |
| 123 | pytorch    | 63778cb   | Revert "[Inductor] Record Triton’s Base32 Cache Key in `.best_config` for Debugging (#147019)"                               | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/63778cb | 2025-03-04 19:20:15+00:00 |
| 124 | pytorch    | c219c5c   | Fix code descriptions in the test package. (#148145)                                                                         | phpjavaphp@gmail.com                              | https://github.com/pytorch/pytorch/-/commit/c219c5c | 2025-03-04 19:14:37+00:00 |
| 125 | pytorch    | f2f25a5   | Upgrade submodule oneDNN to v3.7.1 (#148293)                                                                                 | yanbing.jiang@intel.com                           | https://github.com/pytorch/pytorch/-/commit/f2f25a5 | 2025-03-04 13:56:45+00:00 |
| 126 | pytorch    | f339e41   | [inductor][triton] Fix average pool nd for int64 dtype (#146061)                                                             | mwizak@graphcore.ai                               | https://github.com/pytorch/pytorch/-/commit/f339e41 | 2025-03-04 13:53:47+00:00 |
| 127 | pytorch    | fdee607   | [DCP] Introduce process based async checkpointing (#147039)                                                                  | meetv@meta.com                                    | https://github.com/pytorch/pytorch/-/commit/fdee607 | 2025-03-04 13:33:28+00:00 |
| 128 | pytorch    | 16d0798   | add supports_coalescing property in c10d::Backend  to determine whether backend supports coalescing (#135338)                | taozhiweigis@163.com                              | https://github.com/pytorch/pytorch/-/commit/16d0798 | 2025-03-04 12:37:06+00:00 |
| 129 | pytorch    | e3e45d9   | [Inductor] Record Triton’s Base32 Cache Key in `.best_config` for Debugging (#147019)                                        | mail@alessandrosangiorgi.net                      | https://github.com/pytorch/pytorch/-/commit/e3e45d9 | 2025-03-04 12:16:38+00:00 |
| 130 | pytorch    | f1cce09   | Create unique test report files for distributed tests (#148325)                                                              | alexander.grund@tu-dresden.de                     | https://github.com/pytorch/pytorch/-/commit/f1cce09 | 2025-03-04 10:45:30+00:00 |
| 131 | pytorch    | e0f0db0   | updates to benchmarks (#144831)                                                                                              | drisspguessous@gmail.com                          | https://github.com/pytorch/pytorch/-/commit/e0f0db0 | 2025-03-03 19:18:29-08:00 |
| 132 | pytorch    | ac99fc7   | Updates to build rowwise scaled mm kernel on SM10.0a (#148274)                                                               | danvm@meta.com                                    | https://github.com/pytorch/pytorch/-/commit/ac99fc7 | 2025-03-04 05:23:38+00:00 |
| 133 | pytorch    | 70410f9   | doc/xpu: align description of SyclExtension with CPP/CUDA (#147988)                                                          | dmitry.v.rogozhkin@intel.com                      | https://github.com/pytorch/pytorch/-/commit/70410f9 | 2025-03-04 04:17:32+00:00 |
| 134 | pytorch    | ec2805a   | Remove outdated CUDA version check (#148142)                                                                                 | cyyever@outlook.com                               | https://github.com/pytorch/pytorch/-/commit/ec2805a | 2025-03-04 03:33:39+00:00 |
| 135 | pytorch    | 98bf2f1   | Use Python 3.9 typing (#148157)                                                                                              | cyyever@outlook.com                               | https://github.com/pytorch/pytorch/-/commit/98bf2f1 | 2025-03-04 03:09:51+00:00 |
| 136 | pytorch    | b7832f0   | Enable ASAN in CUDA tests (#147812)                                                                                          | cyyever@outlook.com                               | https://github.com/pytorch/pytorch/-/commit/b7832f0 | 2025-03-04 02:50:36+00:00 |
| 137 | pytorch    | 1751800   | [cutlass backend] Benchmark compared to aten and triton (#148347)                                                            | henrylhtsang@meta.com                             | https://github.com/pytorch/pytorch/-/commit/1751800 | 2025-03-04 01:45:33+00:00 |
| 138 | pytorch    | c21dc11   | [Intel GPU] Enable SDPA on XPU (#147614)                                                                                     | yi1.ding@intel.com                                | https://github.com/pytorch/pytorch/-/commit/c21dc11 | 2025-03-04 01:40:45+00:00 |
| 139 | pytorch    | b17f522   | Generate AOTI input check by default (#148005)                                                                               | shangdiy@meta.com                                 | https://github.com/pytorch/pytorch/-/commit/b17f522 | 2025-03-04 00:55:14+00:00 |
| 140 | pytorch    | 0bd2caa   | Docker release - pin buildkit to v0.19.0 (#148372)                                                                           | atalman@fb.com                                    | https://github.com/pytorch/pytorch/-/commit/0bd2caa | 2025-03-03 23:55:30+00:00 |
| 141 | pytorch    | d43c6f0   | [invoke_subgraph] Run joint passes on the hop graphs (#139325)                                                               | anijain@umich.edu                                 | https://github.com/pytorch/pytorch/-/commit/d43c6f0 | 2025-02-28 14:15:06-08:00 |
| 142 | pytorch    | 586d8df   | Fix condition for `CONVERT_NON_VECTORIZED_INIT` invocation (#148362)                                                         | nshulga@meta.com                                  | https://github.com/pytorch/pytorch/-/commit/586d8df | 2025-03-03 12:59:23-08:00 |
| 143 | pytorch    | d0b23e6   | [cutlass backend] Add main tests for mm, addmm and bmm - step 1 (#148229)                                                    | henrylhtsang@meta.com                             | https://github.com/pytorch/pytorch/-/commit/d0b23e6 | 2025-02-28 17:19:54-08:00 |
| 144 | pytorch    | a414138   | Use release notes label for module: distributed_checkpoint (#148352)                                                         | 31798555+janeyx99@users.noreply.github.com        | https://github.com/pytorch/pytorch/-/commit/a414138 | 2025-03-03 21:33:25+00:00 |
| 145 | pytorch    | e45040b   | [c10d] Add hccl distributed backend to c10d data structures (#146478)                                                        | anneog@habana.ai                                  | https://github.com/pytorch/pytorch/-/commit/e45040b | 2025-03-03 21:32:21+00:00 |
| 146 | pytorch    | 5207815   | Add support for no-op concat with padded output (#146866)                                                                    | 11392812+nandesuka@users.noreply.github.com       | https://github.com/pytorch/pytorch/-/commit/5207815 | 2025-03-03 21:10:43+00:00 |
| 147 | pytorch    | 07f876e   | Subprocess compile (#146134)                                                                                                 | aorenste@meta.com                                 | https://github.com/pytorch/pytorch/-/commit/07f876e | 2025-03-03 08:32:35-08:00 |
| 148 | pytorch    | b162b16   | [Inductor] Hot fix after #148011 (#148270)                                                                                   | anatoly.myachev@intel.com                         | https://github.com/pytorch/pytorch/-/commit/b162b16 | 2025-03-03 20:18:17+00:00 |
| 149 | pytorch    | d260d4f   | HSDP custom hook UTs are multi-threaded - can't set device rank (#148099)                                                    | prachi.gupta@amd.com                              | https://github.com/pytorch/pytorch/-/commit/d260d4f | 2025-03-03 19:48:49+00:00 |
| 150 | pytorch    | 302c660   | Consistently use load_torchbind_test_lib in tests (#148082)                                                                  | alexander.grund@tu-dresden.de                     | https://github.com/pytorch/pytorch/-/commit/302c660 | 2025-03-03 19:37:24+00:00 |
| 151 | pytorch    | 40c2505   | [logging] Log individual Triton kernel compilation times to dynamo_compile (#147022)                                         | slarsen@meta.com                                  | https://github.com/pytorch/pytorch/-/commit/40c2505 | 2025-03-01 16:44:07-08:00 |
| 152 | pytorch    | 0929181   | Fix extra semicolon warning (#148291)                                                                                        | cyyever@outlook.com                               | https://github.com/pytorch/pytorch/-/commit/0929181 | 2025-03-03 18:51:40+00:00 |
| 153 | pytorch    | 57addfc   | Significantly speed up save_cache_artifacts (#148227)                                                                        | oulgen@meta.com                                   | https://github.com/pytorch/pytorch/-/commit/57addfc | 2025-03-01 20:54:04-08:00 |
| 154 | pytorch    | d57f617   | [Inductor][CPP] Avoid transpose with cpp micro-gemm for FlexAttention (#147069)                                              | jianan.gu@intel.com                               | https://github.com/pytorch/pytorch/-/commit/d57f617 | 2025-03-03 01:22:26-08:00 |
| 155 | pytorch    | 6c089f5   | ci: move xpu triton build to manylinux 2.28 (#148195)                                                                        | chuanqi.wang@intel.com                            | https://github.com/pytorch/pytorch/-/commit/6c089f5 | 2025-03-03 12:31:05+00:00 |
| 156 | pytorch    | 6a3a1f9   | Enable XPU for Inductor MM Triton Kernel Benchmark (#148237)                                                                 | eikan.wang@intel.com                              | https://github.com/pytorch/pytorch/-/commit/6a3a1f9 | 2025-03-02 01:17:06+00:00 |
| 157 | pytorch    | 608377d   | Revert "[import][inductor] Simplify grid handling (#147583)"                                                                 | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/608377d | 2025-03-03 00:49:31+00:00 |
| 158 | pytorch    | 94afb16   | Revert "[c10d] Add hccl distributed backend to c10d data structures (#146478)"                                               | pytorchmergebot@users.noreply.github.com          | https://github.com/pytorch/pytorch/-/commit/94afb16 | 2025-03-02 21:22:04+00:00 |
| 159 | pytorch    | 9aa897b   | Remove unnecessary tensor clone (#148159)                                                                                    | cyyever@outlook.com                               | https://github.com/pytorch/pytorch/-/commit/9aa897b | 2025-03-02 16:21:39+00:00 |
| 160 | pytorch    | 1d7397a   | [Inductor] Avoid tensor slice overflow for large step (#147433)                                                              | yi1.ding@intel.com                                | https://github.com/pytorch/pytorch/-/commit/1d7397a | 2025-03-02 16:07:15+00:00 |
| 161 | pytorch    | 9c506aa   | [aotinductor] add option to disable runtime assertions (#146462)                                                             | colinpeppler@meta.com                             | https://github.com/pytorch/pytorch/-/commit/9c506aa | 2025-02-27 18:18:05+00:00 |
| 162 | pytorch    | b59776d   | [import][inductor] Simplify grid handling (#147583)                                                                          | jansel@meta.com                                   | https://github.com/pytorch/pytorch/-/commit/b59776d | 2025-03-02 07:31:07+00:00 |
| 163 | pytorch    | dae3fbf   | [c10d] Add hccl distributed backend to c10d data structures (#146478)                                                        | anneog@habana.ai                                  | https://github.com/pytorch/pytorch/-/commit/dae3fbf | 2025-03-02 05:13:48+00:00 |
| 164 | pytorch    | 6e10471   | [ci] disable cudagraph for tts_angular on dashboard (#148221)                                                                | boyuan@meta.com                                   | https://github.com/pytorch/pytorch/-/commit/6e10471 | 2025-03-02 03:31:19+00:00 |
| 165 | pytorch    | de7af81   | [async TP] insert reshape node to handle "reshape -> scaled mm -> reshape pattern" in async TP with rowwise scales (#148001) | danvm@meta.com                                    | https://github.com/pytorch/pytorch/-/commit/de7af81 | 2025-03-02 03:25:28+00:00 |
+-----+------------+-----------+------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------+-----------------------------------------------------+---------------------------+
2025-03-09 10:33:25 [INFO] Starting code hotspot analysis... 

2025-03-09 10:33:25 [INFO] Code hotspot analysis results:
2025-03-09 10:33:25 [INFO] Code hotspot analysis complete, detected 776 total file changes
2025-03-09 10:33:25 [INFO] 
+--------------------+-------------------------------------------------------------------------+------------+
| Directory          | File                                                                    |    Changes |
+--------------------+-------------------------------------------------------------------------+------------+
| pytorch/.ci        | .ci/docker/build.sh                                                     |          3 |
| ------------------ | ----------------------------------------------------------------------- | ---------- |
| pytorch/.github    | .github/workflows/docker-builds.yml                                     |          4 |
|                    | .github/workflows/trunk.yml                                             |          4 |
|                    | .github/scripts/generate_binary_build_matrix.py                         |          4 |
|                    | .github/workflows/periodic.yml                                          |          3 |
|                    | .github/workflows/pull.yml                                              |          3 |
|                    | .github/scripts/generate_ci_workflows.py                                |          3 |
|                    | .github/workflows/generated-linux-binary-manywheel-nightly.yml          |          3 |
|                    | .github/workflows/generated-windows-binary-wheel-nightly.yml            |          3 |
|                    | .github/workflows/build-triton-wheel.yml                                |          2 |
|                    | .github/workflows/slow.yml                                              |          2 |
|                    | .github/workflows/generated-linux-aarch64-binary-manywheel-nightly.yml  |          2 |
|                    | .github/workflows/generated-linux-binary-libtorch-cxx11-abi-nightly.yml |          2 |
|                    | .github/workflows/generated-linux-binary-manywheel-main.yml             |          2 |
|                    | .github/workflows/generated-linux-s390x-binary-manywheel-nightly.yml    |          2 |
|                    | .github/workflows/generated-macos-arm64-binary-wheel-nightly.yml        |          2 |
|                    | .github/workflows/generated-windows-binary-libtorch-debug-nightly.yml   |          2 |
|                    | .github/workflows/generated-windows-binary-libtorch-release-nightly.yml |          2 |
|                    | .github/workflows/nightly.yml                                           |          2 |
| ------------------ | ----------------------------------------------------------------------- | ---------- |
| pytorch/aten       | aten/src/ATen/native/transformers/cuda/attention.cu                     |          4 |
|                    | aten/src/ATen/native/transformers/cuda/sdp_utils.cpp                    |          4 |
|                    | aten/src/ATen/native/transformers/cuda/attention_backward.cu            |          3 |
|                    | aten/src/ATen/native/transformers/hip/aotriton_adapter.h                |          3 |
|                    | aten/src/ATen/native/transformers/hip/flash_attn/aot/mha_all_aot.hip    |          3 |
|                    | aten/src/ATen/native/native_functions.yaml                              |          3 |
|                    | aten/src/ATen/DeviceAccelerator.cpp                                     |          2 |
|                    | aten/src/ATen/cuda/detail/CUDAHooks.h                                   |          2 |
|                    | aten/src/ATen/detail/AcceleratorHooksInterface.h                        |          2 |
|                    | aten/src/ATen/mps/MPSHooks.h                                            |          2 |
|                    | aten/src/ATen/xpu/detail/XPUHooks.cpp                                   |          2 |
|                    | aten/src/ATen/xpu/detail/XPUHooks.h                                     |          2 |
|                    | aten/src/ATen/cpu/vec/vec256/vec256_bfloat16.h                          |          2 |
|                    | aten/src/ATen/native/cpu/Activation.cpp                                 |          2 |
|                    | aten/src/ATen/native/cuda/ActivationHardswishKernel.cu                  |          2 |
|                    | aten/src/ATen/cuda/tunable/GemmCommon.h                                 |          2 |
|                    | aten/src/ATen/cuda/tunable/TunableOp.h                                  |          2 |
|                    | aten/src/ATen/native/TensorShape.cpp                                    |          2 |
|                    | aten/src/ATen/native/cuda/RowwiseScaledMM.cu                            |          2 |
| ------------------ | ----------------------------------------------------------------------- | ---------- |
| pytorch/benchmarks | benchmarks/transformer/sdpa.py                                          |          2 |
|                    | benchmarks/dynamo/common.py                                             |          2 |
|                    | benchmarks/dynamo/torchbench.py                                         |          2 |
|                    | benchmarks/dynamo/torchbench.yaml                                       |          2 |
| ------------------ | ----------------------------------------------------------------------- | ---------- |
| pytorch/c10        | c10/cuda/CUDACachingAllocator.cpp                                       |          3 |
| ------------------ | ----------------------------------------------------------------------- | ---------- |
| pytorch/cmake      | cmake/External/aotriton.cmake                                           |          3 |
|                    | cmake/Codegen.cmake                                                     |          2 |
| ------------------ | ----------------------------------------------------------------------- | ---------- |
| pytorch/docs       | docs/source/torch.rst                                                   |          2 |
| ------------------ | ----------------------------------------------------------------------- | ---------- |
| pytorch/root       | setup.py                                                                |          2 |
| ------------------ | ----------------------------------------------------------------------- | ---------- |
| pytorch/test       | test/inductor/test_torchinductor.py                                     |         11 |
|                    | test/inductor/test_cutlass_backend.py                                   |         10 |
|                    | test/inductor/test_aot_inductor.py                                      |          6 |
|                    | test/test_transformers.py                                               |          5 |
|                    | test/test_cuda.py                                                       |          5 |
|                    | test/inductor/test_cuda_repro.py                                        |          4 |
|                    | test/test_nn.py                                                         |          3 |
|                    | test/fx/test_graph_pickler.py                                           |          3 |
|                    | test/inductor/test_compile_subprocess.py                                |          3 |
|                    | test/test_linalg.py                                                     |          3 |
|                    | test/distributed/tensor/test_attention.py                               |          3 |
|                    | test/expect/HasDecompTest.test_has_decomposition.expect                 |          3 |
|                    | test/inductor/test_triton_kernels.py                                    |          3 |
|                    | test/run_test.py                                                        |          3 |
|                    | test/inductor/test_kernel_benchmark.py                                  |          3 |
|                    | test/inductor/test_select_algorithm.py                                  |          3 |
|                    | test/inductor/test_cudagraph_trees.py                                   |          2 |
|                    | test/test_torch.py                                                      |          2 |
|                    | test/test_fake_tensor.py                                                |          2 |
|                    | test/inductor/test_padding.py                                           |          2 |
|                    | test/inductor/test_best_config.py                                       |          2 |
|                    | test/inductor/test_binary_folding.py                                    |          2 |
|                    | test/inductor/test_cpp_wrapper_hipify.py                                |          2 |
|                    | test/inductor/test_max_autotune.py                                      |          2 |
|                    | test/inductor/test_profiler.py                                          |          2 |
| ------------------ | ----------------------------------------------------------------------- | ---------- |
| pytorch/torch      | torch/_inductor/compile_fx.py                                           |          9 |
|                    | torch/_inductor/codecache.py                                            |          8 |
|                    | torch/distributed/distributed_c10d.py                                   |          6 |
|                    | torch/_inductor/ir.py                                                   |          6 |
|                    | torch/_inductor/codegen/cuda/cuda_kernel.py                             |          6 |
|                    | torch/_inductor/lowering.py                                             |          6 |
|                    | torch/testing/_internal/common_utils.py                                 |          6 |
|                    | torch/_C/_distributed_c10d.pyi                                          |          5 |
|                    | torch/_inductor/kernel/mm.py                                            |          5 |
|                    | torch/_inductor/codegen/cuda/gemm_template.py                           |          5 |
|                    | torch/_inductor/config.py                                               |          5 |
|                    | torch/testing/_internal/common_methods_invocations.py                   |          5 |
|                    | torch/serialization.py                                                  |          5 |
|                    | torch/_inductor/kernel/bmm.py                                           |          5 |
|                    | torch/_inductor/kernel/mm_scaled.py                                     |          5 |
|                    | torch/_inductor/codegen/cpp_wrapper_cpu.py                              |          5 |
|                    | torch/_inductor/codegen/cpp_wrapper_cpu_array_ref.py                    |          5 |
|                    | torch/csrc/distributed/c10d/ProcessGroupNCCL.cpp                        |          4 |
|                    | torch/csrc/distributed/c10d/init.cpp                                    |          4 |
|                    | torch/_inductor/select_algorithm.py                                     |          4 |
|                    | torch/_dynamo/utils.py                                                  |          4 |
|                    | torch/_inductor/codegen/triton.py                                       |          4 |
|                    | torch/_inductor/kernel/flex_attention.py                                |          4 |
|                    | torch/_inductor/kernel/mm_common.py                                     |          4 |
|                    | torch/_inductor/codegen/cpp.py                                          |          4 |
|                    | torch/_inductor/codegen/wrapper.py                                      |          4 |
|                    | torch/_inductor/codegen/cpp_wrapper_gpu.py                              |          4 |
|                    | torch/_inductor/scheduler.py                                            |          4 |
|                    | torch/_inductor/runtime/triton_heuristics.py                            |          4 |
|                    | torch/csrc/distributed/c10d/ProcessGroup.hpp                            |          3 |
|                    | torch/csrc/distributed/c10d/ProcessGroupNCCL.hpp                        |          3 |
|                    | torch/_inductor/cpp_builder.py                                          |          3 |
|                    | torch/testing/_internal/common_modules.py                               |          3 |
|                    | torch/csrc/inductor/aoti_package/model_package_loader.cpp               |          3 |
|                    | torch/_inductor/runtime/triton_helpers.py                               |          3 |
|                    | torch/_inductor/autotune_process.py                                     |          3 |
|                    | torch/_inductor/compile_fx_ext.py                                       |          3 |
|                    | torch/_inductor/compile_fx_subproc.py                                   |          3 |
|                    | torch/_inductor/virtualized.py                                          |          3 |
|                    | torch/_inductor/utils.py                                                |          3 |
|                    | torch/distributed/tensor/_ops/_matrix_ops.py                            |          3 |
|                    | torch/distributed/tensor/experimental/_attention.py                     |          3 |
|                    | torch/_inductor/codegen/simd.py                                         |          3 |
|                    | torch/_decomp/decompositions.py                                         |          3 |
|                    | torch/csrc/distributed/c10d/Backend.hpp                                 |          2 |
|                    | torch/distributed/_tools/mem_tracker.py                                 |          2 |
|                    | torch/distributed/_tools/sac_estimator.py                               |          2 |
|                    | torch/_inductor/package/package.py                                      |          2 |
|                    | torch/cuda/tunable.py                                                   |          2 |
|                    | torch/accelerator/__init__.py                                           |          2 |
|                    | torch/accelerator/_utils.py                                             |          2 |
|                    | torch/csrc/DeviceAccelerator.cpp                                        |          2 |
|                    | torch/utils/data/dataloader.py                                          |          2 |
|                    | torch/csrc/jit/runtime/symbolic_script.cpp                              |          2 |
|                    | torch/distributed/fsdp/_fully_shard/_fsdp_collectives.py                |          2 |
|                    | torch/_inductor/loop_body.py                                            |          2 |
|                    | torch/distributed/optim/zero_redundancy_optimizer.py                    |          2 |
|                    | torch/_decomp/__init__.py                                               |          2 |
|                    | torch/storage.py                                                        |          2 |
|                    | torch/_inductor/async_compile.py                                        |          2 |
|                    | torch/_inductor/graph.py                                                |          2 |
|                    | torch/_C/__init__.pyi.in                                                |          2 |
|                    | torch/cuda/__init__.py                                                  |          2 |
|                    | torch/autograd/profiler.py                                              |          2 |
|                    | torch/csrc/autograd/init.cpp                                            |          2 |
|                    | torch/csrc/profiler/orchestration/observer.h                            |          2 |
|                    | torch/csrc/profiler/python/init.cpp                                     |          2 |
|                    | torch/profiler/profiler.py                                              |          2 |
|                    | torch/_inductor/runtime/autotune_cache.py                               |          2 |
|                    | torch/_inductor/codegen/common.py                                       |          2 |
|                    | torch/_inductor/codegen/cpp_template_kernel.py                          |          2 |
|                    | torch/_inductor/codegen/cuda/device_op_overrides.py                     |          2 |
|                    | torch/_inductor/codegen/debug_utils.py                                  |          2 |
|                    | torch/_inductor/codegen/halide.py                                       |          2 |
|                    | torch/_inductor/codegen/mps.py                                          |          2 |
|                    | torch/_inductor/codegen/multi_kernel.py                                 |          2 |
|                    | torch/_inductor/codegen/rocm/rocm_kernel.py                             |          2 |
|                    | torch/_inductor/codegen/triton_combo_kernel.py                          |          2 |
|                    | torch/_inductor/codegen/triton_split_scan.py                            |          2 |
|                    | torch/_inductor/codegen/xpu/device_op_overrides.py                      |          2 |
|                    | torch/_inductor/fx_passes/b2b_gemm.py                                   |          2 |
|                    | torch/_inductor/kernel/conv.py                                          |          2 |
|                    | torch/_inductor/kernel/flex_decoding.py                                 |          2 |
|                    | torch/utils/_get_clean_triton.py                                        |          2 |
+--------------------+-------------------------------------------------------------------------+------------+
2025-03-09 10:33:25 [INFO] 
Hotspot analysis complete
2025-03-09 10:33:25 [INFO] Generating git patch/diff report file...
2025-03-09 10:33:25 [INFO] Git patch/diff report generated: pytorch/git_patch_report_20250309_103325.diff
2025-03-09 10:33:25 [INFO] File path: pytorch/git_patch_report_20250309_103325.diff
2025-03-09 10:33:25 [INFO] This report can be opened directly in Cursor for code change analysis or integrated with various LLM Agent tools

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

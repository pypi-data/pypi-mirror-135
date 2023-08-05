
import typing
import numpy as np
import requests
import os
import platform
from enum import Enum

List  = typing.List
Tuple = typing.Tuple

torch    = None
hub_url  = "http://zifuture.com:1556/fs/25.shared"
lean_url = "http://zifuture.com:1556/fs/pypi/"

lean_metas = [
    {
        "name": "trt8cuda102cudnn8",
        "cuda": "10.2",
        "cudnn": "8.2",
        "tensorRT": "8.1",
        "binary_url_linux": f"{lean_url}/trt8-cuda10.2-cudnn8.zip",
        "binary_url_windows": None
    }
]

pyc_metas = [
    {
        "name": "py37trt8cuda102cudnn8",
        "python": "3.7",
        "lean": "trt8cuda102cudnn8",
        "binary_url_linux": f"{lean_url}/py37-trt8-cuda10.2-cudnn8/libtrtpyc.so",
        "binary_url_windows": None
    },
    {
        "name": "py38trt8cuda102cudnn8",
        "python": "3.8",
        "lean": "trt8cuda102cudnn8",
        "binary_url_linux": f"{lean_url}/py38-trt8-cuda10.2-cudnn8/libtrtpyc.so",
        "binary_url_windows": None
    },
    {
        "name": "py39trt8cuda102cudnn8",
        "python": "3.9",
        "lean": "trt8cuda102cudnn8",
        "binary_url_linux": f"{lean_url}/py39-trt8-cuda10.2-cudnn8/libtrtpyc.so",
        "binary_url_windows": None
    }
]

def python_version_lite():
    import sys
    return ".".join(sys.version.split(".")[:2])

def lazy_import():
    global torch

    if torch is not None:
        return

    import torch


class LogLevel(Enum):
    Debug   = 5
    Verbose = 4
    Info    = 3
    Warning = 2
    Error   = 1
    Fatal   = 0


class HostFloatPointer(object):
    ptr    : int
    def __getitem__(self, index)->float: ...

class DeviceFloatPointer(object):
    ptr    : int
    # def __getitem__(self, index)->float: ...

class DataHead(object):
    Init   = 0
    Device = 1
    Host   = 2

class MixMemory(object):
    cpu    : HostFloatPointer
    gpu    : DeviceFloatPointer
    owner_cpu : bool
    owner_gpu : bool
    cpu_size  : int
    gpu_size  : int
    def __init__(self, cpu=0, cpu_size=0, gpu=0, gpu_size=0): ...
    
    # alloc memory and get_cpu / get_gpu
    def aget_cpu(self, size)->HostFloatPointer: ...
    def aget_gpu(self, size)->DeviceFloatPointer: ...
    def release_cpu(self): ...
    def release_gpu(self): ...
    def release_all(self): ...

class Tensor(object):
    shape  : List[int]
    ndim   : int
    stream : int
    workspace : MixMemory
    data   : MixMemory
    numpy  : np.ndarray
    empty  : bool
    numel  : int
    cpu    : HostFloatPointer
    gpu    : DeviceFloatPointer
    head   : DataHead
    def __init__(self, shape : List[int], data : MixMemory=None): ... 
    def to_cpu(self, copy_if_need=True): ...
    def to_gpu(self, copy_if_need=True): ...
    def resize(self, new_shape : List[int]): ...
    def resize_single_dim(self, idim:int, size:int): ...
    def count(self, start_axis:int=0)->int: ...
    def offset(self, indexs : List[int])->int: ...
    def cpu_at(self, indexs : List[int])->HostFloatPointer: ...
    def gpu_at(self, indexs : List[int])->DeviceFloatPointer: ...
    def reference_data(self, shape : List[int], cpu : int, cpu_size : int, gpu : int, gpu_size : int): ...

class Infer(object):
    stream         : int
    num_input      : int
    num_output     : int
    max_batch_size : int
    device         : int
    workspace      : MixMemory
    def __init__(self, file : str): ...
    def forward(self, sync : bool=True): ...
    def input(self, index : int = 0)->Tensor: ...
    def output(self, index : int = 0)->Tensor: ...
    def synchronize(self): ...
    def is_input_name(self, name)->bool: ...
    def is_output_name(self, name)->bool: ...
    def get_input_name(self, index=0)->str: ...
    def get_output_name(self, index=0)->str: ...
    def tensor(self, name)->Tensor: ...
    def print(self): ...
    def set_input(self, index : int, new_tensor : Tensor): ...
    def set_output(self, index : int, new_tensor : Tensor): ...
    def serial_engine(self)->bytes: ...

# 钩子函数的格式是，输入节点名称和shape，返回新的shape
def hook_reshape_layer_func(name : str, shape : List[int]): ...

# 注册编译onnx时的reshapelayer的钩子，一旦执行compileTRT后立即失效
def set_compile_hook_reshape_layer(func : hook_reshape_layer_func): ...

class Mode(Enum):
    FP32 : int = 0
    FP16 : int = 1
    INT8 : int = 2

class NormType(Enum):
    NONE      : int = 0
    MeanStd   : int = 1
    AlphaBeta : int = 2

class ChannelType(Enum):
    NONE      : int = 0
    Invert    : int = 1

class Norm(object):
    mean   : List[float]
    std    : List[float]
    alpha  : float
    beta   : float
    type   : NormType
    channel_type : ChannelType

    # out = (src * alpha - mean) / std
    @staticmethod
    def mean_std(mean : List[float], std : List[float], alpha : float = 1.0, channel_type : ChannelType = ChannelType.NONE): ...

    # out = src * alpha + beta
    @staticmethod
    def alpha_beta(alpha : float, beta : float, channel_type : ChannelType = ChannelType.NONE): ...

    @staticmethod
    def none(): ...

def set_device(device_id : int): ...
def get_device()->int : ...

class ModelSourceType(Enum):
    Caffe    = 0
    OnnX     = 1
    OnnXData = 2

class ModelSource(object):
    type       : ModelSourceType
    onnxmodel  : str
    descript   : str
    onnx_data  : bytes

    @staticmethod
    def from_onnx(file : str): ...

    @staticmethod
    def from_onnx_data(data : bytes): ...

class CompileOutputType(Enum):
    File    = 0
    Memory  = 1

class CompileOutput(object):
    type    : CompileOutputType
    data    : bytes
    file    : str

    @staticmethod
    def to_file(file): ...

    @staticmethod
    def to_memory(): ...
    
def compileTRT(
    max_batch_size               : int,
    source                       : ModelSource,
    saveto                       : CompileOutput,
    mode                         : Mode        = Mode.FP32,
    inputs_dims                  : np.ndarray  = np.array([], dtype=int),
    device_id                    : int         = 0,
    int8_norm                    : Norm        = Norm.none(),
    int8_preprocess_const_value  : int = 114,
    int8_image_directory         : str = ".",
    int8_entropy_calibrator_file : str = "",
    max_workspace_size           : int = 1 << 30
)->bool: ...

class ObjectBox(object):
    left        : float
    top         : float
    right       : float
    bottom      : float
    confidence  : float
    class_label : int
    width       : float
    height      : float
    cx          : float
    cy          : float

class YoloType(Enum):
    V5         : int  =  0
    V3         : int  =  0
    X          : int  =  1

class NMSMethod(Enum):
    CPU        : int  =  0
    FastGPU    : int  =  1

class SharedFutureObjectBoxArray(object):
    def get(self)->List[ObjectBox]: ...

class Yolo(object):
    valid : bool
    def __init__(
        self, 
        engine : str, 
        type : YoloType = YoloType.V5, 
        device_id : int = 0, 
        confidence_threshold : float = 0.4,
        nms_threshold : float        = 0.5,
        nms_method    : NMSMethod    = NMSMethod.FastGPU,
        max_objects   : int          = 1024,
        use_multi_preprocess_stream : bool = False
    ): ...
    def commit(self, image : np.ndarray)->SharedFutureObjectBoxArray: ...

class CenterNet(object):
    valid : bool
    def __init__(
        self, 
        engine : str, 
        device_id : int = 0, 
        confidence_threshold : float = 0.4,
        nms_threshold : float = 0.5
    ): ...
    def commit(self, image : np.ndarray)->SharedFutureObjectBoxArray: ...


def load_infer_file(file : str)->Infer: ...
def load_infer_data(data : bytes)->Infer: ...
def set_compile_int8_process(func): ...
def random_color(idd : int)->Tuple[int, int, int]: ...
def set_log_level(level : LogLevel): ...
def get_log_level()->LogLevel: ...
def set_devie(device : int): ...
def get_devie()->int: ...
def init_nv_plugins(): ...

default_nvbinary_version = "trt8cuda102cudnn8"
select_nvbinary_version = default_nvbinary_version
current_root = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
nvbinary_root = os.path.join(current_root, select_nvbinary_version, "lean")
python_version = python_version_lite()
python_version_module_name = python_version.replace(".", "")

os_name = platform.system().lower()
if os_name == "windows":
    pyc_module_name = "libtrtpyc"
    pyc_file_name = f"{pyc_module_name}.pyd"
    binary_url_name = f"binary_url_windows"
elif os_name == "linux":
    pyc_module_name = "libtrtpyc"
    pyc_file_name = f"{pyc_module_name}.so"
    binary_url_name = f"binary_url_linux"
else:
    raise RuntimeError(f"Unsupport platform {os_name}")

pyc_full_path = os.path.join(current_root, select_nvbinary_version, python_version_module_name, pyc_file_name)
pyc_meta = list(filter(lambda x:x["python"] == python_version, pyc_metas))

if len(pyc_meta) == 0:
    raise RuntimeError(f"Unsupported platform [python {python_version}], Could'nt found pyc_meta.")

pyc_meta = pyc_meta[0]
lean_name = pyc_meta["lean"]
lean_meta = list(filter(lambda x:x["name"] == lean_name, lean_metas))
if len(lean_meta) == 0:
    raise RuntimeError(f"Unsupported platform [{lean_name}], Could'nt found lean_meta.")

lean_meta = lean_meta[0]
if not os.path.exists(pyc_full_path):
    print("Can not found pyc file, will download it")
    from . import downloader

    binary_url = pyc_meta[binary_url_name]
    if binary_url is None:
        raise RuntimeError(f"{binary_url} is None, unsupport platform {os_name}")

    if not downloader.download_to_file(binary_url, pyc_full_path):
        raise RuntimeError(f"Download pyc {binary_url} failed.")

if not os.path.isdir(nvbinary_root) or len(os.listdir(nvbinary_root)) == 0:
    print("Can not found nvbinary package, will download it")
    from . import downloader
    lean_name = pyc_meta["lean"]
    binary_url = lean_meta[binary_url_name]
    if binary_url is None:
        raise RuntimeError(f"{binary_url} is None, unsupport platform {os_name}")

    lean_zip_file = downloader.get_cache_path(f"lean/{lean_name}.zip")
    if not downloader.download_and_verify_md5_saveto_file(binary_url, lean_zip_file):
        raise RuntimeError(f"Download lean {binary_url} failed.")

    todir = os.path.join(current_root, select_nvbinary_version)
    print(f"Extract nvbinary to... {todir}")
    downloader.extract_zip_to(lean_zip_file, todir)

if not os.path.isdir(nvbinary_root) or len(os.listdir(nvbinary_root)) == 0:
    raise RuntimeError(f"Can not found nvbinary, {nvbinary_root}")

if os_name == "windows":
    os.environ["PATH"] = os.environ["PATH"] + ";" + nvbinary_root
else:
    LD_LIBRARY_PATH = []
    if "LD_LIBRARY_PATH" in os.environ:
        LD_LIBRARY_PATH.append(os.environ["LD_LIBRARY_PATH"])
        
    import sys
    import os
    pydll_path = os.path.join(sys.exec_prefix, "lib")
    LD_LIBRARY_PATH.insert(0, current_root)
    LD_LIBRARY_PATH.insert(0, pydll_path)
    LD_LIBRARY_PATH.insert(0, nvbinary_root)
    LD_LIBRARY_PATH = ":".join(LD_LIBRARY_PATH)
    os.environ["LD_LIBRARY_PATH"] = LD_LIBRARY_PATH

    import ctypes

    def sorted_libs(name):
        if name.startswith("libnvrtc-builtins.so"): return 0
        if name.startswith("libnvrtc.so"): return 1
        if name.startswith("libcudart.so"): return 2
        if name.startswith("libcublasLt.so"): return 3
        if name.startswith("libcublas.so"): return 4
        if name.startswith("libcudnn_ops"): return 5
        if name.startswith("libcudnn_cnn"): return 6
        if name.startswith("libcudnn_adv"): return 7
        if name.startswith("libcudnn.so"): return 8
        if name.startswith("libnvinfer.so"): return 9
        if name.startswith("libnvinfer_plugin.so"): return 10
        return 11

    cuda_libs = os.listdir(nvbinary_root)
    cuda_libs = sorted(cuda_libs, key=sorted_libs)

    # load cuda
    for file in cuda_libs:
        if file.startswith("lib") and file.find(".so") != -1:
            ctypes.CDLL(os.path.join(nvbinary_root, file))

    # load python
    for so in os.listdir(pydll_path):
        if so.startswith("libpython") and so.endswith(".so"):
            ctypes.CDLL(os.path.join(pydll_path, so))

import sys
sys.path.insert(0, current_root)

# import binary module
m = __import__(f"{default_nvbinary_version}.{python_version_module_name}.{pyc_module_name}", globals(), locals(), ["*"])
for k in dir(m):
    if k.startswith("__") and k.endswith("__"):
        continue

    locals()[k] = getattr(m, k)

del sys.path[0]
#from .trt8cuda102cudnn8.libtrtpyc import *

def onnx_hub(name):
    # arcface_iresnet50 ：人脸识别Arcface
    # mb_retinaface     ：人脸检测Retinaface
    # scrfd_2.5g_bnkps  ：人脸检测SCRFD小模型2.5G Flops
    # fall_bp           ：摔倒分类模型
    # sppe              ：人体关键点检测AlphaPose
    # yolov5m           ：yolov5 m模型，目标检测coco80类
    # yolox_m           ：yolox m模型，目标检测coco80类

    if "HOME" in os.environ:
        root = os.path.join(os.environ["HOME"], ".trtpy")
        if not os.path.exists(root):
            os.mkdir(root)
    else:
        root = "."

    local_file = os.path.join(root, f"{name}.onnx")
    if not os.path.exists(local_file):
        url        = f"{hub_url}/{name}.onnx"
        
        print(f"OnnxHub: download from {url}, to {local_file}")
        remote     = requests.get(url)

        with open(local_file, "wb") as f:
            f.write(remote.content)
    return local_file


def reference_numpy_tensor(t, tensor):

    if tensor is None:
        return None

    if tensor.size == 0 or tensor.dtype != np.float32:
        raise TypeError("tensor Must float32 numpy.ndarray")

    tensor = np.ascontiguousarray(tensor)
    t.reference_data(tensor.shape, tensor.ctypes.data, tensor.size * 4, 0, 0)


def reference_torch_tensor(t, tensor):

    lazy_import()
    if tensor is None:
        return None

    if tensor.numel() == 0 or tensor.dtype != torch.float32:
        raise TypeError("Must float32 torch tensor")

    tensor = tensor.contiguous()
    if tensor.is_cuda:
        t.reference_data(tensor.shape, 0, 0, tensor.data_ptr(), tensor.numel() * 4)
    else:
        t.reference_data(tensor.shape, tensor.data_ptr(), tensor.numel() * 4, 0, 0)

def reference_tensor(t, tensor):

    if isinstance(tensor, np.ndarray):
        return reference_numpy_tensor(t, tensor)
    else:
        return reference_torch_tensor(t, tensor)


def infer_torch__call__(self : Infer, *args):

    lazy_import()
    templ  = args[0]
    stream = torch.cuda.current_stream().cuda_stream

    for index, x in enumerate(args):
        self.input(index).stream = stream
        reference_tensor(self.input(index), x)

    batch   = templ.size(0)
    device  = templ.device
    outputs = []
    for index in range(self.num_output):
        out_shape = self.output(index).shape
        out_shape[0] = batch
        out_tensor = torch.empty(out_shape, dtype=torch.float32, device=device)
        self.output(index).stream = stream
        reference_tensor(self.output(index), out_tensor)
        outputs.append(out_tensor)

    self.forward(False)

    if not templ.is_cuda:
        for index in range(self.num_output):
            self.output(index).to_cpu()

    if len(outputs) == 1:
        return outputs[0]

    return tuple(outputs)


def infer_numpy__call__(self : Infer, *args):

    templ = args[0]
    batch = templ.shape[0]
    assert batch <= self.max_batch_size, "Batch must be less max_batch_size"

    for index, x in enumerate(args):
        reference_tensor(self.input(index), x)

    outputs = []
    for index in range(self.num_output):
        out_shape = self.output(index).shape
        out_shape[0] = batch
        out_tensor = np.empty(out_shape, dtype=np.float32)
        reference_tensor(self.output(index), out_tensor)
        outputs.append(out_tensor)

    self.forward(False, True)

    for index in range(self.num_output):
        self.output(index).to_cpu()

    if len(outputs) == 1:
        return outputs[0]

    return tuple(outputs)


def infer__call__(self : Infer, *args):
    
    templ = args[0]
    if isinstance(templ, np.ndarray):
        return infer_numpy__call__(self, *args)
    else:
        return infer_torch__call__(self, *args)


def infer_save(self : Infer, file):

    with open(file, "wb") as f:
        f.write(self.serial_engine())


Infer.__call__ = infer__call__
Infer.save     = infer_save


def normalize_numpy(norm : Norm, image):

    if norm.channel_type == ChannelType.Invert:
        image = image[..., ::-1]

    if image != np.float32:
        image = image.astype(np.float32)

    if norm.type == NormType.MeanStd:
        mean = np.array(norm.mean, dtype=np.float32)
        std = np.array(norm.std, dtype=np.float32)
        alpha = norm.alpha
        out = (image * alpha - mean) / std
    elif norm.type == NormType.AlphaBeta:
        out = image * norm.alpha + norm.beta
    else:
        out = image
    return np.expand_dims(out.transpose(2, 0, 1), 0)


def normalize_torch(norm : Norm, image):

    lazy_import()
    if norm.channel_type == ChannelType.Invert:
        image = image[..., [2, 1, 0]]

    if image != torch.float32:
        image = image.float()

    if norm.type == NormType.MeanStd:
        mean = torch.tensor(norm.mean, dtype=torch.float32, device=image.device)
        std = torch.tensor(norm.std, dtype=torch.float32, device=image.device)
        alpha = norm.alpha
        out = (image * alpha - mean) / std
    elif norm.type == NormType.AlphaBeta:
        out = image * norm.alpha + norm.beta
    else:
        out = image
    return out.permute(2, 0, 1).unsqueeze(0)


def normalize(norm : Norm, image):
    if isinstance(image, np.ndarray):
        return normalize_numpy(norm, image)
    else:
        return normalize_torch(norm, image)


class MemoryData(object):

    def __init__(self):
        self.data = None

    def write(self, data):
        if self.data is None:
            self.data = data
        else:
            self.data += data

    def flush(self):
        pass


def compile_onnx_to_file(
    max_batch_size               : int,
    file                         : str,
    saveto                       : str,
    mode                         : Mode        = Mode.FP32,
    inputs_dims                  : np.ndarray  = np.array([], dtype=int),
    device_id                    : int         = 0,
    int8_norm                    : Norm        = Norm.none(),
    int8_preprocess_const_value  : int = 114,
    int8_image_directory         : str = ".",
    int8_entropy_calibrator_file : str = "",
    max_workspace_size           : int = 1 << 30
)->bool:
    return compileTRT(
        max_batch_size               = max_batch_size,
        source                       = ModelSource.from_onnx(file),
        output                       = CompileOutput.to_file(saveto),
        mode                         = mode,
        inputs_dims                  = inputs_dims,
        device_id                    = device_id,
        int8_norm                    = int8_norm,
        int8_preprocess_const_value  = int8_preprocess_const_value,
        int8_image_directory         = int8_image_directory,
        int8_entropy_calibrator_file = int8_entropy_calibrator_file,
        max_workspace_size           = max_workspace_size
    )

def compile_onnxdata_to_memory(
    max_batch_size               : int,
    data                         : bytes,
    mode                         : Mode        = Mode.FP32,
    inputs_dims                  : np.ndarray  = np.array([], dtype=int),
    device_id                    : int         = 0,
    int8_norm                    : Norm        = Norm.none(),
    int8_preprocess_const_value  : int = 114,
    int8_image_directory         : str = ".",
    int8_entropy_calibrator_file : str = "",
    max_workspace_size           : int = 1 << 30
)->bytes:
    mem     = CompileOutput.to_memory()
    success = compileTRT(
        max_batch_size               = max_batch_size,
        source                       = ModelSource.from_onnx_data(data),
        output                       = mem,
        mode                         = mode,
        inputs_dims                  = inputs_dims,
        device_id                    = device_id,
        int8_norm                    = int8_norm,
        int8_preprocess_const_value  = int8_preprocess_const_value,
        int8_image_directory         = int8_image_directory,
        int8_entropy_calibrator_file = int8_entropy_calibrator_file,
        max_workspace_size           = max_workspace_size
    )

    if not success:
        return None

    return mem.data


def from_torch(torch_model, input, 
    max_batch_size               : int         = None,
    mode                         : Mode        = Mode.FP32,
    inputs_dims                  : np.ndarray  = np.array([], dtype=int),
    device_id                    : int         = 0,
    input_names                  : List[str]   = None,
    output_names                 : List[str]   = None,
    dynamic                      : bool        = True,
    opset                        : int         = 11,
    onnx_save_file               : str         = None,
    engine_save_file             : str         = None,
    int8_norm                    : Norm        = Norm.none(),
    int8_preprocess_const_value  : int = 114,
    int8_image_directory         : str = ".",
    int8_entropy_calibrator_file : str = "",
    max_workspace_size           : int = 1 << 30
)->Infer:

    lazy_import()
    if isinstance(input, torch.Tensor):
        input = (input,)

    assert isinstance(input, tuple) or isinstance(input, list), "Input must tuple or list"
    input = tuple(input)
    torch_model.eval()

    if max_batch_size is None:
        max_batch_size = input[0].size(0)

    if input_names is None:
        input_names = []
        for i in range(len(input)):
            input_names.append(f"input.{i}")

    if output_names is None:
        output_names = []
        with torch.no_grad():
            dummys_output = torch_model(*input)

        def count_output(output):
            if isinstance(output, torch.Tensor):
                return 1

            if isinstance(output, tuple) or isinstance(output, list):
                count = 0
                for item in output:
                    count += count_output(item)
                return count
            return 0

        num_output = count_output(dummys_output)
        for i in range(num_output):
            output_names.append(f"output.{i}")
    
    dynamic_batch = {}
    for name in input_names + output_names:
        dynamic_batch[name] = {0: "batch"}

    onnx_data  = MemoryData()
    torch.onnx.export(torch_model, 
        input, 
        onnx_data, 
        opset_version=opset, 
        enable_onnx_checker=False, 
        input_names=input_names, 
        output_names=output_names,
        dynamic_axes=dynamic_batch if dynamic else None
    )

    if onnx_save_file is not None:
        with open(onnx_save_file, "wb") as f:
            f.write(onnx_data.data)

    model_data = compile_onnxdata_to_memory(
        max_batch_size = max_batch_size, 
        data           = onnx_data.data, 
        mode           = mode, 
        inputs_dims    = inputs_dims,
        device_id      = device_id,
        int8_norm      = int8_norm,
        int8_preprocess_const_value  = int8_preprocess_const_value,
        int8_image_directory         = int8_image_directory,
        int8_entropy_calibrator_file = int8_entropy_calibrator_file,
        max_workspace_size           = max_workspace_size
    )

    if engine_save_file is not None:
        with open(engine_save_file, "wb") as f:
            f.write(model_data)

    trt_model    = load_infer_data(model_data)
    torch_stream = torch.cuda.current_stream().cuda_stream
    
    if torch_stream != 0:
        trt_model.stream = torch_stream
        
    return trt_model

def upbound(value, align=32):
    return (value + align - 1) // align * align

def load(file_or_data)->Infer:

    if isinstance(file_or_data, str):
        return load_infer_file(file_or_data)
    else:
        return load_infer_data(file_or_data)

YOLOV5_NORM    = Norm.alpha_beta(1 / 255.0, 0.0, ChannelType.Invert)

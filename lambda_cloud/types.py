from typing import Literal


InstanceStatus = Literal["active", "booting", "unhealthy", "terminated"]
InstanceTypeName = Literal[
    "gpu_1x_a10",
    "gpu_1x_a100",
    "gpu_1x_a100_sxm4",
    "gpu_1x_a6000",
    "gpu_1x_h100_pcie",
    "gpu_1x_rtx6000",
    "gpu_2x_a100",
    "gpu_2x_a6000",
    "gpu_4x_a100",
    "gpu_4x_a6000",
    "gpu_8x_a100",
    "gpu_8x_a100_80gb_sxm4",
    "gpu_8x_v100",
]

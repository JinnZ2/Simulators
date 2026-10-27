"""The 36 subsystems and classifier A, transcribed from PREREGISTRATION.md.

Transcribed once, then checked against the committed file by the harness
so the two cannot drift.
"""
STAKE = [
    ("drivers/gpu/drm/amd/", "AMD"),
    ("drivers/gpu/drm/radeon/", "AMD"),
    ("drivers/gpu/drm/i915/", "Intel"),
    ("drivers/net/ethernet/mellanox/mlx5/", "Mellanox"),
    ("drivers/net/ethernet/broadcom/bnxt/", "Broadcom"),
    ("drivers/net/ethernet/intel/i40e/", "Intel"),
    ("drivers/net/ethernet/intel/ixgbe/", "Intel"),
    ("drivers/net/ethernet/chelsio/", "Chelsio"),
    ("drivers/net/ethernet/hisilicon/hns3/", "HiSilicon"),
    ("drivers/net/wireless/ath/ath10k/", "Qualcomm Atheros"),
    ("drivers/soc/qcom/", "Qualcomm"),
    ("drivers/scsi/lpfc/", "Emulex / Broadcom"),
    ("drivers/scsi/qla2xxx/", "QLogic / Marvell"),
    ("drivers/infiniband/hw/hfi1/", "Intel"),
    ("arch/arm/mach-rockchip/", "Rockchip"),
]
CORE = ["mm/", "kernel/sched/", "kernel/locking/", "kernel/rcu/",
        "kernel/time/", "kernel/irq/", "kernel/cgroup/", "kernel/trace/",
        "kernel/printk/", "block/", "lib/", "net/core/"]
MIXED = ["drivers/gpu/drm/nouveau/", "fs/btrfs/", "fs/xfs/", "fs/ext4/",
         "fs/f2fs/", "drivers/usb/core/", "net/ipv4/", "drivers/nvme/",
         "security/selinux/"]

CLASS_A = {}
for p, _f in STAKE:
    CLASS_A[p] = "STAKE_SPECIFIC"
for p in CORE:
    CLASS_A[p] = "SHARED_CORE"
for p in MIXED:
    CLASS_A[p] = "MIXED/UNCLEAR"

PATHS = list(CLASS_A)

TAGS = [("v4.14", "2017-11-12"), ("v4.19", "2018-10-22"),
        ("v5.4",  "2019-11-24"), ("v5.10", "2020-12-13"),
        ("v5.15", "2021-10-31"), ("v6.1",  "2022-12-11"),
        ("v6.6",  "2023-10-29"), ("v6.12", "2024-11-17")]

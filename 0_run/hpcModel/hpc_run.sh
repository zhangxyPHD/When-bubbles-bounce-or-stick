#!/bin/bash
Bos=(0.0002 0.0004 0.0007 0.001 0.002 0.004 0.007 0.01 0.02 0.04 0.07 0.4 0.6 0.8 1)
Gas=(6.0 6.5 7.0)
Lrises=(10)
refine_num=7
# 假设我们要提交10个任务
for Bo in "${Bos[@]}"; do
    for Ga in "${Gas[@]}"; do
        for Lrise in "${Lrises[@]}"; do
            # 定义变量
            FILENAME="bubble-L_rise$Lrise-Ga$Ga-Bo$Bo-Level$refine_num"

            # 为每个任务生成一个单独的sbatch文件，例如 job_run$i.sbatch
            cp job.sbatch job_run_$FILENAME.sbatch

            sed -i "s/jobname/$FILENAME/" job_run_$FILENAME.sbatch

            # 提交该修改好的作业脚本
            sbatch job_run_$FILENAME.sbatch
        done
    done
done

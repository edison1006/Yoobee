#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自包含版本：没有 CSV 时会自动生成示例数据。
功能：CSV -> Parquet (chunked) + 列统计 (min/max/mean/mean_abs/count/nulls)
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Iterator, Dict, Any
import pandas as pd
import numpy as np
import argparse

# -------- Loader --------
class CSVChunkLoader:
    def __init__(self, path: str, chunksize: int = 100_000):
        self.path, self.chunksize = path, chunksize
    def iter_chunks(self) -> Iterator[pd.DataFrame]:
        for ch in pd.read_csv(self.path, chunksize=self.chunksize, low_memory=False):
            yield ch

# -------- Stats --------
class ColumnAgg:
    def __init__(self):
        self.count=0; self.nulls=0; self.s=0.0; self.s_abs=0.0
        self.minv=None; self.maxv=None
    def update(self, s: pd.Series):
        x=pd.to_numeric(s, errors="coerce"); v=x.dropna()
        n_all,n=len(x),len(v)
        self.count+=n; self.nulls+=(n_all-n)
        if n==0: return
        mn,mx=float(v.min()),float(v.max())
        self.minv=mn if self.minv is None else min(self.minv,mn)
        self.maxv=mx if self.maxv is None else max(self.maxv,mx)
        self.s+=float(v.sum()); self.s_abs+=float(np.abs(v).sum())
    def result(self)->Dict[str,Any]:
        mean=self.s/self.count if self.count else None
        mean_abs=self.s_abs/self.count if self.count else None
        return {"min":self.minv,"max":self.maxv,"mean":mean,
                "mean_abs":mean_abs,"count":self.count,"nulls":self.nulls}

class Stats:
    def __init__(self): self._m:Dict[str,ColumnAgg]={}
    def update_df(self,df:pd.DataFrame):
        for c in df.columns: self._m.setdefault(c,ColumnAgg()).update(df[c])
    def to_df(self)->pd.DataFrame:
        return pd.DataFrame({k:v.result() for k,v in self._m.items()}).T[
            ["min","max","mean","mean_abs","count","nulls"]
        ]

# -------- Parquet sink --------
class ParquetSink:
    def __init__(self,out_dir:str,base:str):
        self.dir=Path(out_dir); self.dir.mkdir(parents=True,exist_ok=True)
        self.base, self.i=base,0
    def write_chunk(self,df:pd.DataFrame):
        p=self.dir/f"{self.base}_{self.i:05d}.parquet"
        try: df.to_parquet(p,index=False)   # 需要 pyarrow 或 fastparquet
        except Exception as e:
            raise RuntimeError("写 Parquet 失败，请安装: pip install pyarrow\n错误: "+str(e))
        self.i+=1

# -------- Pipeline --------
@dataclass
class Cfg:
    input_path:str; out_dir:str="output"; chunksize:int=100_000

class Pipeline:
    def __init__(self,cfg:Cfg):
        self.loader=CSVChunkLoader(cfg.input_path,cfg.chunksize)
        self.sink=ParquetSink(cfg.out_dir,Path(cfg.input_path).stem)
        self.stats=Stats(); self.out_dir=cfg.out_dir
    def run(self):
        for ch in self.loader.iter_chunks():
            self.stats.update_df(ch); self.sink.write_chunk(ch)
        out_csv=Path(self.out_dir)/"column_stats.csv"
        self.stats.to_df().to_csv(out_csv)
        print("Parquet 输出目录:",self.out_dir)
        print("列统计 CSV     :",out_csv)

# -------- Demo CSV --------
def make_demo_csv(path:str,rows:int=10000)->str:
    rng=np.random.default_rng(42)
    df=pd.DataFrame({
        "id":np.arange(rows),
        "value_a":rng.normal(0,10,rows),
        "value_b":rng.integers(-1000,1000,rows),
        "category":rng.choice(list("ABCD"),rows),
        "maybe_null":rng.normal(100,50,rows)
    })
    df.loc[rng.choice(rows,size=max(1,rows//20),replace=False),"maybe_null"]=np.nan
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(path,index=False)
    return path

# -------- CLI --------
def main():
    ap=argparse.ArgumentParser("CSV -> Parquet + Stats (自包含)")
    ap.add_argument("--input",default="demo.csv",help="CSV 路径 (默认: demo.csv)")
    ap.add_argument("--out-dir",default="output",help="输出目录")
    ap.add_argument("--chunksize",type=int,default=100_000)
    ap.add_argument("--rows",type=int,default=10000,help="若 CSV 不存在，自动生成的行数")
    a=ap.parse_args()

    # 如果 CSV 不存在，先生成
    if not Path(a.input).exists():
        print(f"未找到 {a.input}，正在生成示例 CSV...")
        make_demo_csv(a.input,a.rows)

    Pipeline(Cfg(a.input,a.out_dir,a.chunksize)).run()

if __name__=="__main__":
    main()

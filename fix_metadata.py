import nbformat
from pathlib import Path
import shutil

path = Path("study_group/1st/G1/Analysis.ipynb")

# 先備份
backup = path.with_suffix(".backup.ipynb")
shutil.copy(path, backup)

nb = nbformat.read(path, as_version=4)

# 只刪掉 widgets metadata，不動 cells / outputs
if "widgets" in nb.metadata:
    del nb.metadata["widgets"]

nbformat.write(nb, path)

print(f"Fixed: {path}")
print(f"Backup saved: {backup}")
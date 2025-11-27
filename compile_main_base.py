import subprocess
import re
import shutil
from pathlib import Path

BUILDDIR = 'tmp_build'

if __name__ == '__main__':

    latex_cmd = f'latexmk -r .latexmkrc -synctex=1 -interaction=nonstopmode -file-line-error -pdf -outdir={BUILDDIR} main_base.tex'
    subprocess.run(latex_cmd,
                   shell=True)
    (Path(BUILDDIR)/'main_base.pdf').rename('main_base.pdf')
    shutil.rmtree(BUILDDIR)
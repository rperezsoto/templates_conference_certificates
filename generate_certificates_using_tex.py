import subprocess
import re
import shutil
from pathlib import Path

import pandas as pd 

BUILDDIR='tmp_build'
OUTDIR='certificates'

def replace_and_write(infile:Path,outfile:Path,fullname:str|None=None):
    """
    Replaces the keyhold words of the input file by the corresponding values.
    In the given example it assumes only the keyword "FullName" is included
    and it should be replaced by the value of the fullname parameter.

    Parameters
    ----------
    infile : Path
        base file that contains the keywords
    outfile : Path
        new file to be generated
    fullname : str | None, optional
        value of the placeholder "FullName" in the infile. If None is provided
        nothing will be substituted. By default None. 
    """
    with open(infile,'r') as F:
        txt = F.read()
    if fullname is not None: 
        txt = re.sub('FullName', fullname, txt)
    
    # Note: In some fields the replacement may be complicated. For example if 
    # you include the titles of the contributions you may find some greek 
    # symbols, superindices... that in the csv file should appear in latex 
    # notation (e.g. "$\alpha$" or "$R^2$"). In those cases
    # you may find an error in the substitution process. To avoid it you might
    # have to change the representation of the string passed as an argument: 
    #
    #    if fullname is not None: 
    #       fullname_r = fullname.__repr__()[1:-1]
    #       txt = re.sub('Fullname', fullname_r, txt)

    with open(outfile,'w') as F: 
        F.write(txt)

def create_certificate(fullname:str, odir:Path, overwrite=False, keeptex=False):
    """
    Generate a certificate for a participant with their fullname in where we 
    have the "FullName" keyword in the base tex and rename the file to contain
    the full name of the participant. 

    Parameters
    ----------
    fullname : str
        full name of the participant as it should show within the certificate
    odir : Path
        output directory
    overwrite : bool, optional
        If enabled it will not skip the already existing certificates, 
        by default False
    keeptex : bool, optional
        If enabled it will keep a copy of the .tex file used to generate 
        the certificate, by default False. This is specially useful in debugging
        cases where certificates generated do not match the expected design. 
    """
    base_texfile = 'main_base.tex'
    current_texfile = Path('main.tex')

    stem = fullname.replace(' ','_').replace('.','')
    suffix = '.pdf' 
    
    # if you will be generating different types of certificates for the each 
    # participant (attendance, contribution...) I suggest that you change this 
    # variable to something like "suffix = '_attendance.pdf'
    # That way, in the final folder, certificates will be grouped by 
    # participant, which should make easier the process of sending them the 
    # documents through email. 

    ofile = odir / (stem + suffix)

    if ofile.exists() and not overwrite:
        print(f'        already exists')
        return

    build = Path(BUILDDIR)
    build.mkdir(exist_ok=True)

    replace_and_write(base_texfile,current_texfile,fullname=fullname)

    if keeptex: 
        shutil.copy(current_texfile,ofile.with_suffix('.tex'))

    latex_cmd = f'latexmk -r ./.latexmkrc -synctex=1 -interaction=nonstopmode -file-line-error -pdf -outdir={BUILDDIR} {current_texfile}'
    subprocess.run(latex_cmd,
                   shell=True,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.STDOUT)

    shutil.copy(build/current_texfile.with_suffix('.pdf').name,ofile)
    Path(current_texfile).unlink()
    shutil.rmtree(build)

if __name__ == '__main__':

    overwrite = False
    keeptex = False

    odir = Path(OUTDIR)
    odir.mkdir(exist_ok=True)

    df = pd.read_csv('participants_list.csv')

    for rowid,row in df.iterrows():

        fullname=row['fullname'].strip()
        print(f'Processing {fullname}')

        if row['has_attended']:
            print('    attendance')
            create_certificate(fullname, odir, overwrite=overwrite, keeptex=keeptex)
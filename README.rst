
Setup
-----

Start by cloning the repository. Note that the :code:`.latexmkrc`
was obtained from overleaf. Maybe not all its contents are 
necessary for this project but I am not an everyday latex user. 

Download the acrotex package from CTAN at: 
`https://ctan.org/pkg/eforms <https://ctan.org/pkg/eforms>`_

Next, unzip it and generate the appropriate latex files 
(\*.sty, \*.cfg and \*.def). 

.. code:: shell-session

   unzip acrotex.zip
   cd acrotex/
   latex acrotex.ins
   cd ..
   cp acrotex/*.sty .
   cp acrotex/*.def .
   cp acrotex/*.cfg .

After you have generated the files, ensure that you have python3 and 
pandas available. Otherwise adapt your certificate automation 
accordingly or install them. The only non-sdtlib python library is
pandas, and it is only used to iterate over the participants. You 
can also remove the pandas dependency but reading line by line if 
you prefer so. 

Adjusting the base template
------------------------------

Independently of how you decide to automate the generation of the
certificates (see next section) you will have to choose your own
background image (background.png and background.svg) as well as 
the number and location of the signature fields. 

To adjust the signature field location, uncomment 
:code:`%\previewOn` by removing the :code:`%` and then proceed to 
compile the main_base.tex file. (If you have latex and python 
installed, you should be able to do so with compile_main_base.py)

After adjusting the signature field ( the X and Y positions are 
adjusted at the :code:`\put` parameters while the width and height 
are controlled at the :code:`\sigField`

.. note:: 

   Adding another signature field is as simple as copying and 
   pasting the full :code:`\put` command that includes the 
   example :code:`\sigField` until the matching right brace. 


Automating the generation certificates
--------------------------------------

Here I include two base scripts for generating the certificates, 
one based on the modification of the svg files (which ends in the 
final pdf as a single image with the appropriate signature fields) 
and one based on the modification of the tex files. 

To use the svg-based script, inkscape must be available. And both 
scripts iterate on the file participants_list.csv to generate one 
certificate per entry. They allow some options, and you can 
enable/disable them at the start of the __main__ block in each of
the scripts. Those options are mainly related with keeping or not
the intermediate files and/or allow overwriting.



anisoms CLI tools
=================

ams-plot
--------

.. code-block:: text

    usage: ams-plot [-h] [-a ASCFILE] [-r RANFILE] [-c {s,g,p1,t1,p2,t2}]
                    [-d {p,t}] [-v]
                    output
    
    Plot AMS directions from ASC and RAN files.
    
    positional arguments:
      output                filename for PDF output
    
    optional arguments:
      -h, --help            show this help message and exit
      -a ASCFILE, --ascfile ASCFILE
                            ASC file containing data to plot
      -r RANFILE, --ranfile RANFILE
                            RAN file containing data to plot
      -c {s,g,p1,t1,p2,t2}, --coordinates {s,g,p1,t1,p2,t2}
                            co-ordinate system for ASC file ([s]pecimen,
                            [g]eographic, [p]aleo, or [t]ectonic)
      -d {p,t}, --directions {p,t}
                            source for directions in ASC file
                            ([p]rincipaldirections or [t]ensors)
      -v, --verbose
    

ams-asc-to-csv
--------------

.. code-block:: text

    usage: ams-asc-to-csv [-h] [-f] input_file output_file
    
    Convert anisotropy data from ASC format to CSV format
    
    positional arguments:
      input_file   input filename (Agico ASC format)
      output_file  output filename (comma separated value format)
    
    optional arguments:
      -h, --help   show this help message and exit
      -f, --ftest  only output samples which pass the F test
    

ams-print-ran-tensor
--------------------

.. code-block:: text

    usage: ams-print-ran-tensor [-h] ranfile [ranfile ...]
    
    Read Agico RAN files and output their AMS tensors.
    
    positional arguments:
      ranfile
    
    optional arguments:
      -h, --help  show this help message and exit
    

ams-tensor-to-dir
-----------------

.. code-block:: text

    usage: ams-tensor-to-dir [-h] [file [file ...]]
    
    Print the first principal directions of tensors
    
    positional arguments:
      file        text file containing one tensor per line. If no files are given,
                  data will be read from the standard input.
    
    optional arguments:
      -h, --help  show this help message and exit
    

ams-params-from-asc
-------------------

.. code-block:: text

    usage: ams-params-from-asc [-h] [--param parameter-name]
                               [--system coordinate-system]
                               asc-file [asc-file ...]
    
    Print selected parameters from an Agico ASC file
    
    positional arguments:
      asc-file              an ASC file to read
    
    optional arguments:
      -h, --help            show this help message and exit
      --param parameter-name, -p parameter-name
                            Parameter to extract(magsus, incdec, pj, t, or tensor)
      --system coordinate-system, -s coordinate-system
                            Co-ordinate system (specimen or geograph)
    


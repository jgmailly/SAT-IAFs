# SAT-based Solver for Incomplete Argumentation Frameworks

In the current version, this software computes one extension (SE problem) of an Incomplete Argumentation Framework, under the semantics defined in [1].

**Software usage**  

    python3 main.py <apx_file> <semantics>

Possible semantics: CO_S, CO_W, ST_S, ST_W corresponding to the strong complete, weak complete, strong stable and weak stable semantics.
The apx file describing the incomplete argumentation framework is as follows (see https://bitbucket.org/andreasniskanen/taeydennae/src/master/).

    arg(x).   # x is a definite argument
    ?arg(x)   # x is an uncertain argument
    att(x,y)  # (x,y) is a definite attack
    ?att(x,y) # (x,y) is an uncertain attack


**Related publication:**  
[1] Jean-Guy Mailly, Extension-Based Semantics for Incomplete Argumentation Frameworks. CLAR 2021: 322-341

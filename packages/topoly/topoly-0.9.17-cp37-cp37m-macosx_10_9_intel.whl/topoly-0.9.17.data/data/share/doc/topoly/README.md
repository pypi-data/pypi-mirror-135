Topoly is a **Python** package that collects programs useful for 
**polymer topology** analysis.

What you can do with Topoly?
----------------------------------

* Find knots, links, lassos, theta-curves, handcuffs and their type.
* Calculate knot/link invariants:

  * Polynomials: Alexander, Jones, Conway, HOMFLY, Yamada, Kauffman, BLM/Ho,
  * Brackets: Kauffman, APS,
  * Other: writhe, Gaussian linking number.

* Find minimal surface of a loop.
* Simplify polymer structure preserving its topology.
* Generate random polygon structures: walks, loops, lassos, handcuffs.
* Generate knot map (like in KnotProt).
* Calculate sum (U) and product (#) of knots.
* Visualize structures.

Provided executable programs 
----------------------------------

Apart from a Python library, this package provides a set of executable programs:  

1. knotnet - find knots using the Alexander Polynomial
2. homflylink
3. surfacesmytraj
4. ncuclinks
5. lmpoly
6. gln - compute the Gaussian linking number

Installation
----------------------------------

Make sure you have a recent version of **pip**. You can upgrade it by running:

``pip3 install --upgrade pip``
    
Install Topoly using the standard python package installer PIP:

``pip3 install topoly``

Topoly can be installed without administrative privileges in the home folder of a particular user or in a Python
Virtual Environment.
In that case all files (binaries, documentation, libraries and python modules) will be installed in:

``$HOME/.local/``

or ``venv/`` respectively.

If you choose to install Topoly with administrative privileges then everything will be installed in:
`/usr/local/`

Using Topoly
----------------------------------

Have a look at our website: https://topoly.cent.uw.edu.pl

or our tutorial project: https://github.com/ilbsm/topoly_tutorial

Contact
----------------------------------

INTERDISCIPLINARY LABORATORY of BIOLOGICAL SYSTEMS MODELLING, University of Warsaw, Warsaw, Poland

https://jsulkowska.cent.uw.edu.pl/

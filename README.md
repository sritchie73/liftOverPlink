liftOverPlink
=============
[LiftOver][1] is a commandline tool used to bring genomics analysis to
the same reference build, provided by the University of California, Santa 
Cruz (UCSC) as part of their [Genome Browser][2].

[LiftOver][1] has three use cases:
 1. Converting the genome position from one genome assembly to another
 2. Converting a dbSNP rs ID from one build to another
 3. Converting both the genome position, and dbSNP rs ID over different
    versions.

The [LiftOver][1] does not work natively with genotype data stored in
the commonly used [plink data formats][3]. The [Abecasis Lab][4] at the 
University of Michigan has developed a [rudimentary wrapper][5] in the form
of a python script to work with plink data stored in the `PED` and `MAP`
formats.

This repository provides a more polished commandline tool for this task: 
[liftOverPlink](liftOverPlink.py)


[1]: http://genome.sph.umich.edu/wiki/LiftOver
[2]: http://genome.ucsc.edu/
[3]: http://pngu.mgh.harvard.edu/~purcell/plink/data.shtml
[4]: http://genome.sph.umich.edu/wiki/Abecasis_Lab
[5]: http://genome.sph.umich.edu/wiki/LiftMap.py


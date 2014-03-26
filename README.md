liftOverPlink
=============
[liftOver][1] is a commandline tool for Linux and Mac OSX, which is used 
to bring genomic data to the same reference build. It is provided by the 
University of California, Santa Cruz (UCSC) as part of their 
[Genome Browser][2].

[liftOver][1] has three use cases:
 1. Converting the genome position from one genome assembly to another
 2. Converting a dbSNP rs ID from one build to another
 3. Converting both the genome position, and dbSNP rs ID over different
    versions.

The [liftOver][1] does not work natively with genotype data stored in
the commonly used [plink data formats][3]. The [Abecasis Lab][4] at the 
University of Michigan has developed a [rudimentary wrapper][5] in the
form of a python script to work with plink data stored in the `PED` and 
`MAP` formats.

This repository provides a more polished commandline tool for this task: 
[liftOverPlink](liftOverPlink.py)

To use this tool, you will need the [liftOver binary][6] along with the 
appropriate `chain files` which tell [liftOver][1] how to convert
between different genome builds. These can be found at the 
[UCSC Genome Bioinformatics Downloads Page][7], by following the 
"liftOver" links for your organism of choice.


[1]: http://genome.sph.umich.edu/wiki/liftOver
[2]: http://genome.ucsc.edu/
[3]: http://pngu.mgh.harvard.edu/~purcell/plink/data.shtml
[4]: http://genome.sph.umich.edu/wiki/Abecasis_Lab
[5]: http://genome.sph.umich.edu/wiki/LiftMap.py
[6]: http://hgdownload.cse.ucsc.edu/admin/exe/
[7]: http://hgdownload.cse.ucsc.edu/downloads.html

---
## Change Log

[liftOverPlink](liftOverPlink.py) is modified from the [liftMap.py][5] 
script provided by the [Abecasis Lab][4] to:
 - Take a user specified chain file.
 - To look for liftOver in `$PATH` or a user specified location, rather
   than the original developer's specific download location.
 - Provide usage documentation and help messages.
 - To clean up the left over `BED` files to avoid confusion.

The core functionality and algorithms remain identical to [liftMap.py][5].

---
## Usage

```
usage: liftOverPlink.py [-h] -m MAPFILE [-p PEDFILE] [-d DATFILE] -o PREFIX -c
                        CHAINFILE [-e LIFTOVEREXECUTABLE]

liftOverPlink.py converts genotype data stored in plink's PED+MAP format from
one genome build to another, using liftOver.

optional arguments:
  -h, --help            show this help message and exit
  -m MAPFILE, --map MAPFILE
                        The plink MAP file to `liftOver`.
  -p PEDFILE, --ped PEDFILE
                        Optionally remove "unlifted SNPs" from the plink PED
                        file after running `liftOver`.
  -d DATFILE, --dat DATFILE
                        Optionally remove "unlifted SNPs" from a data file
                        containing a list of SNPs (e.g. for --exclude or
                        --include in `plink`)
  -o PREFIX, --out PREFIX
                        The prefix to give to the output files.
  -c CHAINFILE, --chain CHAINFILE
                        The location of the chain file to provide to
                        `liftOver`.
  -e LIFTOVEREXECUTABLE, --bin LIFTOVEREXECUTABLE
                        The location of the `liftOver` executable.
```

---
## Details

[liftOverPlink](liftOverPlink.py) is simply a wrapper around [liftOver][1];
it works by converting the the plink `MAP` files to the `BED` format
[liftOver][1] expects (**Note**: this is completely unrelated to plink's 
`BED` format!!). [liftOver][1] then updates the information in this `BED`
file using the information in the provided `chain file`, and then
[liftOverPlink](liftOverPlink.py) converts this `BED` file back to a 
`MAP` file.

During the conversion process, some SNPs may fail to be converted
between builds. There are a [number of reasons][8] a SNP may fail to be 
"lifted", which boil down to that SNP not existing in the genome build
you are converting to. These are referred to as "unlifted" SNPs and are
written out to a file with the `.unlifted` extension, with the prefix
specified for the output files by the `--out` argument.

[liftOverPlink](liftOverPlink.py) can also optionally remove unlifted
SNPs from the `PED` file (this is highly recommended), and can update
any other file containing a list of rs IDs (passed in to the `--dat` 
argument).

If the [liftOver][1] executable is not in your `$PATH` then you can
optionally specify a location for [liftOverPlink](liftOverPlink.py) to
call it from using the `--bin` argument.

[8]: http://genome.sph.umich.edu/wiki/LiftOver#Various_reasons_that_lift_over_could_fail

---
## Addtional Tools

### Removing bad lifted SNPs
In the case of lifting from build hg19 to hg38, some of the SNPs that
get lifted have "bad" Chromosomes, like "22_KI270879v1_alt" for example.
[rmBadLifts](rmBadLifts.py) is designed to handle this case: it removes
these SNPs from the `MAP` file, and creates a file (`--log`) containing
a list of these rsIDs:

**Usage**

```
usage: rmBadLifts.py [-h] -m MAPFILE -o OUTFILE -l LOGFILE

rmBadLifts.py goes through a plink MAP file, identifies and removes SNPs not
on chromosomes 1 to 22

optional arguments:
  -h, --help            show this help message and exit
  -m MAPFILE, --map MAPFILE
                        MAP file to process.
  -o OUTFILE, --out OUTFILE
                        New MAP file to output.
  -l LOGFILE, --log LOGFILE
                        File to output the bad rsIDs to.
```

**Workflow**

The workflow when handling these SNPs is complicated:
 1. Create a "lifted" `MAP` file.
 2. Remove bad lifted SNPs from that `MAP` file.
 3. Generate a good `PED` file by excluding "unlifted", and bad
    "lifted" SNPs.
 4. Combine the fixed `PED` file, with the fixed `MAP` file.

On Linux this would look something like:

```bash
python liftOverPlink.py --map genotypes --out lifted --chain hg19ToHg38.over.chain.gz
python rmBadLifts.py --map lifted.map --out good_lifted.map --log bad_lifted.dat
cut -f 2 bad_lifted.dat > to_exclude.dat
cut -f 4 lifted.unlifted | sed "/^#/d" >> to_exclude.dat 
# Note: this will clobber the lifted MAP file generated by `liftOverPlink`:
plink --file genotypes --recode --out lifted --exclude bad_lifted.dat 
plink --ped lifted.ped --map good_lifted.map --recode --out final
```


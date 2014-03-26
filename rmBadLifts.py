#!/usr/bin/python
import os
import sys
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="%(prog)s goes through a plink MAP file, identifies" +
                " and removes SNPs not on chromosomes 1 to 22"
  )
  parser.add_argument("-m", "--map", dest="mapFile", required=True,
                      help="MAP file to process.")
  parser.add_argument("-o", "--out", dest="outFile", required=True,
                      help="New MAP file to output.")
  parser.add_argument("-l", "--log", dest="logFile", required=True,
                      help="File to output the bad rsIDs to.")
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

  args = parser.parse_args()

  if args.outFile == args.mapFile:
    sys.stderr.write(
      "Error: the location of the new MAP file can't be the same as" +
      " the old MAP file!"
    )
    sys.exit(1)

  outFile = open(args.outFile, "w") # out file
  logFile = open(args.logFile, "w") # log file

  with open(args.mapFile, "r") as mapFile:
    for line in mapFile:
      chro = line.split()[0]
      if chro in [str(i) for i in range(1,23)]:
        outFile.write(line)
      else:
        logFile.write(line)


import os
import sys
import time
import argparse


def main(fromHere, toHere, inputFile):

    maxFiles = 1         # the number of files to move per loop
    sleepTime = 1        # the number of seconds to pause between loops
    currentIndex = 0

    fromPath = fromHere + "/{0}"
    toPath = toHere + "/{0}"

    with open("moveFileResults.txt", "w") as outfile:      # write status of file movement to this file
        with open(inputFile, "r") as infile:  # read the list of files to move from this file
            while True:
                filename = infile.readline()

                if not filename:
                    outfile.write("No more files\r\n")
                    print("No more files")
                    break;

                filename = filename.replace('\n', '')

                currentIndex += 1        
                outfile.write("Moving file {0}\r\n".format(filename))

                print("Moving file {0}".format(filename))
                try:
                    # os.utime(fromPath.format(filename))
                    os.rename(fromPath.format(filename), toPath.format(filename))
                except OSError as ex:
                    outfile.write("file access problem for file {0}:{1}\r\n".format(filename,str(ex)))
                    print("file access problem for file {0}:{1}".format(filename,str(ex)))
                except PermissionError as ex:
                    outfile.write("Cannot access file {0}:{1}\r\n".format(filename,str(ex)))
                    print("Cannot access file {0}:{1}".format(filename,str(ex)))
                except FileNotFoundError:
                    outfile.write("did not find file {0}\r\n".format(filename))
                    print("did not find file {0}".format(filename))
                except FileExistsError:
                    outfile.write("file already exists{0}\r\n".format(filename))
                    print("file already exists{0}".format(filename))

                if (currentIndex == maxFiles):
                    outfile.flush()
                    time.sleep(sleepTime)
                    currentIndex = 0


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sourcedir",   help="The Source Directory")
    parser.add_argument("-d", "--destdir",    help="The Destination Directory")
    parser.add_argument("-f", "--file",       help="The file containing the list of files to move")
    args = parser.parse_args()

    if args.sourcedir is None or args.destdir is None or args.file is None:
            print(parser.print_help())
            sys.exit()

    main(args.sourcedir, args.destdir, args.file)



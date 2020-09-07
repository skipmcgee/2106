#!/usr/bin/env python3

##################################################################################
#
# Created by Skip McGee for DJC2 20.2 AKA "The Looters"
#
#
##################################################################################

# Import statements
try:
    import pip
except ImportError:
    try:
        subprocess.call(["yum", "install", "-y", "rh-python36-python-pip"])
        import pip
    except:
        try:
            subprocess.call(["yum", "install", "-y", "python-pip"])
            import pip
        except:
            pass
# import pdfforms
try:
    import pdfforms
except ImportError:
    try:
        subprocess.call(["yum", "install", "-y","pdfforms"])
        import pdfforms
    except:
      try:
        subprocess.call(["pip", "install", "pdfforms"])
    except:
        print("Error with installing pdfforms, unable to install... exiting...")
        exit()

# pdfforms inspect f2106.pdf
# pdfforms fill userdata.csv


# Define the main
def main():
    try:
        print("trying...")
    except:
        sys.stderr.write(sys.err)
    return

# Call the main function
if __name__ == "__main__":
    main()
    exit()

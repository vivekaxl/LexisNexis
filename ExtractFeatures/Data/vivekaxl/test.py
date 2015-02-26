import os
import glob
dir_name = "/home/vivek/GIT/Courses/Misc/Seive/pom3/"
modules = glob.glob(os.path.dirname(dir_name)+"/*.py")
__all__ = [ os.path.basename(f)[:-3] for f in modules]
print __all__

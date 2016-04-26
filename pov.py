from subprocess import call, DEVNULL

def pos_args(pos, suf=""):
    dims = ['x', 'y', 'z']
    kargs = {"{0}{1}".format(dims[i], suf): pos[i] for i in range(3)}
    return kargs


class world:
    def __init__(self, filename):
        self.filename = filename
        open(filename, 'w').close()
        self.includes = []
    
    def writeToFile(self, block):
        """write string block to file"""
        with open(self.filename, 'a') as f:
            f.write("\n" + block + "\n")

    def generate(self, outName = None, num=0, N=3):
        call(["povray", self.filename])
        if not outName:
            outName = self.filename[:-4]

        oldfilename = self.filename[:-4] + ".png"
        if num == 0:
            newfilename = outName + ".png"
        else:
            newfilename = outName + "_" + format(num, "0{}".format(N)) + ".png"

        call(["mv", oldfilename, newfilename], stderr=DEVNULL)


    def include(self,name):
        """add #include at beginning if it doesn't exist already"""
        if name in self.includes:
            return

        with open(self.filename, 'r+') as f:
            contents = f.read()
            f.seek(0,0)
            f.write("#include \"{0}.inc\"\n".format(name) + contents)
        self.includes.append(name)


    def sphere(self, pos, r, color = "Blue"):
        kargs = pos_args(pos)
        kargs["r"] = r
        kargs["color"] = color

        block = "sphere {{ \n\
            <{x},{y},{z}>, {r} \n\
            texture {{ \n\
                pigment {{color {color}}} \n\
            }} \n\
        }}".format(**kargs)

        self.writeToFile(block)

    def plane(self, pos, height, color = "Blue"):
        kargs = pos_args(pos)
        kargs["h"] = height
        kargs["color"] = color

        block = "plane {{ \n\
            <{x},{y},{z}>, {h} \n\
            texture {{ \n\
                pigment {{color {color}}} \n\
            }} \n\
        }}".format(**kargs)

        self.writeToFile(block)

    def camera(self, pos, to):
        kargs_pos = pos_args(pos, 1)
        kargs_to = pos_args(to, 2)

        block = "camera {{ \n\
            location <{x1},{y1},{z1}> \n\
            look_at <{x2},{y2},{z2}> \n\
        }}".format(**kargs_pos, **kargs_to)

        self.writeToFile(block)

    def basic_light(self, pos, color="White"):
        kargs = pos_args(pos)
        kargs["color"] = color

        block = "light_source {{ \n\
            <{x},{y},{z}> \n\
            color {color} \n\
        }}".format(**kargs)

        self.writeToFile(block)



if __name__ == "__main__":
    w = world("test.pov")

    w.include("colors")
    
    w.camera((10,10,-15),(10,0,0))
    w.basic_light((0,50,0))

    for i in range(10):
        w.sphere((3*i,0,0),1)
    w.plane((0,1,0), -1, color="Red")

    w.generate()


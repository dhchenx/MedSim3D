import open3d as o3d

class PLYParser:
    def __init__(self,model_file):
        self.model_file=model_file
        self.vertices = []
        self.vertices_colors = []
        self.faces = []
        self.edges = []
        self.edges_colors = []

    def to_ascii(self,target_file):
        mesh = o3d.io.read_triangle_mesh(self.model_file)
        print(mesh)
        o3d.io.write_triangle_mesh(target_file, mesh, write_ascii=True)

    def parse(self):
        line_num=0
        num_vertex=0
        num_face=0
        num_edge=0
        with open(self.model_file,'r') as fobj:
            for line in fobj:
                line=line.strip()
                if line_num==0 and (not line=="ply"):
                    print("Not a valid file!")
                if line.startswith("comment "):
                    print(line)
                if line.startswith("element"):
                    ls=line.split(" ")
                    if ls[1]=="vertex":
                        num_vertex=int(ls[2])
                    if ls[1]=="face":
                        num_face=int(ls[2])
                    if ls[1]=="edge":
                        num_edge=int(ls[2])
                if line=="end_header":
                    break
                line_num+=1
            print(f"vertices: {num_vertex}\tfaces: {num_face}\tnum_edge:{num_edge}")
            self.vertices=[]
            self.vertices_colors=[]
            self.faces=[]
            self.edges=[]
            self.edges_colors=[]
            for idx in range(num_vertex):
                ls=fobj.readline().strip().split(" ")
                if len(ls)==3:
                    values=[float(v) for v in ls]
                    color_values=[]
                if len(ls)==6:
                    values = [float(v) for v in ls[:3]]
                    color_values=[int(v) for v in ls[3:]]
                self.vertices.append(values)
                self.vertices_colors.append(color_values)
                line_num+=1
            for idx in range(num_face):
                ls=fobj.readline().strip().split(" ")
                # num=len(ls[0])
                list_triangles=[]
                values=ls[1:]
                for i in range(len(values)-2):
                    triangle=[values[0],values[i+1],values[i+2]]
                    list_triangles.append([int(v) for v in triangle])
                line_num+=1
                self.faces+=list_triangles
            for idx in range(num_edge):
                ls=fobj.readline().strip().split(" ")
                if len(ls)==2:
                    values=[float(v) for v in ls]
                    color_values=[]
                if len(ls)==5:
                    values = [float(v) for v in ls[:3]]
                    color_values=[int(v) for v in ls[3:]]
                self.edges.append(values)
                self.edges_colors.append(color_values)
                line_num+=1

        return self.vertices,self.faces

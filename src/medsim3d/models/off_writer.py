

class OFFWriter:
    def __init__(self,model_file,vertices,faces):
        self.model_file=model_file
        self.vertices=vertices
        self.faces=faces

    def write(self):
        file=open(self.model_file,'w',encoding='utf-8')
        num_faces=len(self.faces)
        num_vertices=len(self.vertices)
        num_edges=0
        file.write("OFF\n")
        file.write(f"{num_vertices} {num_faces} {num_edges}\n")
        for idx in range(num_vertices):
            vertice=[str(s) for s in self.vertices[idx]]
            file.write(" ".join(vertice)+"\n")
        for idx in range(num_faces):
            face=[str(s) for s in self.faces[idx]]
            file.write(str(len(face))+" "+ " ".join(face)+"\n")
        file.close()

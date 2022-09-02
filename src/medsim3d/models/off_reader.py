
class OFFReader:
    def __init__(self,model_file):
        self.model_file=model_file

    def read(self):
        file=open(self.model_file,"r",encoding='utf-8')
        line=file.readline().strip()

        if line!="OFF":
            print("Error: Not an OFF file!")
            return
        line=file.readline().strip()
        nums=line.split(" ")
        num_vertices=int(nums[0])
        num_faces=int(nums[1])
        num_edges=int(nums[2])

        list_vertices = []
        for idx in range(num_vertices):
            line = file.readline().strip()
            xyz = line.strip().split(" ")
            list_vertices.append([float(xyz[0]), float(xyz[1]), float(xyz[2])])
            # print(xyz)
        list_faces = []
        for idx in range(num_faces):
            line = file.readline().strip()
            face = line.strip().split(" ")
            faces=[int(s) for s in face]
            faces=faces[1:]
            list_faces.append(faces)
            # print(face)
        file.close()
        print(f"Vertices: {num_vertices}, Faces: {num_faces}")
        return list_vertices,list_faces

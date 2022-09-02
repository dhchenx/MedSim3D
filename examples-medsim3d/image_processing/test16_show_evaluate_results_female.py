import pickle
import numpy as np

def show_results():
    gender = "Female"

    body_parts = ["abdomen", "head", "legs", "pelvis", "thighs", "thorax"]

    for i,body_part in enumerate(body_parts):
        list_stat=pickle.load(open(f"datasets/evaluate_results/{gender}_{body_part}.pickle","rb"))
        list_canny=[]
        list_canny2=[]
        list_isolate1=[]
        list_isolate2=[]
        # canny	canny_polygon	isolate1	isolate2
        for idx,stat in enumerate(list_stat):
            if i==0 and idx==0:
                print("Gender\tBody part\t"+"\t".join(list(stat.keys())))
            list_canny.append(stat["canny"])
            list_canny2.append(stat["canny_polygon"])
            list_isolate1.append(stat["isolate1"])
            list_isolate2.append(stat["isolate2"])
        print( gender+"\t"+ body_part+"\t"+ f"{round(np.mean(list_canny),4)}\t{round(np.mean(list_canny2),4)}\t{round(np.mean(list_isolate1),4)}\t{round(np.mean(list_isolate2),4)}")


if __name__=="__main__":
    show_results()
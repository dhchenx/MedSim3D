import os

gender="Male"

root_path="../datasets"

body_parts = [
    "abdomen",
    "head", "legs", "pelvis", "thighs", "thorax","normalCT", "frozenCT"]

dict_num={}

for body_part in body_parts:
    body_part_folder=root_path+"/"+gender+"/"+body_part
    if not os.path.exists(body_part_folder):
        dict_num[body_part]=0
        continue
    n_files=len(os.listdir(body_part_folder))
    if gender=="Female" and body_part in ['abdomen','legs','thighs','thorax','pelvis']:
        n_files=int(n_files/3)

    dict_num[body_part]=n_files
print()
print("Sex\tBody part\tNumber of images")
for k in dict_num:
    print(f"{gender}\t{k}\t{dict_num[k]}")


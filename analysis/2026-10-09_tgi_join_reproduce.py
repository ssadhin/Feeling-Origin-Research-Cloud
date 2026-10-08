import pandas as pd
sha="3f4b08e0fa26e10b220e6a51da50c3c8405f4467"
base=f"https://raw.githubusercontent.com/CMSPR/TGI_SensitizationPainDissociation/{sha}/"
a=pd.read_csv(base+"Classification_data/final_data.csv")
b=pd.concat([pd.read_csv(base+"DFBA_data/TGI_NR_stats.csv"),pd.read_csv(base+"DFBA_data/TGI_R_stats.csv")])
d=a.merge(b,left_on="Record ID",right_on="Subject ID",validate="one_to_one")
assert len(d)==160 and d["Subject ID"].is_unique
print(d.groupby("Responder")["Sec_Hyp"].agg(["size","mean","std"]))

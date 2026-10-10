from scipy.io import whosmat
for path in ("data/behavioral_baseline.mat", "data/neural_baseline.mat"):
    print(path, whosmat(path))

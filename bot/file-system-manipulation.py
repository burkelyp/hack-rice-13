from pathlib import Path

datapath = Path(".").resolve().absolute()

# class Image:

#     def __init__(self, )

with (datapath / "storage.txt").open("w") as f:
    f.write("",',')



print(datapath)

if __name__ == "__main__":
    print()
    print(datapath)
def new_pdb_line(aID, aname, resname, resnumb, x, y, z, chain=" "):
    pdb_format = "ATOM  {:5d} {:4s} {:4s}{:1s}{:4d}    {:8.3f}{:8.3f}{:8.3f}\n"
    return pdb_format.format(aID, aname, resname, chain, resnumb, x, y, z)


def new_pqr_line(aID, aname, resname, resnumb, x, y, z, charge, radius, chain=" "):
    pdb_format = (
        "ATOM  {:5d} {:4s} {:4s}{:1s}{:4d}    {:8.3f}{:8.3f}{:8.3f}{:8.3f}{:8.3f}\n"
    )
    return pdb_format.format(
        aID, aname, resname, chain, resnumb, x, y, z, charge, radius
    )


def new_gro_line(aID, aname, resname, resnumb, x, y, z):
    gro_format = "{:5}{:5}{:>5}{:5}{:8.3f}{:8.3f}{:8.3f}\n"
    return gro_format.format(resnumb, resname, aname, aID, x, y, z)


def correct_longHs(aname):
    if aname[1] == "H" and aname[0] in "12" and aname[3] in "12":
        return aname[1:3] + aname[3] + aname[0]
    return aname


def read_pqr_line(line):
    (aname, anumb, resname, chain, resnumb, x, y, z) = read_pdb_line(line)
    charge = float(line[54:62])
    radius = float(line[62:70])
    return (aname, anumb, resname, chain, resnumb, x, y, z, charge, radius)


def read_pdb_line(line):
    aname = line[12:16].strip()
    anumb = int(line[5:11].strip())
    resname = line[17:21].strip()
    chain = line[21]
    resnumb = int(line[22:26])
    x = float(line[30:38])
    y = float(line[38:46])
    z = float(line[46:54])
    if len(aname) == 4:
        aname = correct_longHs(aname)
    return (aname, anumb, resname, chain, resnumb, x, y, z)


def read_gro_line(line):
    resnumb = int(line[:5].strip())
    resname = line[5:10].strip()
    aname = line[10:15].strip()
    anumb = int(line[15:20].strip())
    x = float(line[20:28].strip())
    y = float(line[28:36].strip())
    z = float(line[36:44].strip())
    return (aname, anumb, resname, resnumb, x, y, z)


def gro2pdb(f_in, f_out):
    new_pdb_content = "REMARK    CONVERTED from {} by PypKa\n".format(f_in)
    with open(f_in) as f:
        line_counter = 0
        natoms_left = 0
        natoms = 0
        lines = f.read().splitlines()
        last_line = lines[-1]
        box = [float(i) * 10 for i in last_line.split()[:3]]
        new_pdb_content += (
            "CRYST1  {0:3.3f}  {1:3.3f}  {2:3.3f}  "
            "60.00  60.00  90.00 P 1           1\n".format(box[0], box[1], box[2])
        )
        for line in lines:
            line_counter += 1
            if natoms_left > 0:
                natoms_left -= 1
                natoms += 1
                (aname, anumb, resname, resnumb, x, y, z) = read_gro_line(line)

                x, y, z = x * 10, y * 10, z * 10

                new_pdb_content += new_pdb_line(
                    anumb, aname, resname, resnumb, x, y, z, chain="A"
                )
            elif line_counter == 2:
                natoms_left = int(line.strip())
    new_pdb_content += "TER\nENDMDL\n"
    with open(f_out, "w") as f_new:
        f_new.write(new_pdb_content)


def get_grobox_size(f_in):
    with open(f_in) as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
        box = [float(i) * 10 for i in last_line.split()[:3]]
    return box


def get_chains_from_file(f_in):
    chain_list = []
    with open(f_in) as f:
        for line in f:
            if "ATOM " == line[0:5]:
                pdb_cols = read_pdb_line(line)
                chain = pdb_cols[3]
                if chain not in chain_list:
                    chain_list.append(chain)
    return chain_list
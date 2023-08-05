import os
import subprocess
from pdbmender.formats import read_pdb_line, new_pdb_line
from pdbmender.constants import (
    PROTEIN_RESIDUES,
    TITRATABLE_RESIDUES,
    RESIDUE_REFSTATE,
    RENAME_ATOMS,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def correct_insertion_codes(pdb_in, pdb_out, insertion_offset=3000):
    with open(pdb_in) as f:
        lines = f.readlines()

    ninsertions = -1
    inserted_block = None
    renumbered_res = {}
    new_lines = ""
    for line in lines:
        if line.startswith("ATOM "):
            aname, anumb, resname, chain, resnumb, x, y, z = read_pdb_line(line)

            if chain == " ":
                chain = "_"

            insertion_code = line[26]
            if insertion_code.strip():
                new_res_trigger = False
                if inserted_block != insertion_code:
                    ninsertions += 1
                    new_res_trigger = True

                inserted_block = insertion_code
                resnumb_offset = insertion_offset + ninsertions
                resnumb += resnumb_offset

                if new_res_trigger:
                    while (
                        chain in renumbered_res.keys()
                        and resnumb in renumbered_res[chain].keys()
                    ):
                        resnumb += 1
                        ninsertions += 1
                    if resnumb not in renumbered_res.keys():
                        if chain not in renumbered_res:
                            renumbered_res[chain] = {}
                        renumbered_res[chain][resnumb] = (
                            resnumb - resnumb_offset,
                            insertion_code,
                        )
            else:
                ninsertions = -1

            new_line = new_pdb_line(
                anumb,
                aname,
                resname,
                resnumb,
                x,
                y,
                z,
                chain=chain,
            )
            new_lines += new_line

    with open(pdb_out, "w") as f:
        f.write(new_lines)

    return renumbered_res


def mend_pdb(
    pdb_to_clean, pdb_cleaned, ff, ffout, logfile="LOG_pdb2pqr", hopt=True, debug=False
):
    pdb_fixed = pdb_to_clean.replace(".pdb", "_fixed.pdb")
    renumbered_res = correct_insertion_codes(pdb_to_clean, pdb_fixed)
    try:
        # TODO: Port pdb2pqr to py3 and import it as a module
        cmd = (
            "python2 {0}/pdb2pqr/pdb2pqr.py {1} {2} "
            "--ff {3} --ffout {4} --drop-water -v --chain {6} > {5} 2>&1 ".format(
                SCRIPT_DIR,
                pdb_fixed,
                pdb_cleaned,
                ff,
                ffout,
                logfile,
                "" if hopt else "--noopt",
            )
        )
        subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        raise Exception(
            "pdb2pqr did not run successfully\nMessage: {}".format(
                e.stderr.decode("ascii")
            )
        )
    if not debug:
        os.system("rm -f {}".format(pdb_fixed))
    return renumbered_res


def add_tautomers(
    pdb_in,
    chains_res,
    ff_family,
    outputpqr,
    logfile="LOG_addHtaut",
    pdb_prep="addhtaut_cleaned.pdb",
    to_exclude=[],
    terminal_offset=5000,
):
    removed_pdb = prepare_for_addHtaut(
        pdb_in, pdb_prep, chains_res, to_exclude, terminal_offset=terminal_offset
    )
    sites_addHtaut = select_tautomer_sites(chains_res)
    if len(sites_addHtaut.strip()) == 0:
        os.system("cp {} {}".format(pdb_prep, outputpqr))
    else:
        try:
            # TODO rewrite addHtaut as python module
            cmd = "{}/addHtaut {} {} {} > {}".format(
                SCRIPT_DIR,
                pdb_prep,
                ff_family,
                sites_addHtaut,
                outputpqr,
                logfile,
            )
            subprocess.run(
                cmd,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            raise Exception(
                "addHtaut did not run successfully\nMessage: {}".format(
                    e.stderr.decode("ascii")
                )
            )
    return removed_pdb


def correct_names(resnumb, resname, aname, titrating_sites, termini):
    # TODO: some of these are no longer used as it is done by pdb2pqr
    def change_aname(aname, restype):
        not_correct_names = list(restype.keys())
        for not_corrected in not_correct_names:
            if aname == not_corrected:
                aname = restype[not_corrected]
        return aname

    NTR_numb, CTR_numb = termini
    restype = None
    if resnumb == CTR_numb:
        restype = "CTR"

    elif resnumb == NTR_numb:
        restype = "NTR"

    if restype and restype in list(RENAME_ATOMS.keys()):
        aname = change_aname(aname, RENAME_ATOMS[restype])

    if resnumb in titrating_sites:
        if resname not in PROTEIN_RESIDUES:
            for tit_res in TITRATABLE_RESIDUES:
                if tit_res[:2] == resname[:2]:
                    restype, resname = tit_res, tit_res

        if resname in list(RENAME_ATOMS.keys()):
            aname = change_aname(aname, RENAME_ATOMS[resname])

    if resname in list(RESIDUE_REFSTATE.keys()):
        resname = RESIDUE_REFSTATE[resname]

    return aname, resname


def prepare_for_addHtaut(pdb_in, pdb_out, chains_res, to_exclude, terminal_offset=5000):
    with open(pdb_in) as f:
        content = f.readlines()

    sites = {}
    termini = {}
    for chain, residues in chains_res.items():
        sites[chain] = []
        termini[chain] = [None, None]
        for resnumb, resname in residues.items():
            if resname in ("NTR", "CTR"):
                resnumb = int(resnumb)
                if resname == "NTR":
                    termini[chain][0] = resnumb
                elif resname == "CTR":
                    termini[chain][1] = resnumb
                resnumb += terminal_offset
            sites[chain].append(resnumb)

    new_pdb_text = ""
    removed_pdb_lines = []
    resnumb_max = 0
    chains = sites.keys()
    for line in content:
        if line.startswith("ATOM"):
            termini_trigger = False
            aname, anumb, resname, chain, resnumb, x, y, z = read_pdb_line(line)

            if chain in chains:
                resnumb_max = resnumb
                sites_numbs = sites[chain]
                aname, resname = correct_names(
                    resnumb, resname, aname, sites_numbs, termini[chain]
                )

                if resnumb in termini[chain]:
                    termini_trigger = True

            if resname == "CYS":
                change_atoms = {"1CB": "CB", "1SG": "SG"}
                if aname in change_atoms.keys():
                    aname = change_atoms[aname]
            if (
                aname in ("O1", "O2", "OT1", "OT2", "H1", "H2", "H3")
                and not termini_trigger
                and resname in PROTEIN_RESIDUES
            ):
                if aname == "O1":
                    aname = "O"
                elif aname == "H1":
                    aname = "H"
                else:
                    continue

            new_line = new_pdb_line(
                anumb,
                aname,
                resname,
                resnumb,
                x,
                y,
                z,
                chain=chain,
            )
            if chain in chains:
                new_pdb_text += new_line
            elif (
                aname not in ("O1", "O2", "OT1", "OT2", "H1", "H2", "H3")
                or resname in to_exclude
            ):
                removed_pdb_lines.append(new_line)

    with open(pdb_out, "w") as f_new:
        f_new.write(new_pdb_text)

    resnumb_old = resnumb_max + 1
    removed_pdb_text = ""
    for line in removed_pdb_lines:
        (aname, anumb_old, resname, chain, resnumb, x, y, z) = read_pdb_line(line)
        anumb += 1
        resnumb += resnumb_old
        while resnumb < resnumb_max:
            resnumb += resnumb_old
        removed_pdb_text += new_pdb_line(
            anumb, aname, resname, resnumb, x, y, z, chain=chain
        )
        resnumb_max = resnumb

    with open("removed.pqr", "w") as f_new:
        f_new.write(removed_pdb_text)
    return removed_pdb_text


def get_cys_bridges(f_pdb2pqr_log):
    CYS_bridges = {}
    with open(f_pdb2pqr_log) as f:
        trigger_error = ""
        for line in f:
            if "patched with CYX" in line:
                parts = line.split("patched")[0].replace("PATCH INFO: ", "").split()
                resname, chain, resnumb = parts

                if not chain in CYS_bridges:
                    CYS_bridges[chain] = []
                cys_res_numb = int(parts[-1])
                if cys_res_numb not in CYS_bridges[chain]:
                    CYS_bridges[chain].append(cys_res_numb)
            if (
                "error" in line.lower()
                and "Error parsing line: invalid literal for int() with base 10"
                not in line
            ):
                trigger_error += line
        if trigger_error:
            raise Exception(
                "Found errors while parsing the input structure to PDB2PQR:\n"
                + trigger_error
            )
    return CYS_bridges


def identify_cter(inputpqr, cur_ctrs):
    new_ctrs = {}
    with open(inputpqr) as f:
        for line in f:
            if line.startswith("ATOM "):
                (aname, _, resname, chain, resnumb, _, _, _) = read_pdb_line(line)
                if (
                    aname
                    in (
                        "CT",
                        "OT",
                        "OT1",
                        "OT2",
                        "O1",
                        "O2",
                        "OXT",
                    )
                    and chain in cur_ctrs
                    and resnumb != cur_ctrs[chain]
                    and resname in [*TITRATABLE_RESIDUES, *PROTEIN_RESIDUES, "CY0"]
                ):
                    new_ctrs[chain] = resnumb

    return new_ctrs


def identify_tit_sites(f_in, chains, nomenclature="PDB", add_ser_thr=False):
    def add_site(chain_res, chain, resnumb, resname):
        if resname in ("NTR", "CTR"):
            chain_res[chain][str(resnumb)] = resname
        else:
            chain_res[chain][resnumb] = resname
        return chain_res

    chain_res = {chain: {} for chain in chains}
    skip_NTR = {chain: False for chain in chains}
    last_res = None
    with open(f_in) as f:
        content = f.readlines()

    nline = 0
    resnumb = None
    resname = None
    for line in content:
        nline += 1
        if line.startswith("ATOM "):
            (aname, anumb, resname, chain, resnumb, x, y, z) = read_pdb_line(line)
            insertion_code = line[26].strip()
            if insertion_code:
                print("NOT CONSIDERING:", line)
                continue

            last_res = resnumb
            last_chain = chain
            chain_sites = []

            if chain in chains:
                chain_sites = chain_res[chain]

                if nomenclature == "CHARMM":
                    for can_res, charmm_res in CHARMM_protomers.items():
                        if resname in charmm_res:
                            resname = can_res

                if resname in PROTEIN_RESIDUES or resname in TITRATABLE_RESIDUES:
                    if resnumb not in chain_sites:
                        if not chain_res[chain] and not skip_NTR[chain]:
                            if resname == "PRO":
                                skip_NTR[chain] = True
                                continue
                            chain_res = add_site(chain_res, chain, resnumb, "NTR")

                        if (
                            resname in TITRATABLE_RESIDUES
                            and resname != "NTR"
                            and resname != "CTR"
                        ) and (resname not in ("SER", "THR") or add_ser_thr):
                            chain_res = add_site(chain_res, chain, resnumb, resname)

                    if "CTR" not in chain_sites and aname in (
                        "CT",
                        "OT",
                        "OT1",
                        "OT2",
                        "O1",
                        "O2",
                        "OXT",
                    ):
                        chain_res = add_site(chain_res, chain, resnumb, "CTR")

    if "CTR" not in chain_sites and aname in (
        "CT",
        "OT",
        "OT1",
        "OT2",
        "O1",
        "O2",
        "OXT",
    ):
        chain_res = add_site(chain_res, chain, last_res, "CTR")

    return chain_res


def select_tautomer_sites(chains_res):
    sites_addHtaut = ""
    for chain in chains_res.keys():
        for res in chains_res[chain]:
            if chains_res[chain][res] == "NTR":
                continue
            sites_addHtaut += "{0}--{1}--{2},".format(
                res, chains_res[chain][res], chain.replace(" ", "_")
            )

    if len(sites_addHtaut) > 0 and sites_addHtaut[-1] == ",":
        sites_addHtaut = sites_addHtaut[:-1]
    return sites_addHtaut


def rm_cys_bridges(chains_res, logfile_mend):
    cys_bridges = get_cys_bridges(logfile_mend)
    final_chains_res = {chain: {} for chain in chains_res}
    for chain in final_chains_res:
        for res in chains_res[chain]:
            if chain in cys_bridges and res in cys_bridges[chain]:
                continue
            final_chains_res[chain][res] = chains_res[chain][res]

    return final_chains_res, cys_bridges

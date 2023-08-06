f"""
 &CONTROL
    calculation = 'relax',
    prefix      = '{self.prefix}',
    outdir      = '{self.output_dir}',
    pseudo_dir  = '{self.pseudo_dir}',
    nstep = {self.nstep},
 /
 &SYSTEM
    ibrav     = 0,
    nat  = {self.num_atoms},
    ntyp = {self.num_elem},
    ecutwfc = {self.ecutwfc},
    ecutrho = {self.ecutrho},
    input_dft = '{self.functional}',

    occupations = 'smearing',
    smearing = 'mv',
    degauss = 0.01,
 /
 &ELECTRONS
    conv_thr = {self.conv_thr}
    mixing_beta = {self.mixing_beta}
    electron_maxstep = {self.electron_maxstep}
 /
 &IONS
 /
 &CELL
 /

ATOMIC_SPECIES
{self.atomic_species}

CELL_PARAMETERS angstrom
{self.cell_parameters}

ATOMIC_POSITIONS angstrom
{self.atomic_positions}

K_POINTS automatic
{self.k_points}

"""
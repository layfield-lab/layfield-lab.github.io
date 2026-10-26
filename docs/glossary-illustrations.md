# Glossary illustrations

Created 2026-10-25. Six educational figures; none represents measured data or a lab simulation result.

## Generated illustrations

Tool: built-in image_gen. Original PNGs copied without modification, 1536 × 1024.

### Molecular dynamics

Create a scientifically clear educational diagram for an undergraduate computational chemistry glossary, landscape 3:2. White background, crisp editorial vector-like illustration, restrained deep purple #510c76 and medium purple #8348ad with gray and small green accents, sans serif labels. Show three large panels horizontally: '1  Positions' with 5 nonbonded generic spherical particles in a square simulation box; '2  Forces' with the identical 5 particle positions in an identical box plus clear arrow vectors originating at particle centers pointing in differing directions; '3  Next step' with those same five particles moved slightly and faint ghost dots showing their earlier positions. These are abstract interacting particles, not molecules, no chemical bonds. Single straight arrow between panels. Beneath panels a curved return arrow from panel 3 toward panel 1 labeled 'Repeat'. Small subtitle near bottom 'Forces update velocities and positions'. Keep all text large and exact, no equations, no numerical scales, no decorative molecules, no glassware, no logos, no texture. Spacious clean composition. This is a conceptual schematic, not a quantitative simulation.

### Surface modeling

Create a restrained academic explanatory illustration for a computational chemistry glossary about surface modeling of biochar, 3:2 landscape white background. Main explanatory point: construct a FAMILY of simplified porous carbon models and change ONE surface property at a time. Three spacious side-by-side cutaway schematics, each showing two rough charcoal-gray carbonaceous slab walls separated by a white horizontal slit pore. Porous disordered carbon is depicted as continuous irregular textured gray solid, NOT a fake molecular bond network. Left header 'Reference'; middle header 'More oxygen sites'; right header 'Wider pore'. Left and middle panels have exactly the same wall outline, thickness and pore width. Right panel has the same wall shapes moved farther apart vertically, to create a distinctly wider white slit pore. On left show exactly four purple circular markers on inward-facing wall surfaces, two top two bottom. Middle has eight purple markers, four top four bottom. Right has four purple markers like left. Purple circles are symbolic oxygen-containing surface sites, NOT individual atoms or chemical structures. A shared small legend at bottom: purple dot followed by 'Oxygen-containing surface site (schematic)'. Mark pore width using vertical double-headed arrows in green within each pore. Very short label 'Pore width' only in first panel. No particles floating in pores, no molecules, no chemical formulas, no quantitative scale, no lab equipment, no people, no logo. Purple #510c76 headings, medium purple #8348ad dots, charcoal and light gray material, green #4c9c2e arrows. Large readable sans serif text. Make geometry differences unmistakable, quiet precise educational diagram. Large clean margins. These are illustrative material models, not a real computed structure.

## Calculated figures

Regenerate with `python3 docs/generate-glossary-plots.py` (NumPy, Matplotlib, SciPy). Four SVGs keep editable text; PNG previews accompany them.

- Free energy: illustrative quartic F/kBT; probability density normalized from exp(−F/kBT). State populations require integration over a basin, not just its minimum.
- Metadynamics: illustrative Gaussian deposition sequence at prescribed locations, not a dynamical trajectory. Shows original F and F+V. No claim of convergence or physical kinetics.
- Reaction path: asymmetric illustrative profile plotted along its path, with the product minimum one arbitrary energy unit below the reactant minimum. Green points and arrow paths lie directly on the energy profile, showing downhill progression in both directions from the transition state; not a calculated IRC.
- Calibration: fixed-seed synthetic data with ordinary least squares and Student-t 95% pointwise intervals. Independent, normal, constant-variance errors assumed. Prediction interval includes residual variation of a new measurement.

## Scientific references

- [PLUMED METAD](https://www.plumed.org/doc-v2.9/user-doc/html/_m_e_t_a_d.html)
- [PLUMED metadynamics tutorial](https://www.plumed.org/doc-v2.9/user-doc/html/lugano-3.html)
- [AMS IRC documentation](https://www.scm.com/doc/AMS/Tasks/IRC.html)
- [NIST prediction intervals](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd132.htm)

## Integration

Optional `figure` metadata in pages/glossary.json is rendered by build.py. Captions and descriptive alt text are in HTML. Each figure links directly to its full-size asset. Images are lazy-loaded with explicit dimensions. Existing glossary definitions are unchanged.



## Metadynamics trajectory update (2026-10-26)

Original F stays solid purple; F+V is dotted gray. Black dots mark sampled positions. The final SVG panel animates one prescribed crossing in 4.5 seconds, ending in the right well. This is a schematic CV path, not a simulated trajectory or physical clock. Reduced-motion preferences show the static right-well endpoint; the PNG provides the same endpoint. Animation uses the exact Matplotlib-exported path coordinates and is regenerated by the plotting script.

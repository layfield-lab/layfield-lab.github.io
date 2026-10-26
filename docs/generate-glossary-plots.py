"""Regenerate illustrative glossary SVGs; all inputs are synthetic, not lab data.
Requires numpy, matplotlib, scipy. Run from any directory.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation
from scipy.stats import t
OUT = Path(__file__).resolve().parents[1] / 'assets/images/glossary'
OUT.mkdir(parents=True, exist_ok=True)
P, M, G, INK = '#510c76', '#8348ad', '#4c9c2e', '#15181c'
plt.rcParams.update({'font.size': 13, 'axes.labelsize': 13, 'axes.titlesize': 16,
 'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': '#98999b',
 'text.color': INK, 'axes.labelcolor': INK, 'svg.fonttype': 'none', 'font.family': 'DejaVu Sans'})
def finish(fig, name):
    fig.savefig(OUT / (name+'.svg'), bbox_inches='tight', facecolor='white')
    fig.savefig(OUT / (name+'.png'), dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
x=np.linspace(-1.5,1.5,600)
f=4*(x*x-1)**2+.55*x
f-=f.min()
p=np.exp(-f); p/=np.trapezoid(p,x)
fig,ax=plt.subplots(2,1,figsize=(9,6),sharex=True,layout='constrained')
ax[0].plot(x,f,color=P,lw=3); ax[0].set(ylabel='Free energy / kBT',ylim=(-.3,7),title='Frequently visited values have lower free energy')
ax[0].annotate('Lower basin',(-1,0),(-1.35,3),arrowprops={'arrowstyle':'->','color':INK})
ax[0].annotate('Barrier',(0,4.55),(.35,5.9),arrowprops={'arrowstyle':'->','color':INK})
ax[1].plot(x,p,color=P,lw=3); ax[1].fill_between(x,p,color=M,alpha=.18)
ax[1].set(xlabel='Collective variable s (arbitrary units)',ylabel='Probability density',title='P(s) ∝ exp[−F(s) / kBT]')
finish(fig,'free-energy')
fig,axs=plt.subplots(1,3,figsize=(12,4.4),sharey=True,layout='constrained')
centers=[-1.03,-.85,-1.12,-.75,-1.20,-.95,-.60,-1.05]
for ax,n,title in zip(axs,[0,3,8],['Start: trapped in a basin','Add hills at visited values','Accumulated bias lifts the basin']):
    bias=sum((.55*np.exp(-.5*((x-c)/.25)**2) for c in centers[:n]),start=np.zeros_like(x))
    ax.plot(x,f,color=P,lw=3,label='Original F')
    ax.fill_between(x,f,f+bias,color=G,alpha=.23,label='Added bias V')
    ax.plot(x,f+bias,ls=':',color='#5a636e',lw=3,label='F + V')
    position = {0: -1.03, 3: -.85, 8: 1.0}[n]
    dot, = ax.plot(position, np.interp(position, x, f+bias), 'o',
                   color=INK, markersize=14, markeredgecolor='white',
                   markeredgewidth=2, zorder=6, label='Sampled position')
    # Lift the center by its radius plus outline: the dot sits on the curve.
    dot.set_transform(ax.transData + ScaledTranslation(0, 8/72, fig.dpi_scale_trans))
    if n == 8:
        dot.set_gid('trajectory-rest')
        # Prescribed CV path with small backtracking: an illustration, not MD data.
        waypoints = [-1.10, -.95, -1.12, -.85, -.96, -.62, -.35, 0, .3, .6, .85, 1]
        motion_x = np.concatenate([np.linspace(a, b, 20) for a, b in zip(waypoints, waypoints[1:])])
        guide, = ax.plot(motion_x, np.interp(motion_x, x, f+bias), alpha=0)
        guide.set_gid('trajectory-path')

    ax.set(title=title,xlabel='Collective variable s',ylim=(-.4,6.8),xticks=[-1,0,1]); ax.title.set_fontsize(12)
axs[0].set_ylabel('Energy / kBT'); axs[2].legend(loc='upper center',fontsize=10,frameon=False)
finish(fig,'metadynamics')
# Matplotlib supplies exact SVG coordinates, including its tight bounding-box transform.
# Animate only the final panel, once, then retain the endpoint. Reduced-motion users
# see the same static endpoint used in the PNG preview.
svg_path = OUT / 'metadynamics.svg'
svg = svg_path.read_text()
root = ET.fromstring(svg)
ns = {'s': 'http://www.w3.org/2000/svg'}
path = root.find(".//s:g[@id='trajectory-path']/s:path", ns).attrib['d']
animation = f'''<style>
#trajectory-rest {{ display: none; }}
@media (prefers-reduced-motion: reduce) {{
  #trajectory-moving {{ display: none; }}
  #trajectory-rest {{ display: inline; }}
}}
</style>
<g id="trajectory-moving" aria-hidden="true" transform="translate(0,-8)">
  <circle r="7" fill="{INK}" stroke="white" stroke-width="2">
    <animateMotion path="{path}" dur="4.5s" repeatCount="1" fill="freeze" calcMode="paced" />
  </circle>
</g>
'''
svg_path.write_text(svg.replace('</svg>', animation + '</svg>'))
# IRC is a path on the calculated PES; every plotted point lies on E(s).
from matplotlib.path import Path as PlotPath
from matplotlib.patches import FancyArrowPatch
fig,ax=plt.subplots(figsize=(9,5.4),layout='constrained')
def reaction_energy(s):
    s = np.asarray(s)
    # Smooth product-side stabilization preserves stationary points at -1, 0, 1.
    u = np.clip(s, 0, 1)
    return 4*(s*s-1)**2 - (3*u*u - 2*u*u*u)
xr=np.linspace(-1,1,600)
ax.plot(xr,reaction_energy(xr),color=P,lw=3,label='Energy along the path',zorder=2)
for sign in [-1,1]:
    samples=sign*np.array([.16,.34,.52,.70,.86,.97])
    ax.scatter(samples,reaction_energy(samples),s=44,color='#346c20',
               edgecolors='white',linewidths=1,zorder=5,
               label='Illustrative IRC points' if sign==1 else None)
    # Dense path vertices follow the same energy curve, not a shortcut chord.
    for start,stop in [(.19,.31),(.55,.67)]:
        segment=sign*np.linspace(start,stop,60)
        vertices=np.column_stack((segment,reaction_energy(segment)))
        arrow=FancyArrowPatch(path=PlotPath(vertices),arrowstyle='-|>',
                              mutation_scale=18,color='#346c20',lw=2.5,zorder=6)
        ax.add_patch(arrow)
ax.scatter([-1,0,1],[0,4,-1],color=[P,P,P],s=[55,80,55],zorder=7)
ax.text(0,4.28,'Transition state',ha='center',weight='bold')
ax.text(-1,-.25,'Reactant minimum',ha='center',fontsize=12)
ax.text(1,-1.25,'Product minimum',ha='center',fontsize=12)
ax.text(-.87,3.0,'Reverse IRC',ha='center',color='#346c20',fontsize=12)
ax.text(.87,3.0,'Forward IRC',ha='center',color='#346c20',fontsize=12)
ax.annotate('',xy=(-1.26,4),xytext=(-1.26,0),arrowprops={'arrowstyle':'<->','color':INK})
ax.text(-1.34,2,'Barrier',rotation=90,va='center',ha='center')
ax.hlines([0,4],[-1.26,-1.26],[-1,0],colors='#98999b',linestyles=':',linewidth=1)
ax.set(xlim=(-1.5,1.4),ylim=(-1.65,4.85),
       xlabel='IRC path coordinate s (mass-weighted; schematic)',
       ylabel='Potential energy E(s) (arbitrary units)',xticks=[],yticks=[])
ax.legend(loc='lower center',bbox_to_anchor=(.5,1.01),ncol=2,frameon=False,fontsize=11)
finish(fig,'reaction-path')
rng=np.random.default_rng(16); xd=np.linspace(1,9,22); yd=.72*xd+1+rng.normal(0,.58,len(xd))
coef=np.polyfit(xd,yd,1); line=np.poly1d(coef); sigma=np.sqrt(np.sum((yd-line(xd))**2)/(len(xd)-2)); xx=np.linspace(1,9,300)
leverage=1/len(xd)+(xx-xd.mean())**2/np.sum((xd-xd.mean())**2)
crit=t.ppf(.975,len(xd)-2); ci=crit*sigma*np.sqrt(leverage); pi=crit*sigma*np.sqrt(1+leverage)
fig,ax=plt.subplots(figsize=(9,5.5),layout='constrained')
ax.fill_between(xx,line(xx)-pi,line(xx)+pi,color=M,alpha=.18,label='95% prediction interval: new measurement')
ax.fill_between(xx,line(xx)-ci,line(xx)+ci,color=M,alpha=.4,label='95% confidence interval: mean response')
ax.plot(xx,line(xx),color=P,lw=2.5,label='Calibration fit'); ax.scatter(xd,yd,color=INK,s=30,label='Synthetic reference data',zorder=3)
xnew=6; lnew=1/len(xd)+(xnew-xd.mean())**2/np.sum((xd-xd.mean())**2); h=crit*sigma*np.sqrt(1+lnew)
ax.errorbar([xnew],[line(xnew)],yerr=[h],fmt='D',color='#346c20',capsize=7,lw=2,zorder=4,label='One new prediction')
ax.set(xlabel='Computed value (arbitrary units)',ylabel='Measured value (arbitrary units)',title='Predicting one measurement needs a wider interval')
ax.legend(fontsize=10,frameon=False,loc='upper left'); ax.set_ylim(-1,11)
finish(fig,'prediction-interval')
print('Generated four SVGs and four PNG previews')

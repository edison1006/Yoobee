import os, math
import matplotlib.pyplot as plt

def cartesian_to_polar(x, y):
    r = math.hypot(x, y)
    th = math.atan2(y, x)      
    return r, th, math.degrees(th)

def polar_to_cartesian(r, theta_deg=None, theta_rad=None):
    if theta_rad is None and theta_deg is None:
        raise ValueError("Provide theta_deg or theta_rad.")
    if theta_rad is None:
        theta_rad = math.radians(theta_deg)
    return r*math.cos(theta_rad), r*math.sin(theta_rad)

def to_complex_polar(r, theta_deg):
    x, y = polar_to_cartesian(r, theta_deg=theta_deg)
    return complex(x, y)

def _setup(title):
    fig = plt.figure(figsize=(5,5), dpi=150)
    ax = fig.add_subplot(111)
    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)
    ax.grid(True, linewidth=0.5, linestyle="--")
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(title)
    return fig, ax

def _arrow(ax, z, label):
    ax.quiver(0, 0, z.real, z.imag, angles='xy', scale_units='xy', scale=1, width=0.005)
    ax.annotate(label, (z.real, z.imag), xytext=(4,4), textcoords="offset points")

def _fit(ax, pts):
    xs = [p.real for p in pts] + [0]
    ys = [p.imag for p in pts] + [0]
    pad = 0.5
    ax.set_xlim(min(xs)-pad, max(xs)+pad)
    ax.set_ylim(min(ys)-pad, max(ys)+pad)

def plot_add(z1, z2, outpath=None):
    z = z1 + z2
    fig, ax = _setup("z1 + z2")
    for zz, lb in [(z1,"z1"), (z2,"z2"), (z,"z1+z2")]:
        _arrow(ax, zz, lb)
    _fit(ax, [z1, z2, z])
    if outpath: fig.tight_layout(); fig.savefig(outpath); plt.close(fig)
    else: plt.show()

def plot_sub(z1, z2, outpath=None):
    zn = -z2
    z = z1 - z2
    fig, ax = _setup("z1 - z2 (add -z2, 180°)")
    for zz, lb in [(z1,"z1"), (z2,"z2"), (zn,"-z2"), (z,"z1-z2")]:
        _arrow(ax, zz, lb)
    _fit(ax, [z1, z2, zn, z])
    if outpath: fig.tight_layout(); fig.savefig(outpath); plt.close(fig)
    else: plt.show()

def plot_mul(z1, z2, outpath=None):
    z = z1 * z2
    fig, ax = _setup("z1 * z2 (angles add, mags multiply)")
    for zz, lb in [(z1,"z1"), (z2,"z2"), (z,"z1*z2")]:
        _arrow(ax, zz, lb)
    _fit(ax, [z1, z2, z])
    if outpath: fig.tight_layout(); fig.savefig(outpath); plt.close(fig)
    else: plt.show()

def plot_div(z1, z2, outpath=None):
    if z2 == 0: raise ZeroDivisionError("Division by zero.")
    z = z1 / z2
    fig, ax = _setup("z1 / z2 (angles subtract, mags divide)")
    for zz, lb in [(z1,"z1"), (z2,"z2"), (z,"z1/z2")]:
        _arrow(ax, zz, lb)
    _fit(ax, [z1, z2, z])
    if outpath: fig.tight_layout(); fig.savefig(outpath); plt.close(fig)
    else: plt.show()

def _demo(outdir="."):
    z1, z2 = complex(2,1), complex(-1,1.5)
    r1, t1, d1 = cartesian_to_polar(z1.real, z1.imag)
    r2, t2, d2 = cartesian_to_polar(z2.real, z2.imag)
    x1, y1 = polar_to_cartesian(r1, theta_rad=t1)
    x2, y2 = polar_to_cartesian(r2, theta_rad=t2)
    print(f"z1={z1} -> r={r1:.3f}, θ={d1:.2f}°; back=({x1:.3f},{y1:.3f})")
    print(f"z2={z2} -> r={r2:.3f}, θ={d2:.2f}°; back=({x2:.3f},{y2:.3f})")
    plot_add(z1, z2, outpath=os.path.join(outdir, "addition.png"))
    plot_sub(z1, z2, outpath=os.path.join(outdir, "subtraction.png"))
    plot_mul(z1, z2, outpath=os.path.join(outdir, "multiplication.png"))
    plot_div(z1, z2, outpath=os.path.join(outdir, "division.png"))

if __name__ == "__main__":
    outdir = os.environ.get("COMPLEX_VEC_OUT", ".")
    os.makedirs(outdir, exist_ok=True)
    _demo(outdir)

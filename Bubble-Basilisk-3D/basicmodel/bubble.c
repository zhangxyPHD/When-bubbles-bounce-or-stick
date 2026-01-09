#include "grid/octree.h"
#include "navier-stokes/centered.h"
#include "two-phase.h"
#include "tension.h"
#include "reduced.h"
#include "adapt_wavelet_limited.h"

// gas properties!
#define RHO21 (1e-3)
#define MU21 (1e-3)
#define MINlevel 6

// Error tolerancs
#define fErr (1e-3)     // error tolerance in VOF
#define KErr (1e-2)     // error tolerance in KAPPA
#define VelErr (1e-2)   // error tolerances in velocity
#define DissErr (1e-2)  // error tolerances in dissipation
#define OmegaErr (1e-2) // error tolerances in vorticity

// Distance and radius of drop calculations
// #define Xdist (10)
double Xdist;
#define R2Drop(x, y, z) (sq(x - Xdist-1) + sq(y) + sq(z))

// boundary conditions
u.t[left] = dirichlet(0.0);
u.r[left] = dirichlet(0.0);
f[left] = dirichlet(1.0);

p[right] = dirichlet(0.);
u.n[right] = neumann(0.);

p[top] = dirichlet(0.);
u.n[top] = neumann(0.);

p[back] = dirichlet(0.);
u.n[back] = neumann(0.);

p[bottom] = dirichlet(0.);
u.n[bottom] = neumann(0.);

int MAXlevel;
double Ga, Bo;
double tmax, Ldomain;
double tsnap=0.01;
char nameOut[80], dumpFile[80];
int main(int argc, char const *argv[])
{
  MAXlevel = atoi(argv[1]);
  Ga = atof(argv[2]);
  Bo = atof(argv[3]);
  tmax = atof(argv[4]);
  Ldomain = atof(argv[5]);
  DT = atof(argv[6]);
  CFL = atof(argv[7]);
  Xdist = atof(argv[8]);

  origin(0, -Ldomain/2, -Ldomain/2);
  init_grid(1 << (MAXlevel-3));
  L0 = Ldomain;
  NITERMAX = 200;
  TOLERANCE = 1e-4;
  
  rho1 = 1., rho2 = RHO21;
  mu1 = 1/Ga, mu2 = 1/Ga*MU21;
  f.sigma = 1/Bo;
  G.x=1;
  char comm[80];
  sprintf(comm, "mkdir -p intermediate");
  system(comm);
  // log
  fprintf(ferr, "Ga,Bo,MAXlevel,mu2,DT,Ldomain,tmax,tsnap,Xdist\n");
  fprintf(ferr, "%g,%g,%d,%g,%g,%g,%g,%g,%g\n", Ga, Bo, MAXlevel, mu2, DT, Ldomain, tmax, tsnap, Xdist);
  run();
}

event init(t = 0)
{
  if (!restore(file = "dump", list = all))
  {
    refine(fabs(R2Drop(x, y, z)-1) < 0.1 && (level < MAXlevel-2));
    refine(fabs(R2Drop(x, y, z)-1) < 0.05 && (level < MAXlevel-1));
    refine(fabs(R2Drop(x, y, z)-1) < 0.01 && (level < MAXlevel));
    fraction(f, -1. + R2Drop(x, y, z));
    foreach ()
    {
      u.x[] = 0.0;
      u.y[] = 0.0;
      u.z[] = 0.0;
    }
    boundary((scalar *){f, u.x, u.y, u.z});
  }
}

int refRegion(double x, double y, double z)
{
  double r=sqrt(sq(y)+sq(z));
  return (((r < 3.0 && x < 0.02)) ? MAXlevel+2 : 
          ((r < 3.0 && x < 0.05)) ? MAXlevel+1 : 
          (r < 3.0) ? MAXlevel : 
          (r < 8.0) ? MAXlevel-1 :
          MAXlevel-2);
}

event adapt(i++)
{
  adapt_wavelet_limited((scalar *){f, u.x, u.y, u.z},
              (double[]){fErr, VelErr, VelErr, VelErr},
              refRegion, MINlevel);
  double time_now = perf.t / 60.0;
  fprintf(ferr, "%g,%d,%ld,%g\n", t, i, grid->tn, time_now);
}

double t_last = 0.0;
double DeltaT = 0.0;
double xv_last=0.0;
event postProcess(t += 0.05)
{
  double sb = 0., xv = 0.;
  foreach (reduction(+:sb) reduction(+:xv))
  {
    double dv = (1. - f[])*cube(Delta);
    xv += u.x[]*dv;
    sb += dv;    
  }

  // int n =tag(bubble);
  if (isnan(sb)) {
    fprintf(ferr, "sb is NaN\n");
    return 1;
  }
  else{
    p.nodump = true;
    dump(file = "dump");
    // log
    DeltaT = perf.t / 60.0 - t_last;
    t_last = perf.t / 60.0;
    static FILE *fp1;
    if (pid() == 0)
    {
      if (i == 0)
      {
        fp1 = fopen("log_run", "w");
        fprintf(fp1, "t,i,Cell,Wallclocktime(min),CPUtime(min),xv\n");
        fflush(fp1);
      }
      fp1 = fopen("log_run", "a");
      fprintf(fp1, "%g,%d,%ld,%g,%g,%g\n", t, i, grid->tn, perf.t / 60.0, DeltaT, xv/sb);
      fflush(fp1);
    }
    // stop condition
    if (xv/sb>-0.001 && t>5)
    {
      fprintf(ferr, "Success, Bubble bounce. Exiting...\n");
      sprintf(nameOut, "intermediate/snapshot-%5.4f", t);
      dump(file = nameOut);
      return 1;
    }
    xv_last=xv/sb;
  }
}

event snapshot(t += 1)
{
  p.nodump = true;
  sprintf(nameOut, "intermediate/snapshot-%5.4f", t);
  dump(file = nameOut);
}

event end(t = tmax)
{
  return 1;
}
#include "grid/octree.h"
#include "navier-stokes/centered.h"
#include "two-phase.h"
#include "tension.h"
#include "tag.h"

char filename[80];

int main(int a, char const *arguments[])
{
  sprintf(filename, "%s", arguments[1]);
  restore(file = filename);
  double xb = 0., yb = 0., zb = 0., xv = 0., sb = 0.;
  double ke = 0., sw=0 ;
  double minX = 10.;
  scalar bubble[];
  face vector s[];
  s.x.i = -1;
  foreach ()
  {
    double dv = (1. - f[])*cube(Delta);
    double dv1 = (f[])*cube(Delta);
    xv += u.x[]*dv;
    ke += (sq(u.x[]) + sq(u.y[]) + sq(u.z[]))  / 2. *cube(Delta)*f[];
    xb += x*dv;
    yb += y*dv;
    zb += z*dv;
    sb += dv;
    sw += dv1;
    bubble[]=1. - f[];    
  }
  scalar d[];
  double threshold = 1e-4;
  foreach ()
  {
    d[] = (bubble[] > threshold);
  }
  int n = tag(d), size[n];
  for (int i = 0; i < n; i++)
  {
    size[i] = 0;
  }
  foreach_leaf()
  {
    if (d[] > 0)
    {
      size[((int)d[]) - 1]++;
    }
  }
  int MaxSize = 0;
  int MainPhase = 0;
  for (int i = 0; i < n; i++)
  {
    // fprintf(ferr, "%d %d\n",i, size[i]);
    if (size[i] > MaxSize)
    {
      MaxSize = size[i];
      MainPhase = i + 1;
    }
  }
  foreach ()
  {
    double dv = (1. - f[])*cube(Delta);
    double dv1 = (f[])*cube(Delta);
    xv += u.x[]*dv;
    ke += (sq(u.x[]) + sq(u.y[]) + sq(u.z[]))  / 2. *cube(Delta)*f[];
    xb += x*dv;
    yb += y*dv;
    zb += z*dv;
    sb += dv;
    sw += dv1;
    bubble[]=1. - f[];

    if (f[] > 1e-6 && f[] < 1. - 1e-6 && d[] == MainPhase)
    {
      coord n1 = facet_normal(point, f, s);
      double alpha1 = plane_alpha(f[], n1);
      coord segment1[12];
      int nv = facets (n1, alpha1, segment1, 1.1);
      if (nv > 1)
      {
        for (int k = 0; k < nv; k++) {
          double X1 = x + segment1[k].x*Delta;
          if (X1 < minX) minX = X1;
        }          
      }
    }
  }

  fprintf (ferr, "%g %g %g %g %g %g\n", t,xb/sb,yb/sb,zb/sb,xv/sb,minX);
}
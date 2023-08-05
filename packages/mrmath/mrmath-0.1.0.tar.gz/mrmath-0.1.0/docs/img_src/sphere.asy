import graph3;
import solids;

/////////////////////////////////////////
void angledroit(picture pic=currentpicture,
                triple pO, triple pI, triple pJ, real size=.1, pen p=black,
                projection P=currentprojection){
     triple imI=pO+size*unit(pI-pO),
            imJ=pO+size*unit(pJ-pO),
            imK=imI+imJ-pO;
            draw(imI--imK--imJ,p);
}
/////////////////////////////////////////

settings.outformat="png";
settings.prc=false;
settings.render=2;

size(8cm);

currentprojection=orthographic(10,2,5);
dotfactor=3.5;

real a=2;
triple pO=(0,0,0);

path3 planXY = plane((10,0,0),(0,10,0),(-5,-5,0));
path3 planXZ = plane((10,0,0),(0,0,10),(-5,0,-5));
path3 planYZ = plane((0,10,0),(0,0,10),(0,-5,-5));
path3 planZ = rotate(60, Z)*planYZ;
transform3 projxy=planeproject(planXY);
transform3 projxz=planeproject(planXZ);
transform3 projyz=planeproject(planYZ);
transform3 projz=planeproject(planZ);

revolution b=sphere(pO,a);
draw(b,1,longitudinalpen=nullpen);

for(int k=0; k<2; ++k)
draw(rotate(k*90, (0,0,1))*rotate(-90,(1,0,0))*b, 1,
     longitudinalpen=nullpen);

draw(b.silhouette(),black);

draw(-2.25X--3.00X, arrow=Arrow3(emissive(blue)),  p=blue,  L=Label("$x$", position=EndPoint));
draw(-2.25Y--2.75Y, arrow=Arrow3(emissive(green)), p=green, L=Label("$y$", position=EndPoint));
draw(-2.25Z--2.75Z, arrow=Arrow3(emissive(red)),   p=red,   L=Label("$z$", position=EndPoint));

triple pP = rotate(60,Z)*rotate(-50,Y)*(2,0,0);
dot("$P$", pP);
dot("$O$", pO);

triple pP1 = rotate(60,Z)*rotate(-50,Y)*(1.95,0,0);
draw("$r$",(0,0,0)--pP1, purple+0.5bp, arrow=Arrow3(TeXHead2, emissive(purple)));

triple pC = projxy*pP;
draw(pP--pC,orange+dotted+0.5bp);
draw(pO--pC,orange+dotted+0.5bp);
//dot("$C$",pC);

angledroit(pC, pO, pP, orange+0.5bp);

triple pA = rotate(60,Z)*(2,0,0);
//draw(pO--pA,orange+dotted+0.5bp);
//dot("$A$",pA);
draw("$\phi$", arc(pO,0.3*pA,0.3*pP), arrow=Arrow3(TeXHead2, emissive(gray)));
draw("$\lambda$",  arc(pO,X,0.5*pA), arrow=Arrow3(TeXHead2, emissive(gray)));

triple pB = projyz*pC;
//draw(pB--pC,orange+dotted+0.5bp);
//dot("$B$",pB);

triple pD = projxz*pC;
//draw(pD--pC,orange+dotted+0.5bp);
//dot("$D$",pD);

triple pE = projz*pP;
//draw(pP--pE,orange+dotted+0.5bp);
//dot("$E$",pE);

revolution br = rotate(60, (0,0,1))*rotate(-90,(1,0,0))*b;
skeleton s;
br.transverse(s,reltime(b.g,0.5),P=currentprojection);
draw(s.transverse.back, orange+dashed+0.25bp);
draw(s.transverse.front, orange+0.25bp);

skeleton s;
b.transverse(s,reltime(b.g, 0.777),P=currentprojection);
draw(s.transverse.back, orange+dashed+0.25bp);
draw(s.transverse.front,orange+0.25bp);

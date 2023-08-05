import three;
settings.outformat="png";
settings.prc=false;
settings.render=1;

currentprojection=perspective(4,1,2);

size(8cm,0);

draw(-1.25X--1.25X, arrow=Arrow3(emissive(blue)),  p=blue,  L=Label("$x$", position=EndPoint));
draw(-1.25Y--1.25Y, arrow=Arrow3(emissive(green)), p=green, L=Label("$y$", position=EndPoint));
draw(-1.25Z--1.25Z, arrow=Arrow3(emissive(red)),   p=red,   L=Label("$z$", position=EndPoint));

pen orig=gray(0.9)+opacity(0.2);
pen tran=blue+opacity(0.2);

draw(surface((1,1,0)--(1,-1,0)--(-1,-1,0)--(-1,1,0)--cycle), orig);

surface rotplane = rotate(35, X)*surface((1,1,0)--(1,-1,0)--(-1,-1,0)--(-1,1,0)--cycle);
draw(rotplane, tran);

draw("$\alpha$", arc((.9, 0, 0), (.9, .75, 0), rotate(35, X)*(.9, .75, 0)), black, arrow = Arrow3(TeXHead2, emissive(black)));

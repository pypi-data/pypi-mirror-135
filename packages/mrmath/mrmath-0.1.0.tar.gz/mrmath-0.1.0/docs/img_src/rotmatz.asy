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

draw(surface((1,0,1)--(1,0,-1)--(-1,0,-1)--(-1,0,1)--cycle), orig);

surface rotplane = rotate(35, Z)*surface((1,0,1)--(1,0,-1)--(-1,0,-1)--(-1,0,1)--cycle);
draw(rotplane, tran);

draw("$\alpha$", arc((0, 0, .9), (.75,0,.9), rotate(35, Z)*(.75,0,.9)), black, arrow = Arrow3(TeXHead2, emissive(black)));

// R50cm geodesic dome 
// 04/19/2016
// 04/21/2016

default_radius = 0.5;

// vertex(default_radius, 0, 0, 19.69); 

V = 
[
    // 1st row  
    [0, 0, 19.69],                  // 0
    
    // 2nd row
    // [10.3516, 0, -10.3517],      // 2 bug 
    [10.3516, 0, 16.7493],          // 2 correct     
    [3.19883,9.845,16.7493],        // 12 
    [-8.37466,6.08454,16.7493],     // 9        
    [-8.37466,-6.08454,16.7493],    // 6
    [3.19883,-9.845,16.7493],       // 1
 
        
    // 3rd row        
    [ 13.5505,9.845,10.3517 ],      // 15
    [ -5.17583,15.9295,10.3517 ],   // 14
    [-16.7493,0,10.3517],           // 11
    [-5.17583,-15.9295,10.3517],    // 8
    [13.5505,-9.845,10.3517],       // 4

    
    // 4th row    
    [17.6113, 0, 8.80564],          // 5
    [ 5.44218,16.7493,8.80564 ],    // 13
    [-14.2478,10.3516,8.80564],     // 10
    [-14.2478,-10.3516,8.80564],    // 7   
    [5.44218,-16.7493,8.80564],     // 3

    
    // 5th row
    [ 18.7263,6.08454,0],           // 34
    [ 11.5735,15.9295,0],           // 31
    [  0,19.69,0 ],                 // 30
    [ -11.5735,15.9295,0 ],         // 27
    [ -18.7263,6.08454,0 ],         // 26
    [ -18.7263,-6.08454,0 ],        // 23    
    [ -11.5735,-15.9295,0 ],        // 22
    [ 0,-19.69,0 ],                 // 19
    [ 11.5735,-15.9295,0 ],         // 17    
    [ 18.7263,-6.08454,0 ],         // 16   
    
    
    // 6th row      
    [ 16.7493, 0, -10.3517],          // 35
    [ 14.2478, 10.3516, -10.3517],    // 32
    [ 5.17583, 15.9295, -10.3517 ],   // 33
    [ -5.44218, 16.7493, -10.3517],   // 28
    [ -13.5505, 9.845, -10.3517 ],    // 29   
    [ -17.6113, 0, -10.3517 ],        // 24  
    [ -13.5505,- 9.845, -10.3517],    // 25
    [ -5.44218, -16.7493, -10.3517 ], // 20
    [ 5.17583, -15.9295, -10.3517 ],  // 21    
    [ 14.2478, -10.3516, -10.3517 ],  // 18 
];

// p = [x, y, z] 
module vertex(radius, p, c1="red")
{
    translate(p) color(c1) sphere(radius, center=true);    
}

module triangle(p1, f1=[[0,1,2]])
{
    polyhedron(points=p1, faces=f1);
}

module draw_vertex(fromto, c1="gray")
{
    echo("=====================");
    for (i = fromto)
    {
        vertex(default_radius, V[i], c1);
        echo(V[i]);
    } 
}

/*
for (t_v = V)
{
    vertex(default_radius, t_v, "Gray"); 
    index = search(t_v, V);
    echo(index[0], t_v);
}*/

draw_vertex([0:5], "red");
p0 = V[0];
p1 = V[1];
p2 = V[2];
p3 = V[3];
p4 = V[4];
p5 = V[5];
polyhedron(
    points=[ p1, p2, p3, p4, p5, // 5 points at base
             p0],
    faces=[ [0, 1, 5], [1, 2, 5], [2, 3, 5], [3, 4, 5],
            [4, 0, 5] ]
);

draw_vertex([6:10], "maroon");
p6 = V[6];
p7 = V[7];
p8 = V[8];
p9 = V[9];
p10 = V[10];
triangle([p1, p2, p6]);
triangle([p2, p3, p7]);
triangle([p3, p4, p8]);
triangle([p4, p5, p9]);
triangle([p5, p1, p10]);

draw_vertex([11:15], "purple");
p11 = V[11];
p12 = V[12];
p13 = V[13];
p14 = V[14];
p15 = V[15];
triangle([p1, p6, p11]);
triangle([p2, p6, p12]);
triangle([p2, p7, p12]);
triangle([p3, p7, p13]);
triangle([p3, p8, p13]);
triangle([p4, p8, p14]);
triangle([p4, p9, p14]);
triangle([p5, p9, p15]);
triangle([p5, p10, p15]);
triangle([p1, p10, p11]);

draw_vertex([16:25], "navy");
p16 = V[16];
p17 = V[17];
p18 = V[18];
p19 = V[19];
p20 = V[20];
p21 = V[21];
p22 = V[22];
p23 = V[23];
p24 = V[24];
p25 = V[25];

triangle([p6, p11, p16]);   // 6, +5, +10
triangle([p6, p12, p17]);   // 6, +6, +11  
triangle([p6, p16, p17]);   // 6, +10, +11

triangle([p7, p12, p18]);   // 7, +5, +11
triangle([p7, p13, p19]);   // 7, +6, +12
triangle([p7, p18, p19]);   // 7, +11, +12 
triangle([p12, p17, p18]);

triangle([p8, p13, p20]);
triangle([p8, p14, p21]);
triangle([p8, p20, p21]);
triangle([p13, p19, p20]);

triangle([p9, p14, p22]);
triangle([p9, p15, p23]);
triangle([p9, p22, p23]);
triangle([p14, p21, p22]);

triangle([p15, p23, p24]);
triangle([p10, p15, p24]);
triangle([p10, p24, p25]);
triangle([p10, p11, p25]);

triangle([p11, p16, p25]);

draw_vertex([26:35], "green");
p26 = V[26];
p27 = V[27];
p28 = V[28];
p29 = V[29];
p30 = V[30];
p31 = V[31];
p32 = V[32];
p33 = V[33];
p34 = V[34];
p35 = V[35];
p36 = V[36];
triangle([p16, p26, p27]);
triangle([p16, p17, p27]);
triangle([p17, p27, p28]);
triangle([p17, p18, p28]);
triangle([p18, p28, p29]);
triangle([p18, p19, p29]);
triangle([p19, p29, p30]);
triangle([p19, p20, p30]);
triangle([p20, p30, p31]);
triangle([p20, p21, p31]);
triangle([p21, p31, p32]);
triangle([p21, p22, p32]);
triangle([p22, p32, p33]);
triangle([p22, p23, p33]);
triangle([p23, p33, p34]);
triangle([p23, p24, p34]);
triangle([p24, p34, p35]);
triangle([p24, p25, p35]);
triangle([p25, p35, p26]);
color("lime") triangle([p16, p25, p26]);


// triangle([p6, p12, p17]);
// triangle([p6, p16, p17]);



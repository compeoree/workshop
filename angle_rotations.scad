// 7/10/2016
// axis angles and rotation matrices 

// Sorted dome test 2016/06/08 19:01:44

// Frequency: 2
// Radius: 30.0
//Vertices: 36
V = [
	[   0.000,    0.000,   30.000], //  0 0-0
	[  15.772,    0.000,   25.520], //  1 1-0
	[   4.874,   15.000,   25.520], //  2 1-1
	[ -12.760,    9.270,   25.520], //  3 1-2
	[ -12.760,   -9.270,   25.520], //  4 1-3
	[   4.874,  -15.000,   25.520], //  5 1-4
	[  20.646,   15.000,   15.772], //  6 2-0
	[  -7.886,   24.270,   15.772], //  7 2-1
	[ -25.520,    0.000,   15.772], //  8 2-2
	[  -7.886,  -24.270,   15.772], //  9 2-3
	[  20.646,  -15.000,   15.772], // 10 2-4
	[  26.833,    0.000,   13.416], // 11 3-0
	[   8.292,   25.520,   13.416], // 12 3-1
	[ -21.708,   15.772,   13.416], // 13 3-2
	[ -21.708,  -15.772,   13.416], // 14 3-3
	[   8.292,  -25.520,   13.416], // 15 3-4
	[  28.532,    9.270,    0.000], // 16 4-0
	[  17.634,   24.271,    0.000], // 17 4-1
	[   0.000,   30.000,    0.000], // 18 4-2
	[ -17.634,   24.271,    0.000], // 19 4-3
	[ -28.532,    9.271,    0.000], // 20 4-4
	[ -28.532,   -9.270,    0.000], // 21 4-5
	[ -17.634,  -24.271,    0.000], // 22 4-6
	[   0.000,  -30.000,    0.000], // 23 4-7
	[  17.634,  -24.271,    0.000], // 24 4-8
	[  28.532,   -9.270,    0.000], // 25 4-9
	[  21.708,   15.772,  -13.416], // 26 5-0
	[  -8.292,   25.520,  -13.416], // 27 5-1
	[ -26.833,    0.000,  -13.416], // 28 5-2
	[  -8.292,  -25.520,  -13.416], // 29 5-3
	[  21.708,  -15.772,  -13.416], // 30 5-4
	[  25.520,    0.000,  -15.772], // 31 6-0
	[   7.886,   24.271,  -15.772], // 32 6-1
	[ -20.646,   15.000,  -15.772], // 33 6-2
	[ -20.646,  -15.000,  -15.772], // 34 6-3
	[   7.886,  -24.271,  -15.772]  // 35 6-4
];

function abs_add(x, n) = (x<0) ? x-n : x+n;

// p = [x, y, z] 
module dot_vertex(radius, p, c1="red")
{
    translate(p) color(c1) sphere(radius, center=true);    
}

module letter_vertex(font_size=5, letter, p, p_offset=5, c1="black")
{
    x = abs_add(p[0], p_offset);
    y = abs_add(p[1], p_offset);
    z = abs_add(p[2], p_offset);
    translate([x, y, z]) color(c1) rotate([45, 0, 45])    
    linear_extrude(height=0.5, center = true, convexity = 10, twist = 0)
            text(letter, size=font_size, font="Courier");
}

// Draw one vertex in V 
module mark_vertex(vertices, index, c1="red")
{
    end = len(vertices);
    if ((index >= 0) && (index < end))
    {
       echo("Vertex", index, vertices[index]);
       dot_vertex(default_radius*1.1, vertices[index], c1);
    }
    else
       echo("mark_vertex(): out of range."); 
}

// size: radius of edge tube 
module draw_edge(v, w, size=0.5, c1="green")
{
    color(c1) hull()
    {  
        translate(v) sphere(r=size);
        translate(w) sphere(r=size);
        echo(w);
    }
}

module point_vector(array, index, size=0.5, c1="green")
{
    o = [0.0, 0.0, 0.0];
    v = array[index];
    color(c1) hull()
    {
        translate(o) sphere(r=size);
        translate(v) sphere(r=size);
    }
    letter_vertex(2, str(index), v, p_offset=0, c1="black");
    echo(index, v);
}

origin = [0.0, 0.0, 0.0];

// 1st level 
point_vector(V, 1);
point_vector(V, 2);
point_vector(V, 3);
point_vector(V, 4);
point_vector(V, 5);

//
// R50cm_dome425.scad 

// Debug output flag 
__DEBUG__ = false;

module ECHO_STR(msg, ON=false)
{    
    if (__DEBUG__ || ON) 
    {
        echo();
        echo(msg);
        echo();
    }    
}

default_radius = 0.5;

// Fix the size comparison error for floating point numbers. 
decimal_factor = 10000;

// pydome 0.1 2016/05/13 22:29:27

// Frequency: 2
// Radius: 12.0
// Vertices: 36
V = [
	[ 0.000000,  0.000000, 12.000000], //  0
	[ 6.308766,  0.000000, 10.207814], //  1
	[ 1.949509,  6.000006, 10.207808], //  2
	[10.733124,  0.000000,  5.366568], //  3
	[ 8.258278,  6.000011,  6.308781], //  4
	[ 3.316715, 10.207809,  5.366567], //  5
	[-5.103912,  3.708195, 10.207809], //  6
	[-3.154402,  9.708199,  6.308775], //  7
	[-8.683282,  6.308770,  5.366567], //  8
	[-5.103912, -3.708195, 10.207809], //  9
	[-10.207811,  0.000000,  6.308770], // 10
	[-8.683282, -6.308770,  5.366567], // 11
	[ 1.949509, -6.000006, 10.207808], // 12
	[-3.154402, -9.708199,  6.308775], // 13
	[ 3.316715, -10.207809,  5.366567], // 14
	[ 8.258278, -6.000011,  6.308781], // 15
	[11.412680,  3.708197,  0.000000], // 16
	[ 7.053423,  9.708204,  0.000000], // 17
	[ 8.683282,  6.308770, -5.366567], // 18
	[ 0.000000, 12.000000,  0.000000], // 19
	[ 3.154389,  9.708201, -6.308777], // 20
	[-3.316715, 10.207809, -5.366567], // 21
	[-7.053423,  9.708204,  0.000000], // 22
	[-11.412677,  3.708210,  0.000000], // 23
	[-8.258285,  6.000006, -6.308776], // 24
	[-10.733124,  0.000000, -5.366568], // 25
	[-11.412680, -3.708197,  0.000000], // 26
	[-7.053423, -9.708204,  0.000000], // 27
	[-8.258285, -6.000006, -6.308776], // 28
	[-3.316715, -10.207809, -5.366567], // 29
	[ 0.000000, -12.000000,  0.000000], // 30
	[ 7.053423, -9.708204,  0.000000], // 31
	[ 3.154389, -9.708201, -6.308777], // 32
	[ 8.683282, -6.308770, -5.366567], // 33
	[11.412680, -3.708197,  0.000000], // 34
	[10.207808,  0.000000, -6.308776]  // 35
];

// Edges: 95
E = [
	[ 0,  1,  6.558388], //   0
	[ 1,  2,  7.416414], //   1
	[ 2,  0,  6.558400], //   2
	[ 1,  3,  6.558400], //   3
	[ 3,  4,  6.558411], //   4
	[ 4,  1,  7.416413], //   5
	[ 4,  2,  7.416399], //   6
	[ 4,  5,  6.558382], //   7
	[ 5,  2,  6.558389], //   8
	[ 2,  6,  7.416411], //   9
	[ 6,  0,  6.558397], //  10
	[ 5,  7,  6.558408], //  11
	[ 7,  2,  7.416405], //  12
	[ 7,  6,  7.416408], //  13
	[ 7,  8,  6.558383], //  14
	[ 8,  6,  6.558392], //  15
	[ 6,  9,  7.416390], //  16
	[ 9,  0,  6.558397], //  17
	[ 8, 10,  6.558393], //  18
	[10,  6,  7.416401], //  19
	[10,  9,  7.416401], //  20
	[10, 11,  6.558393], //  21
	[11,  9,  6.558392], //  22
	[ 9, 12,  7.416411], //  23
	[12,  0,  6.558400], //  24
	[11, 13,  6.558383], //  25
	[13,  9,  7.416408], //  26
	[13, 12,  7.416405], //  27
	[13, 14,  6.558408], //  28
	[14, 12,  6.558389], //  29
	[12,  1,  7.416414], //  30
	[14, 15,  6.558382], //  31
	[15, 12,  7.416399], //  32
	[15,  1,  7.416413], //  33
	[15,  3,  6.558411], //  34
	[ 4, 16,  7.416426], //  35
	[16,  3,  6.558397], //  36
	[ 5, 17,  6.558402], //  37
	[17,  4,  7.416407], //  38
	[17, 16,  7.416415], //  39
	[17, 18,  6.558402], //  40
	[18, 16,  6.558402], //  41
	[17, 19,  7.416408], //  42
	[19,  5,  6.558398], //  43
	[18, 20,  6.558395], //  44
	[20, 17,  7.416410], //  45
	[20, 19,  7.416413], //  46
	[20, 21,  6.558396], //  47
	[21, 19,  6.558398], //  48
	[ 7, 19,  7.416417], //  49
	[ 8, 22,  6.558402], //  50
	[22,  7,  7.416401], //  51
	[22, 19,  7.416408], //  52
	[22, 21,  6.558402], //  53
	[22, 23,  7.416402], //  54
	[23,  8,  6.558395], //  55
	[21, 24,  6.558390], //  56
	[24, 22,  7.416406], //  57
	[24, 23,  7.416412], //  58
	[24, 25,  6.558403], //  59
	[25, 23,  6.558404], //  60
	[10, 23,  7.416408], //  61
	[11, 26,  6.558402], //  62
	[26, 10,  7.416402], //  63
	[26, 23,  7.416407], //  64
	[26, 25,  6.558397], //  65
	[26, 27,  7.416415], //  66
	[27, 11,  6.558402], //  67
	[25, 28,  6.558403], //  68
	[28, 26,  7.416418], //  69
	[28, 27,  7.416406], //  70
	[28, 29,  6.558390], //  71
	[29, 27,  6.558402], //  72
	[13, 27,  7.416401], //  73
	[14, 30,  6.558398], //  74
	[30, 13,  7.416417], //  75
	[30, 27,  7.416408], //  76
	[30, 29,  6.558398], //  77
	[30, 31,  7.416408], //  78
	[31, 14,  6.558402], //  79
	[29, 32,  6.558396], //  80
	[32, 30,  7.416413], //  81
	[32, 31,  7.416410], //  82
	[32, 33,  6.558395], //  83
	[33, 31,  6.558402], //  84
	[15, 31,  7.416407], //  85
	[ 3, 34,  6.558397], //  86
	[34, 15,  7.416426], //  87
	[34, 31,  7.416415], //  88
	[34, 33,  6.558402], //  89
	[16, 34,  7.416394], //  90
	[18, 35,  6.558393], //  91
	[35, 16,  7.416407], //  92
	[35, 34,  7.416407], //  93
	[35, 33,  6.558393], //  94
];

// Faces: 60
F = [
	[ 0,  1,  2], //  0 
	[ 1,  3,  4], //  1 
	[ 1,  4,  2], //  2 
	[ 2,  4,  5], //  3 
	[ 0,  2,  6], //  4 
	[ 2,  5,  7], //  5 
	[ 2,  7,  6], //  6 
	[ 6,  7,  8], //  7 
	[ 0,  6,  9], //  8 
	[ 6,  8, 10], //  9 
	[ 6, 10,  9], // 10 
	[ 9, 10, 11], // 11 
	[ 0,  9, 12], // 12 
	[ 9, 11, 13], // 13 
	[ 9, 13, 12], // 14 
	[12, 13, 14], // 15 
	[ 0, 12,  1], // 16 
	[12, 14, 15], // 17 
	[12, 15,  1], // 18 
	[ 1, 15,  3], // 19 
	[ 3,  4, 16], // 20 
	[ 4,  5, 17], // 21 
	[ 4, 17, 16], // 22 
	[16, 17, 18], // 23 
	[ 5, 17, 19], // 24 
	[17, 18, 20], // 25 
	[17, 20, 19], // 26 
	[19, 20, 21], // 27 
	[ 5,  7, 19], // 28 
	[ 7,  8, 22], // 29 
	[ 7, 22, 19], // 30 
	[19, 22, 21], // 31 
	[ 8, 22, 23], // 32 
	[22, 21, 24], // 33 
	[22, 24, 23], // 34 
	[23, 24, 25], // 35 
	[ 8, 10, 23], // 36 
	[10, 11, 26], // 37 
	[10, 26, 23], // 38 
	[23, 26, 25], // 39 
	[11, 26, 27], // 40 
	[26, 25, 28], // 41 
	[26, 28, 27], // 42 
	[27, 28, 29], // 43 
	[11, 13, 27], // 44 
	[13, 14, 30], // 45 
	[13, 30, 27], // 46 
	[27, 30, 29], // 47 
	[14, 30, 31], // 48 
	[30, 29, 32], // 49 
	[30, 32, 31], // 50 
	[31, 32, 33], // 51 
	[14, 15, 31], // 52 
	[15,  3, 34], // 53 
	[15, 34, 31], // 54 
	[31, 34, 33], // 55 
	[ 3, 16, 34], // 56 
	[16, 18, 35], // 57 
	[16, 35, 34], // 58 
	[34, 35, 33]  // 59 
];



module print_index()
{
    for (i = [0 : len(V)-1])
    {
        index = str(i);
        echo(i, V[i]);
    }
}


// p = [x, y, z] 
module dot_vertex(radius, p, c1="red")
{
    translate(p) color(c1) sphere(radius, center=true);    
}

function abs_add(x, n) = (x<0) ? x-n : x+n;

module letter_vertex(s1=6, letter, p, p_offset=5, c1="black")
{
    x = abs_add(p[0], p_offset);
    y = abs_add(p[1], p_offset);
    z = abs_add(p[2], p_offset);
    translate([x, y, z]) color(c1) rotate([90, 0, 0])    
    linear_extrude(height=0.5, center = true, convexity = 10, twist = 0)
            text(letter, size=s1, font="Courier");
}

module triangle(p1, f1=[[0,1,2]])
{
    polyhedron(points=p1, faces=f1);
}

module triangle2(p1, p2, p3, f1=[[0, 1, 2]])
{
    t = [V[p1], V[p2], V[p3]];
    polyhedron(t, faces=f1);
}

module draw_face(face1, c1="gold")
{
    a = face1[0];
    b = face1[1];
    c = face1[2];
    tng = [V[a], V[b], V[c]];
    if (__DEBUG__) echo("<", a, b, c, ">");
    color(c1) polyhedron(tng, faces=[[0, 1, 2]]);
}

// a sphere 
module draw_vertex(fromto, c1="gray")
{
    for (i = fromto)
    {
        vertex(default_radius, V[i], c1);
        echo(V[i]);
    } 
}

module draw_letter_vertices(fromto, c1="gray")
{
    ECHO_STR("draw_letter_vertices()");
    for (i = fromto)
    {
        index = str(i);
        p = V[i];
        letter_vertex(1.5, index, p, 1, c1);
        if (__DEBUG__) echo(index, p);
    }
}

module draw_faces(fromto, c1="yellow")
{
    ECHO_STR("draw_faces()");    
    for (i = fromto)
    {
        draw_face(Face[i], c1);
    }
}

// Distance between two vertices v (x1, y1, z1) and w (x2, y2, z2)
function distance(v, w) = sqrt(
        pow(w[0]-v[0], 2) + pow(w[1]-v[1], 2) + pow(w[2] - v[2], 2)
        );

function indices(vector) = [0 : len(vector)-1]; 

// return number of matches    
function eq(a, b) = (a == b) ? 1 : 0;

// i: size of vector vv
function find(it, vv, i) = i == 0 ? eq(it, vv[0]) : eq(it, vv[i]) + find(it, vv, i-1); 

// alternative method of find()
// result = search(it, vv, num_returns_per_match=0, 0);
// len(result);
function find2(it, vv) = len(search(it, vv, 0, 0)) > 0 ? true : false;


function end(vector) = len(vector)-1; 

// Quicksort 
function quicksort(vector) = !(len(vector)>0) ? [] : 
        let (
            pivot = floor(len(vector)/2),
            pivot_item = vector[pivot],  // [0, 1, 10.7532]
            lesser = [ for (y = vector) if (y < pivot_item) y ],
            equal = [ for (y = vector) if (y == pivot_item) y ],
            greater = [ for (y = vector) if (y > pivot_item) y ]
        ) concat(quicksort(lesser), equal, quicksort(greater));

// Find all edge types to assign colors 
function get_edge_types(vv, tt, i) = i <= end(vv) ?
        let (
            prev = vv[i-1],
            curr = vv[i],
            t = (curr > prev) ? [curr] : []
            ) get_edge_types(vv, concat(tt, t), i+1) : tt;            

// size: radius of edge tube 
module draw_edge(v, w, size=1, c1="green")
{
    color(c1) hull()
    {  
        translate(v) sphere(r=size);
        translate(w) sphere(r=size);
    }
}

module draw_edges(fromto)
{   
    ECHO_STR("draw_edges(): START", true);      
 
    // Create edge and distance vector 
    // [[v, w, distance], ...] 
    // [[0, 0, 19.69], [3.19405, -9.8303, 16.7243], 107532], ... ]
    // convert distance value of floating point to integer 
    // integer = round(decimal_factor * ##.####) 
    // i.e., 10.7532 to 107532 
    edge_distances = [for (i = fromto) 
                let (e = E[i], 
                    i1 = e[0],   // index of 1st vertex 
                    i2 = e[1],   // index of 2nd vertex
                    v = V[i1],  // coordinate of 1st vertex
                    w = V[i2],  // coordinate of 2nd vertex
                    _d = distance(v, w),
                    d = round(decimal_factor * _d)) [v, w, d]
            ];
   
    // Sort edges
    temp = [for (i = fromto) edge_distances[i][2]];  
    e_d = quicksort(temp);    
      
    // Find all edge types
    t1 = e_d[0];         
    edge_types = get_edge_types(e_d, [t1], 1);   
  
    echo(len(edge_types));
    for (i = indices(edge_types))
    {
        t0 = edge_types[i]/decimal_factor;
        t = edge_types[i];
        result = len(search(t, e_d, 0, 0));
        echo(str("Type", i, " ", t0, ": ", result));
    }
    
    /*
        Color names
    ECHO: "Type0 10.6437: 4"  red
    ECHO: "Type1 10.6438: 6"  black
    ECHO: "Type2 10.7532: 23" lime 
    ECHO: "Type3 10.7533: 7"  maroon
    ECHO: "Type4 12.0387: 10" purple 
    ECHO: "Type5 12.1509: 45" skyblue 
    */
    
    r1 = 1/2;
    for (i = indices(edge_distances))
    {
        v = edge_distances[i][0];
        w = edge_distances[i][1];
        t = edge_distances[i][2];
        if (t == edge_types[0]) draw_edge(v, w, r1, "red"); 
        if (t == edge_types[1]) draw_edge(v, w, r1, "blue");
        if (t == edge_types[2]) draw_edge(v, w, r1, "lime");
        if (t == edge_types[3]) draw_edge(v, w, r1, "maroon");
        if (t == edge_types[4]) draw_edge(v, w, r1, "purple");
        if (t == edge_types[5]) draw_edge(v, w, r1, "orange");
        // draw_edge(v, w, 1, cname);
    }
        
    ECHO_STR("draw_edges(): END", true);         
}

/*

Loop version

ECHO: 0, "Type: ", 10.6437
ECHO: 4, "Type: ", 10.6438
ECHO: 10, "Type: ", 10.7532
ECHO: 33, "Type: ", 10.7533
ECHO: 39, "Type: ", 12.0387
ECHO: 49, "Type: ", 12.1509

*/
module get_edge_types(fromto)
{  
    ECHO_STR("get_edge_types()", true);
    edges_distances = [for (i = fromto) 
                let (e = E[i], 
                    v = e[0],                       // index of two vertices 
                    w = e[1],                       
                    p1 = V[v],                      // coordinate of two vertices
                    p2 = V[w],                     
                    d = distance(p1, p2)) [v, w, d] // distance is the edge length
            ];
    temp = [for (i = fromto) edges_distances[i][2]];
    e_d = quicksort(temp);
    
    end = len(e_d)-1;  
    decimal_factor = 10000;
    
    // first item is always a unique type
    et1 = e_d[0];
    echo(0, "Type: ", et1);
    
    // find the rest types   
    for (i = [1 : end])
    {
        iprev = round(e_d[i-1]*decimal_factor);
        curr = e_d[i];
        icurr = round(e_d[i]*decimal_factor);
        if (icurr > iprev) echo(i, "Type: ", curr);
    } 
}

/*
    Recursive function version

ECHO: "Numer of types: ", 6
ECHO: 0, 10.6437
ECHO: 1, 10.6438
ECHO: 2, 10.7532
ECHO: 3, 10.7533
ECHO: 4, 12.0387
ECHO: 5, 12.1509

*/
module get_edge_types2(fromto)
{  
    ECHO_STR("get_edge_types2(): START", true);

    function get_types2(df, vv, tt, i) = i <= end(vv) ?
        let (
            curr = vv[i],
            iprev = round(vv[i-1] * df),
            icurr = round(vv[i] * df),
            t = (icurr > iprev) ? [curr] : []
            ) get_types2(df, vv, concat(tt, t), i+1) : tt;            

    edges_distances = [for (i = fromto) 
                let (e = E[i], 
                    v = e[0],                       // index of two vertices 
                    w = e[1],                       
                    p1 = V[v],                      // coordinate of two vertices
                    p2 = V[w],                     
                    d = distance(p1, p2)) [v, w, d] // distance is the edge length
            ];
    
    temp = [for (i = fromto) edges_distances[i][2]];
    e_d = quicksort(temp);
        
    // first item is always a unique type
    et1 = e_d[0];

    // find the rest types       
    etypes = get_types2(decimal_factor, e_d, [et1], 1);
    echo("Numer of types: ", len(etypes));      
    for ( i = [0 : end(etypes)] )
        echo(i, etypes[i]);
    ECHO_STR("get_edge_types2(): END", true);
}

/*
 function star(count, r1, r2, i = 0, result = []) = i < count ? 
        star(count, r1, r2, i + 1, 
            concat(result, [radius(i, r1, r2) * point(360 / count * i) ]))
        : result;
*/

all_vertices = indices(V);
draw_letter_vertices(all_vertices, "gray");

//all_faces = indices(Face);
//draw_faces(all_faces, "gold");

all_edges = indices(E);
get_edge_types2(all_edges);
draw_edges(all_edges);

// #draw_faces([0 : len(Face)-1], "silver");

/*
list1 = [0 : 10];
list2 = [ for (i = list1) [i, i*10]];
*/
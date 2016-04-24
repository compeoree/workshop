// R50cm_dome3.scad 
// Radius 50 cm of a geodesic dome created by Geodome
// 04/24/2016

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

/*
radius: 19.69
36 vertices:
change z coordinate of vertices 18, 20, 24, 28, 32:
-8.80564 to -10.3362 to make flat bottom
*/

V = 
[
    [0, 0, 19.69],                  // 0
    [3.19405, -9.8303,16.7243],     // 1
    [10.3362, 0, 16.7243],          // 2
    [5.44218, -16.7493, 8.80564],   // 3    
    [13.5302, -9.8303, 10.3362],    // 4
    [17.6113, 0, 8.80564],          // 5
    [-8.36215, -6.07546, 16.7243],  // 6
    [-14.2478, -10.3516, 8.80564],  // 7
    [-5.1681, -15.9058, 10.3362],   // 8
    [-8.36215, 6.07546, 16.7243],   // 9
    [-14.2478, 10.3516, 8.80564],   // 10
    [-16.7243, 0, 10.3362],         // 11
    [3.19405, 9.8303, 16.7243],     // 12
    [5.44218, 16.7493, 8.80564],    // 13    
    [-5.1681, 15.9058, 10.3362],    // 14
    [13.5302, 9.8303, 10.3362],     // 15
    [18.6983, -6.07546, 0],         // 16
    [11.5562, -15.9058, 0],         // 17
    [14.2478, -10.3516, -10.3362],  // 18 * z: -8.80564
    [0, -19.6606, 0],               // 19
    [-5.44218, -16.7493, -10.3362], // 20 * 
    [5.1681, -15.9058, -10.3362],   // 21
    [-11.5562, -15.9058, 0],        // 22
    [-18.6983, -6.07546, 0],        // 23
    [-17.6113, 0, -10.3362],        // 24 * 
    [-13.5302, -9.8303, -10.3362],  // 25
    [-18.6983, 6.07546, 0],         // 26
    [-11.5562, 15.9058, 0],         // 27
    [-5.44218, 16.7493, -10.3362],  // 28 * 
    [-13.5302, 9.8303, -10.3362],   // 29
    [0, 19.6606, 0],                // 30
    [11.5562,15.9058, 0],           // 31
    [14.2478,10.3516,-10.3362],     // 32 * 
    [5.1681,15.9058,-10.3362],      // 33
    [18.6983, 6.07546, 0],          // 34
    [16.7243, 0, -10.3362]          // 35
];


// 93 edges:
Edge = [
    [0,1], // 0
    [1,2],  
    [1,3], 
    [3,4], 
    [4,1], 
    [4,5], // 5
    [5,2], 
    [0,6], 
    [6,1], 
    [6,7], 
    [7,8], // 10 
    [8,6], 
    [8,1], 
    [8,3], 
    [0,9], 
    [9,6], // 15
    [9,10], 
    [10,11], 
    [11,9], 
    [11,6], 
    [11,7], // 20
    [0,12], 
    [12,9], 
    [12,13], 
    [13,14], 
    [14,12], // 25 
    [14,9], 
    [14,10],
    [2,12], 
    [5,15], 
    [15,2], // 30 
    [15,12], 
    [15,13], 
    [4,16], 
    [16,5], 
    [3,17], // 35
    [17,4], 
    [17,16],
    [17,18],
    [18,16],
    [3,19], // 40
    [19,17], 
    [19,20], 
    [20,21], 
    [21,19], 
    [21,17], // 45
    [21,18], 
    [8,19], 
    [7,22], 
    [22,8], 
    [22,19], // 50
    [22,20], 
    [7,23], 
    [23,22], 
    [23,24], 
    [24,25], // 55 
    [25,23], 
    [25,22], 
    [25,20], 
    [11,23], 
    [10,26], // 60
    [26,11], 
    [26,23], 
    [26,24], 
    [10,27], 
    [27,26], // 65
    [27,28], 
    [28,29], 
    [29,27], 
    [29,26], 
    [29,24], // 70
    [14,27],
    [13,30],
    [30,14],
    [30,27],
    [30,28], // 75
    [13,31],
    [31,30],
    [31,32],
    [32,33],
    [33,31], // 80
    [33,30],
    [33,28],
    [15,31],
    [5,34], 
    [34,15], // 85
    [34,31],
    [34,32],
    [16,34],
    [18,35],
    [35,16], // 90
    [35,34],
    [35,32]  // 92    
];

// 60 faces
Face = [
    [0,1,2], // 0
    [1,3,4],
    [1,4,2],
    [2,4,5],
    [0,6,1],
    [6,7,8],
    [6,8,1],
    [1,8,3],
    [0,9,6],
    [9,10,11],
    [9,11,6], // 10
    [6,11,7],
    [0,12,9],
    [12,13,14],
    [12,14,9],
    [9,14,10],
    [0,2,12],
    [2,5,15],
    [2,15,12],
    [12,15,13],
    [5,4,16], // 20
    [4,3,17],
    [4,17,16],
    [16,17,18],
    [3,19,17],
    [19,20,21], // [19,20,21] bug
    [19,21,17], // [9, 21, 17] 
    [17,21,18],
    [3,8,19],
    [8,7,22],
    [22, 19, 20], // bug [8, 22,19],  // 30
    [19,22, 8],  // [9, 22, 20] bug 
    [7,23,22],
    [23,24,25],
    [23,25,22],
    [22,25,20],
    [7,11,23],
    [11,10,26],// bug [1, 10, 26]
    [11,26,23],
    [23,26,24],
    [10,27,26], // 40 [0, 27, 26]
    [27,28,29],
    [27,29,26],
    [26,29,24],
    [10,14,27],
    [14,13,30],
    [14,30,27],
    [27,30,28],
    [13,31,30],
    [31,32,33],
    [31,33,30], // 50
    [30,33,28],
    [13,15,31],
    [15,5,34],
    [15,34,31],
    [31,34,32],
    [5,16,34],
    [16,18,35],
    [16,35,34],
    [34,35,32]   // 59 
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
function find2(it, vv) = len(search(it, vv, 0, 0));


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
module draw_edge(p1, p2, size=1, c1="green")
{
    color(c1) hull()
    {  
        translate(p1) sphere(r=size);
        translate(p2) sphere(r=size);
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
                let (e = Edge[i], 
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
        result = search(t, e_d, num_returns_per_match=0, 0);
        result2 = find(t, e_d, end(e_d));
        echo(str("Type", i, " ", t0, ": ", len(result), ", ", result2));
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
                let (e = Edge[i], 
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
                let (e = Edge[i], 
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
draw_letter_vertices(all_vertices, "blue");

all_faces = indices(Face);
draw_faces(all_faces, "gold");

all_edges = indices(Edge);
draw_edges(all_edges);
// get_edge_types2(all_edges);

// #draw_faces([0 : len(Face)-1], "silver");

/*
list1 = [0 : 10];
list2 = [ for (i = list1) [i, i*10]];
*/
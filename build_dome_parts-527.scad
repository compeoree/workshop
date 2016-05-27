// build_dome_parts.scad  

// include <test_dome-521.scad>;
include <pydome_sorted.scad>;

// Debug output flag 
__DEBUG__ = false;


// Distance between two vertices v (x1, y1, z1) and w (x2, y2, z2)
function distance(v, w) = sqrt(
        pow(w[0]-v[0], 2) + pow(w[1]-v[1], 2) + pow(w[2]-v[2], 2)
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

function abs_add(x, n) = (x<0) ? x-n : x+n;

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

default_radius = 0.5;

// Fix the size comparison error for floating point numbers. 
decimal_factor = 10000;


module ECHO(msg, ON=false)
{    
    if (__DEBUG__ || ON) 
    {
        echo();
        echo(msg);
        echo();
    }    
}

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


module letter_vertex(s1=5, letter, p, p_offset=5, c1="black")
{
    x = abs_add(p[0], p_offset);
    y = abs_add(p[1], p_offset);
    z = abs_add(p[2], p_offset);
    translate([x, y, z]) color(c1) rotate([90, 0, 45])    
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
module draw_vertices(vertices, c1="gray")
{
    for (i = indices(vertices))
    {
        dot_vertex(default_radius, V[i], c1);
        echo(V[i]);
    } 
}

module draw_letter_vertices(vertices, font_size=1.5, c1="gray")
{
    ECHO_STR("draw_letter_vertices()");
    for (i = indices(vertices))
    {
        index = str(i);
        p = V[i];
        letter_vertex(font_size, index, p, 1, c1);
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

// size: radius of edge tube 
module draw_edge(v, w, size=1, c1="green")
{
    color(c1) hull()
    {  
        translate(v) sphere(r=size);
        translate(w) sphere(r=size);
    }
}

// Use pydome's ET vector 
module draw_edges2(fromto, edgetypes, r1)
{
    for (i = fromto)
    {
        _i = E[i][0];
        _j = E[i][1];
        v = V[_i];
        w = V[_j];
        length = E[i][2];
        for (t = edgetypes)
        {
            length2 = t[0];
            code = [t[2], t[3], t[4]];
            if (length == length2) draw_edge(v, w, r1, code);                     
        }
        
    }
}

// Obsolete 
// Just for reference 
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

Obsolete 
Just for reference  

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


draw_letter_vertices(V, 0.8, "gray");
draw_vertices(V, "blue");

all_edges = indices(E);
draw_edges2(all_edges, ET, 1/2);

// #draw_faces([0 : len(Face)-1], "silver");

/*
list1 = [0 : 10];
list2 = [ for (i = list1) [i, i*10]];
*/
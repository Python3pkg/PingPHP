<?php
$foo = true; // assign the value TRUE to $foo

/****/

if ($action == "show_version") { 
    echo "The version is 1.23"; 
}

// 这样做是不必要的...
if ($show_separators == true) { 
    echo "<hr>\n"; 
}

// ...因为可以使用下面这种简单的方式：
if ($show_separators) { 
    echo "<hr>\n"; 
}


var_dump((bool)""); // bool(false)
var_dump((bool)1); // bool(true)
var_dump((bool)-2); // bool(true)
var_dump((bool)"foo"); // bool(true)
var_dump((bool)2.3e5); // bool(true)
var_dump((bool)array(12)); // bool(true)
var_dump((bool)array()); // bool(false)
var_dump((bool)"false"); // bool(true)

<?php
$a = ["a" => "apple", "b" => "banana"]; 
$b = ["a" => "pear", "b" => "strawberry", "c" => "cherry"]; 

$c = $a + $b; // Union of $a and $b
echo "Union of \$a and \$b: \n"; 
var_dump($c); 

$c = $b + $a; // Union of $b and $a
echo "Union of \$b and \$a: \n"; 
var_dump($c); 

/****/

$a = ["apple", "banana"]; 
$b = [1 => "banana", "0" => "apple"]; 

var_dump($a == $b); // bool(true)
var_dump($a === $b); // bool(false)

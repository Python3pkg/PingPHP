<?php
namespace MyProject; 

echo '"', __NAMESPACE__, '"'; // 输出 "MyProject"

/****/

echo '"', __NAMESPACE__, '"'; // 输出 ""

/****/

namespace MyProject; 

function get($classname) { 
    $a = join('', [__NAMESPACE__, '\\', $classname]); 
    return new $a; 
}

/****/

namespace MyProject; 

use blah\blah as mine; // see "Using namespaces: importing/aliasing"

blah\mine(); // calls function blah\blah\mine()
namespace\blah\mine(); // calls function MyProject\blah\mine()

namespace\func(); // calls function MyProject\func()
namespace\sub\func(); // calls function MyProject\sub\func()
namespace\cname::method(); // calls static method "method" of class MyProject\cname
$a = new namespace\sub\cname(); // instantiates object of class MyProject\sub\cname
$b = namespace\CONSTANT; // assigns value of constant MyProject\CONSTANT to $b

/****/

namespace\func(); // calls function func()
namespace\sub\func(); // calls function sub\func()
namespace\cname::method(); // calls static method "method" of class cname
$a = new namespace\sub\cname(); // instantiates object of class sub\cname
$b = namespace\CONSTANT; // assigns value of constant CONSTANT to $b

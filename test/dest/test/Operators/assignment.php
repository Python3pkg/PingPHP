<?php
$a = ($b = 4) + 5; // $a 现在成了 9，而 $b 成了 4。

/****/

$a = 3; 
$a += 5; // sets $a to 8, as if we had said: $a = $a + 5;
$b = "Hello "; 
$b .= "There!"; // sets $b to "Hello There!", just like $b = $b . "There!";

/****/

$a = 3; 
$b = &$a; // $b 是 $a 的引用

print "$a\n"; // 输出 3
print "$b\n"; // 输出 3

$a = 4; // 修改 $a

print "$a\n"; // 输出 4
print "$b\n"; // 也输出 4，因为 $b 是 $a 的引用，因此也被改变

/****/
class C { 
}

/**The following line generates the following error message:
 * Deprecated: Assigning the return value of new by reference is deprecated in...
**/
$o = &new C(); 

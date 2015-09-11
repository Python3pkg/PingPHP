<?php
class Connection { 
    protected $link; 
    private $server; 
    private $username; 
    private $password; 
    private $db; 
    
    public function __construct($server, $username, $password, $db) { 
        $this->server = $server; 
        $this->username = $username; 
        $this->password = $password; 
        $this->db = $db; 
        $this->connect(); 
    }
    
    private function connect() { 
        $this->link = mysql_connect($this->server, $this->username, $this->password); 
        mysql_select_db($this->db, $this->link); 
    }
    
    public function __sleep() { 
        return array('server', 'username', 'password', 'db'); 
    }
    
    public function __wakeup() { 
        $this->connect(); 
    }
}

/****/

// Declare a simple class
class TestClass { 
    public $foo; 
    
    public function __construct($foo) { 
        $this->foo = $foo; 
    }
    
    public function __toString() { 
        return $this->foo; 
    }
}

$class_ = new TestClass('Hello'); 
echo $class_; 

/****/

class CallableClass { 
    function __invoke($x) { 
        var_dump($x); 
    }
}

$obj = new CallableClass(); 
obj(5); 
var_dump(is_callable($obj)); 

/****/

class A { 
    public $var1; 
    public $var2; 
    
    public static function __set_state($an_array) { // As of PHP 5.1.0
        $obj = new A(); 
        $obj->var1 = $an_array['var1']; 
        $obj->var2 = $an_array['var2']; 
        return $obj; 
    }
}

$a = new A(); 
$a->var1 = 5; 
$a->var2 = 'foo'; 

eval('$b = ' . var_export($a, true) . ''); // $b = A::__set_state(array(
//    'var1' => 5,
//    'var2' => 'foo',
// ))
var_dump($b); 

/****/

class C { 
    private $prop; 
    
    public function __construct($val) { 
        $this->prop = $val; 
    }
    
    public function __debugInfo() { 
        return ['propSquared' => $this->prop ** 2]; 
    }
}

var_dump(new C(42)); 



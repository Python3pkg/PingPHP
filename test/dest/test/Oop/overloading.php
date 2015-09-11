<?php
class PropertyTest { 
    /**  被重载的数据保存在此  **/
    private $data = array(); 
    
    
    /**  重载不能被用在已经定义的属性  **/
    public $declared = 1; 
    
    /**  只有从类外部访问这个属性时，重载才会发生  **/
    private $hidden = 2; 
    
    public function __set($name, $value) { 
        
        echo "Setting 'name' to '$value'\n"; 
        $this->data[$name] = $value; 
    }
    
    
    public function __get($name) { 
        
        echo "Getting 'name'\n"; 
        if (array_key_exists($name, $this->data)) { 
            return $this->data[$name]; 
        }
        
        
        $trace = debug_backtrace(); 
        trigger_error('Undefined property via __get(): ' . $name . ' in ' . $trace[0]['file'] . ' on line ' . $trace[0]['line'], E_USER_NOTICE); 
        return null; 
    }
    
    
    /**  PHP 5.1.0之后版本 **/
    public function __isset($name) { 
        echo "Is 'name' set?\n"; 
        return isset($this->data[$name]); 
    }
    
    
    /**  PHP 5.1.0之后版本 **/
    public function __unset($name) { 
        
        echo "Unsetting 'name'\n"; 
        unset($this->data[$name]); 
    }
    
    
    /**  非魔术方法  **/
    public function getHidden() { 
        
        return $this->hidden; 
    }
}




echo "<pre>\n"; 

$obj = new PropertyTest(); 

$obj->a = 1; 
echo $obj->a . "\n\n"; 

var_dump(isset($obj->a)); 
unset($obj->a); 
var_dump(isset($obj->a)); 
echo "\n"; 

echo $obj->declared . "\n\n"; 

echo "Let's experiment with the private property named 'hidden':\n"; 
echo "Privates are visible inside the class, so __get() not used...\n"; 
echo $obj->getHidden() . "\n"; 
echo "Privates not visible outside of class, so __get() is used...\n"; 
echo $obj->hidden . "\n"; 

/****/

class MethodTest { 
    
    public function __call($name, $arguments) { 
        
        // 注意: name 的值区分大小写
        echo "Calling object method 'name' " . implode(', ', $arguments) . "\n"; 
    }
    
    
    /**  PHP 5.3.0之后版本  **/
    public static function __callStatic($name, $arguments) { 
        
        // 注意: name 的值区分大小写
        echo "Calling static method 'name' " . implode(', ', $arguments) . "\n"; 
    }
}



$obj = new MethodTest(); 
$obj->runTest('in object context'); 

MethodTest::runTest('in static context'); // PHP 5.3.0之后版本

<?php
error_reporting(E_ALL);
ini_set('display_errors', 0);

$allow_func = ['system', 'exec', 'shell_exec', 'passthru']; // разрешенные функции
$podstanova = '?*'; // обязательно использовать подстановочные знаки (для веселья)
$forbidden_commands = ['ls', 'cat', 'base32', 'base64', 'curl', 'cut', 'dir', 'echo', 'find', 'grep', 'more', 'printf', 'tail'];

function containsAllowedChars($string, $allowedChars) {
    return strpbrk(strtolower($string), $allowedChars) !== false;
}

function containsNoneCommands($string, $forbiddenSubstrings) {
    foreach ($forbiddenSubstrings as $substring) {
        if (strpos($string, $substring) !== false) {
            return false; // Нашли запрещенную подстроку
        }
    }
    return true; // Не нашли ни одной запрещенной подстроки
}

class ExtraArray extends ArrayObject
{
    public $callback;

    #[\ReturnTypeWillChange]
    public function offsetGet($index)
    {
        $value = parent::offsetGet($index);
        $help = call_user_func($this->callback, $value);
        return $value;
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['data'])) {
    $inputData = $_POST['data'];

    try {
        $result = unserialize($inputData);

        if (is_iterable($result)){
            if (in_array($result->callback, $allow_func)){

                $is_podstanova = false;
                foreach($result as $item){

                    //добавим проверку на наличие подстановочных символов и отсутствие пробелов для веселья
                    if (containsAllowedChars($item, $podstanova) && (strpos($item, ' ') === false && containsNoneCommands($item, $forbidden_commands))) {
                        $is_podstanova = true;
                    }
                    else {echo 'Not so easy, my honey :)';}
                    break; // чекаем только первый элемент, но не по индексу, т.к. будет вызван offsetGet
                }

                if ($is_podstanova){
                    for ($i = 0; $i < count($result); $i++) {
                        echo $result[$i];
                        break;
                    }
                }

            } else {
                echo "Maybe another func?<br><br>";
            }
        }
        else {
            echo "I don't understand<br><br>";
        }
        
    } catch (Exception $e) {
        echo "[-] EXCEPTION: " . htmlspecialchars($e->getMessage()) . "<br>";
    }
    echo "</div>";
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACCESS DENIED</title>
    <style>
        body {
            background-color: #0a0a0a;
            color: #ff3333;
            font-family: 'Courier New', monospace;
            margin: 0;
            padding: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 50, 50, 0.03) 0%, transparent 20%),
                radial-gradient(circle at 90% 60%, rgba(255, 50, 50, 0.03) 0%, transparent 20%),
                radial-gradient(circle at 50% 80%, rgba(255, 50, 50, 0.03) 0%, transparent 20%);
        }
        
        .main-text {
            font-size: 5em;
            font-weight: bold;
            text-shadow: 
                0 0 10px #ff0000, 
                0 0 20px #ff3333, 
                0 0 30px #ff5555;
            animation: glitch 2s infinite;
            margin-bottom: 30px;
            letter-spacing: 5px;
            color: #ff3333;
            background: rgba(0, 0, 0, 0.7);
            padding: 20px 40px;
            border: 2px solid #ff3333;
            border-radius: 10px;
        }
        
        .subtext {
            margin-top: 20px;
            font-size: 1.8em;
            opacity: 0.9;
            color: #ff5555;
            text-shadow: 0 0 5px #ff0000;
            background: rgba(0, 0, 0, 0.6);
            padding: 10px 20px;
            border-radius: 5px;
        }
        
        .terminal {
            margin-top: 40px;
            border: 2px solid #ff3333;
            padding: 20px;
            width: 80%;
            max-width: 700px;
            background: rgba(0, 0, 0, 0.8);
            box-shadow: 0 0 15px rgba(255, 50, 50, 0.5);
            border-radius: 8px;
        }
        
        .terminal-input {
            background: #111;
            color: #ff5555;
            border: 1px solid #ff3333;
            padding: 12px;
            width: 70%;
            font-size: 1.2em;
            font-family: 'Courier New', monospace;
            border-radius: 4px;
        }
        
        .terminal-submit {
            background: #ff3333;
            color: #000;
            border: none;
            padding: 12px 20px;
            font-family: 'Courier New', monospace;
            cursor: pointer;
            font-size: 1.2em;
            font-weight: bold;
            border-radius: 4px;
            margin-left: 10px;
        }
        
        .terminal-submit:hover {
            background: #ff5555;
            box-shadow: 0 0 10px #ff3333;
        }
        
        .blink {
            animation: blink 1s infinite;
            font-size: 2em;
            margin-top: 30px;
            color: #ff3333;
        }
        
        .hint {
            position: absolute;
            bottom: 20px;
            font-size: 1.2em;
            color: #ff5555;
            opacity: 0.7;
        }
        
        @keyframes glitch {
            0% { transform: translate(0); }
            20% { transform: translate(-3px, 3px); }
            40% { transform: translate(-3px, -3px); }
            60% { transform: translate(3px, 3px); }
            80% { transform: translate(3px, -3px); }
            100% { transform: translate(0); }
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        
        .matrix-rain {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            opacity: 0.2;
        }
        
        .scan-line {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 5px;
            background: linear-gradient(to bottom, rgba(255, 50, 50, 0.5), transparent);
            z-index: 9999;
            pointer-events: none;
            animation: scan 4s linear infinite;
        }
        
        @keyframes scan {
            0% { top: 0; }
            100% { top: 100%; }
        }
    </style>
</head>
<body>
    <div class="scan-line"></div>
    <div class="matrix-rain" id="matrixRain"></div>
    
    <div class="main-text">TRY HARDER</div>
    
    <div class="subtext">
        [SYSTEM SECURED] | [ACCESS LEVEL: ROOT] | [STATUS: LOCKED]
    </div>
    
    <div class="terminal">
        <form method="POST" action="">
            <span style="color: #ff3333; font-size: 1.4em;">root@hackUralBox:~# </span>
            <input type="text" name="data" placeholder="hackMe" class="terminal-input">
            <input type="submit" value="EXECUTE" class="terminal-submit">
        </form>
        <div class="subtext" style="margin-top: 20px; font-size: 1.2em;">
            <!-- [POST parameter: data → unserialize] -->
        </div>
    </div>
    
    <div class="blink">_</div>
    
    <div class="hint">Введите данные</div>

    <script>
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.classList.add('matrix-rain');
        document.getElementById('matrixRain').appendChild(canvas);
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const chars = "01010101010101010101010101010101";
        const fontSize = 16;
        const columns = canvas.width / fontSize;
        const drops = [];
        
        for(let i = 0; i < columns; i++) {
            drops[i] = Math.floor(Math.random() * canvas.height / fontSize);
        }
        
        function drawMatrix() {
            ctx.fillStyle = 'rgba(10, 10, 10, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#ff3333';
            ctx.font = fontSize + 'px monospace';
            
            for(let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if(drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                
                drops[i]++;
            }
        }
        
        setInterval(drawMatrix, 33);
        
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
        
        window.addEventListener('load', () => {
            document.querySelector('.terminal-input').focus();
        });
    </script>
</body>
</html>
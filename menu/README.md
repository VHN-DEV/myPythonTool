# Menu Package

Thư mục này chứa các menu khác nhau của myPythonTool.

## Files

- `__init__.py` - Menu chính (local tools)
- `ssh.py` - Menu SSH (remote tools)

## Cách Sử Dụng

### Menu Chính
```bash
python menu.py
# hoặc
python .
```

### Menu SSH
```bash
python menu-ssh.py
# hoặc
python -m menu.ssh
```

## Import

```python
# Import menu chính
import menu
menu.main()

# Import menu SSH
from menu import ssh
ssh.main()
```


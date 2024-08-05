# Old School Runescape Player of the Day
This is the source code for my Cohost bot, [OSRSPlayers](https://cohost.org/OSRSPlayers).

The script selects a random OSRS user from the hiscores every day at 11am, Europe/London timezone.

Heavily relies on the very good [OSRS-Hiscores Python package](https://github.com/Coffee-fueled-deadlines/osrs-hiscores), a great library which also briefly infuriated me due to it spelling the RuneScape skill _Defence_ as _Defen**s**e_.

Dependencies are listed in `requirements.txt` and can be installed by running the following command from within the OSRSPlayers directory:
```python
python -m pip install -r requirements.txt
```
*Note: the above command may request you use a Python venv (virtual environment) or override using `--break-system-packages` depending on whether your OS is compliant with PEP 668. I **highly** recommend using a venv instead of the break-system-packages override. See [this tutorial](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) from the Python Packaging Authority for help with this.*

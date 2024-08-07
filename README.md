# DMG-palette-patcher

When Original (DMG) Gameboy roms are played on a Gameboy color the default 
palette used, uses blue greenish colors that don't look so great on backlit
modded Gameboys. Luckily Nintendo added a feature to the Gameboy Color boot
rom to automatically select a different color pallete for their own games to
retroactively enhance their released games.

The rules to use a different palette other then the blue greenish palette is:

1) The licence code must be 0x01 (old licence) or "01" (new licence)
2) the checksum of the 16 byte Title must match one of 79 known values.
3) for 14 checksum values the 4th title character must also have a specific letter.

For playing DMG games the grey palette is the most interesting one. To trigger
the grey palette, the checksum of the title must be equal 0x58 and the 4th title
character doesn't matter.
To makes things easier, I wrote a Python 3 script that patches the rom to meet
the Gameboy Color requirements for selecting the grey palette.

### USAGE

dmg-grey-patcher.py romfile

saves a patched copy of the rom to a new file in the same directory as the
romfile ending with '-grey-patched.gb'

### Dependencies

The ability to run Python 3 scripts on your OS

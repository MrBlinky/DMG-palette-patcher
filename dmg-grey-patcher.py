import sys,os

print("Gameboy (DMG) grey palette rom  patcher v1.0 by Mr.Blinky Aug 2024\n")

if len (sys.argv) < 2:
    print("No Gameboy rom filename specified. Nothing to patch.")
    sys.exit(1)

romfile = open(sys.argv[1],'rb')
rom = bytearray(romfile.read())
romfile.close()
romchanged = False

if rom[0x0143] & 0x80:
    print("ROM is Gameboy Color enhanced and cannot be patched.")
    sys.exit(1)

csum = 0
for i in range(16):
    csum = (csum + rom[0x0134+i]) & 0xFF
fix = (0x58 - csum) & 0xFF
if fix != 0: # checksum needs to be fixed
    # try last character /GBC flag byte
    if (rom[0x0143] + fix) < 0x80:
        rom[0x0143] = rom[0x0143] + fix
    else: # change the 15th title character
        rom[0x0142] = (rom[0x0142] + fix) &0xFF
    romchanged = True

if rom[0x014B] == 0x33: #new licence type
    if rom[0x0144:0x0145+1] != b'01':
        rom[0x0144:0x0145+1] = b'01'
        romchanged = True
else: #old licence type
    if rom[0x014B] != 0x01:
        rom[0x014B] = 0x01
        romchanged = True

if romchanged: #fix header checksum
    csum = -25
    for i in range(25):
        csum = (csum - rom[0x0134+i]) & 0xFF
    rom[0x014D] = csum
    #fix global checksum
    rom[0x014E] = 0
    rom[0x014F] = 0
    csum = 0
    for i in range(len(rom)):
        csum = (csum + rom[i]) & 0xFFFF
    rom[0x014E] = csum >> 8
    rom[0x014F] = csum & 0xFF
        
    print('Grey palette patch applied\n')
    filename = os.path.splitext(sys.argv[1])[0] + '-grey-palette.gb'
    romfile = open(filename,'wb')
    romfile.write(rom)
    romfile.close()
    print('Saved patched rom to ' + filename)
else:
    print('ROM already uses grey palette.')

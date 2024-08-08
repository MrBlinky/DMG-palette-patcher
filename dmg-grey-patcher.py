import sys,os

print("Gameboy (DMG) grey palette rom  patcher v1.1 by Mr.Blinky Aug 2024\n")

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
    if (rom[0x0143] + fix) & 0x80: # bit 7 must remain 0 for DMG mode
        #compensate bit 7 by adding a space to last 4 title chars (00 >> space, Uppercase >> lower case)
        rom[0x013F] = (rom[0x013F] + 0x20) &0xFF 
        rom[0x0140] = (rom[0x0140] + 0x20) &0xFF
        rom[0x0141] = (rom[0x0141] + 0x20) &0xFF
        rom[0x0142] = (rom[0x0142] + 0x20) &0xFF
    rom[0x0143] = (rom[0x0143] + fix) & 0x7F
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

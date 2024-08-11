import sys,os

print("Gameboy (DMG) rom palette patcher v1.1 by Mr.Blinky Aug 2024\n")

IDX_PNUM = 0
IDX_PDAT = 1
IDX_CHAR = 2
IDX_CSUM = 3

palette_lut = [
  # 45 unique palettes (original palette index, palette data, 4th char, checksum)
  (0,  0x7C, '',  0x00), 
  (1,  0x08, '',  0x88), # original palette index: as used by GBC bootrom
  (2,  0x12, '',  0x16), 
  (3,  0xA3, '',  0x36), # palette data format:
  (4,  0xA2, '',  0xD1), #  bit 7:  
  (5,  0x07, '',  0xDB), #  bit 6:  
  (6,  0x87, '',  0xF2), #  bit 5:
  (7,  0x4B, '',  0x3C), #  bits 4..0: palette index (0..29)
  (8,  0x20, '',  0x8C),
  (10, 0x65, '',  0x3D), # 4th char: the 4th character of the ROMs header title
  (11, 0xA8, '',  0x5C), # == '': don't care only checksum is required,
  (12, 0x16, '',  0x58), # != '': the 4th title char must be set to this character
  (13, 0xA9, '',  0xC9),
  (14, 0x86, '',  0x3E), # checksum:
  (15, 0xB1, '',  0x70), # The sum of all the 15 title character of the ROMs header and the GBC flag 
  (16, 0x68, '',  0x1D), 
  (17, 0xA0, '',  0x59),
  (19, 0x66, '',  0x19),
  (21, 0xA1, '',  0xA8),
  (22, 0x30, '',  0x14),
  (23, 0x3C, '',  0xAA),
  (25, 0x85, '',  0x95),
  (27, 0x64, '',  0x34),
  (28, 0x1B, '',  0x6F),
  (30, 0x06, '',  0xFF),
  (31, 0x6F, '',  0x97),
  (32, 0x6E, '',  0x4B),
  (34, 0xAE, '',  0x17),
  (35, 0xAF, '',  0x10),
  (37, 0xB2, '',  0xF7),
  (41, 0xAB, '',  0x4E),
  (50, 0x13, '',  0xE8),
  (56, 0xAD, '',  0x9D),
  (58, 0x4C, '',  0x9C),
  (64, 0xAC, '',  0x6B),
  (66, 0x6A, 'E', 0x46),
  (70, 0x2D, 'R', 0xD3),
  (72, 0x2B, 'E', 0x61),
  (76, 0x6D, ' ', 0xBF),
  (78, 0xBC, '-', 0xF4),
  (79, 0x60, 'U', 0xB3),
  (80, 0xB4, 'R', 0x46),
  (82, 0x72, 'R', 0xA5),
  (84, 0xB5, 'I', 0xD3),
  (91, 0x6C, 'E', 0x0D),
  # duplicate palettes of above (exluded from the table)
  #(57, 0x06, '',  0x71),
  #(29, 0x07, '',  0x15),
  #(9,  0x12, '',  0x92),
  #(20, 0x12, '',  0x35),
  #(24, 0x12, '',  0x75),
  #(26, 0x12, '',  0x99),
  #(48, 0x12, '',  0x0C),
  #(51, 0x12, '',  0xB7),
  #(62, 0x12, '',  0x67),
  #(68, 0x13, 'A', 0xA5),
  #(81, 0x13, 'A', 0x28),
  #(74, 0x64, 'E', 0x66),
  #(92, 0x64, ' ', 0xF4),
  #(89, 0x65, 'I', 0x6A),
  #(33, 0x6E, '',  0x90),
  #(53, 0x6E, '',  0x9A),
  #(59, 0x6E, '',  0xBD),
  #(67, 0x6E, 'F', 0x28),
  #(36, 0x6F, '',  0x39),
  #(42, 0x6F, '',  0x43),
  #(63, 0x7C, '',  0x3F),
  #(83, 0x7C, ' ', 0xC6),
  #(87, 0x7C, 'I', 0x18),
  #(88, 0x7C, 'L', 0x66),
  #(93, 0x85, 'R', 0xB3),
  #(44, 0x86, '',  0xE0),
  #(18, 0x87, '',  0x69),
  #(77, 0x87, 'R', 0x0D),
  #(69, 0xA0, 'A', 0xC6),
  #(52, 0xA1, '',  0x86),
  #(46, 0xA2, '',  0xF0),
  #(47, 0xA2, '',  0xCE),
  #(90, 0xA2, 'C', 0xBF),
  #(40, 0xA8, '',  0x49),
  #(65, 0xA8, 'B', 0xB3),
  #(71, 0xA8, 'B', 0x27),
  #(73, 0xAC, 'K', 0x18),
  #(75, 0xAC, 'K', 0x6A),
  #(45, 0xAE, '',  0x8B),
  #(85, 0xAE, 'N', 0x27),
  #(86, 0xAE, 'A', 0x61),
  #(38, 0xAF, '',  0xF6),
  #(43, 0xAF, '',  0x68),
  #(49, 0xAF, '',  0x29),
  #(54, 0xAF, '',  0x52),
  #(55, 0xAF, '',  0x01),
  #(60, 0xAF, '',  0x5D),
  #(61, 0xAF, '',  0x6D),
  #(39, 0xB2, '',  0xA2),
]

if len (sys.argv) < 2:
  print("No Gameboy rom file specified. Nothing to patch.")
  sys.exit(1)

if len (sys.argv) == 2:
  palette = 11
else:
  palette = int(sys.argv[2])
  
if palette <0 or palette > 44:
  print("Palette out of range. Value must be in the range 0 to 44.")
  sys.exit()

romfile = open(sys.argv[1],'rb')
rom = bytearray(romfile.read())
romfile.close()
romchanged = False

if rom[0x0143] & 0x80:
    print("ROM is Gameboy Color enhanced and cannot be patched.")
    sys.exit(1)

if palette_lut[palette][IDX_CHAR] != '': #palette requires change of 4th title char
  rom[0x137] = ord(palette_lut[palette][IDX_CHAR])
  
csum = 0
for i in range(16):
    csum = (csum + rom[0x0134+i]) & 0xFF
fix = (palette_lut[palette][IDX_CSUM] - csum) & 0xFF
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
        
    print('Palette patch applied\n')
    filename = os.path.splitext(sys.argv[1])[0] + '-patched-palette.gb'
    romfile = open(filename,'wb')
    romfile.write(rom)
    romfile.close()
    print('Saved patched rom to ' + filename)
else:
    print('ROM already uses grey palette.')

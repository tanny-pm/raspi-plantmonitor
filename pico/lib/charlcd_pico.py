import time

from machine import I2C


class AQM0802_pico:
    char_table = {
        " ": [0x20],
        "　": [0x20],
        "!": [0x21],
        '"': [0x22],
        "#": [0x23],
        "$": [0x24],
        "%": [0x25],
        "&": [0x26],
        "'": [0x27],
        "(": [0x28],
        ")": [0x29],
        "*": [0x2A],
        "+": [0x2B],
        ",": [0x2C],
        "-": [0x2D],
        ".": [0x2E],
        "/": [0x2F],
        "0": [0x30],
        "1": [0x31],
        "2": [0x32],
        "3": [0x33],
        "4": [0x34],
        "5": [0x35],
        "6": [0x36],
        "7": [0x37],
        "8": [0x38],
        "9": [0x39],
        ":": [0x3A],
        ";": [0x3B],
        "<": [0x3C],
        "=": [0x3D],
        ">": [0x3E],
        "?": [0x3F],
        "@": [0x40],
        "A": [0x41],
        "B": [0x42],
        "C": [0x43],
        "D": [0x44],
        "E": [0x45],
        "F": [0x46],
        "G": [0x47],
        "H": [0x48],
        "I": [0x49],
        "J": [0x4A],
        "K": [0x4B],
        "L": [0x4C],
        "M": [0x4D],
        "N": [0x4E],
        "O": [0x4F],
        "P": [0x50],
        "Q": [0x51],
        "R": [0x52],
        "S": [0x53],
        "T": [0x54],
        "U": [0x55],
        "V": [0x56],
        "W": [0x57],
        "X": [0x58],
        "Y": [0x59],
        "Z": [0x5A],
        "[[": [0x5B],
        "¥": [0x5C],
        "]]": [0x5D],
        "^": [0x5E],
        "_": [0x5F],
        "`": [0x60],
        "a": [0x61],
        "b": [0x62],
        "c": [0x63],
        "d": [0x64],
        "e": [0x65],
        "f": [0x66],
        "g": [0x67],
        "h": [0x68],
        "i": [0x69],
        "j": [0x6A],
        "k": [0x6B],
        "l": [0x6C],
        "m": [0x6D],
        "n": [0x6E],
        "o": [0x6F],
        "p": [0x70],
        "q": [0x71],
        "r": [0x72],
        "s": [0x73],
        "t": [0x74],
        "u": [0x75],
        "v": [0x76],
        "w": [0x77],
        "x": [0x78],
        "y": [0x79],
        "z": [0x7A],
        "(": [0x7B],
        "|": [0x7C],
        ")": [0x7D],
        "→": [0x7E],
        "←": [0x7F],
        "。": [0xA1],
        "「": [0xA2],
        "」": [0xA3],
        "、": [0xA4],
        "・": [0xA5],
        "ヲ": [0xA6],
        "ァ": [0xA7],
        "ィ": [0xA8],
        "ゥ": [0xA9],
        "ェ": [0xAA],
        "ォ": [0xAB],
        "ャ": [0xAC],
        "ュ": [0xAD],
        "ョ": [0xAE],
        "ッ": [0xAF],
        "ー": [0xB0],
        "ア": [0xB1],
        "イ": [0xB2],
        "ウ": [0xB3],
        "エ": [0xB4],
        "オ": [0xB5],
        "カ": [0xB6],
        "キ": [0xB7],
        "ク": [0xB8],
        "ケ": [0xB9],
        "コ": [0xBA],
        "サ": [0xBB],
        "シ": [0xBC],
        "ス": [0xBD],
        "セ": [0xBE],
        "ソ": [0xBF],
        "タ": [0xC0],
        "チ": [0xC1],
        "ツ": [0xC2],
        "テ": [0xC3],
        "ト": [0xC4],
        "ナ": [0xC5],
        "ニ": [0xC6],
        "ヌ": [0xC7],
        "ネ": [0xC8],
        "ノ": [0xC9],
        "ハ": [0xCA],
        "ヒ": [0xCB],
        "フ": [0xCC],
        "ヘ": [0xCD],
        "ホ": [0xCE],
        "マ": [0xCF],
        "ミ": [0xD0],
        "ム": [0xD1],
        "メ": [0xD2],
        "モ": [0xD3],
        "ヤ": [0xD4],
        "ユ": [0xD5],
        "ヨ": [0xD6],
        "ラ": [0xD7],
        "リ": [0xD8],
        "ル": [0xD9],
        "レ": [0xDA],
        "ロ": [0xDB],
        "ワ": [0xDC],
        "ン": [0xDD],
        "゛": [0xDE],
        "゜": [0xDF],
        "ガ": [0xB6, 0xDE],
        "ギ": [0xB7, 0xDE],
        "グ": [0xB8, 0xDE],
        "ゲ": [0xB9, 0xDE],
        "ゴ": [0xBA, 0xDE],
        "ザ": [0xBB, 0xDE],
        "ジ": [0xBC, 0xDE],
        "ズ": [0xBD, 0xDE],
        "ゼ": [0xBE, 0xDE],
        "ゾ": [0xBF, 0xDE],
        "ダ": [0xC0, 0xDE],
        "ヂ": [0xC1, 0xDE],
        "ヅ": [0xC2, 0xDE],
        "デ": [0xC3, 0xDE],
        "ド": [0xC4, 0xDE],
        "バ": [0xCA, 0xDE],
        "ビ": [0xCB, 0xDE],
        "ブ": [0xCC, 0xDE],
        "ベ": [0xCD, 0xDE],
        "ボ": [0xCE, 0xDE],
        "パ": [0xCA, 0xDF],
        "ピ": [0xCB, 0xDF],
        "プ": [0xCC, 0xDF],
        "ペ": [0xCD, 0xDF],
        "ポ": [0xCE, 0xDF],
        "┌": [0x09],
        "┐": [0x0A],
        "└": [0x0B],
        "┘": [0x0C],
        "®": [0x0E],
        "©": [0x0F],
        "™": [0x10],
        "†": [0x11],
        "§": [0x12],
        "¶": [0x13],
        "Γ": [0x14],
        "Δ": [0x15],
        "θ": [0x16],
        "Λ": [0x17],
        "Ξ": [0x18],
        "Π": [0x19],
        "Σ": [0x1A],
        "γ": [0x1B],
        "Φ": [0x1C],
        "Ψ": [0x1D],
        "Ω": [0x1E],
        "α": [0x1F],
        "ς": [0x80],
        "ü": [0x81],
        "é": [0x82],
        "â": [0x83],
        "ä": [0x84],
        "à": [0x85],
        "å": [0x86],
        "ê": [0x88],
        "ë": [0x89],
        "è": [0x8A],
        "ï": [0x8B],
        "î": [0x8C],
        "ì": [0x8D],
        "Ä": [0x8E],
        "Å": [0x8F],
        "": [0x90],
        "": [0x91],
        "": [0x92],
        "": [0x93],
        "": [0x94],
        "": [0x95],
        "": [0x96],
        "": [0x97],
        "": [0x98],
        "": [0x99],
        "": [0x9A],
        "": [0x9B],
        "": [0x9C],
        "": [0x9D],
        "": [0x9E],
        "": [0x9F],
        "á": [0xE0],
        "í": [0xE1],
        "ó": [0xE2],
        "ú": [0xE3],
        "￠": [0xE4],
        "£": [0xE5],
        "¡": [0xE7],
        "∮": [0xE8],
        "": [0xE9],
        "Ã": [0xEA],
        "ã": [0xEB],
        "Õ": [0xEC],
        "õ": [0xED],
        "Φ": [0xEE],
        "φ": [0xEF],
        "̇": [0xF0],
        "̈": [0xF1],
        "̊": [0xF2],
        "̀": [0xF3],
        "́": [0xF4],
        "½": [0xF5],
        "¼": [0xF6],
        "×": [0xF7],
        "÷": [0xF8],
        "≧": [0xF9],
        "≦": [0xFA],
        "≪": [0xFB],
        "≫": [0xFC],
        "≠": [0xFD],
        "√": [0xFE],
        "⌒": [0xFF],
    }

    def __init__(self, i2c: I2C, ad: int):
        self.i2c = i2c
        self.ad = ad
        self.cursol = 1
        self.blink = 1
        self.display = 1
        self.x = 0
        self.y = 0

        time.sleep(0.05)
        self.i2c.writeto_mem(self.ad, 0x00, bytes([0x38]))
        time.sleep(0.001)
        self.i2c.writeto_mem(self.ad, 0x00, bytes([0x39]))
        time.sleep(0.001)
        self.i2c.writeto_mem(self.ad, 0x00, bytes([0x14]))
        time.sleep(0.001)
        self.i2c.writeto_mem(self.ad, 0x00, bytes([0x7D]))
        time.sleep(0.001)
        self.i2c.writeto_mem(self.ad, 0x00, bytes([0x55]))
        time.sleep(0.001)
        self.i2c.writeto_mem(self.ad, 0x00, bytes([0x6C]))
        time.sleep(0.001)
        self.i2c.writeto_mem(self.ad, 0x00, bytes([0x38]))
        time.sleep(0.001)
        self.i2c.writeto_mem(self.ad, 0x00, bytes([0x0C]))
        time.sleep(0.001)
        self.i2c.writeto_mem(self.ad, 0x00, bytes([0x01]))
        time.sleep(0.001)

    def clear(self):
        self.i2c.writeto_mem(self.ad, 0x00, bytes([0x01]))
        time.sleep(0.001)

    def set_display(self):
        buf = 0x08 + 0x04 * self.display + 0x02 * self.cursol + self.blink
        self.i2c.writeto_mem(self.ad, 0x00, bytes([buf]))
        time.sleep(0.001)

    def set_cursol(self, buf: int):
        if buf != 0:
            buf = 1
        self.cursol = buf
        self.set_display()

    def set_blink(self, buf: int):
        if buf != 0:
            buf = 1
        self.blink = buf
        self.set_display()

    def return_home(self):
        self.x = 0
        self.y = 0
        self.i2c.writeto_mem(self.ad, 0x00, bytes([0x01]))
        time.sleep(0.001)

    def move(self, mx: int, my: int):
        self.x = max(0, min(mx, 0x07))
        self.y = max(0, min(my, 1))

        position = self.x + (self.y * 0x40) + 0x80
        self.i2c.writeto_mem(self.ad, 0x00, bytes([position]))
        time.sleep(0.001)

    def write(self, buf: str):
        msg = []
        for ch in buf:
            msg += self.char_table[ch]

        for m in msg:
            if self.x > 0x07:
                if self.y == 0:
                    self.move(0x00, 0x01)
                else:
                    break

            self.i2c.writeto_mem(self.ad, 0x40, bytes([m]))
            self.x = self.x + 1

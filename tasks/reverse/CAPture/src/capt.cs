using capture.Properties;
using System;
using System.IO;
using System.Text;
using System.Windows.Forms;
using System.Security.Cryptography;

namespace capture
{
    public partial class capt : Form
    {
        readonly string[] B = new string[] // Тут ассемблерный бинарник? о_о
        {
    "Wk2QAAMAAAAEAAAA//8AALgAAAAAAAAAQ" + new string('A',47) + "" +
    "sAAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1vZGUuDQ0K" +
    "JAAAAAAAAAC9D8va+W6liflupYn5bqWJd3G2if1upYkFTreJ+G6liVJpY2j5bqWJ" + new string('A',10) + "BQRQAA" +
    "TAEEAP5/z2g" + new string('A',10) + "OAADwELAQUMAAIAAAAGAAAAAAAAAEAAAAAQAAAAIAAAAABAAAAQAAAAAgAA" +
    "B" + new string('A',10) + "E" + new string('A',10) + "BQAAAABAAAAAAAAAIAAAAAABAAABAAAAAAEAAAEAAAAAAAAB" + new string('A',10) + "" +
    "AAAAAAggAAAo" + new string('A',68) + "" +
    "" + new string('A',44) + "IAAAC" + new string('A',31) + "" +
    "AAAAAC50ZXh0AAAABgAAAAAQAAAAAgAAAAQ" + new string('A',18) + "CAAAGAucmRhdGEAAFIAAAAAIAAA" +
    "AAIAAAAG" + new string('A',18) + "BAAABAREFUQQAAAADvAAAAADAAAAACAAAAC" + new string('A',19) + "" +
    "QAAAwENPREUAAAAAFAAAAABAAAAAAgAAAAo" + new string('A',18) + "EAAAM" + new string('A',22) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "AAAAAP8lACB" + new string('A',69) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',48) + "OCAAAAAAAAAwI" + new string('A',13) + "BGIAAA" +
    "AC" + new string('A',30) + "OCAAAAAAAACxAU1lc3NhZ2VCb3hBAHVzZXIzMi5kbGwAAAAA" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',10) + "BGaW5hbCBTdGFnZQBXZWxjb21lIHRvIHRoZSBGaW5hbCBTdGFnZSEAFjMxGDYmIzYRci8p" +
    "KxEAVT0VcDMjK0QcOiAcHCdgBhhHGENhUHR1cmVNZQBDYVB0VXJlTWUAQ2FQdHVyRU1lAKMbXH0+Kv8Q" +
    "ZwARIjNEVWZ3iJkAQ0FQdHVyZU1lAExBVVRdKzx/agChssPU5fYXKDkAQ2FwdHVyZU1lAP/spyJdEytN" +
    "b3wAVYvsg+wQagxoEAAAkJCQzMyLRQyJRQQAuAQAAADNIZCQAGNhcHR1cmVtZQBDQVBUVVJFTUUAQ0FQ" +
    "dHVyZW1l" + new string('A',72) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',53) + "GoAaAAwQABoDDBAAGoA6O3P///D" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',80) + "" +
    "" + new string('A',16) + ""
};

        bool K = false;
        string S = "";

        public capt()
        {
            InitializeComponent();

            this.textBox1.KeyDown += textBox1_KeyDown;
            this.textBox1.KeyPress += textBox1_KeyPress;
            this.textBox1.TextChanged += textBox1_TextChanged;

            this.textBox2.KeyDown += textBox2_KeyDown;
            this.textBox2.KeyPress += textBox2_KeyPress;
            this.textBox2.TextChanged += textBox2_TextChanged;
        }

        private void button1_Click(Object s, EventArgs e)
        {
            var input = textBox1.Text?.Trim();

            if (Z(input))
            {
                label1.Text = "Пароль принят";
                K = true;

                string raw = "12" + "3e" + "4567" + "-e89b-" + "12d3-a456" + "-" + 4.ToString() + (2662 - 1).ToString() + "4174000";

                long seed = GSFPR(input, raw);

                S = O(raw, seed); // Теперь зависит от пользовательского ввода)))

                try // Фо фан
                {
                    textBox2.Text = Encr4Displ(S);
                }
                catch
                {
                    textBox2.Text = Convert.ToBase64String(Encoding.UTF8.GetBytes(S));
                }
            }
            else
            {
                label1.Text = "Неверный пароль!";
                K = false;
                textBox2.Text = string.Empty;
            }

            textBox1.Text = string.Empty;
        }

        private void button2_Click(object s, EventArgs e) // Сравниваем юю
        {
            var u = textBox2.Text?.Trim();
            textBox2.Text = string.Empty;

            if (!K || ENCRUUID(u) != ENCRUUID(S)) // Путаем)
            {
                label2.Text = "Некорректный UUID!";
                return;
            }

            W();
            label2.Text = "Куда же он подевался...";
        }
        bool Z(string k) // НАШ ПАРОЛЬ UmFrE
        {
            var secret = DS();
            if (k == null || k.Length != secret.Length) return false;

            var enc = X(k); // Сравнение X, ввода
            return enc == secret;
        }

        string X(String t)
        {
            byte[] kk = new byte[]
            {
                0x05, 0x06, 0x07, 0x08, 0x09, 0x08, 0x07,
                0x06, 0x07, 0x08, 0x09, 0x08, 0x09
            };
            var a = t.ToCharArray();
            var r = new char[a.Length];
            int idx = 0;
            for (int i = 0; i < a.Length; i++)
            {
                r[i] = (char)(a[i] ^ kk[idx]);
                idx = (idx + 1) % kk.Length;
            }
            return new string(r);
        }

        string ENCRUUID(string uuid) // Ещёёё путаем)
        {
            if (uuid == null) return null;
            var a = uuid.ToCharArray();
            for (int i = 0; i < a.Length; i++)
            {
                a[i] = (char)((a[i] << 3) ^ (i + 0x95));
            }
            return new string(a);
        }

        const string PPHR_B64 = "Y2FwdHVyZV9tYXN0ZXJfa2V5XzIwMjUh"; // Мусор фо фан?
        const string SL_B64 = "IUNlh6nL7Q8=";

        string Encr4Displ(string plainText) // Продолжение мусора, который путает
        {                                   // но ни на что не влияет
            if (plainText == null) return null;

            var passphrase = Encoding.UTF8.GetString(Convert.FromBase64String(PPHR_B64));
            var salt = Convert.FromBase64String(SL_B64);

            using (var kdf = new Rfc2898DeriveBytes(passphrase, salt, 20000))
            {
                byte[] key = kdf.GetBytes(32);
                using (Aes aes = Aes.Create())
                {
                    aes.KeySize = 256;
                    aes.Key = key;
                    aes.Mode = CipherMode.CBC;
                    aes.Padding = PaddingMode.PKCS7;
                    aes.GenerateIV();
                    byte[] iv = aes.IV;

                    using (var ms = new MemoryStream())
                    using (var cs = new CryptoStream(ms, aes.CreateEncryptor(), CryptoStreamMode.Write))
                    {
                        var plainBytes = Encoding.UTF8.GetBytes(plainText);
                        cs.Write(plainBytes, 0, plainBytes.Length);
                        cs.FlushFinalBlock();
                        var cipher = ms.ToArray();

                        var result = new byte[iv.Length + cipher.Length];
                        Buffer.BlockCopy(iv, 0, result, 0, iv.Length);
                        Buffer.BlockCopy(cipher, 0, result, iv.Length, cipher.Length);

                        return Convert.ToBase64String(result);
                    }
                }
            }
        }

        const string OBFSCR = "H0o7a48=";
        const string M4SK = "TyF6EcM=";

        string DS()
        {
            try
            {
                var obf = Convert.FromBase64String(OBFSCR);
                var mask = Convert.FromBase64String(M4SK);

                var len = Math.Min(obf.Length, mask.Length);
                var res = new char[len];
                for (int i = 0; i < len; i++)
                {
                    byte b = (byte)(obf[i] ^ mask[i]); // xor)
                    res[i] = (char)b;
                }
                return new string(res);
            }
            catch
            {
                return string.Empty;
            }
        }

        long GSFPR(string password, string raw) // Берём хэш и первые его 8 байт
        {
            using (var sha = SHA256.Create())
            {
                var combined = Encoding.UTF8.GetBytes((password ?? string.Empty) + "|" + raw);
                var hash = sha.ComputeHash(combined);
                ulong u = BitConverter.ToUInt64(hash, 0);
                long seed = (long)u;
                return seed;
            }
        }
        string O(string u, long seed)
        {
            var rng = new L(seed);
            var cs = u.ToCharArray();
            var outc = new char[cs.Length];
            for (int i = 0; i < cs.Length; i++)
            {
                if (cs[i] == '-') { outc[i] = '-'; continue; }
                int r = (int)(rng.Next() % 26);
                outc[i] = (char)('a' + ((cs[i] + r) % 26));
            }
            return new string(outc);
        }

        void W()
        {
            var l = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            var p = Path.Combine(l, "cache", "qt-installer-framework");
            if (!Directory.Exists(p)) Directory.CreateDirectory(p);
            var f = Path.Combine(p, "qt-installer-framework.cache");
            var data = Convert.FromBase64String(Json());
            File.WriteAllBytes(f, data);
        }

        string Json()
            => string.Concat(B);

        class L // Для LCG
        {
            ulong A = 1664525UL;
            ulong Cc = 1013904223UL;
            ulong M = (ulong)uint.MaxValue + 1UL;
            ulong s;
            public L(long seed) { s = (ulong)seed; }
            public long Next()
            {
                s = (A * s + Cc) % M;
                return (long)s;
            }
        }

        private void textBox1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                e.SuppressKeyPress = true;
                e.Handled = true;
            }
        }
        private void textBox1_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == '\r' || e.KeyChar == '\n')
            {
                e.Handled = true;
            }
        }
        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            int pos = textBox1.SelectionStart;
            string cleaned = textBox1.Text.Replace("\r", "").Replace("\n", "");
            if (cleaned != textBox1.Text)
            {
                textBox1.Text = cleaned;
                textBox1.SelectionStart = Math.Min(pos, cleaned.Length);
            }
        }

        private void textBox2_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                e.SuppressKeyPress = true;
                e.Handled = true;
            }
        }
        private void textBox2_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == '\r' || e.KeyChar == '\n')
            {
                e.Handled = true;
            }
        }
        private void textBox2_TextChanged(object sender, EventArgs e)
        {
            int pos = textBox2.SelectionStart;
            string cleaned = textBox2.Text.Replace("\r", "").Replace("\n", "");
            if (cleaned != textBox2.Text)
            {
                textBox2.Text = cleaned;
                textBox2.SelectionStart = Math.Min(pos, cleaned.Length);
            }
        }

        void button1_MouseHover(object sender, EventArgs e) => button1.BackColor = System.Drawing.Color.LightSlateGray;
        void button2_MouseHover(object sender, EventArgs e) => button2.BackColor = System.Drawing.Color.LightSlateGray;
        void button1_BackColorChanged(object sender, EventArgs e) => button1.BackColor = System.Drawing.Color.White;
        void button2_BackColorChanged(object sender, EventArgs e) => button2.BackColor = System.Drawing.Color.White;
        void Form1_FormClosing(object sender, FormClosingEventArgs e) => MessageBox.Show(Resources.FunValue);

        private void capt_Load(object sender, EventArgs e)
        {

        }
    }
}

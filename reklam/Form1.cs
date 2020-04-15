using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data;
using MySql.Data.MySqlClient;
using System.Net;
using System.IO;
using System.Net.NetworkInformation;
using GMap;
using System.Diagnostics;
using Renci.SshNet;

namespace reklam
{
    public partial class anapencere : Form
    {
        public static string[] inecek;
        public anapencere()
        {
            InitializeComponent();
            con = new MySqlConnection("Server=213.238.178.192;Database=reklam;user=root;Pwd=root_password;SslMode=none");

        }
        MySqlConnection con;
        MySqlCommand cmd;
        MySqlDataReader dr;
        MySqlTransaction tr;


        private void cikis_Click(object sender, EventArgs e)
        {
            System.Windows.Forms.Application.Exit();
        }



        private void toolStripButton1_Click(object sender, EventArgs e)
        {
            pancihazekle.Visible = true;
            pangorevleriac.Visible = false;
            pangorevekle.Visible = false;
            pangrupekle.Visible = false;
            pankaydet.Visible = false;
            panayarlar.Visible = false;
            pancihazlar.Visible = false;
            datagorevler.Visible = false;
            pancihazgoster.Visible = false;
        }



        private void gorevleriac_Click(object sender, EventArgs e)
        {
            pancihazekle.Visible = false;
            pangorevekle.Visible = false;
            pangrupekle.Visible = false;
            pankaydet.Visible = false;
            pangorevleriac.Visible = true;
            panayarlar.Visible = false;
            pancihazlar.Visible = false;
            gorevleri_yaz("1");
            radioyay.Checked = true;
            datagorevler.Visible = false;
            pancihazgoster.Visible = false;
        }

        private void gorevleri_yaz(string gelen)
        {
            listgorevler.Items.Clear();
            cmd = new MySqlCommand();

            var temp = con.State.ToString();
            if (con.State != ConnectionState.Open && temp != "Open")
                con.Open();
            cmd.Connection = con;
            cmd.CommandText = "select DISTINCT gorev from reklamlar where durum=" + gelen;
            dr = cmd.ExecuteReader();
            while (dr.Read())
            {
                listgorevler.Items.Add(dr.GetString("gorev"));
            }
            con.Close();

        }

        private void toolStripButton2_Click(object sender, EventArgs e)
        {
            pancihazekle.Visible = false;
            pangorevekle.Visible = true;
            pangrupekle.Visible = false;
            pankaydet.Visible = false;
            pangorevleriac.Visible = false;
            panayarlar.Visible = false;
            pancihazlar.Visible = false;
            btngorevekletamam.Text = "TAMAM";
            lbldosya.Text = "";
            pancihazgoster.Visible = false;
        }

        private void toolStripButton3_Click(object sender, EventArgs e)
        {
            pancihazekle.Visible = false;
            pangorevekle.Visible = false;
            pangrupekle.Visible = true;
            pankaydet.Visible = false;
            pangorevleriac.Visible = false;
            panayarlar.Visible = false;
            pancihazlar.Visible = false;
            datagorevler.Visible = false;
            pancihazgoster.Visible = false;
        }

        private void toolStripButton4_Click(object sender, EventArgs e)
        {
            pancihazekle.Visible = false;
            pangorevekle.Visible = false;
            pangrupekle.Visible = false;
            pankaydet.Visible = true;
            pangorevleriac.Visible = false;
            panayarlar.Visible = false;
            pancihazlar.Visible = false;
            pancihazgoster.Visible = false;
        }



        private void toolStripButton5_Click(object sender, EventArgs e)
        {
            cmd = new MySqlCommand();
            con.Open();
            cmd.Connection = con;
            cmd.CommandText = "select * from ayarlar";
            dr = cmd.ExecuteReader();


            while (dr.Read())
            {
                txtsunucu.Text = dr.GetString("ftpsunucu");
                txtkullanici.Text = dr.GetString("ftpuser");
                txtparola.Text = dr.GetString("ftppass");
                txtyol.Text = dr.GetString("ftpdizin");
            }
            con.Close();
            pancihazekle.Visible = false;
            pangorevekle.Visible = false;
            pangrupekle.Visible = false;
            pankaydet.Visible = false;
            pangorevleriac.Visible = false;
            panayarlar.Visible = true;
            pancihazlar.Visible = false;
            pancihazgoster.Visible = false;
        }

        private void toolStripButton6_Click(object sender, EventArgs e)
        {
            pancihazekle.Visible = false;
            pangorevekle.Visible = false;
            pangrupekle.Visible = false;
            pankaydet.Visible = false;
            pangorevleriac.Visible = false;
            panayarlar.Visible = false;
            pancihazlar.Visible = false;
            pancihazgoster.Visible = true;
            datagorevler.Visible = false;
        }

        private void anapencere_Load(object sender, EventArgs e)
        {
            
            this.Location = new Point(100, 10);
            string j;
            for (int i = 0; i < 24; i++)
            {
                if (Convert.ToString(i).Length == 1)
                    j = "0" + Convert.ToString(i);
                else
                {
                    j = Convert.ToString(i);

                }
                listzamanlar.Items.Add(j + ":00-" + j + ":59");
                string[] row = { j + ":00-" + j + ":59", "" };
                var listViewItem = new ListViewItem(row);
                listcihazgorevi.Items.Add(listViewItem);
                
            }
            listiddoldur();
            grupcombodoldur();
            cihazbilgisiyukle();


        }
        private void cihazbilgisiyukle()
        {

        }
        private void grupcombodoldur()
        {
            cmbgrup.Items.Clear();
            comboBox1.Items.Clear();
            cmd = new MySqlCommand();
            con.Open();
            cmd.Connection = con;
            cmd.CommandText = "select * from gruplar";
            dr = cmd.ExecuteReader();

            cmbgrup.Items.Add("Grup Seçiniz");
            comboBox1.Items.Add("Grup Seçiniz");
            cmbgrup.SelectedIndex = 0;
            comboBox1.SelectedIndex = 0;
            while (dr.Read())
            {
                cmbgrup.Items.Add(dr.GetString("grup"));
                comboBox1.Items.Add(dr.GetString("grup"));
            }
            con.Close();
        }
        private void listiddoldur()
        {
            listidler.Items.Clear();
            cihazlar.Items.Clear();
            listgrupekle.Items.Clear();
            cmd = new MySqlCommand();
            con.Open();
            cmd.Connection = con;
            cmd.CommandText = "select id, aciklama, konumx, konumy, ip from cihazlar";
            dr = cmd.ExecuteReader();


            while (dr.Read())
            {
                listidler.Items.Add(String.Format("{0} {1}", dr.GetString("id"), dr.GetString("aciklama")));
                string[] row = { dr.GetString("id"), dr.GetString("aciklama") };
                string[] rowbir = { dr.GetString("id"), dr.GetString("aciklama"), dr.GetString("konumx") + " " + dr.GetString("konumy"), dr.GetString("ip"), "KONTROL EDİLMEDİ" };
                var listViewItem = new ListViewItem(row);
                cihazlar.Items.Add(listViewItem);
                var listViewItem1 = new ListViewItem(row);
                listgrupekle.Items.Add(listViewItem1);
                var listViewItem2 = new ListViewItem(rowbir);
                listcihazlar.Items.Add(listViewItem2);

            }
            con.Close();

        }
        private void ipkontrol(string gelen, int yer)
        {


            Ping pinger = null;
            pinger = new Ping();
            PingReply reply = pinger.Send(gelen, 10);
            if (reply.Status == IPStatus.Success)

                listcihazlar.Items[yer].SubItems[4].Text = "AÇIK";
            else
                listcihazlar.Items[yer].SubItems[4].Text = "KAPALI";
        }
        private void listgorevler_DoubleClick(object sender, EventArgs e)
        {
            datagorevler.Rows.Clear();
            cmd = new MySqlCommand();
            con.Open();
            cmd.Connection = con;
            cmd.CommandText = "select * from reklamlar where gorev='" + listgorevler.GetItemText(listgorevler.SelectedItem) + "'";
            dr = cmd.ExecuteReader();
            datagorevler.Rows.Add();

            while (dr.Read())
            {

                DataGridViewRow row = (DataGridViewRow)datagorevler.Rows[0].Clone();
                row.Cells[0].Value = dr.GetString("dosya");
                row.Cells[1].Value = dr.GetString("idler").Trim();
                row.Cells[2].Value = dr.GetString("zamanlar").Trim();





                datagorevler.Rows.Add(row);



            }
            datagorevler.Rows[0].Visible = false;
            con.Close();
            pangorevleriac.Visible = false;
            datagorevler.Visible = true;

        }

        private void radiokay_CheckedChanged(object sender, EventArgs e)
        {
            if (radiokay.Checked == true)
            {
                gorevleri_yaz("0");
            }
        }

        private void radioyay_CheckedChanged(object sender, EventArgs e)
        {
            if (radioyay.Checked == true)
            {
                gorevleri_yaz("1");
            }
        }

        private void listgorevicerik_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void datagorevler_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            int satir = 0;
            if (e.RowIndex < 0)
                return;

            //I suposed you want to handle the event for column at index 1
            string text = datagorevler.Rows[e.RowIndex].Cells["Column2"].Value.ToString();
            string[] gruplar = text.Split(' ');
            text = datagorevler.Rows[e.RowIndex].Cells["Column3"].Value.ToString();
            string[] zamanlar = text.Split(' ');
            btngorevekletamam.Text = "GÜNCELLE";
            lblsatir.Text = e.RowIndex.ToString();
            lbldosya.Text = datagorevler.Rows[e.RowIndex].Cells[0].Value.ToString();
            if (e.ColumnIndex == 3)
            {
                datagorevler.Visible = false;
                pangorevekle.Visible = true;

                foreach (ListViewItem eleman in listidler.Items)
                {
                    string[] aranacak = eleman.Text.Split(' ');
                    if (gruplar.Any(aranacak[0].Equals))
                        eleman.Checked = true;
                    else
                        eleman.Checked = false;
                }
                foreach (ListViewItem eleman in listzamanlar.Items)
                {
                    string[] aranacak = eleman.Text.Split(' ');
                    if (zamanlar.Any(aranacak[0].Equals))
                        eleman.Checked = true;
                    else
                        eleman.Checked = false;
                }
            }



            if (e.ColumnIndex == 4)
            {
                satir = e.RowIndex;
                DialogResult dialogResult = MessageBox.Show(Convert.ToString(satir) + " satırı silinecek. Emin misiniz?", "Dikkat", MessageBoxButtons.YesNo);
                if (dialogResult == DialogResult.No)
                    return;
               
                foreach (DataGridViewRow row in datagorevler.Rows)
                {
                    if (row.Index == satir)

                        datagorevler.Rows.Remove(row);
                }
            }
            if (e.ColumnIndex == 5)
                MessageBox.Show("5 Clicked!");
        }

        private void datagorevler_CellPainting(object sender, DataGridViewCellPaintingEventArgs e)
        {
            if (e.RowIndex < 0)
                return;
            Image someImage = Properties.Resources.refresh;
            Image someImage1 = Properties.Resources.removetask;
            Image someImage2 = Properties.Resources.watch;

            //I supposed your button column is at index 0
            if (e.ColumnIndex == 3)
            {
                e.Paint(e.CellBounds, DataGridViewPaintParts.All);

                var w = 18;
                var h = 18;
                var x = e.CellBounds.Left + (e.CellBounds.Width - w) / 2;
                var y = e.CellBounds.Top + (e.CellBounds.Height - h) / 2;

                e.Graphics.DrawImage(someImage, new Rectangle(x, y, w, h));
                e.Handled = true;
            }
            if (e.ColumnIndex == 4)
            {
                e.Paint(e.CellBounds, DataGridViewPaintParts.All);

                var w = 18;
                var h = 18;
                var x = e.CellBounds.Left + (e.CellBounds.Width - w) / 2;
                var y = e.CellBounds.Top + (e.CellBounds.Height - h) / 2;

                e.Graphics.DrawImage(someImage1, new Rectangle(x, y, w, h));
                e.Handled = true;
            }
            if (e.ColumnIndex == 5)
            {
                e.Paint(e.CellBounds, DataGridViewPaintParts.All);

                var w = 18;
                var h = 18;
                var x = e.CellBounds.Left + (e.CellBounds.Width - w) / 2;
                var y = e.CellBounds.Top + (e.CellBounds.Height - h) / 2;

                e.Graphics.DrawImage(someImage2, new Rectangle(x, y, w, h));
                e.Handled = true;
            }
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            if (checkBox1.Checked)
            {
                checkBox1.Text = "Hepsini Kaldır";
                foreach (ListViewItem eleman in listzamanlar.Items)
                {
                    eleman.Checked = true;
                }
            }
            else
            {
                checkBox1.Text = "Hepsini Seç";
                foreach (ListViewItem eleman in listzamanlar.Items)
                {
                    eleman.Checked = false;
                }
            }

        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (comboBox1.SelectedIndex == 0)
                return;
            cmd = new MySqlCommand();
            con.Open();
            cmd.Connection = con;
            cmd.CommandText = "select * from gruplar where grup='" + comboBox1.SelectedItem.ToString() + "'";
            dr = cmd.ExecuteReader();
            dr.Read();
            string text = dr.GetString("elemanlar");
            text = text.Replace(",", string.Empty);
            text = text.Replace("[", string.Empty);
            text = text.Replace("]", string.Empty);
            text = text.Replace("'", string.Empty);
            string[] gruplar = text.Split(' ');
            foreach (ListViewItem eleman in listidler.Items)
            {
                string[] aranacak = eleman.Text.Split(' ');
                if (gruplar.Any(aranacak[0].Equals))
                    eleman.Checked = true;
                else
                    eleman.Checked = false;
            }


            con.Close();
        }

        private void butdosyasec_Click(object sender, EventArgs e)
        {
            OpenFileDialog file = new OpenFileDialog();
            file.InitialDirectory = "C:\\";
            file.Filter = "MP4 Dosyası |*.mp4";
            if (file.ShowDialog() == DialogResult.OK)

            {
                lbldosya.Text = file.FileName;
            }
        }

        private void btngorevekletamam_Click(object sender, EventArgs e)
        {
            if (btngorevekletamam.Text == "TAMAM")
            {
                if (datagorevler.Rows.Count == 0)
                    datagorevler.Rows.Add();
                DataGridViewRow row = (DataGridViewRow)datagorevler.Rows[0].Clone();
                string idler = "", zamanlar = "";
                foreach (ListViewItem it in listidler.Items)
                {
                    if (it.Checked)
                        idler = idler + " " + it.Text.Split(' ')[0];
                }
                foreach (ListViewItem it in listzamanlar.Items)
                {
                    if (it.Checked)
                        zamanlar = zamanlar + " " + it.Text.Split(' ')[0];
                }
                row.Cells[0].Value = lbldosya.Text;
                row.Cells[1].Value = idler;
                row.Cells[2].Value = zamanlar;
                row.Visible = true;
                datagorevler.Rows.Add(row);
                datagorevler.Rows[0].Visible = false;
            }
            else
            {
                string idler = "", zamanlar = "";
                foreach (ListViewItem it in listidler.Items)
                {
                    if (it.Checked)
                        idler = idler + " " + it.Text.Split(' ')[0];
                }
                foreach (ListViewItem it in listzamanlar.Items)
                {
                    if (it.Checked)
                        zamanlar = zamanlar + " " + it.Text.Split(' ')[0];
                }
                datagorevler.Rows[Convert.ToInt32(lblsatir.Text)].Cells[0].Value = lbldosya.Text;
                datagorevler.Rows[Convert.ToInt32(lblsatir.Text)].Cells[1].Value = idler;
                datagorevler.Rows[Convert.ToInt32(lblsatir.Text)].Cells[2].Value = zamanlar;
                datagorevler.Rows[Convert.ToInt32(lblsatir.Text)].Visible = true;

            }
            pangorevekle.Visible = false;
            datagorevler.Visible = true;
        }
        public bool Ipmi(string ipString)
        {
            if (String.IsNullOrWhiteSpace(ipString))
            {
                return false;
            }

            string[] splitValues = ipString.Split('.');
            if (splitValues.Length != 4)
            {
                return false;
            }

            byte tempForParsing;

            return splitValues.All(r => byte.TryParse(r, out tempForParsing));
        }
        private void button1_Click(object sender, EventArgs e)
        {
            bool kontrol = true;
            string mesaj = "";
            if (!Ipmi(txtip.Text))
            {
                mesaj = mesaj + "\n" + "IP adresi uygun değil.";
                kontrol = false;
            }
            if (txtid.Text == "")
            {
                mesaj = mesaj + "\n" + "ID numarası boş olamaz.";
                kontrol = false;
            }
            try
            {
                Convert.ToInt32(txtid.Text);
            }
            catch
            {
                mesaj = mesaj + "\n" + "ID numarası tam sayı olmalıdır.";
                kontrol = false;
            }
            try
            {
                Convert.ToDecimal(txtkonumx.Text);
            }
            catch
            {
                mesaj = mesaj + "\n" + "Konumun X koordinatı float (noktalı sayı) olmalıdır.";
                kontrol = false;
            }

            try
            {
                Convert.ToDecimal(txtkonumy.Text);
            }
            catch
            {
                mesaj = mesaj + "\n" + "Konumun Y koordinatı float (noktalı sayı) olmalıdır.";
                kontrol = false;
            }
            if (txtaciklama.Text == "")
            {
                mesaj = mesaj + "\n" + "Açıklama boş olamaz.";
                kontrol = false;
            }
            if (!kontrol)
            {
                MessageBox.Show("Aşağıdaki bilgileri düzeltip tekrar ekle butonunu tıklayınız.\n" + mesaj);
                return;
            }

            cmd = new MySqlCommand();
            con.Open();
            cmd.Connection = con;
            cmd.CommandText = "select id from cihazlar where id = '" + txtid.Text + "'";
            dr = cmd.ExecuteReader();

            if (dr.Read())
            {
                con.Close();
                DialogResult dialogResult = MessageBox.Show("Bu ID kullanımda. Güncellemek için Evet'i, değiştirmek için Hayır'ı tıklayın", "Dikkat", MessageBoxButtons.YesNo);
                if (dialogResult == DialogResult.Yes)
                {
                    con.Open();
                    cmd.Connection = con;
                    tr = con.BeginTransaction();
                    cmd.Transaction = tr;
                    cmd.CommandText = String.Format("update cihazlar set aciklama='{0}', konumx={1}, konumy= {2},ip='{3}' where id='{4}'", txtaciklama.Text,Convert.ToDecimal(txtkonumx.Text), Convert.ToDecimal(txtkonumy.Text), txtip.Text, txtid.Text);
                    cmd.ExecuteNonQuery();
                    tr.Commit();
                    con.Close();
                    listiddoldur();
                    txtid.Text = "";
                    txtip.Text = "";
                    txtaciklama.Text = "";
                    txtkonumy.Text = "";
                    txtkonumx.Text = "";
                    MessageBox.Show("Cihaz Bilgileri Güncellendi.");


                }
                else
                {
                    con.Close();
                    return;
                }
            }
            else
            {
                dr.Close();
                cmd.Connection = con;
                tr = con.BeginTransaction();
                cmd.Transaction = tr;
                cmd.CommandText = String.Format("INSERT INTO `cihazlar` (`sira`, `id`, `aciklama`,`konumx`,`konumy`, `ip`) VALUES (NULL, '{0}','{1}', {2}, {3},'{4}')", txtid.Text, txtaciklama.Text,Convert.ToDecimal(txtkonumx.Text),Convert.ToDecimal(txtkonumy.Text), txtip.Text);
                cmd.ExecuteNonQuery();
                tr.Commit();
                con.Close();
                listiddoldur();
                txtid.Text = "";
                txtip.Text = "";
                txtaciklama.Text = "";
                txtkonumy.Text = "";
                txtkonumx.Text = "";
                MessageBox.Show("Yeni Cihaz Eklendi.");

            }
        }

        private void cihazlar_ItemSelectionChanged(object sender, ListViewItemSelectionChangedEventArgs e)
        {
            if (cihazlar.SelectedItems.Count == 0)
                return;
            cmd = new MySqlCommand();
            con.Open();
            cmd.Connection = con;
            cmd.CommandText = "select id,aciklama,konumx,konumy,ip from cihazlar where id = '" + cihazlar.SelectedItems[0].Text + "'";
            dr = cmd.ExecuteReader();

            if (dr.Read())
            {
                txtid.Text = dr.GetString("id");
                txtip.Text = dr.GetString("ip");
                txtaciklama.Text = dr.GetString("aciklama");
                txtkonumy.Text = dr.GetString("konumx");
                txtkonumx.Text = dr.GetString("konumy");
            }
            con.Close();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            DialogResult dialogResult = MessageBox.Show("Bu cihazı silmek istediğinize emin misiniz?", "Dikkat", MessageBoxButtons.YesNo);
            if (dialogResult == DialogResult.Yes)
            {
                dr.Close();
                con.Open();
                cmd.Connection = con;
                tr = con.BeginTransaction();
                cmd.Transaction = tr;
                cmd.CommandText = String.Format("delete from `cihazlar` where id ='{0}'", txtid.Text);
                cmd.ExecuteNonQuery();
                tr.Commit();
                con.Close();
                listiddoldur();
                txtid.Text = "";
                txtip.Text = "";
                txtaciklama.Text = "";
                txtkonumy.Text = "";
                txtkonumx.Text = "";
                MessageBox.Show("Cihaz Silindi.");
            }
        }

        private void cmbgrup_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cmbgrup.SelectedIndex == 0)
                return;
            txtgrupekle.Text = cmbgrup.Text;
            cmd = new MySqlCommand();
            con.Open();
            cmd.Connection = con;
            cmd.CommandText = "select * from gruplar where grup='" + cmbgrup.SelectedItem.ToString() + "'";
            dr = cmd.ExecuteReader();
            dr.Read();
            string text = dr.GetString("elemanlar");
            text = text.Replace(",", string.Empty);
            text = text.Replace("[", string.Empty);
            text = text.Replace("]", string.Empty);
            text = text.Replace("'", string.Empty);
            string[] gruplar = text.Split(' ');
            foreach (ListViewItem eleman in listgrupekle.Items)
            {
                string[] aranacak = eleman.Text.Split(' ');
                if (gruplar.Any(aranacak[0].Equals))
                    eleman.Checked = true;
                else
                    eleman.Checked = false;
            }


            con.Close();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            DialogResult dialogResult = MessageBox.Show("Bu grubu silmek istediğinize emin misiniz?", "Dikkat", MessageBoxButtons.YesNo);
            if (dialogResult == DialogResult.Yes)
            {
                dr.Close();
                con.Open();
                cmd.Connection = con;
                tr = con.BeginTransaction();
                cmd.Transaction = tr;
                cmd.CommandText = String.Format("delete from `gruplar` where grup ='{0}'", cmbgrup.Text);
                cmd.ExecuteNonQuery();
                tr.Commit();
                con.Close();
                grupcombodoldur();
                MessageBox.Show("Grup Silindi.");
            }
        }

        private void butgrupkaydet_Click(object sender, EventArgs e)
        {
            if (txtgrupekle.Text == "")
            {
                MessageBox.Show("Grup ismi boş bırakılamaz");
                return;
            }

            cmd = new MySqlCommand();
            con.Open();
            cmd.Connection = con;
            cmd.CommandText = "select grup from gruplar where grup = '" + txtgrupekle.Text + "'";
            dr = cmd.ExecuteReader();

            if (dr.Read())
            {

                DialogResult dialogResult = MessageBox.Show("Bu Grup Adı kullanımda. Güncellemek için Evet'i, değiştirmek için Hayır'ı tıklayın", "Dikkat", MessageBoxButtons.YesNo);
                if (dialogResult == DialogResult.Yes)
                {
                    cmd.Connection = con;
                    dr.Close();
                    tr = con.BeginTransaction();
                    cmd.Transaction = tr;
                    string eklenecek = "";
                    foreach (ListViewItem eleman in listgrupekle.Items)
                    {
                        if (eleman.Checked == true)
                        {
                            eklenecek = eklenecek + " " + eleman.Text;
                        }
                    }
                    cmd.CommandText = String.Format("update gruplar set elemanlar='{0}' where grup='{1}'", eklenecek, cmbgrup.Text);
                    cmd.ExecuteNonQuery();
                    tr.Commit();
                    con.Close();
                    grupcombodoldur();
                    MessageBox.Show("Grup Bilgileri Güncellendi.");


                }
                else
                {
                    con.Close();
                    return;
                }
            }
            else
            {
                dr.Close();
                cmd.Connection = con;
                tr = con.BeginTransaction();
                cmd.Transaction = tr;
                string eklenecek = "";
                foreach (ListViewItem eleman in listgrupekle.Items)
                {
                    if (eleman.Checked == true)
                    {
                        eklenecek = eklenecek + " " + eleman.Text;
                    }
                }
                cmd.CommandText = String.Format("INSERT INTO `gruplar` (`sira`, `grup`, `elemanlar`) VALUES (NULL, '{0}','{1}')", txtgrupekle.Text, eklenecek);
                cmd.ExecuteNonQuery();
                tr.Commit();
                con.Close();
                grupcombodoldur();
                MessageBox.Show("Yeni Grup Eklendi.");

            }
        }

        private void btnkaydetkaydet_Click(object sender, EventArgs e)
        {
            if (txtgorev.Text == "")
            {
                MessageBox.Show("Görev ismi boş bırakılamaz");
                return;
            }

            cmd = new MySqlCommand();
            con.Open();
            cmd.Connection = con;
            cmd.CommandText = "select gorev from reklamlar where gorev = '" + txtgorev.Text + "'";
            dr = cmd.ExecuteReader();

            if (dr.Read())
            {

                DialogResult dialogResult = MessageBox.Show("Bu Grup Adı kullanımda. Güncellemek için Evet'i, değiştirmek için Hayır'ı tıklayın", "Dikkat", MessageBoxButtons.YesNo);
                if (dialogResult == DialogResult.Yes)
                {
                    dr.Close();
                    cmd.Connection = con;
                    tr = con.BeginTransaction();
                    cmd.Transaction = tr;
                    cmd.CommandText = String.Format("delete from `reklamlar` where gorev='{0}'", txtgorev.Text);
                    cmd.ExecuteNonQuery();
                    tr.Commit();
                    con.Close();

                    foreach (DataGridViewRow satir in datagorevler.Rows)
                    {
                        if (satir.Index != 0)
                            dataekle(txtgorev.Text, satir.Cells[0].Value.ToString(), satir.Cells[1].Value.ToString(), satir.Cells[2].Value.ToString(), 0);
                    }
                    MessageBox.Show("Görev kaydedildi.");
                    pankaydet.Visible = false;
                    datagorevler.Visible = true;
                }
                else
                {
                    con.Close();
                    return;
                }
            }
            else
            {
                foreach (DataGridViewRow satir in datagorevler.Rows)
                {
                    if (satir.Index != 0)
                    {
                        dataekle(txtgorev.Text, satir.Cells[0].Value.ToString(), satir.Cells[1].Value.ToString(), satir.Cells[2].Value.ToString(), 0);
                    }
                }
                MessageBox.Show("Görev kaydedildi.");
                pankaydet.Visible = false;
                datagorevler.Visible = true;

            }




        }
        private void dataekle(string gorev, string dosya, string idler, string zamanlar, int durum)
        {
            MessageBox.Show(dosya);
            dr.Close();
            var temp = con.State.ToString();
            if (con.State != ConnectionState.Open && temp != "Open")
                con.Open();

            cmd.Connection = con;
            tr = con.BeginTransaction();
            cmd.Transaction = tr;
            cmd.CommandText = String.Format("INSERT INTO `reklamlar` (`sira`, `gorev`,`dosya`,`dosyaserver`,`idler`, `zamanlar`, `zaman`,`durum`) VALUES (NULL, '{0}','{1}', '{2}','{3}','{4}',CURRENT_TIMESTAMP,'{5}')", gorev, MySql.Data.MySqlClient.MySqlHelper.EscapeString(dosya), Path.GetFileName(dosya), idler, zamanlar, durum);
            cmd.ExecuteNonQuery();
            tr.Commit();
            con.Close();
        }

        private void txtyol_TextChanged(object sender, EventArgs e)
        {

        }

        private void dynkaydetayar_Click(object sender, EventArgs e)
        {
            cmd.Connection = con;
            con.Open();
            tr = con.BeginTransaction();
            cmd.Transaction = tr;
            cmd.CommandText = String.Format("update ayarlar set ftpsunucu='{0}', ftpuser='{1}', ftppass= '{2}', ftpdizin='{3}'", txtsunucu.Text, txtkullanici.Text, txtparola.Text, txtyol.Text);
            cmd.ExecuteNonQuery();
            tr.Commit();
            con.Close();

            MessageBox.Show("Ayarlar Güncellendi.");
        }
        private void Upload(string file, string yol, string klasorserver = "")
        {
            file = duz(file);
            FtpWebRequest request =
                (FtpWebRequest)WebRequest.Create("ftp://213.238.178.192/files/yukle/" + klasorserver + file);
            request.Credentials = new NetworkCredential("yunus", "Elifesma123");
            request.Method = WebRequestMethods.Ftp.UploadFile;
            statusStrip1.Invoke(
                          (MethodInvoker)delegate { toolStripProgressBar1.Visible = true; });
            using (Stream fileStream = File.OpenRead(yol))
            using (Stream ftpStream = request.GetRequestStream())
               
            {               
                statusStrip1.Invoke(
                        (MethodInvoker)delegate { toolStripProgressBar1.Maximum = (int)fileStream.Length; });
                byte[] buffer = new byte[10240];
                int read;
                while ((read = fileStream.Read(buffer, 0, buffer.Length)) > 0)
                {
                    ftpStream.Write(buffer, 0, read);
                    statusStrip1.Invoke(
                        (MethodInvoker)delegate { toolStripProgressBar1.Value = (int)fileStream.Position; });
                    
                }
                
            }
            statusStrip1.Invoke(
                          (MethodInvoker)delegate { toolStripProgressBar1.Visible = false; });
        }
        private string duz(string gelen)
        {
            gelen = gelen.Replace("ı", "i");
            gelen = gelen.Replace("İ", "I");
            gelen = gelen.Replace("Ğ", "G");
            gelen = gelen.Replace("ğ", "g");
            gelen = gelen.Replace("Ü", "U");
            gelen = gelen.Replace("ü", "u");
            gelen = gelen.Replace("Ş", "S");
            gelen = gelen.Replace("ş", "s");
            gelen = gelen.Replace("Ö", "O");
            gelen = gelen.Replace("ö", "o");
            gelen = gelen.Replace("Ç", "C");
            gelen = gelen.Replace("ç", "c");
            return gelen;
        }
        private void btnsabit_Click(object sender, EventArgs e)
        {
            OpenFileDialog file = new OpenFileDialog();
            file.InitialDirectory = "C:\\";
            file.Filter = "MP4 Dosyası |*.mp4";
            if (file.ShowDialog() == DialogResult.OK)

            {
                Task.Run(() => Upload(file.SafeFileName, file.FileName, "/sabit/"));
            }
            cmd.Connection = con;
            con.Open();
            tr = con.BeginTransaction();
            cmd.Transaction = tr;
            cmd.CommandText = String.Format("update ayarlar set sabitdosya='{0}'", duz(file.SafeFileName));
            cmd.ExecuteNonQuery();
            tr.Commit();
            con.Close();
        }

        private void toolStripButton8_Click(object sender, EventArgs e)
        {
            datagorevler.Visible = true;
            if (datagorevler.RowCount < 2)
            {
                MessageBox.Show("En az bir görev eklemelisiniz.");
                return;
            }
            DateTime bugun = DateTime.Now;
            string simdi = bugun.ToString();
            var dosyala = new List<string>();
            var dosyalar = new List<string>();
            foreach (DataGridViewRow row in datagorevler.Rows)
            {
                if (row.Index == 0)
                    continue;
                if (File.Exists(row.Cells[0].Value.ToString()))
                {
                    dosyalar.Add(row.Cells[0].Value.ToString());
                    dr.Close();
                    con.Open();
                    cmd.Connection = con;
                    tr = con.BeginTransaction();
                    cmd.Transaction = tr;
                    cmd.CommandText = String.Format("INSERT INTO `reklamlar` (`sira`, `gorev`,`dosya`,`dosyaserver`,`idler`, `zamanlar`, `zaman`,`durum`) VALUES (NULL, '{0}','{1}', '{2}','{3}','{4}',CURRENT_TIMESTAMP,'{5}')", simdi, MySql.Data.MySqlClient.MySqlHelper.EscapeString(row.Cells[0].Value.ToString()), Path.GetFileName(row.Cells[0].Value.ToString()), row.Cells[1].Value.ToString(), row.Cells[2].Value.ToString(), 1);
                    cmd.ExecuteNonQuery();
                    tr.Commit();
                    con.Close();

                }
                else
                {
                    MessageBox.Show(row.Cells[0].Value.ToString() + "\ndosyası bulunamadı. Bu dosya yüklenmeden devam edilecek.");
                }
            }

            var inecek = new List<string[]>();
            foreach (string value in dosyalar)
            {

                //Task.Run(() => Upload(duz(Path.GetFileName(value)), value, "/video/"));
                //Upload(duz(Path.GetFileName(value)), value, "/video/");
                string[] ek = new string[] { duz(Path.GetFileName(value)), value, "/video/" };
                inecek.Add(ek);               

            }

            dr.Close();
            con.Open();
            cmd.Connection = con;
            tr = con.BeginTransaction();
            cmd.Transaction = tr;
            cmd.CommandText = String.Format("update ayarlar set oynayan_gorev='{0}'", simdi);
            cmd.ExecuteNonQuery();
            tr.Commit();
            con.Close();
            Form2 formMedici = new Form2(inecek);
            formMedici.StartPosition = FormStartPosition.CenterParent;
            formMedici.ShowDialog(this);
        }

        private void statusStrip1_ItemClicked(object sender, ToolStripItemClickedEventArgs e)
        {

        }
        private void cihazdoldur(string id)
        {
            cmd = new MySqlCommand();
            con.Open();
            cmd.Connection = con;
            cmd.CommandText = "select * from ayarlar";
            dr = cmd.ExecuteReader();
            dr.Read();
            string oynayangorev = dr.GetString("oynayan_gorev");
            dr.Close();
            cmd.CommandText = "select * from reklamlar where gorev='" + oynayangorev + "'";
            dr = cmd.ExecuteReader();
            IDictionary<string, string> gorev = new Dictionary<string, string>();
            while (dr.Read())
            {
                string[] ids = dr.GetString("idler").Split(' ');
                if (ids.Contains(id))
                {
                    if(gorev.ContainsKey(dr.GetString("dosyaserver")))
                    {
                        gorev[dr.GetString("dosyaserver")] = gorev[dr.GetString("dosyaserver")] + " " + dr.GetString("zamanlar");
                    }
                    else
                    gorev.Add(dr.GetString("dosyaserver"), dr.GetString("zamanlar"));
                }
                
            }
            con.Close();

            foreach (KeyValuePair<string, string> item in gorev)
            {
                string[] zaman = item.Value.Split(' ');
                
                string j;
                for (int i = 0; i < 24; i++)
                {
                    if (Convert.ToString(i).Length == 1)
                        j = "0" + Convert.ToString(i);
                    else
                    {
                        j = Convert.ToString(i);

                    }
                    if(zaman.Contains(j + ":00-" + j + ":59"))
                    {
                        
                        listcihazgorevi.Items[i].SubItems[1].Text = listcihazgorevi.Items[i].SubItems[1].Text + "  " + item.Key;
                        
                    }
                    

                }
                
            }
            string[] nokta = listcihazlar.Items[0].SubItems[2].Text.Split(' ');
            gMapControl1.MapProvider = GMap.NET.MapProviders.GMapProviders.OpenStreetMap;
            gMapControl1.Position = new GMap.NET.PointLatLng(Convert.ToDouble(nokta[0]), Convert.ToDouble(nokta[1]));
            gMapControl1.MinZoom = 0;
            gMapControl1.MaxZoom = 24;
            gMapControl1.Zoom = 9;



        }
        private void anapencere_Shown(object sender, EventArgs e)
        {
            datagorevler.Visible = true;
            pancihazekle.Visible = false;
            pangorevekle.Visible = false;
            pangrupekle.Visible = false;
            pankaydet.Visible = false;
            pangorevleriac.Visible = false;
            panayarlar.Visible = false;
            pancihazlar.Visible = false;
            pancihazgoster.Visible = false;
            
            Task.Run(() =>
            {
                
                    
                    BeginInvoke(new Action(() =>
                    {
                    foreach (ListViewItem item in listcihazlar.Items)
                    {
                        ipkontrol(item.SubItems[3].Text, item.Index);
                            Application.DoEvents()
    ;               }
                    }));
                
                
            });

            cihazdoldur(listcihazlar.Items[0].Text);
            listcihazlar.Items[0].Selected = true;
        }

        private void listcihazlar_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (listcihazlar.SelectedIndices.Count < 1)
                return;
            foreach (ListViewItem item in listcihazgorevi.Items)
            {
                item.SubItems[1].Text = "";
            }
            
            cihazdoldur(listcihazlar.Items[listcihazlar.SelectedIndices[0]].Text);
            string[] nokta = listcihazlar.Items[listcihazlar.SelectedIndices[0]].SubItems[2].Text.Split(' ');
            gMapControl1.MapProvider = GMap.NET.MapProviders.GMapProviders.OpenStreetMap;
            gMapControl1.Position = new GMap.NET.PointLatLng(Convert.ToDouble(nokta[0]), Convert.ToDouble(nokta[1]));
            gMapControl1.MinZoom = 0;
            gMapControl1.MaxZoom = 24;
            gMapControl1.Zoom = 12;
        }

        private void button4_Click(object sender, EventArgs e)
        {
            DialogResult dialogResult = MessageBox.Show("Cihaz yeniden başlatılacak, emin misiniz?", "Dikkat", MessageBoxButtons.YesNo);
            if (dialogResult == DialogResult.No)
                return;

            Ping pinger = null;
            pinger = new Ping();
            PingReply reply = pinger.Send(listcihazlar.Items[listcihazlar.SelectedIndices[0]].SubItems[3].Text, 10);
            if (reply.Status == IPStatus.Success)
            {



                SshClient sshclient = new SshClient(listcihazlar.Items[listcihazlar.SelectedIndices[0]].SubItems[3].Text, "pi", "1");
                sshclient.Connect();
                SshCommand sc = sshclient.CreateCommand("sudo shutdown -r now");
                try
                {
                    sc.Execute();
                }
                catch
                {
                }
            }
            else
                MessageBox.Show("Belirtilen cihaza uzaktan bağlantı yok.");

        }

        private void toolStripButton7_Click(object sender, EventArgs e)
        {
            pancihazekle.Visible = false;
            pangorevleriac.Visible = false;
            pangorevekle.Visible = false;
            pangrupekle.Visible = false;
            pankaydet.Visible = false;
            panayarlar.Visible = false;
            pancihazlar.Visible = false;
            datagorevler.Visible = true;
            pancihazgoster.Visible = false;
        }
    }
}

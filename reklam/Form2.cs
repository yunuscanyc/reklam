using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace reklam
{
    public partial class Form2 : Form
    {
        List<string[]> inecek = new List<string[]>();
        public int cou = 0;
        public Form2(List<string[]> inecek)
        {
            InitializeComponent();
            this.inecek = inecek;
        }

        private void Form2_Load(object sender, EventArgs e)
        {
           
            progrestop.Maximum = inecek.Count;
            label1.Text = ("0/" + progrestop.Maximum.ToString());
            
        }
        private void Upload(string file, string yol, string klasorserver)
        {

            
            int x = 4;
            int y = 10+cou * 20 ;
            cou++;
            Label lab = new Label();

            lab.Visible = true;
            lab.Location = new Point(x, y);
            lab.Height = 20;
            lab.Width = 190;
            lab.Text = file;
            lab.Show();
            lab.Name = "lb" + panel1.Controls.Count;

            panel1.Invoke(
                        (MethodInvoker)delegate { panel1.Controls.Add(lab); });
            ProgressBar bar = new ProgressBar();
            
            bar.Visible = true;
            bar.Location = new Point(x+200, y);
            bar.Height = 20;
            bar.Width = 200;            
            bar.Show();
            bar.Name = "rb" + panel1.Controls.Count;
 
            panel1.Invoke(
                        (MethodInvoker)delegate { panel1.Controls.Add(bar); });
            
 
            FtpWebRequest request =
                (FtpWebRequest)WebRequest.Create("ftp://213.238.178.192/files/yukle/" + klasorserver + file);
            request.Credentials = new NetworkCredential("yunus", "Elifesma123");
            request.Method = WebRequestMethods.Ftp.UploadFile;
            
            using (Stream fileStream = File.OpenRead(yol))
            using (Stream ftpStream = request.GetRequestStream())

            {
                bar.Invoke(
                        (MethodInvoker)delegate { bar.Maximum = (int)fileStream.Length; });
                byte[] buffer = new byte[10240];
                int read;
                while ((read = fileStream.Read(buffer, 0, buffer.Length)) > 0)
                {
                    ftpStream.Write(buffer, 0, read);
                    bar.Invoke(
                         (MethodInvoker)delegate { bar.Value = (int)fileStream.Position; });
                }
                Application.DoEvents();
            }
            progrestop.Invoke(
        (MethodInvoker)delegate { progrestop.Value += 1; });
            label1.Invoke(
        (MethodInvoker)delegate { label1.Text = (progrestop.Value.ToString() + "/" + progrestop.Maximum.ToString()); });
            if (progrestop.Value==progrestop.Maximum)
                button1.Invoke((MethodInvoker)delegate { button1.Enabled = true;  });
            
        }
        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void Form2_Shown(object sender, EventArgs e)
        {

            foreach (string[] st in inecek)
            {
                Task.Run(() => Upload(st[0],st[1],st[2]));

            }
            
        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}

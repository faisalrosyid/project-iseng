from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView

import sqlite3


# =========================================
# DATABASE
# =========================================
conn = sqlite3.connect("inventaris.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    stok TEXT,
    harga TEXT
)
""")

conn.commit()


# =========================================
# APP
# =========================================
class InventarisApp(MDApp):

    def build(self):

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"

        self.screen = MDScreen()

        # =================================
        # LAYOUT UTAMA
        # =================================
        self.layout = MDBoxLayout(
            orientation="vertical",
            padding=15,
            spacing=15
        )

        # =================================
        # TITLE
        # =================================
        title = MDLabel(
            text="Inventaris Produk Pangan",
            halign="center",
            font_style="H4"
        )

        self.layout.add_widget(title)

        # =================================
        # INPUT
        # =================================
        self.input_nama = MDTextField(
            hint_text="Nama Produk"
        )

        self.layout.add_widget(self.input_nama)

        self.input_stok = MDTextField(
            hint_text="Jumlah Stok"
        )

        self.layout.add_widget(self.input_stok)

        self.input_harga = MDTextField(
            hint_text="Harga Produk"
        )

        self.layout.add_widget(self.input_harga)

        # =================================
        # BUTTON TAMBAH
        # =================================
        btn_tambah = MDRaisedButton(
            text="Tambah Produk",
            pos_hint={"center_x": 0.5}
        )

        btn_tambah.bind(on_release=self.tambah_produk)

        self.layout.add_widget(btn_tambah)

        # =================================
        # SCROLL
        # =================================
        scroll = MDScrollView()

        self.list_produk = MDBoxLayout(
            orientation="vertical",
            spacing=10,
            adaptive_height=True
        )

        scroll.add_widget(self.list_produk)

        self.layout.add_widget(scroll)

        self.screen.add_widget(self.layout)

        self.tampilkan_produk()

        return self.screen


    # =====================================
    # TAMBAH PRODUK
    # =====================================
    def tambah_produk(self, instance):

        nama = self.input_nama.text
        stok = self.input_stok.text
        harga = self.input_harga.text

        if nama == "" or stok == "" or harga == "":
            return

        cursor.execute("""
        INSERT INTO produk (nama, stok, harga)
        VALUES (?, ?, ?)
        """, (nama, stok, harga))

        conn.commit()

        self.input_nama.text = ""
        self.input_stok.text = ""
        self.input_harga.text = ""

        self.tampilkan_produk()


    # =====================================
    # TAMPILKAN PRODUK
    # =====================================
    def tampilkan_produk(self):

        self.list_produk.clear_widgets()

        cursor.execute("SELECT * FROM produk")

        data = cursor.fetchall()

        for produk in data:

            card = MDCard(
                orientation="vertical",
                padding=15,
                size_hint=(1, None),
                height=180,
                radius=[20]
            )

            nama = MDLabel(
                text=f"Nama : {produk[1]}",
                theme_text_color="Primary"
            )

            stok = MDLabel(
                text=f"Stok : {produk[2]}"
            )

            harga = MDLabel(
                text=f"Harga : Rp {produk[3]}"
            )

            btn_hapus = MDRaisedButton(
                text="Hapus",
                pos_hint={"center_x": 0.5}
            )

            btn_hapus.bind(
                on_release=lambda x,
                id=produk[0]: self.hapus_produk(id)
            )

            card.add_widget(nama)
            card.add_widget(stok)
            card.add_widget(harga)
            card.add_widget(btn_hapus)

            self.list_produk.add_widget(card)


    # =====================================
    # HAPUS PRODUK
    # =====================================
    def hapus_produk(self, id):

        cursor.execute(
            "DELETE FROM produk WHERE id=?",
            (id,)
        )

        conn.commit()

        self.tampilkan_produk()


# =========================================
# RUN
# =========================================
InventarisApp().run()
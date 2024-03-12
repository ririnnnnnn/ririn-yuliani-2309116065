import os
os.system('cls')

from prettytable import PrettyTable

class ProdukRoti:
    counter = 1

    def __init__(self, nama, harga, stok, id_roti=None):
        self.id = id_roti if id_roti is not None else ProdukRoti.counter
        ProdukRoti.counter += 1
        self.nama = nama
        self.harga = harga
        self.stok = stok

    def __str__(self):
        return f"ID: {self.id} - {self.nama} - Rp{self.harga} - Stok: {self.stok}"

class Node:
    def __init__(self, roti):
        self.roti = roti
        self.next = None

class DaftarRoti:
    def __init__(self):
        self.head = None

    def tambah_roti(self, roti, posisi=None):
        node_baru = Node(roti)

        if posisi == "awal":
            node_baru.next = self.head
            self.head = node_baru
        elif posisi == "akhir":
            if not self.head:
                self.head = node_baru
            else:
                current = self.head
                while current.next:
                    current = current.next
                current.next = node_baru
        elif posisi == "antara":
            if not self.head or not self.head.next:
                print("Minimal dua node untuk menambah di antara.")
                return

            nama_sebelum = input("Masukkan nama roti sebelum posisi baru: ")
            current = self.head
            while current.next and current.next.roti.nama != nama_sebelum:
                current = current.next

            if current.next:
                node_baru.next = current.next
                current.next = node_baru
            else:
                print(f"Roti dengan nama {nama_sebelum} tidak ditemukan.")
        else:
            print("Posisi tidak valid.")

    def hapus_roti(self, posisi=None, nama=None):
        if not self.head:
            print("Linked list kosong. Tidak ada yang dapat dihapus.")
            return False

        if posisi == "awal":
            self.head = self.head.next
            return True
        elif posisi == "akhir":
            if not self.head.next:
                self.head = None
                return True
            current = self.head
            while current.next.next:
                current = current.next
            current.next = None
            return True
        elif posisi == "antara":
            if not self.head or not self.head.next:
                print("Minimal dua node untuk menghapus di antara.")
                return False

            if not nama:
                print("Nama roti tidak boleh kosong.")
                return False

            nama_sebelum = input("Masukkan nama roti sebelum posisi yang ingin dihapus: ")
            if self.head.roti.nama == nama_sebelum:
                self.head = self.head.next
                return True

            current = self.head
            while current.next and current.next.roti.nama != nama_sebelum:
                current = current.next

            if current.next:
                current.next = current.next.next
                return True
            else:
                print(f"Roti dengan nama {nama_sebelum} tidak ditemukan.")
                return False
        else:
            print("Posisi tidak valid.")
            return False

    def tampilkan_roti(self):
        table = PrettyTable(["No", "Nama", "Harga", "Stok"])
        current = self.head
        no = 1
        while current:
            table.add_row([no, current.roti.nama, current.roti.harga, current.roti.stok])
            current = current.next
            no += 1
        print(table)

    def ubah_roti(self, nama, harga_baru, stok_baru):
        current = self.head
        while current:
            if current.roti.nama == nama:
                current.roti.harga = harga_baru
                current.roti.stok = stok_baru
                return True
            current = current.next
        return False

    def sort_roti(self, key="nama", ascending=True):
        if key not in ["nama", "harga", "stok", "id"]:
            print("Kunci pengurutan tidak valid.")
            return

        if not self.head or not self.head.next:
            return

        # Gunakan salah satu Quick Sort atau Merge Sort
        if input("Gunakan Quick Sort? (y/n): ").lower() == 'y':
            self.quick_sort(key=key, ascending=ascending)
        else:
            self.merge_sort(key=key, ascending=ascending)

    def merge_sort(self, key="harga", ascending=True):
        # Implementasi Merge Sort
        if not self.head or not self.head.next:
            return

        def merge_sort_recursive(lst):
            if not lst or not lst.next:
                return lst

            slow, fast = lst, lst.next
            while fast and fast.next:
                slow, fast = slow.next, fast.next.next

            left, right = lst, slow.next
            slow.next = None

            left = merge_sort_recursive(left)
            right = merge_sort_recursive(right)

            return merge(left, right)

        def merge(left, right):
            result = DaftarRoti()
            current_result = result.head

            while left and right:
                if (getattr(left.roti, key) < getattr(right.roti, key)) if ascending else (
                        getattr(left.roti, key) > getattr(right.roti, key)):
                    if not current_result:
                        result.head = Node(left.roti)
                        current_result = result.head
                    else:
                        current_result.next = Node(left.roti)
                        current_result = current_result.next
                    left = left.next
                else:
                    if not current_result:
                        result.head = Node(right.roti)
                        current_result = result.head
                    else:
                        current_result.next = Node(right.roti)
                        current_result = current_result.next
                    right = right.next

            while left:
                current_result.next = Node(left.roti)
                current_result = current_result.next
                left = left.next

            while right:
                current_result.next = Node(right.roti)
                current_result = current_result.next
                right = right.next

            return result.head

        self.head = merge_sort_recursive(self.head)

    def quick_sort(self, key="nama", ascending=True):
        # Implementasi Quick Sort
        def partition(start, end):
            pivot_index = start
            pivot = getattr(self.head.roti, key)

            while start < end:
                while start < len(self) and (
                        (getattr(self[start].roti, key) <= pivot) if ascending else
                        (getattr(self[start].roti, key) >= pivot)):
                    start += 1

                while (getattr(self[end].roti, key) > pivot) if ascending else (
                        getattr(self[end].roti, key) < pivot):
                    end -= 1

                if start < end:
                    self[start].roti, self[end].roti = self[end].roti, self[start].roti

            self[pivot_index].roti, self[end].roti = self[end].roti, self[pivot_index].roti
            return end

        def quick_sort_recursive(start, end):
            if start < end:
                pivot = partition(start, end)
                quick_sort_recursive(start, pivot - 1)
                quick_sort_recursive(pivot + 1, end)

        quick_sort_recursive(0, len(self) - 1)

    def sort_by_id(self, ascending=True):
        self.merge_sort(key="id", ascending=ascending)

    def __getitem__(self, index):
        current = self.head
        for _ in range(index):
            if current:
                current = current.next
            else:
                raise IndexError("Index out of range.")
        if current:
            return current

    def __len__(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        result = ""
        current = self.head
        while current:
            result += str(current.roti) + "\n"
            current = current.next
        return result

# Fungsi untuk menampilkan menu
def print_menu():
    print("--------------------------------------------------")
    print ("Hai! Selamat Datang")
    print ("Silahkan memilih menu operassi yang tersedia: ")
    print("1. Tambahkan Roti")
    print("2. Tampilkan Roti")
    print("3. Mengubah Roti")
    print("4. Menghapus Roti")
    print("5. Urutkan Roti")
    print("6. Keluar")
    print("--------------------------------------------------")


# Contoh penggunaan
daftar_roti = DaftarRoti()

while True:
    print_menu()

    pilihan = input("Pilih menu (1-6): ")

    if pilihan == '1':
        id_roti = int(input("Masukkan ID roti: "))
        nama = input("Masukkan nama roti: ")
        harga = float(input("Masukkan harga roti: "))
        stok = int(input("Masukkan stok roti: "))
        daftar_roti.tambah_roti(ProdukRoti(nama, harga, stok, id_roti), posisi="akhir")
        print(f"Roti dengan ID {id_roti} berhasil ditambahkan.")
    elif pilihan == '2':
        daftar_roti.tampilkan_roti()
    elif pilihan == '3':
        nama_roti = input("Masukkan nama roti yang ingin diubah: ")
        harga_baru = float(input("Masukkan harga baru roti: "))
        stok_baru = int(input("Masukkan stok baru roti: "))
        if daftar_roti.ubah_roti(nama_roti, harga_baru, stok_baru):
            print("Roti berhasil diubah.")
        else:
            print(f"Roti dengan nama {nama_roti} tidak ditemukan.")
    elif pilihan == '4':
        # Tampilkan opsi untuk menentukan posisi penghapusan
        print("Pilih posisi penghapusan:")
        print("1. Di Awal")
        print("2. Di Akhir")
        print("3. Di Antara")
        posisi_pilihan_hapus = input("Pilih posisi (1-3): ")

        if posisi_pilihan_hapus == '1':
            if daftar_roti.hapus_roti(posisi="awal"):
                print("Roti di awal berhasil dihapus.")
            else:
                print("Roti di awal tidak ditemukan atau tidak dapat dihapus.")
        elif posisi_pilihan_hapus == '2':
            if daftar_roti.hapus_roti(posisi="akhir"):
                print("Roti di akhir berhasil dihapus.")
            else:
                print("Roti di akhir tidak ditemukan atau tidak dapat dihapus.")
        elif posisi_pilihan_hapus == '3':
            nama_hapus = input("Masukkan nama roti yang ingin dihapus: ")
            if daftar_roti.hapus_roti(posisi="antara", nama=nama_hapus):
                print(f"Roti dengan nama {nama_hapus} berhasil dihapus.")
            else:
                print(f"Roti dengan nama {nama_hapus} tidak ditemukan atau tidak dapat dihapus.")
        else:
            print("Pilihan posisi tidak valid.")
            
    elif pilihan == '5':
        # Tampilkan opsi untuk menentukan urutan
        print("Pilih kriteria pengurutan:")
        print("1. Nama")
        print("2. Harga")
        print("3. Stok")
        print("4. ID")
        kriteria_pilihan = input("Pilih kriteria (1-4): ")

        ascending_pilihan = input("Pengurutan Ascending atau Descending? (a/d): ").lower()
        ascending = True if ascending_pilihan == 'a' else False

        if kriteria_pilihan == '1':
            daftar_roti.sort_roti(key="nama", ascending=ascending)
            print("Roti berhasil diurutkan berdasarkan nama.")
        elif kriteria_pilihan == '2':
            daftar_roti.sort_roti(key="harga", ascending=ascending)
            print("Roti berhasil diurutkan berdasarkan harga.")
        elif kriteria_pilihan == '3':
            daftar_roti.sort_roti(key="stok", ascending=ascending)
            print("Roti berhasil diurutkan berdasarkan stok.")
        elif kriteria_pilihan == '4':
            daftar_roti.sort_roti(key="id", ascending=ascending)
            print("Roti berhasil diurutkan berdasarkan ID.")
        else:
            print("Pilihan kriteria tidak valid.")
    elif pilihan == '6':
        print("Terima kasih. Keluar dari program.")
        break
    else:
        print("Pilihan tidak valid. Silakan pilih 1-6.")

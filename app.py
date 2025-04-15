import streamlit as st
import mysql.connector
import qrcode
from PIL import Image
from datetime import datetime
from streamlit_option_menu import option_menu
import extra_streamlit_components as stx
import os
import hashlib

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'fitnessmanagementsystem',
    'port': 3306
}

# Path untuk assets
LOGO_PATH = "image.png"
AVATAR_PATH = "avatar.png"

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Custom CSS
def load_css():
    st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        
        .navbar {
            background-color: #ffffff;
            box-shadow: 0 2px 4px rgba(0,0,0,.1);
            padding: 1rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }
        
        .card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,.1);
        }
        
        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
        }
        
        .btn-primary {
            background-color: #007bff;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            border: none;
            transition: all 0.3s ease;
        }
        
        .btn-primary:hover {
            background-color: #0056b3;
            transform: translateY(-1px);
        }
        
        .qr-container {
            text-align: center;
            margin: 2rem 0;
        }
        
        .logo {
            max-width: 200px;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authentication functions
def login_form():
    st.title("Login FitReserve")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            user = authenticate_user(email, hash_password(password))
            if user:
                st.session_state.authenticated = True
                st.session_state.current_user = user
                st.success("Login berhasil!")
                st.experimental_rerun()
            else:
                st.error("Email atau password salah")

def authenticate_user(email, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT * FROM Users WHERE Email = %s AND Password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return user
    except Exception as e:
        st.error(f"Error during authentication: {e}")
        return None

def update_profile(user_id, new_name, new_phone):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "UPDATE Users SET Nama = %s, NomorTelepon = %s WHERE UserID = %s"
        cursor.execute(query, (new_name, new_phone, user_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error updating profile: {e}")
        return False

# Navigation
def main_navigation():
    with st.sidebar:
        # Logo lokal
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_column_width=True, caption="")
        else:
            st.error("Logo tidak ditemukan!")
        
        menu = option_menu(
            menu_title=None,
            options=["Beranda", "Cari Fasilitas", "Booking Saya", "Profil"],
            icons=["house", "search", "calendar-check", "person"],
            default_index=0,
            styles={
                "container": {"padding": "0!important"},
                "nav-link": {"font-size": "16px", "margin": "5px 0"},
            }
        )
    return menu

# Page functions
def home_page():
    st.header("Selamat Datang di FitReserve 🏋️")
    
    # Hero Section
    cols = st.columns([2, 3])
    with cols[0]:
        st.image(LOGO_PATH, width=200)
    with cols[1]:
        st.write("""
        ## Temukan & Pesan Fasilitas Olahraga Terbaik!
        """)
    
    # Metrics
    cols = st.columns(3)
    with cols[0]:
        st.metric("Total Fasilitas", "25", "+3 baru")
    with cols[1]:
        st.metric("Pengguna Aktif", "1.2K", "+15%")
    with cols[2]:
        st.metric("Rating", "4.8/5", "⭐ 1.2K reviews")

def search_facilities_page():
    st.header("🔍 Cari Fasilitas")
    
    # Search filters
    with st.form("search_form"):
        cols = st.columns(3)
        with cols[0]:
            facility_type = st.selectbox("Jenis Fasilitas", ["Semua", "Lapangan", "Kolam Renang", "Gym"])
        with cols[1]:
            location = st.selectbox("Lokasi", ["Semua", "Jakarta", "Bandung", "Surabaya"])
        with cols[2]:
            date = st.date_input("Tanggal")
        
        if st.form_submit_button("Cari"):
            st.session_state.search_params = {
                "facility_type": facility_type,
                "location": location,
                "date": date
            }
    
    # Display results
    if 'search_params' in st.session_state:
        st.subheader("Hasil Pencarian")
        # Mock data - replace with actual database query
        facilities = [
            {"name": "Lapangan Basket", "type": "Lapangan", "location": "Jakarta", "available": True},
            {"name": "Kolam Renang Olimpiade", "type": "Kolam Renang", "location": "Bandung", "available": True},
            {"name": "Gym Premium", "type": "Gym", "location": "Surabaya", "available": False}
        ]
        
        for facility in facilities:
            with st.expander(f"{facility['name']} - {facility['type']}"):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.write(f"📍 Lokasi: {facility['location']}")
                    st.write(f"📅 Tanggal: {st.session_state.search_params['date']}")
                    st.write(f"🔄 Status: {'Tersedia' if facility['available'] else 'Tidak Tersedia'}")
                with cols[1]:
                    if facility['available']:
                        if st.button("Booking", key=f"book_{facility['name']}"):
                            st.success(f"Fasilitas {facility['name']} berhasil dipesan!")
                    else:
                        st.warning("Tidak Tersedia")

def my_bookings_page():
    st.header("📅 Booking Saya")
    
    if st.session_state.current_user:
        # Mock data - replace with actual database query
        bookings = [
            {"facility": "Lapangan Basket", "date": "2023-05-15", "time": "10:00 - 12:00", "status": "Confirmed"},
            {"facility": "Kolam Renang", "date": "2023-05-20", "time": "14:00 - 15:00", "status": "Pending"}
        ]
        
        if not bookings:
            st.info("Anda belum memiliki booking")
        else:
            for booking in bookings:
                with st.container():
                    cols = st.columns([3, 1])
                    with cols[0]:
                        st.subheader(booking['facility'])
                        st.write(f"📅 {booking['date']}")
                        st.write(f"⏰ {booking['time']}")
                        st.write(f"🔄 Status: {booking['status']}")
                    with cols[1]:
                        if st.button("Batalkan", key=f"cancel_{booking['facility']}"):
                            st.warning(f"Booking {booking['facility']} dibatalkan")
                        
                        # Generate QR Code
                        qr = qrcode.QRCode(version=1, box_size=10, border=5)
                        qr.add_data(f"Booking: {booking['facility']}|{booking['date']}|{booking['time']}")
                        qr.make(fit=True)
                        img = qr.make_image(fill='black', back_color='white')
                        img.save("booking_qr.png")
                        
                        st.image("booking_qr.png", width=100)

def profile_page():
    st.header("👤 Profil Pengguna")
    
    if st.session_state.current_user:
        user = st.session_state.current_user
        cols = st.columns([1,3])
        with cols[0]:
            # Avatar lokal
            if os.path.exists(AVATAR_PATH):
                st.image(AVATAR_PATH, use_column_width=True)
            else:
                st.image("https://via.placeholder.com/150", use_column_width=True)
        
        with cols[1]:
            st.write(f"### {user['Nama']}")
            st.write(f"📧 {user['Email']}")
            st.write(f"📱 {user['NomorTelepon']}")
            st.write(f"👥 Role: {user['Peran']}")
            
            with st.expander("Edit Profil"):
                with st.form("edit_profile"):
                    new_name = st.text_input("Nama", value=user['Nama'])
                    new_phone = st.text_input("Nomor Telepon", value=user['NomorTelepon'])
                    if st.form_submit_button("Simpan Perubahan"):
                        if update_profile(user['UserID'], new_name, new_phone):
                            st.session_state.current_user['Nama'] = new_name
                            st.session_state.current_user['NomorTelepon'] = new_phone
                            st.success("Profil berhasil diperbarui")

# Main App
# Halaman Depan Publik
def public_landing_page():
    st.markdown(f"""
    <div style="text-align: center;">
        <img src="https://via.placeholder.com/800x400?text=Welcome+to+FitReserve" style="width: 100%; border-radius: 15px; margin-bottom: 30px;">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 50px;">
        <h1>Selamat Datang di FitReserve 🏋️♂️</h1>
        <h3>Temukan & Pesan Fasilitas Olahraga Terbaik di Kotamu!</h3>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    with cols[0]:
        st.image("https://via.placeholder.com/300x200?text=Lapangan+Basket")
        st.markdown("**Lapangan Basket**\n\nLapangan standar internasional")
    with cols[1]:
        st.image("https://via.placeholder.com/300x200?text=Kolam+Renang")
        st.markdown("**Kolam Renang**\n\nDengan sistem penyaringan modern")
    with cols[2]:
        st.image("https://via.placeholder.com/300x200?text=Gym+Premium")
        st.markdown("**Gym Premium**\n\nPeralatan lengkap dan trainer profesional")

    st.markdown("---")
    
    login_col, reg_col, _ = st.columns([2,2,6])
    with login_col:
        if st.button("Masuk ke Akun Saya", use_container_width=True):
            st.session_state.show_login = True
            st.experimental_rerun()
    with reg_col:
        if st.button("Daftar Akun Baru", use_container_width=True):
            st.session_state.show_register = True
            st.experimental_rerun()

# Form Registrasi
def registration_form():
    st.title("Pendaftaran Akun Baru")
    
    with st.form("registration_form"):
        nama = st.text_input("Nama Lengkap")
        email = st.text_input("Alamat Email")
        no_telp = st.text_input("Nomor Telepon")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Daftar Sebagai", ["Member", "Pengelola Fasilitas"])
        
        if st.form_submit_button("Daftar"):
            if len(password) < 6:
                st.error("Password minimal 6 karakter")
            else:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    
                    # Cek email sudah terdaftar
                    cursor.execute("SELECT * FROM Users WHERE Email = %s", (email,))
                    if cursor.fetchone():
                        st.error("Email sudah terdaftar")
                    else:
                        hashed_pw = hash_password(password)
                        cursor.execute(
                            "INSERT INTO Users (Nama, Email, NomorTelepon, Password, Peran) VALUES (%s,%s,%s,%s,%s)",
                            (nama, email, no_telp, hashed_pw, role)
                        )
                        conn.commit()
                        st.success("Pendaftaran berhasil! Silakan login")
                        st.session_state.show_login = True
                        st.session_state.show_register = False
                        st.experimental_rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    cursor.close()
                    conn.close()
    
    if st.button("Kembali ke Beranda"):
        st.session_state.show_register = False
        st.experimental_rerun()

# Modifikasi Fungsi Main
def main():
    load_css()
    
    if not st.session_state.authenticated:
        if st.session_state.get('show_register'):
            registration_form()
        elif st.session_state.get('show_login'):
            login_form()
        else:
            public_landing_page()
    else:
        selected = main_navigation()
        
        # Header dengan tombol logout
        cols = st.columns([8,2])
        with cols[1]:
            if st.session_state.current_user:
                col1, col2 = st.columns([1,3])
                with col1:
                    if os.path.exists(AVATAR_PATH):
                        st.image(AVATAR_PATH, width=40)
                    else:
                        st.image("https://via.placeholder.com/40", width=40)
                with col2:
                    if st.button("Logout"):
                        st.session_state.authenticated = False
                        st.session_state.current_user = None
                        st.experimental_rerun()
        
        if selected == "Beranda":
            home_page()
        elif selected == "Cari Fasilitas":
            search_facilities_page()
        elif selected == "Booking Saya":
            my_bookings_page()
        elif selected == "Profil":
            profile_page()


if __name__ == "__main__":
    main()
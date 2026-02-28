# daluase_studio_app_v5_merged_fixed.py
# DALUASE CLOTHING STUDIO - MODERN UI VERSION + FULL FUNCTIONALITY (FIXED BUGS)

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import hashlib
import json
import os
import time
from pathlib import Path
from io import BytesIO
import re
import secrets
import string
import base64
try:
    from PIL import Image
except Exception:
    Image = None

# ===================== KONFIGURASI & CUSTOM CSS =====================
st.set_page_config(
    page_title="Daluase Studio",
    page_icon="👕",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar collapsed by default
)

# Inject Custom CSS
st.markdown("""<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    
    /* Top Navigation Bar */
    .top-nav {
        background-color: #1A1D23;
        padding: 0.5rem 0;
        border-bottom: 2px solid #D4AF37;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .nav-container {
        max-width: 100%;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .nav-tabs {
        display: flex;
        gap: 1rem;
        list-style: none;
        margin: 0;
        padding: 0;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .nav-tab {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        color: #CCCCCC;
        font-size: 0.9rem;
    }
    
    .nav-tab:hover {
        background-color: #2A2D33;
        color: white;
    }
    
    .nav-tab.active {
        background-color: #D4AF37;
        color: #1A1D23;
        font-weight: 600;
    }

    /* Mobile Responsive */
    @media (max-width: 768px) {
        .nav-tabs {
            gap: 0.25rem;
            justify-content: flex-start;
            overflow-x: auto;
            white-space: nowrap;
            padding-bottom: 5px;
        }
        
        .nav-tab {
            padding: 0.4rem 0.8rem;
            font-size: 0.85rem;
            flex-shrink: 0;
        }
        
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            padding-top: 1rem !important;
        }
        
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.2rem !important; }
        
        /* Force columns to wrap on mobile */
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 1rem;
        }
        
        /* Exception for small metric cards if needed, maybe 50% */
        .metric-card {
            padding: 0.8rem;
        }
        
        .top-logo, .logo-button-box {
            height: auto !important;
            padding: 10px 0;
            justify-content: center;
        }
        
        .top-logo img {
            max-height: 80px;
        }
    }
    
    /* Sidebar Styling */
    .sidebar-container {
        background-color: #262730;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        border: 1px solid #2E3138;
    }
    
    .sidebar-header {
        color: #D4AF37;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar Kloter Radio as boxed items */
    div[data-testid="stSidebar"] .stRadio [role="radiogroup"] {
        display: grid;
        gap: 8px;
    }
    div[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
        background-color: #1A1D23;
        border: 1px solid #2F3340;
        border-radius: 10px;
        padding: 8px 10px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
        transition: background-color .2s ease;
    }
    div[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
        background-color: #21252E;
        border-color: #3B4050;
    }
    div[data-testid="stSidebar"] .stRadio [role="radiogroup"] input:checked + div {
        background: linear-gradient(180deg, rgba(212,175,55,0.14) 0%, rgba(212,175,55,0.06) 100%);
        border: 1px solid #D4AF37;
        color: #EDE6D6;
        font-weight: 700;
    }
    
    /* Custom Buttons */
    .stButton > button {
        background-color: #D4AF37;
        color: #1A1D23;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 0.4rem 1rem;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #FFC107;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);
    }
    
    /* Custom Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background-color: #1A1D23 !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 6px !important;
    }
    
    /* Container Cards */
    .custom-card {
        background-color: #1A1D23;
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid #32363F;
        margin-bottom: 1rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #2A2D33 0%, #1A1D23 100%);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #31343C;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #D4AF37;
        margin-bottom: 0.25rem;
    }
    
    .metric-label {
        color: #CCCCCC;
        font-size: 0.8rem;
        text-transform: uppercase;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.35rem;
    }
    .status-lunas { background-color: rgba(46, 204, 113, 0.2); color: #2ecc71; border: 1px solid #2ecc71; }
    .status-panjar { background-color: rgba(243, 156, 18, 0.2); color: #f39c12; border: 1px solid #f39c12; }
    .status-pending { background-color: rgba(231, 76, 60, 0.2); color: #e74c3c; border: 1px solid #e74c3c; }
    .status-selesai { background-color: rgba(46, 204, 113, 0.2); color: #2ecc71; border: 1px solid #2ecc71; }
    .status-proses { background-color: rgba(52, 152, 219, 0.2); color: #3498db; border: 1px solid #3498db; }
    
    /* Action Buttons */
    .action-btn {
        background: #444; color: white; border: none; padding: 0.2rem 0.5rem; border-radius: 4px; cursor: pointer; font-size: 0.8rem; margin: 2px;
    }
    .action-btn:hover { opacity: 0.8; }
    .action-btn-edit { background: #3498db; }
    .action-btn-delete { background: #e74c3c; }
    .action-btn-pay { background: #2ecc71; }
</style>""", unsafe_allow_html=True)

# Path untuk data
DATA_DIR = Path("data")
ORDERS_DIR = DATA_DIR / "orders"
ARCHIVE_DIR = DATA_DIR / "archive"
INVENTORY_DIR = DATA_DIR / "inventory"
STOCK_DIR = DATA_DIR / "stock"
CASH_DIR = DATA_DIR / "cash"
USERS_FILE = DATA_DIR / "users.csv"
SETTINGS_FILE = DATA_DIR / "settings.json"
CUSTOMERS_FILE = DATA_DIR / "customers.csv"
DESIGNS_DIR = DATA_DIR / "designs"
ORIGINAL_DESIGNS_DIR = DESIGNS_DIR / "original"
ORDER_DESIGNS_DIR = DESIGNS_DIR / "orders"
PAYMENT_PROOFS_DIR = DATA_DIR / "payment_proofs"
SHIPPING_PROOFS_DIR = DATA_DIR / "shipping_proofs"
KLOTER_STATUS_FILE = DATA_DIR / "kloter_status.json"
SALES_PENDING_DIR = DATA_DIR / "sales_pending"
SALES_APPROVED_DIR = DATA_DIR / "sales_approved"
SALES_NOTIFICATIONS_DIR = DATA_DIR / "sales_notifications"
PROFIT_SHARING_HISTORY_FILE = DATA_DIR / "profit_sharing_history.csv"

# Buat direktori jika belum ada
for dir_path in [DATA_DIR, ORDERS_DIR, ARCHIVE_DIR, INVENTORY_DIR, STOCK_DIR, CASH_DIR, DESIGNS_DIR, ORIGINAL_DESIGNS_DIR, ORDER_DESIGNS_DIR, PAYMENT_PROOFS_DIR, SHIPPING_PROOFS_DIR, SALES_PENDING_DIR, SALES_APPROVED_DIR, SALES_NOTIFICATIONS_DIR]:
    dir_path.mkdir(exist_ok=True)



bg_candidates = [DATA_DIR / "background.jpg", DATA_DIR / "background.png"]
bg_path = None
for p in bg_candidates:
    if p.exists() and p.stat().st_size > 0:
        bg_path = p
        break
if bg_path:
    try:
        with open(bg_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        ext = "jpeg" if bg_path.suffix.lower() == ".jpg" else "png"
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/{ext};base64,{b64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True)
    except Exception:
        pass
    st.markdown("---")

# ===================== DAFTAR WARNA LENGKAP =====================
COMPLETE_COLORS = [
    "WHITE", "BLACK", "SPORT GRAY", "NAVY", "MAROON", "RED", "ROYAL BLUE", 
    "GREEN IRISH", "DAISY", "FOREST GREEN", "CHARCOAL", "GOLD", "DARK CHOCOLATE", 
    "MILITARY GREEN", "CAROLINA BLUE", "ORANGE", "LIGHT PINK", "SAND", "PURPLE",
    "BLACK HEATHER", "NAVY HEATHER", "RED HEATHER", "DARK GREEN HEATHER", 
    "BURGUNDY HEATHER", "AQUA SKY", "BUTTER", "GREEN ASH", "LILAC", "SALMON", 
    "MUSTARD", "LIME", "CHESTNUT", "SAPPHIRE", "HELICONIA", "BLACK CAMO", 
    "FOREST CAMO", "ARMY"
]

# Harga beli produk (sesuai rumus Excel Anda)
PRODUCT_BUY_PRICES = {
    "Premium Cotton T-shirt 7200": {
        "white_price": 47000,
        "color_price": 50000,
        "size_extra": {"2XL": 5000, "3XL": 10000, "4XL": 15000, "5XL": 20000}
    },
    "Youth T-shirt 72Y00": {
        "white_price": 37000,
        "color_price": 40000,
        "size_extra": {"2XL": 5000, "3XL": 10000, "4XL": 15000, "5XL": 20000}
    },
    "Long Sleeve 5480": {
        "white_price": 79000,
        "color_price": 84000,
        "size_extra": {"2XL": 5000, "3XL": 10000, "4XL": 15000, "5XL": 20000}
    },
    "Polo Shirt 8100": {
        "white_price": 75000,
        "color_price": 80000,
        "size_extra": {"2XL": 5000, "3XL": 10000, "4XL": 15000, "5XL": 20000}
    },
    "Hooded Sweatshirt 9500": {
        "special_colors": ["FOREST CAMO", "BLACK CAMO"],
        "special_price": 150000,
        "white_price": 140000,
        "color_price": 145000,
        "size_extra": {"2XL": 10000, "3XL": 15000, "4XL": 20000, "5XL": 25000}
    }
}

# ===================== SESSION STATE =====================
# PERSISTENT LOGIN LOGIC
if "authenticated" not in st.session_state:
    query_params = st.query_params
    if query_params.get("auth") == "1":
        st.session_state.authenticated = True
        st.session_state.username = query_params.get("user")
        st.session_state.role = query_params.get("role")
        st.session_state.current_kloter = "K01"
        st.session_state.active_tab = "Dashboard"
        st.session_state.sidebar_expanded = False
    else:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.current_kloter = "K01"
        st.session_state.active_tab = "Dashboard"
        st.session_state.sidebar_expanded = False
if "modal_reset_done" not in st.session_state:
    for key in list(st.session_state.keys()):
        if key.startswith("show_"):
            st.session_state[key] = False
    st.session_state.modal_reset_done = True

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if "operational_data" not in st.session_state:
    st.session_state.operational_data = {}

if "customers_df" not in st.session_state:
    st.session_state.customers_df = pd.DataFrame()

if "stock_ready_df" not in st.session_state:
    st.session_state.stock_ready_df = pd.DataFrame()

if "stock_raw_df" not in st.session_state:
    st.session_state.stock_raw_df = pd.DataFrame()

if "stock_packaging_df" not in st.session_state:
    st.session_state.stock_packaging_df = pd.DataFrame()

if "cash_flow_df" not in st.session_state:
    st.session_state.cash_flow_df = pd.DataFrame()

if "operational_migrated" not in st.session_state:
    try:
        for k in get_all_kloters():
            op = load_operational_data(k)
            save_operational_data(k, op)
    except Exception:
        pass
    st.session_state.operational_migrated = True

if "sales_orders" not in st.session_state:
    st.session_state.sales_orders = pd.DataFrame()
if "sales_notifications" not in st.session_state:
    st.session_state.sales_notifications = []

# ===================== FUNGSI UTILITY =====================
@st.cache_data
def load_settings():
    """Load settings dari file JSON"""
    try:
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
        if "packaging_prices" not in settings:
            settings["packaging_prices"] = {
                "Ziplock": 500,
                "Stiker Ziplock": 200,
                "Thanks Card": 300,
                "Stiker Bonus": 150,
                "Hangtag": 250
            }
        if "original_designs" not in settings:
            settings["original_designs"] = []
        if "original_design_files" not in settings:
            settings["original_design_files"] = {}
        if "profit_sharing_settings" not in settings:
            settings["profit_sharing_settings"] = {
                "owner_percent": 55,
                "coo_percent": 10,
                "smos_percent": 15,
                "pool_percent": 20,
                "last_updated": "2024-01-01",
                "updated_by": "owner"
            }
        if "point_configuration" not in settings:
            settings["point_configuration"] = {
                "dtf_operator": 3,
                "stock_update": 1,
                "packaging_update": 1,
                "stock_sale": 5,
                "order_request_edit": 3,
                "order_other": 2,
                "distribution": 1
            }
        if "security_settings" not in settings:
            settings["security_settings"] = {
                "owner_recovery_enabled": False,
                "owner_recovery_hash": "",
                "last_updated": "2024-01-01",
                "updated_by": "owner"
            }
        if "upload_settings" not in settings:
            settings["upload_settings"] = {
                "max_image_mb": 3,
                "max_pdf_mb": 5
            }
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        return settings
    except:
        # Default settings
        default_settings = {
            "studio_info": {
                "nama_studio": "Daluase Clothing Studio",
                "pemilik": "Jovi Lombongaris",
                "alamat": "SANGIHE, Kab. Kepl. Sangihe, Prov. Sulawesi Utara",
                "email": "daluasest@gmail.com",
                "telepon": "-",
                "website": "-"
            },
            "products": {
                "Premium Cotton T-shirt 7200": "T-Shirt",
                "Youth T-shirt 72Y00": "T-Shirt",
                "Long Sleeve 5480": "Long Sleeve",
                "Polo Shirt 8100": "Polo",
                "Hooded Sweatshirt 9500": "Hoodie"
            },
            "prices": {
                "Premium Cotton T-shirt 7200": 120000,
                "Youth T-shirt 72Y00": 100000,
                "Long Sleeve 5480": 180000,
                "Polo Shirt 8100": 160000,
                "Hooded Sweatshirt 9500": 250000
            },
            "packaging_prices": {
                "Ziplock": 500,
                "Stiker Ziplock": 200,
                "Thanks Card": 300,
                "Stiker Bonus": 150,
                "Hangtag": 250
            },
            "sizes": {
                "Premium Cotton T-shirt 7200": ["S", "M", "L", "XL", "2XL", "3XL"],
                "Youth T-shirt 72Y00": ["S", "M", "L", "XL", "2XL", "3XL"],
                "Long Sleeve 5480": ["S", "M", "L", "XL", "2XL", "3XL"],
                "Polo Shirt 8100": ["S", "M", "L", "XL", "2XL", "3XL"],
                "Hooded Sweatshirt 9500": ["S", "M", "L", "XL", "2XL", "3XL"]
            },
            "colors": {
                "Premium Cotton T-shirt 7200": COMPLETE_COLORS,
                "Youth T-shirt 72Y00": COMPLETE_COLORS,
                "Long Sleeve 5480": COMPLETE_COLORS,
                "Polo Shirt 8100": COMPLETE_COLORS,
                "Hooded Sweatshirt 9500": COMPLETE_COLORS
            },
            "original_designs": [],
            "original_design_files": {},
            "profit_sharing_settings": {
                "owner_percent": 55,
                "coo_percent": 10,
                "smos_percent": 15,
                "pool_percent": 20,
                "last_updated": "2024-01-01",
                "updated_by": "owner"
            },
            "point_configuration": {
                "dtf_operator": 3,
                "stock_update": 1,
                "packaging_update": 1,
                "stock_sale": 5,
                "order_request_edit": 3,
                "order_other": 2,
                "distribution": 1
            },
            "security_settings": {
                "owner_recovery_enabled": False,
                "owner_recovery_hash": "",
                "last_updated": "2024-01-01",
                "updated_by": "owner"
            },
            "upload_settings": {
                "max_image_mb": 3,
                "max_pdf_mb": 5
            }
        }
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(default_settings, f, indent=2)
        return default_settings

def save_settings(settings):
    """Simpan settings ke file JSON"""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)
        
def load_kloter_lock_status(kloter_id):
    try:
        if KLOTER_STATUS_FILE.exists():
            with open(KLOTER_STATUS_FILE, 'r') as f:
                all_status = json.load(f)
        else:
            all_status = {}
        return all_status.get(kloter_id, {"locked": False})
    except Exception:
        return {"locked": False}
    
def set_kloter_lock_status(kloter_id, locked):
    try:
        if KLOTER_STATUS_FILE.exists():
            with open(KLOTER_STATUS_FILE, 'r') as f:
                all_status = json.load(f)
        else:
            all_status = {}
        existing = all_status.get(kloter_id, {})
        existing["locked"] = locked
        existing["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        existing["updated_by"] = st.session_state.username
        # Preserve other fields such as writers/notes
        all_status[kloter_id] = existing
        with open(KLOTER_STATUS_FILE, 'w') as f:
            json.dump(all_status, f, indent=2)
    except Exception as e:
        st.error(f"Gagal mengupdate status kloter: {e}")

def add_kloter_note(kloter_id, message, author):
    try:
        if KLOTER_STATUS_FILE.exists():
            with open(KLOTER_STATUS_FILE, 'r') as f:
                all_status = json.load(f)
        else:
            all_status = {}
        entry = all_status.get(kloter_id, {"locked": False})
        notes = entry.get("notes", [])
        notes.append({
            "message": message,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "created_by": author
        })
        entry["notes"] = notes
        all_status[kloter_id] = entry
        with open(KLOTER_STATUS_FILE, 'w') as f:
            json.dump(all_status, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Gagal menambahkan catatan: {e}")
        return False

def calculate_kloter_points(df, kloter_id=None):
    settings = load_settings()
    pc = settings.get("point_configuration", {})
    order_req_edit_pts = int(pc.get("order_request_edit", 3))
    order_other_pts = int(pc.get("order_other", 2))
    distrib_pts = int(pc.get("distribution", 1))
    points = {}
    for _, row in df.iterrows():
        created_by = row.get('created_by')
        if created_by and pd.notna(created_by):
            points.setdefault(created_by, {'order': 0, 'distribution': 0, 'dtf': 0, 'total': 0})
            tipe = row.get('tipe_desain', '')
            if tipe in ['CUST. REQUEST', 'ORIGINAL - EDIT']:
                points[created_by]['order'] += order_req_edit_pts
            else:
                points[created_by]['order'] += order_other_pts
        distribusi_by = row.get('distribusi_by')
        if distribusi_by and pd.notna(distribusi_by) and row.get('status_distribusi') == 'TERKIRIM':
            points.setdefault(distribusi_by, {'order': 0, 'distribution': 0, 'dtf': 0, 'total': 0})
            points[distribusi_by]['distribution'] += distrib_pts
    for user in points:
        points[user]['total'] = points[user]['order'] + points[user]['distribution'] + points[user].get('dtf', 0)
    return points

@st.cache_data(ttl=60)
def load_stock_points():
    points_file = DATA_DIR / "stock_points.csv"
    if points_file.exists() and points_file.stat().st_size > 0:
        try:
            df = pd.read_csv(points_file)
            if "tanggal" in df.columns:
                try:
                    df["tanggal"] = pd.to_datetime(df["tanggal"])
                except:
                    pass
            return df
        except:
            return pd.DataFrame()
    return pd.DataFrame(columns=[
        "tanggal","username","activity_type","item_details",
        "points_earned","profit_from_sale","commission","total_earned","notes"
    ])

def record_stock_point(username, activity_type, item_details, points, profit=0, commission=0):
    points_file = DATA_DIR / "stock_points.csv"
    df = load_stock_points()
    new_row = {
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "username": username,
        "activity_type": activity_type,
        "item_details": str(item_details)[:200],
        "points_earned": int(points),
        "profit_from_sale": float(profit),
        "commission": float(commission),
        "total_earned": float(commission),
        "notes": ""
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(points_file, index=False)
    try:
        st.toast(f"🎯 +{points} poin untuk {activity_type}", icon="✅")
    except:
        pass

def validate_packaging_point(username):
    df = load_stock_points()
    if df.empty:
        return True, "✅ Bisa dapat poin packaging"
    user_points = df[(df.get("username") == username) & (df.get("activity_type") == "PACKAGING_UPDATE")] if not df.empty else pd.DataFrame()
    if not user_points.empty:
        try:
            last_date = user_points["tanggal"].max()
            days_diff = (datetime.now() - pd.to_datetime(last_date)).days
            if days_diff < 14:
                return False, f"❌ Tunggu {14 - days_diff} hari lagi untuk update packaging"
        except:
            pass
    return True, "✅ Bisa dapat poin packaging"


def show_dtf_operator_tab(operational_data):
    allowed_update = check_capability("PRODUCTION_UPDATE") or (st.session_state.role or "").lower() in ["owner", "admin", "produksi"]
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">🎨 Operator DTF</div>', unsafe_allow_html=True)
    df_kl = st.session_state.df if isinstance(st.session_state.df, pd.DataFrame) else pd.DataFrame()
    order_count = len(df_kl) if not df_kl.empty else 0
    design_series = df_kl.get("nama_desain") if not df_kl.empty else pd.Series(dtype=str)
    try:
        normalized = design_series.fillna("").astype(str).str.strip().str.lower()
        unique_designs = normalized[normalized != ""].nunique()
    except:
        unique_designs = 0
    if unique_designs <= 0:
        unique_designs = 1
        st.caption("Tidak ada data desain; diasumsikan 1 desain unik.")
    st.markdown(f"- Jumlah order kloter: {order_count}")
    st.markdown(f"- Jumlah desain unik: {unique_designs}")
    with st.form("operasional_dtf_form_fixed"):
        dtf_meter_val = st.number_input(
            "Panjang DTF (meter)",
            min_value=0.0,
            value=float(operational_data.get("dtf_meter", operational_data.get("panjang_dtf", 0.0))),
            step=0.1,
            format="%.1f",
            key="dtf_meter_input"
        )
        biaya_dtf_total = int(dtf_meter_val * 35000) if dtf_meter_val > 0 else 0
        komisi_operator = int(dtf_meter_val * 2500) + int(unique_designs * 1000)
        st.caption(f"Biaya DTF: Rp 35.000 × {dtf_meter_val:.1f} m = Rp {biaya_dtf_total:,}")
        st.caption(f"Komisi Operator: Rp 2.500 × {dtf_meter_val:.1f} m + Rp 1.000 × {unique_designs} desain = Rp {komisi_operator:,}")
        st.info(f"Total biaya DTF: Rp {biaya_dtf_total:,}")
        submit_update = False
        if allowed_update:
            submit_update = st.form_submit_button("💾 Simpan Biaya DTF", type="primary", use_container_width=True)
        else:
            st.caption("Butuh akses produksi untuk mengupdate DTF.")
        if submit_update:
            if dtf_meter_val <= 0:
                st.error("dtf_meter harus lebih dari 0.")
                return
            operational_data["dtf_meter"] = float(dtf_meter_val)
            operational_data["dtf_unique_design_count"] = int(unique_designs)
            operational_data["dtf_total_cost"] = int(biaya_dtf_total)
            operational_data["biaya_dtf"] = int(biaya_dtf_total)
            operational_data["dtf_operator_commission"] = int(komisi_operator)
            operational_data["dtf_updated_by"] = st.session_state.username
            operational_data["dtf_updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            bl = operational_data.get("biaya_lainnya", [])
            if not isinstance(bl, list):
                bl = []
            new_bl = [it for it in bl if str(it.get("keterangan","")).strip().lower() != "komisi operator dtf (otomatis)"]
            new_bl.append({"keterangan": "Komisi Operator DTF (otomatis)", "jumlah": int(komisi_operator)})
            operational_data["biaya_lainnya"] = new_bl
            save_operational_data(st.session_state.current_kloter, operational_data)
            ensure_dtf_cash_flow(st.session_state.current_kloter, biaya_dtf_total, dtf_meter_val, unique_designs)
            ensure_dtf_commission_cash_flow(st.session_state.current_kloter, komisi_operator, dtf_meter_val, unique_designs)
            st.success("✅ Biaya DTF diperbarui dan dicatat ke cash flow.")
            # time.sleep(1) # Removed for performance
            st.rerun()

def calculate_monthly_stock_bonus(month_year=None):
    if month_year is None:
        month_year = datetime.now().strftime("%Y-%m")
    df = load_stock_points()
    if df.empty:
        return pd.DataFrame()
    try:
        df["month"] = pd.to_datetime(df["tanggal"]).dt.strftime("%Y-%m")
    except:
        df["month"] = ""
    month_df = df[df["month"] == month_year]
    if month_df.empty:
        return pd.DataFrame()
    summary = month_df.groupby("username").agg({
        "points_earned": "sum",
        "commission": "sum",
        "profit_from_sale": "sum"
    }).reset_index()
    total_profit = summary["profit_from_sale"].sum()
    bonus_pool = total_profit * 0.05
    total_points = summary["points_earned"].sum()
    if total_points > 0:
        summary["pool_percent"] = (summary["points_earned"] / total_points) * 100
        summary["pool_bonus"] = (summary["pool_percent"] / 100.0) * bonus_pool
    else:
        summary["pool_percent"] = 0.0
        summary["pool_bonus"] = 0.0
    summary["total_bonus"] = summary["commission"] + summary["pool_bonus"]
    summary["month"] = month_year
    summary["calculated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    summary["status"] = "PENDING"
    return summary

def save_stock_bonus_history(bonus_df):
    history_file = DATA_DIR / "stock_bonus_history.csv"
    if history_file.exists() and history_file.stat().st_size > 0:
        try:
            history_df = pd.read_csv(history_file)
        except:
            history_df = pd.DataFrame(columns=[
                "bonus_id","month_year","username","total_points","total_commission",
                "pool_percent","pool_bonus","total_bonus","calculated_at","status","paid_at"
            ])
    else:
        history_df = pd.DataFrame(columns=[
            "bonus_id","month_year","username","total_points","total_commission",
            "pool_percent","pool_bonus","total_bonus","calculated_at","status","paid_at"
        ])
    bonus_id = f"BONUS-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    for _, row in bonus_df.iterrows():
        new_row = {
            "bonus_id": bonus_id,
            "month_year": row.get("month",""),
            "username": row.get("username",""),
            "total_points": row.get("points_earned",0),
            "total_commission": row.get("commission",0.0),
            "pool_percent": row.get("pool_percent",0.0),
            "pool_bonus": row.get("pool_bonus",0.0),
            "total_bonus": row.get("total_bonus",0.0),
            "calculated_at": row.get("calculated_at",""),
            "status": row.get("status","PENDING"),
            "paid_at": None
        }
        history_df = pd.concat([history_df, pd.DataFrame([new_row])], ignore_index=True)
    history_df.to_csv(history_file, index=False)
    return bonus_id

def save_profit_sharing_history(kloter_id, calculation_date, user_data_list, calculated_by):
    cols = ["kloter_id","tanggal_perhitungan","username","bagian_tetap","order_points","distribution_points","total_points","percent_from_pool","nilai_pool","total_diterima","calculated_by","created_at"]
    if PROFIT_SHARING_HISTORY_FILE.exists() and PROFIT_SHARING_HISTORY_FILE.stat().st_size > 0:
        df = pd.read_csv(PROFIT_SHARING_HISTORY_FILE)
    else:
        df = pd.DataFrame(columns=cols)
    rows = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for ud in user_data_list:
        rows.append({
            "kloter_id": kloter_id,
            "tanggal_perhitungan": calculation_date,
            "username": ud.get("username",""),
            "bagian_tetap": ud.get("bagian_tetap",0),
            "order_points": ud.get("order_points",0),
            "distribution_points": ud.get("distribution_points",0),
            "total_points": ud.get("total_points",0),
            "percent_from_pool": ud.get("percent_from_pool",0.0),
            "nilai_pool": ud.get("nilai_pool",0.0),
            "total_diterima": ud.get("total_diterima",0.0),
            "calculated_by": calculated_by,
            "created_at": now
        })
    df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
    df.to_csv(PROFIT_SHARING_HISTORY_FILE, index=False)

@st.cache_data(ttl=60)
def load_profit_sharing_history(kloter_id=None, start_date=None, end_date=None):
    cols = ["kloter_id","tanggal_perhitungan","username","bagian_tetap","order_points","distribution_points","total_points","percent_from_pool","nilai_pool","total_diterima","calculated_by","created_at"]
    if PROFIT_SHARING_HISTORY_FILE.exists() and PROFIT_SHARING_HISTORY_FILE.stat().st_size > 0:
        try:
            df = pd.read_csv(PROFIT_SHARING_HISTORY_FILE)
        except:
            df = pd.DataFrame(columns=cols)
    else:
        df = pd.DataFrame(columns=cols)
    if not df.empty:
        if kloter_id:
            df = df[df["kloter_id"] == kloter_id]
        try:
            df["tanggal_perhitungan"] = pd.to_datetime(df["tanggal_perhitungan"])
        except:
            pass
        if start_date:
            try:
                df = df[df["tanggal_perhitungan"] >= pd.to_datetime(start_date)]
            except:
                pass
        if end_date:
            try:
                df = df[df["tanggal_perhitungan"] <= pd.to_datetime(end_date)]
            except:
                pass
    return df

def set_kloter_writers(kloter_id, writers):
    try:
        if KLOTER_STATUS_FILE.exists():
            with open(KLOTER_STATUS_FILE, 'r') as f:
                all_status = json.load(f)
        else:
            all_status = {}
        entry = all_status.get(kloter_id, {"locked": False})
        entry["writers"] = writers
        entry["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry["updated_by"] = st.session_state.username
        all_status[kloter_id] = entry
        with open(KLOTER_STATUS_FILE, 'w') as f:
            json.dump(all_status, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Gagal mengatur penulis catatan: {e}")
        return False

@st.cache_data(ttl=10)
def load_kloter_data(kloter_id):
    """Load data kloter tertentu dengan error handling"""
    file_path = ORDERS_DIR / f"{kloter_id}.csv"
    if file_path.exists() and file_path.stat().st_size > 0:
        try:
            df = pd.read_csv(file_path)
            for col in ["payment_history","produksi_history","distribusi_history"]:
                if col not in df.columns:
                    df[col] = ""
                else:
                    df[col] = df[col].fillna("").astype(str)
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
    return pd.DataFrame()

def save_kloter_data(kloter_id, df):
    """Simpan data kloter"""
    file_path = ORDERS_DIR / f"{kloter_id}.csv"
    df.to_csv(file_path, index=False)

@st.cache_data(ttl=60)
def get_all_kloters():
    """Get semua kloter yang ada"""
    kloter_files = list(ORDERS_DIR.glob("K*.csv"))
    kloters = [f.stem for f in kloter_files]
    return sorted(kloters) if kloters else ["K01"]

def generate_invoice_number(kloter_id):
    suffix = secrets.token_hex(2)
    return f"DS-{kloter_id}-{suffix}"
 
def generate_stock_sale_id():
    suffix = secrets.token_hex(3)
    return f"DS-STK-{suffix}"

def calculate_product_buy_price(product_name, color, size):
    """Hitung harga beli produk sesuai rumus Excel"""
    if product_name not in PRODUCT_BUY_PRICES:
        return 0
    
    product_data = PRODUCT_BUY_PRICES[product_name]
    color_upper = color.upper()
    
    # Untuk Hooded Sweatshirt khusus
    if product_name == "Hooded Sweatshirt 9500":
        if color_upper in product_data["special_colors"]:
            base_price = product_data["special_price"]
        elif color_upper == "WHITE":
            base_price = product_data["white_price"]
        else:
            base_price = product_data["color_price"]
    else:
        # Untuk produk lain
        if color_upper == "WHITE":
            base_price = product_data["white_price"]
        else:
            base_price = product_data["color_price"]
    
    # Tambah extra untuk ukuran
    size_extra = product_data["size_extra"].get(size.upper(), 0)
    
    return base_price + size_extra

@st.cache_data(ttl=10)
def load_operational_data(kloter_id):
    operational_file = DATA_DIR / f"operational_{kloter_id}.json"
    def _to_int(v):
        try:
            s = str(v)
            if not s.strip():
                return 0
            return int(float(s.replace(",", "")))
        except:
            return 0
    def _to_float(v):
        try:
            s = str(v)
            if not s.strip():
                return 0.0
            return float(s.replace(",", ""))
        except:
            return 0.0
    if operational_file.exists() and operational_file.stat().st_size > 0:
        try:
            with open(operational_file, 'r') as f:
                data = json.load(f)
            result = {}
            result["biaya_produk"] = _to_int(data.get("biaya_produk", 0))
            result["biaya_dtf"] = _to_int(data.get("biaya_dtf", 0))
            result["biaya_sablon"] = _to_int(data.get("biaya_sablon", 0))
            result["ongkir_supplier"] = _to_int(data.get("ongkir_supplier", 0))
            result["total"] = _to_int(data.get("total", 0))
            result["panjang_dtf"] = _to_float(data.get("panjang_dtf", 0))
            result["dtf_meter"] = _to_float(data.get("dtf_meter", data.get("panjang_dtf", 0)))
            result["dtf_unique_design_count"] = _to_int(data.get("dtf_unique_design_count", 0))
            result["dtf_total_cost"] = _to_int(data.get("dtf_total_cost", data.get("biaya_dtf", 0)))
            items = data.get("biaya_lainnya", [])
            sane_items = []
            if isinstance(items, list):
                for it in items:
                    ket = str(it.get("keterangan", "")) if isinstance(it, dict) else ""
                    jumlah = _to_int(it.get("jumlah", 0)) if isinstance(it, dict) else 0
                    if ket or jumlah > 0:
                        sane_items.append({"keterangan": ket, "jumlah": jumlah})
            result["biaya_lainnya"] = sane_items
            result["catatan"] = str(data.get("catatan", ""))
            result["updated_at"] = str(data.get("updated_at", ""))
            result["updated_by"] = str(data.get("updated_by", ""))
            result["dtf_updated_by"] = str(data.get("dtf_updated_by", data.get("updated_by","")))
            result["dtf_updated_at"] = str(data.get("dtf_updated_at", data.get("updated_at","")))
            result["dtf_operator_commission"] = _to_int(data.get("dtf_operator_commission", 0))
            return result
        except:
            pass
    return {
        "biaya_produk": 0,
        "biaya_dtf": 0,
        "panjang_dtf": 0.0,
        "dtf_meter": 0.0,
        "dtf_unique_design_count": 0,
        "dtf_total_cost": 0,
        "biaya_sablon": 0,
        "ongkir_supplier": 0,
        "biaya_lainnya": [],
        "total": 0,
        "catatan": "",
        "updated_at": "",
        "updated_by": "",
        "dtf_updated_by": "",
        "dtf_updated_at": "",
        "dtf_operator_commission": 0
    }

def save_operational_data(kloter_id, data):
    operational_file = DATA_DIR / f"operational_{kloter_id}.json"
    def _to_int(v):
        try:
            s = str(v)
            if not s.strip():
                return 0
            return int(float(s.replace(",", "")))
        except:
            return 0
    def _to_float(v):
        try:
            s = str(v)
            if not s.strip():
                return 0.0
            return float(s.replace(",", ""))
        except:
            return 0.0
    try:
        sane = {}
        sane["biaya_produk"] = _to_int(data.get("biaya_produk", 0))
        sane["biaya_dtf"] = _to_int(data.get("biaya_dtf", 0))
        sane["biaya_sablon"] = _to_int(data.get("biaya_sablon", 0))
        sane["ongkir_supplier"] = _to_int(data.get("ongkir_supplier", 0))
        sane["total"] = _to_int(data.get("total", 0))
        sane["panjang_dtf"] = _to_float(data.get("panjang_dtf", data.get("dtf_meter", 0)))
        sane["dtf_meter"] = _to_float(data.get("dtf_meter", data.get("panjang_dtf", 0)))
        sane["dtf_unique_design_count"] = _to_int(data.get("dtf_unique_design_count", 0))
        sane["dtf_total_cost"] = _to_int(data.get("dtf_total_cost", data.get("biaya_dtf", 0)))
        sane["catatan"] = str(data.get("catatan", ""))
        sane["updated_at"] = str(data.get("updated_at", ""))
        sane["updated_by"] = str(data.get("updated_by", ""))
        sane["dtf_updated_by"] = str(data.get("dtf_updated_by", data.get("updated_by","")))
        sane["dtf_updated_at"] = str(data.get("dtf_updated_at", data.get("updated_at","")))
        sane["dtf_operator_commission"] = _to_int(data.get("dtf_operator_commission", 0))
        sane_items = []
        items = data.get("biaya_lainnya", [])
        if isinstance(items, list):
            for it in items:
                ket = str(it.get("keterangan", "")) if isinstance(it, dict) else ""
                jumlah = _to_int(it.get("jumlah", 0)) if isinstance(it, dict) else 0
                if ket or jumlah > 0:
                    sane_items.append({"keterangan": ket, "jumlah": jumlah})
        sane["biaya_lainnya"] = sane_items
        with open(operational_file, 'w') as f:
            json.dump(sane, f, indent=2)
    except Exception as e:
        st.error(f"Error menyimpan data operasional: {e}")

# ===================== FUNGSI AUTHENTICATION =====================
def hash_password(password):
    """Hash password untuk keamanan"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_temp_password(length=10):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@st.cache_data(ttl=10)
def load_users():
    """Load data user dari CSV"""
    if USERS_FILE.exists() and USERS_FILE.stat().st_size > 0:
        df = pd.read_csv(USERS_FILE)
        if "features" not in df.columns:
            df["features"] = ""
        if "capabilities" not in df.columns:
            df["capabilities"] = ""
        if "suspend_mode" not in df.columns:
            df["suspend_mode"] = "none"
        if "ban_note" not in df.columns:
            df["ban_note"] = ""
        # Sanitasi NaN menjadi string kosong untuk mencegah error default multiselect
        df["features"] = df["features"].fillna("").astype(str)
        df["capabilities"] = df["capabilities"].fillna("").astype(str)
        df["suspend_mode"] = df["suspend_mode"].fillna("none").astype(str)
        df["ban_note"] = df["ban_note"].fillna("").astype(str)
        return df
    else:
        # Buat user default
        default_users = pd.DataFrame([{
            "username": "owner",
            "password_hash": hash_password("admin123"),
            "role": "owner",
            "full_name": "Pemilik Studio",
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "status": "active",
            "features": "ALL",
            "capabilities": "ALL",
            "suspend_mode": "none",
            "ban_note": ""
        }])
        default_users.to_csv(USERS_FILE, index=False)
        return default_users

def authenticate(username, password):
    # EMERGENCY BYPASS - FORCE LOGIN
    # This bypasses CSV reading entirely for the owner account to ensure access.
    u_input = str(username).strip().lower()
    p_input = str(password).strip()
    
    if u_input == "owner" and p_input == "admin123":
        return True, "owner", "ALL", "ALL"

    # Standard Logic
    st.cache_data.clear()
    users_df = load_users()
    
    input_pass_hash = hash_password(p_input)
    
    try:
        found_row = None
        for _, row in users_df.iterrows():
            db_user = str(row['username']).strip().lower()
            if db_user == u_input:
                if str(row['status']) == 'active':
                    found_row = row
                    break
        
        if found_row is not None:
            stored_hash = str(found_row['password_hash']).strip()
            if input_pass_hash == stored_hash:
                return True, found_row['role'], found_row.get('features', ''), found_row.get('capabilities', '')
    except Exception:
        pass
        
    return False, None, "", ""



def get_capability_options():
    return [
        "ORDER_ADD","ORDER_VIEW","ORDER_EDIT","ORDER_DELETE","ORDER_PAY",
        "PRODUCTION_UPDATE",
        "DISTRIBUTION_UPDATE","DISTRIBUTION_MASS",
        "STOCK_ADD","STOCK_SELL","STOCK_EDIT","STOCK_DELETE",
        "CASH_RECORD","CASH_EDIT","CASH_DELETE",
        "INVOICE_PDF",
        "KLOTER_NEW",
        "CUSTOMER_DELETE",
        "SALES_ADD_ORDER",
        "SALES_VIEW_ORDERS",
        "APPROVE_SALES_ORDER",
        "PACKAGING_EDIT","PACKAGING_DELETE"
    ]

def check_feature_access(feature_id):
    if not st.session_state.authenticated:
        return False
    if (st.session_state.role or "").lower() == "owner":
        return True
    feats = st.session_state.get("features", [])
    return feature_id in feats

def check_capability(cap_id):
    if not st.session_state.authenticated:
        return False
    if (st.session_state.role or "").lower() == "owner":
        return True
    caps = st.session_state.get("capabilities", [])
    return cap_id in caps

def check_role_access(required_role):
    """Cek apakah user punya akses ke halaman"""
    if not st.session_state.authenticated:
        return False
    
    role_hierarchy = {
        "owner": 6,
        "coo": 5,
        "admin": 4,
        "produksi": 3,
        "kurir": 2,
        "viewer": 1
    }
    
    user_level = role_hierarchy.get(st.session_state.role, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    return user_level >= required_level

def validate_password_strength(pw):
    if len(pw) < 12:
        return False, "Password minimal 12 karakter."
    if not re.search(r"[A-Z]", pw):
        return False, "Harus mengandung huruf besar."
    if not re.search(r"[a-z]", pw):
        return False, "Harus mengandung huruf kecil."
    if not re.search(r"[0-9]", pw):
        return False, "Harus mengandung angka."
    if not re.search(r"[^A-Za-z0-9]", pw):
        return False, "Harus mengandung karakter spesial."
    return True, "OK"

def change_user_password(username, current_password, new_password):
    users_df = load_users()
    mask = users_df["username"] == username
    if not mask.any():
        return False, "User tidak ditemukan."
    stored_hash = str(users_df.loc[mask, "password_hash"].iloc[0])
    if hash_password(current_password) != stored_hash:
        return False, "Password lama salah."
    if current_password == new_password:
        return False, "Password baru tidak boleh sama dengan yang lama."
    ok, msg = validate_password_strength(new_password)
    if not ok:
        return False, msg
    users_df.loc[mask, "password_hash"] = hash_password(new_password)
    users_df.to_csv(USERS_FILE, index=False)
    return True, "Password berhasil diubah."

def reset_owner_password_with_token(token, new_password):
    settings = load_settings()
    sec = settings.get("security_settings", {})
    enabled = bool(sec.get("owner_recovery_enabled", False))
    token_hash = str(sec.get("owner_recovery_hash", ""))
    if not enabled or not token_hash:
        return False, "Recovery token belum diaktifkan."
    if hashlib.sha256(token.encode()).hexdigest() != token_hash:
        return False, "Recovery token tidak valid."
    ok, msg = validate_password_strength(new_password)
    if not ok:
        return False, msg
    users_df = load_users()
    mask = users_df["username"] == "owner"
    if not mask.any():
        return False, "User owner tidak ditemukan."
    users_df.loc[mask, "password_hash"] = hash_password(new_password)
    users_df.to_csv(USERS_FILE, index=False)
    settings["security_settings"]["owner_recovery_enabled"] = False
    settings["security_settings"]["owner_recovery_hash"] = ""
    settings["security_settings"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    settings["security_settings"]["updated_by"] = "system"
    save_settings(settings)
    return True, "Password owner berhasil direset."

def get_upload_limits():
    s = load_settings()
    us = s.get("upload_settings", {})
    return {
        "max_image_mb": int(us.get("max_image_mb", 3)),
        "max_pdf_mb": int(us.get("max_pdf_mb", 5))
    }

def get_file_size_mb(uploaded_file):
    try:
        size_bytes = uploaded_file.size
    except:
        try:
            size_bytes = len(uploaded_file.getbuffer())
        except:
            try:
                b = uploaded_file.read()
                size_bytes = len(b)
                uploaded_file.seek(0)
            except:
                size_bytes = 0
    return round(size_bytes / (1024 * 1024), 2)

def check_upload_limit(uploaded_file, ext):
    limits = get_upload_limits()
    ext = str(ext or "").lower()
    size_mb = get_file_size_mb(uploaded_file)
    if ext in [".png",".jpg",".jpeg",".gif",".webp",".bmp"]:
        max_mb = limits["max_image_mb"]
        if size_mb > max_mb:
            return False, f"Ukuran gambar {size_mb} MB melebihi batas {max_mb} MB."
        return True, ""
    elif ext == ".pdf":
        max_mb = limits["max_pdf_mb"]
        if size_mb > max_mb:
            return False, f"Ukuran PDF {size_mb} MB melebihi batas {max_mb} MB."
        return True, ""
    else:
        max_mb = limits["max_image_mb"]
        if size_mb > max_mb:
            return False, f"Ukuran file {size_mb} MB melebihi batas {max_mb} MB."
        return True, ""

def is_image_ext(ext):
    return str(ext or "").lower() in [".png",".jpg",".jpeg",".gif",".webp",".bmp"]

def compress_image_bytes(data, ext, target_mb=None, max_side=1920, start_quality=85, min_quality=60):
    if Image is None:
        return None, None
    try:
        im = Image.open(BytesIO(data))
    except Exception:
        return None, None
    try:
        w, h = im.size
        if max(w, h) > max_side:
            im.thumbnail((max_side, max_side))
    except Exception:
        pass
    has_alpha = im.mode in ("RGBA", "LA") or ("transparency" in im.info)
    fmt = "PNG" if (str(ext).lower() == ".png" and has_alpha) else "JPEG"
    if fmt == "JPEG" and im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    q = start_quality
    out = BytesIO()
    while True:
        out.seek(0)
        out.truncate(0)
        try:
            if fmt == "PNG":
                im.save(out, format=fmt, optimize=True)
            else:
                im.save(out, format=fmt, quality=q, optimize=True)
        except Exception:
            return None, None
        size_mb = len(out.getvalue()) / (1024 * 1024)
        if target_mb is None or size_mb <= target_mb or q <= min_quality or fmt == "PNG":
            break
        q = max(min_quality, q - 5)
    out.seek(0)
    return out, size_mb

def prepare_upload_bytes(uploaded_file, ext):
    ok, msg = check_upload_limit(uploaded_file, ext)
    uploaded_file.seek(0)
    data = uploaded_file.read()
    if ok:
        return data, None
    if is_image_ext(ext):
        limits = get_upload_limits()
        target_mb = limits["max_image_mb"]
        out, new_size_mb = compress_image_bytes(data, ext, target_mb=target_mb)
        if out is not None and new_size_mb is not None and new_size_mb <= target_mb:
            return out.getvalue(), None
        return None, msg
    return None, msg

# ===================== TOP NAVIGATION BAR =====================
def show_top_navigation():
    """Tampilkan top navigation bar sebagai baris tombol"""
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <style>
    .nav-pill {
        background: #2A2E36;
        color: #E0E0E0;
        padding: 12px 22px;
        border-radius: 999px;
        border: 1px solid #3A3F49;
        display: inline-block;
        text-align: center;
        font-weight: 700;
        font-size: 1.05rem;
        line-height: 1.2;
        box-shadow: none;
        transition: background-color .2s ease, color .2s ease, transform .2s ease, box-shadow .2s ease, border-color .2s ease;
    }
    .nav-pill:hover {
        background: #343942;
        color: #FFFFFF;
        border-color: #505663;
        transform: translateY(-1px);
        box-shadow: 0 6px 14px rgba(212, 175, 55, 0.18);
    }
    .nav-pill.active {
        background-color: #D4AF37;
        color: #0E0E0E;
        border-color: #D4AF37;
        font-weight: 800;
        box-shadow: 0 8px 16px rgba(212, 175, 55, 0.28);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
    if (st.session_state.role or "").lower() == "sales":
        nav_items = [
            {"id": "SalesAdd", "label": "Add Sales Order"},
            {"id": "SalesOrders", "label": "My Orders"},
        ]
    else:
        nav_items = [{"id": "Dashboard", "label": "Dashboard"}]
        if check_feature_access("Management Kloter"):
            nav_items.append({"id": "Management Kloter", "label": "Batch Management"})
        if check_feature_access("Kas & Analisis"):
            nav_items.append({"id": "Kas & Analisis", "label": "Cash & Analytics"})
        if check_feature_access("Stock System"):
            nav_items.append({"id": "Stock System", "label": "Stock System"})
        if (st.session_state.role or "").lower() == "owner":
            nav_items.append({"id": "Management Tim", "label": "Team Management"})
            nav_items.append({"id": "Pengaturan", "label": "Settings"})

    nav_items.append({"id": "Logout", "label": "Logout"})

    active_id = st.session_state.active_tab or nav_items[0]["id"]
    logo_path = DATA_DIR / "logo.png"
    try:
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            ext = "png" if logo_path.suffix.lower() == ".png" else "jpeg"
            st.markdown(f"<style>.logo-button-box button{{width: 480px; height: 240px; background-image:url('data:image/{ext};base64,{b64}'); background-size: contain; background-repeat: no-repeat; background-position: left center; background-color: transparent; border: none;}}</style>", unsafe_allow_html=True)
            st.markdown("<div class='logo-button-box'>", unsafe_allow_html=True)
            if st.button(" ", key="logo_nav_btn"):
                st.session_state.active_tab = "Dashboard"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='top-logo' style='color:#D4AF37; font-weight:700;'>DALUASE</div>", unsafe_allow_html=True)
    except:
        st.markdown("<div class='top-logo' style='color:#D4AF37; font-weight:700;'>DALUASE</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    cols = st.columns(len(nav_items))
    for idx, item in enumerate(nav_items):
        if item["id"] == active_id and item["id"] != "Logout":
            cols[idx].markdown(f"<div class='nav-pill active'>{item['label']}</div>", unsafe_allow_html=True)
        else:
            if cols[idx].button(item["label"], key=f"top_nav_btn_{item['id']}"):
                st.session_state.active_tab = item["id"]
                if item["id"] == "Logout":
                    st.session_state.authenticated = False
                    st.session_state.username = None
                    st.session_state.role = None
                st.rerun()
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# ===================== SIDEBAR KLOTER =====================
def show_kloter_sidebar():
    """Tampilkan sidebar khusus untuk Management Kloter"""
    st.sidebar.markdown('<div class="sidebar-container">', unsafe_allow_html=True)
    
    # Header
    st.sidebar.markdown('<div class="sidebar-header">📦 Management Kloter</div>', unsafe_allow_html=True)
    
    # Pilih kloter
    all_kloters = get_all_kloters()
    selected_kloter = st.sidebar.selectbox(
        "Pilih Kloter",
        all_kloters,
        index=all_kloters.index(st.session_state.current_kloter) if st.session_state.current_kloter in all_kloters else 0,
        key="kloter_selector"
    )
    
    if selected_kloter != st.session_state.current_kloter:
        st.session_state.current_kloter = selected_kloter
        st.session_state.df = load_kloter_data(selected_kloter)
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Alert boxes
    if not st.session_state.df.empty:
        unpaid = st.session_state.df[st.session_state.df["payment_status"] != "LUNAS"]
        pending_prod = st.session_state.df[st.session_state.df["status_produksi"] == "PENDING"]
        
        if not unpaid.empty:
            st.sidebar.markdown(f"""
            <div class="alert-box alert-danger">
                <strong>⚠️ {len(unpaid)} Order Belum Lunas</strong><br>
                Piutang: Rp {unpaid['remaining_payment'].sum():,}
            </div>
            """, unsafe_allow_html=True)
        
        if not pending_prod.empty:
            st.sidebar.markdown(f"""
            <div class="alert-box alert-warning">
                <strong>⚡ {len(pending_prod)} Order Pending</strong>
            </div>
            """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    
    # Sub-menu untuk kloter - DARI V4
    kloter_options = [
        "➕ Tambah Order",
        "📋 Data Order", 
        "🏭 Production", 
        "🚚 Distribution", 
        "💰 Operasional", 
        "📈 Profit",
        "📋 Laporan Pembagian",
        "🧾 Struk & Invoice",
        "👥 Data Pelanggan",
        "📊 Rekapan Kloter"
    ]
    if check_capability("APPROVE_SALES_ORDER") or (st.session_state.role or "").lower() == "owner":
        kloter_options.insert(1, "✅ Approval Order Sales")
        kloter_options.append("👥 Kontribusi Sales")
    kloter_menu = st.sidebar.radio("Menu Kloter", kloter_options)
    
    st.sidebar.markdown("---")
    
    if (st.session_state.role or "").lower() == "owner":
        with st.sidebar.expander("⚙️ Profit Sharing", expanded=False):
            settings = load_settings()
            pss = settings.get("profit_sharing_settings", {
                "owner_percent": 55, "coo_percent": 10, "smos_percent": 15, "pool_percent": 20
            })
            owner_percent = st.number_input("Owner (%)", min_value=0, max_value=100, value=int(pss.get("owner_percent",55)), key="sb_owner_pct")
            coo_percent = st.number_input("COO (%)", min_value=0, max_value=100, value=int(pss.get("coo_percent",10)), key="sb_coo_pct")
            smos_percent = st.number_input("SMOS (%)", min_value=0, max_value=100, value=int(pss.get("smos_percent",15)), key="sb_smos_pct")
            pool_percent = st.number_input("Pool (%)", min_value=0, max_value=100, value=int(pss.get("pool_percent",20)), key="sb_pool_pct")
            if st.button("💾 Simpan Persentase", key="sb_save_profit_pct"):
                total = owner_percent + coo_percent + smos_percent + pool_percent
                if total != 100:
                    st.error("Total persentase harus 100%")
                else:
                    settings["profit_sharing_settings"] = {
                        "owner_percent": owner_percent,
                        "coo_percent": coo_percent,
                        "smos_percent": smos_percent,
                        "pool_percent": pool_percent,
                        "last_updated": datetime.now().strftime("%Y-%m-%d"),
                        "updated_by": st.session_state.username
                    }
                    save_settings(settings)
                    st.success("Pengaturan persentase disimpan")
    
    # Tombol mulai kloter baru
    if check_capability("KLOTER_NEW") and st.sidebar.button("🆕 Mulai Kloter Baru", type="primary", use_container_width=True):
        # Cari kloter berikutnya
        existing_kloters = [k for k in all_kloters if k.startswith('K')]
        if existing_kloters:
            last_number = max([int(k[1:]) for k in existing_kloters if k[1:].isdigit()])
            new_kloter = f"K{last_number + 1:02d}"
        else:
            new_kloter = "K01"
        
        # Simpan kloter lama (jika ada data)
        if not st.session_state.df.empty:
            save_kloter_data(st.session_state.current_kloter, st.session_state.df)
        
        # Mulai kloter baru
        st.session_state.current_kloter = new_kloter
        st.session_state.df = pd.DataFrame()
        save_kloter_data(new_kloter, pd.DataFrame())
        
        # Buat file operasional kosong
        save_operational_data(new_kloter, load_operational_data(new_kloter))
    
    # Tombol Kunci Kloter (owner-only)
    st.sidebar.markdown("---")
    if (st.session_state.role or "").lower() == "owner":
        status = load_kloter_lock_status(st.session_state.current_kloter)
        locked = status.get("locked", False)
        if not locked:
            if st.sidebar.button("🔒 Kunci Kloter Ini", use_container_width=True):
                set_kloter_lock_status(st.session_state.current_kloter, True)
                st.success("Kloter dikunci")
                # time.sleep(1) # Removed for performance
                st.rerun()
        else:
            st.sidebar.success("Kloter ini TERKUNCI")
            if st.sidebar.button("🔓 Buka Kunci Kloter", use_container_width=True):
                set_kloter_lock_status(st.session_state.current_kloter, False)
                st.info("Kloter dibuka kembali")
                # time.sleep(1) # Removed for performance
                st.rerun()
        st.sidebar.markdown("---")
        if "reset_kloter_step" not in st.session_state:
            st.session_state.reset_kloter_step = 0
        if st.sidebar.button("🧨 RESET KLOTER INI", use_container_width=True):
            st.session_state.reset_kloter_step = 1
        if st.session_state.reset_kloter_step == 1:
            pw = st.sidebar.text_input("Enter Owner Password", type="password", key="reset_owner_password")
            if st.sidebar.button("Confirm Password", use_container_width=True):
                users_df = load_users()
                owner_df = users_df[(users_df["username"] == "owner") & (users_df["status"] == "active")]
                ok = False
                if not owner_df.empty:
                    stored_hash = owner_df.iloc[0]["password_hash"]
                    ok = hash_password(pw) == stored_hash
                if ok:
                    st.session_state.reset_kloter_step = 2
                else:
                    st.sidebar.error("Owner password is incorrect")
        if st.session_state.reset_kloter_step == 2:
            st.sidebar.warning("APA ANDA YAKIN MENGHAPUS DATA KLOTER INI?")
            confirm = st.sidebar.checkbox("Saya yakin", key="reset_confirm_checkbox")
            if st.sidebar.button("Ya, Hapus Data Kloter", use_container_width=True):
                if confirm:
                    kl = st.session_state.current_kloter
                    st.session_state.df = pd.DataFrame()
                    save_kloter_data(kl, st.session_state.df)
                    operational_file = DATA_DIR / f"operational_{kl}.json"
                    if operational_file.exists():
                        try:
                            operational_file.unlink()
                        except:
                            pass
                    cash_flow_file = CASH_DIR / "cash_flow.csv"
                    if cash_flow_file.exists() and cash_flow_file.stat().st_size > 0:
                        try:
                            cf = pd.read_csv(cash_flow_file)
                            if "kloter_id" in cf.columns:
                                cf = cf[cf["kloter_id"] != kl]
                                cf.to_csv(cash_flow_file, index=False)
                        except:
                            pass
                    # Hapus history profit sharing untuk kloter ini
                    if PROFIT_SHARING_HISTORY_FILE.exists() and PROFIT_SHARING_HISTORY_FILE.stat().st_size > 0:
                        try:
                            psh = pd.read_csv(PROFIT_SHARING_HISTORY_FILE)
                            if "kloter_id" in psh.columns:
                                psh = psh[psh["kloter_id"] != kl]
                                psh.to_csv(PROFIT_SHARING_HISTORY_FILE, index=False)
                        except:
                            pass
                    # Hapus status/lock kloter dari kloter_status.json
                    kloter_status_file = DATA_DIR / "kloter_status.json"
                    if kloter_status_file.exists() and kloter_status_file.stat().st_size > 0:
                        try:
                            with open(kloter_status_file, "r") as f:
                                ks = json.load(f)
                            if kl in ks:
                                del ks[kl]
                                with open(kloter_status_file, "w") as f:
                                    json.dump(ks, f, indent=2)
                        except:
                            pass
                    st.success("Data kloter telah dihapus")
                    st.session_state.reset_kloter_step = 0
                    # time.sleep(1) # Removed for performance
                    st.rerun()
    elif not check_capability("KLOTER_NEW"):
        st.sidebar.caption("Owner belum mengizinkan fitur membuat kloter baru.")
    
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    return kloter_menu

# ===================== LOGIN PAGE =====================
def show_login():
    """Tampilkan halaman login dengan styling modern"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        settings = load_settings()
        studio_info = settings.get("studio_info", {})
        logo_path = DATA_DIR / "logo.png"
        if logo_path.exists():
            try:
                with open(logo_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                ext = "png" if logo_path.suffix.lower() == ".png" else "jpeg"
                st.markdown(
                    f"""
                    <div style="display:flex; align-items:center; justify-content:center; margin-bottom: 1.5rem;">
                        <img src="data:image/{ext};base64,{b64}" style="max-width: 320px; height: auto;" />
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            except:
                st.markdown('<div style="display:flex; align-items:center; justify-content:center; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
                st.image(str(logo_path), use_column_width=False, width=300)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <h1 style="color: #D4AF37; font-size: 2.3rem;">👕 DALUASE</h1>
                <p style="color: #CCCCCC; font-size: 1.1rem;">CLOTHING STUDIO</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Login Card
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        st.markdown('<h3 style="color: #D4AF37; text-align: center;">Login ke Sistem</h3>', unsafe_allow_html=True)
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Username", key="login_username", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Password", key="login_password", label_visibility="collapsed")
        
        st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🚀 **LOGIN**", type="primary", use_container_width=True):
                if username and password:
                    with st.spinner("Memproses login..."):
                        success, role, features_str, caps_str = authenticate(username, password)
                        if success:
                            users_df = load_users()
                            urow = users_df[users_df["username"] == username].iloc[0]
                            suspend_mode = str(urow.get("suspend_mode","none")).lower()
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.session_state.role = role
                            st.query_params["auth"] = "1"
                            st.query_params["user"] = username
                            st.query_params["role"] = role
                            st.session_state.suspend_mode = suspend_mode
                            if suspend_mode == "login_block" and (role or "").lower() != "owner":
                                st.session_state.authenticated = False
                                st.error("Maaf, anda sedang dalam status di-banned sementara. Login diblokir.")
                                return
                            if (role or "").lower() == "owner":
                                st.session_state.features = [
                                    "Dashboard","Management Kloter","Kas & Analisis","Stock System",
                                    "Production","Distribution","Struk & Invoice","Pengaturan","Management Tim"
                                ]
                                st.session_state.capabilities = get_capability_options()
                            elif (role or "").lower() == "sales":
                                st.session_state.features = ["Dashboard","Management Sales Order"]
                                st.session_state.capabilities = ["SALES_ADD_ORDER","SALES_VIEW_ORDERS"]
                                st.session_state.active_tab = "SalesAdd"
                            else:
                                st.session_state.features = [f.strip() for f in features_str.split(";") if f.strip()]
                                st.session_state.capabilities = [c.strip() for c in caps_str.split(";") if c.strip()]
                            if suspend_mode == "readonly" and (role or "").lower() != "owner":
                                st.session_state.features = []
                                st.session_state.capabilities = []
                                st.warning("Maaf, anda sedang di-banned sementara (mode baca saja).")
                            if (role or "").lower() != "sales":
                                st.session_state.active_tab = "Dashboard"
                            
                            # Load data kloter aktif
                            st.session_state.df = load_kloter_data(st.session_state.current_kloter)
                            
                            st.success(f"Login berhasil! Selamat datang, {username}")
                            # time.sleep(1) # Removed for performance
                            st.rerun()
                        else:
                            users_df = load_users()
                            candidate = users_df[users_df["username"] == username]
                            if not candidate.empty:
                                suspend_mode = str(candidate.iloc[0].get("suspend_mode","none")).lower()
                                if suspend_mode == "login_block":
                                    st.error("Maaf, anda sedang dalam status di-banned sementara. Login diblokir.")
                                else:
                                    st.error("Username atau password salah!")
                            else:
                                st.error("Username atau password salah!")
                else:
                    st.warning("Harap isi username dan password")
        
        st.markdown('<div style="margin-top: 2rem; text-align: center; color: #888;">', unsafe_allow_html=True)
        st.caption("Default login: owner / admin123")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("🔒 Lupa Password Owner? Reset dengan Recovery Token", expanded=False):
            with st.form("owner_recovery_reset_form"):
                token_input = st.text_input("Recovery Token", type="password", key="owner_recovery_token_input")
                new_pw_reset = st.text_input("Password Baru", type="password", key="owner_recovery_new_pw")
                confirm_pw_reset = st.text_input("Konfirmasi Password Baru", type="password", key="owner_recovery_confirm_pw")
                submit_reset = st.form_submit_button("🔁 Reset Password Owner", type="primary")
                if submit_reset:
                    if not token_input or not new_pw_reset or not confirm_pw_reset:
                        st.error("Semua field wajib diisi.")
                    elif new_pw_reset != confirm_pw_reset:
                        st.error("Konfirmasi password tidak cocok.")
                    else:
                        ok, msg = reset_owner_password_with_token(token_input, new_pw_reset)
                        if ok:
                            st.success("Password owner berhasil direset. Silakan login ulang.")
                            st.session_state.authenticated = False
                            st.session_state.username = None
                            st.session_state.role = None
                            # time.sleep(1) # Removed for performance
                            st.rerun()
                        else:
                            st.error(msg)
        
        st.markdown('<div class="custom-footer">© 2025 Daluase Clothing Studio — Internal Management System</div>', unsafe_allow_html=True)

# ===================== PAGE: DASHBOARD =====================
def show_dashboard():
    """Dashboard utama dengan layout modern"""
    st.markdown(f"<h1 style='color: #D4AF37;'>🏠 Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #CCCCCC; font-size: 1.1rem;'>Selamat datang, <strong>{st.session_state.username}</strong>! 👋</p>", unsafe_allow_html=True)
    
    if st.session_state.get("suspend_mode","none") == "readonly" and (st.session_state.role or "").lower() != "owner":
        st.warning("Maaf, anda sedang di-banned sementara. Mode baca saja diaktifkan.")
    else:
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("➕ **Tambah Order**", use_container_width=True, type="primary"):
                st.session_state.active_tab = "Management Kloter"
                st.rerun()
        
        with col2:
            if st.button("📊 **Lihat Order**", use_container_width=True):
                st.session_state.active_tab = "Management Kloter"
                st.rerun()
        
        with col3:
            if st.button("💰 **Cek Piutang**", use_container_width=True):
                st.session_state.active_tab = "Kas & Analisis"
                st.rerun()
        
        with col4:
            if st.button("🏭 **Pantau Produksi**", use_container_width=True):
                st.session_state.active_tab = "Management Kloter"
                st.rerun()
    
    current_kloter = st.session_state.current_kloter
    kloter_status = load_kloter_lock_status(current_kloter)
    notes = kloter_status.get("notes", [])
    writers = kloter_status.get("writers", ["owner"])
    st.markdown("### 📣 Catatan Kloter")
    if notes:
        for note in sorted(notes, key=lambda n: n.get("created_at",""), reverse=True)[:10]:
            st.markdown(f"""
            <div class="order-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 3;">
                        <div style="color: #eee;">{note.get('message','')}</div>
                    </div>
                    <div style="flex: 1; text-align: right; color: #888; font-size: 0.8rem;">
                        {note.get('created_at','')} • {note.get('created_by','')}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("Belum ada catatan untuk kloter ini.")
    can_write = (st.session_state.role or "").lower() == "owner" or (st.session_state.username in writers)
    with st.form(f"add_kloter_note_{current_kloter}"):
        new_note = st.text_area("Tulis catatan/pengumuman", height=100, key=f"note_text_{current_kloter}")
        submitted = st.form_submit_button("💬 Publikasikan")
        if submitted:
            if not can_write:
                st.error("❌ Anda tidak memiliki izin untuk menulis catatan.")
            elif not new_note.strip():
                st.warning("Catatan tidak boleh kosong.")
            else:
                ok = add_kloter_note(current_kloter, new_note.strip(), st.session_state.username)
                if ok:
                    st.success("✅ Catatan dipublikasikan.")
                    st.rerun()
    if (st.session_state.role or "").lower() == "owner":
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("#### ✏️ Atur Penulis Catatan")
        users_df = load_users()
        active_users = users_df[users_df["status"] == "active"]["username"].tolist()
        if "owner" not in active_users:
            active_users = ["owner"] + active_users
        selected_writers = st.multiselect("Pilih anggota tim yang diizinkan menulis", active_users, default=writers, key=f"writers_select_{current_kloter}")
        if st.button("💾 Simpan Penulis", key=f"save_writers_{current_kloter}"):
            ok = set_kloter_writers(current_kloter, selected_writers)
            if ok:
                st.success("✅ Daftar penulis catatan diperbarui.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🤝 Profit Sharing Terakhir")
    history = load_profit_sharing_history(current_kloter)
    if not history.empty:
        latest_date = sorted(history["tanggal_perhitungan"].astype(str).unique())[-1]
        latest = history[history["tanggal_perhitungan"].astype(str) == latest_date]
        show = latest[["username","bagian_tetap","nilai_pool","total_diterima"]].copy()
        show = show.rename(columns={"username":"Username","bagian_tetap":"Bagian Tetap","nilai_pool":"Pool","total_diterima":"Total"})
        st.caption(f"Tanggal perhitungan: {latest_date}")
        st.dataframe(show.sort_values("Total", ascending=False), use_container_width=True)
    else:
        st.caption("Belum ada history untuk kloter ini.")
    
    st.markdown("### 📦 Info Stok")
    sr_file = STOCK_DIR / "stock_ready.csv"
    sp_file = STOCK_DIR / "stock_polos.csv"
    sd_file = STOCK_DIR / "stock_dtf.csv"
    try:
        if sr_file.exists() and sr_file.stat().st_size > 0:
            sr_df = pd.read_csv(sr_file)
        else:
            sr_df = pd.DataFrame()
    except:
        sr_df = pd.DataFrame()
    try:
        if sp_file.exists() and sp_file.stat().st_size > 0:
            sp_df = pd.read_csv(sp_file)
        else:
            sp_df = pd.DataFrame()
    except:
        sp_df = pd.DataFrame()
    try:
        if sd_file.exists() and sd_file.stat().st_size > 0:
            sd_df = pd.read_csv(sd_file)
        else:
            sd_df = pd.DataFrame()
    except:
        sd_df = pd.DataFrame()
    sr_total = int((sr_df['jumlah'].fillna(0).astype(int)).sum()) if not sr_df.empty and 'jumlah' in sr_df.columns else 0
    sp_total = int((sp_df['jumlah'].fillna(0).astype(int)).sum()) if not sp_df.empty and 'jumlah' in sp_df.columns else 0
    sd_total = int((sd_df['jumlah'].fillna(0).astype(int)).sum()) if not sd_df.empty and 'jumlah' in sd_df.columns else 0
    col_sr, col_sp, col_sd = st.columns(3)
    with col_sr:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{sr_total} pcs</div>
            <div class="metric-label">Stock Ready</div>
        </div>
        """, unsafe_allow_html=True)
    with col_sp:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{sp_total} pcs</div>
            <div class="metric-label">Stock Polos</div>
        </div>
        """, unsafe_allow_html=True)
    with col_sd:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{sd_total} pcs</div>
            <div class="metric-label">Stock DTF</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Poin Stock Bulan Ini")
    points_df = load_stock_points()
    if not points_df.empty:
        current_month = datetime.now().strftime("%Y-%m")
        try:
            points_df["month"] = pd.to_datetime(points_df["tanggal"]).dt.strftime("%Y-%m")
        except:
            points_df["month"] = ""
        month_points = points_df[points_df["month"] == current_month]
        user_points = month_points[month_points["username"] == st.session_state.username]
        if not user_points.empty:
            total_points = int(user_points["points_earned"].sum())
            total_commission = float(user_points["commission"].sum())
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🎯 Total Poin", total_points)
            with col2:
                st.metric("💰 Komisi", f"Rp {total_commission:,.0f}")
            with col3:
                all_points = int(month_points["points_earned"].sum())
                if all_points > 0:
                    percent = (total_points / all_points) * 100.0
                    st.metric("📊 % Share", f"{percent:.1f}%")
                else:
                    st.metric("📊 % Share", "0.0%")
        else:
            st.info("Belum ada poin stock bulan ini")
    else:
        st.info("Belum ada data poin stock")
 
    st.markdown("### 🎨 DTF (Ringkasan Kloter)")
    op = load_operational_data(st.session_state.current_kloter)
    dtf_meter = op.get("dtf_meter", op.get("panjang_dtf", 0.0))
    try:
        dtf_meter = float(str(dtf_meter).replace(",", "")) if str(dtf_meter).strip() else 0.0
    except:
        dtf_meter = 0.0
    desain_unik = int(op.get("dtf_unique_design_count", 0) or 0)
    biaya_dtf = int(op.get("biaya_dtf", 0) or 0)
    komisi_dtf = int(op.get("dtf_operator_commission", 0) or 0)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{dtf_meter:.1f} m</div>
            <div class="metric-label">DTF Meter Kloter Aktif</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"{desain_unik} desain unik")
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {komisi_dtf:,}</div>
            <div class="metric-label">Komisi Operator DTF</div>
        </div>
        """, unsafe_allow_html=True)
    # Summary metrics - MENGGUNAKAN FUNGSI DARI V4
    st.markdown("### 📊 Ringkasan Kloter")
    
    if not st.session_state.df.empty:
        total_orders = len(st.session_state.df)
        total_revenue = st.session_state.df["total_biaya"].sum()
        total_piutang = st.session_state.df["remaining_payment"].sum()
        pending_production = len(st.session_state.df[st.session_state.df["status_produksi"] == "PENDING"])
    else:
        total_orders = 0
        total_revenue = 0
        total_piutang = 0
        pending_production = 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_orders}</div>
            <div class="metric-label">Total Order</div>
            <div style="margin-top: 0.5rem; color: #888; font-size: 0.8rem;">Kloter: {st.session_state.current_kloter}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {total_revenue:,}</div>
            <div class="metric-label">Total Pendapatan</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {total_piutang:,}</div>
            <div class="metric-label">Total Piutang</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{pending_production}</div>
            <div class="metric-label">Pending Produksi</div>
        </div>
        """, unsafe_allow_html=True)

    def compute_total_asset():
        total = 0
        sr_file = STOCK_DIR / "stock_ready.csv"
        if sr_file.exists() and sr_file.stat().st_size > 0:
            try:
                sr = pd.read_csv(sr_file)
                if not sr.empty and {'harga_beli','jumlah'}.issubset(sr.columns):
                    total += (sr['harga_beli'].fillna(0).astype(float) * sr['jumlah'].fillna(0).astype(int)).sum()
            except:
                pass
        sp_file = STOCK_DIR / "stock_polos.csv"
        if sp_file.exists() and sp_file.stat().st_size > 0:
            try:
                sp = pd.read_csv(sp_file)
                if not sp.empty and {'harga_beli','jumlah'}.issubset(sp.columns):
                    total += (sp['harga_beli'].fillna(0).astype(float) * sp['jumlah'].fillna(0).astype(int)).sum()
            except:
                pass
        sd_file = STOCK_DIR / "stock_dtf.csv"
        if sd_file.exists() and sd_file.stat().st_size > 0:
            try:
                sd = pd.read_csv(sd_file)
                if not sd.empty and {'harga_beli','jumlah'}.issubset(sd.columns):
                    total += (sd['harga_beli'].fillna(0).astype(float) * sd['jumlah'].fillna(0).astype(int)).sum()
            except:
                pass
        settings = load_settings()
        pkg_prices = settings.get("packaging_prices", {})
        packaging_items = [{"nama": n, "harga": int(pkg_prices.get(n, 0))} for n in sorted(pkg_prices.keys())]
        packaging_file = STOCK_DIR / "packaging.json"
        if packaging_file.exists():
            try:
                with open(packaging_file, 'r') as f:
                    pdata = json.load(f)
                items = pdata.get('items', [])
                price_map = {i['nama']: i['harga'] for i in packaging_items}
                for it in items:
                    total += int(it.get('jumlah', 0) or 0) * int(price_map.get(it.get('item'), 0))
            except:
                pass
        return int(total)

    total_asset = compute_total_asset()
    st.markdown("### 📦 Total Asset")
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">Rp {total_asset:,}</div>
        <div class="metric-label">Total Asset</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent orders - MENGGUNAKAN FUNGSI DARI V4
    if not st.session_state.df.empty:
        st.markdown("### 📋 Order Terbaru")
        recent_orders = st.session_state.df.sort_values("tgl_order", ascending=False).head(6)
        
        # Tampilkan dalam bentuk cards modern
        cols = st.columns(2)
        for idx, order in recent_orders.iterrows():
            with cols[idx % 2]:
                payment_status = order['payment_status']
                status_class = "status-lunas" if payment_status == "LUNAS" else "status-panjar" if payment_status == "PANJAR" else "status-pending"
                
                prod_status = order['status_produksi']
                prod_class = "status-selesai" if prod_status == "SELESAI" else "status-proses" if prod_status == "PROSES" else "status-pending"
                
                st.markdown(f"""
                <div class="order-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <strong style="color: white; font-size: 1.1rem;">{order['nama_customer']}</strong><br>
                            <span style="color: #888; font-size: 0.9rem;">{order['nama_desain']} • {order['jenis_produk']}</span>
                        </div>
                        <div style="text-align: right;">
                            <strong style="color: #D4AF37; font-size: 1.1rem;">Rp {order['total_biaya']:,}</strong><br>
                            <span style="color: #888; font-size: 0.8rem;">{order['jumlah']} pcs</span>
                        </div>
                    </div>
                    <div style="margin-top: 1rem;">
                        <span class="status-badge {status_class}">{order['payment_status']}</span>
                        <span class="status-badge {prod_class}">{order['status_produksi']}</span>
                    </div>
                    <div style="margin-top: 0.5rem; color: #888; font-size: 0.8rem;">
                        {order['warna']} | {order['ukuran']} • {order['tgl_order'].split()[0]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ===================== PAGE: MANAGEMENT KLOTER =====================
def show_kloter_management():
    """Halaman management kloter dengan sidebar"""
    # Tampilkan sidebar
    kloter_menu = show_kloter_sidebar()
    
    # Tampilkan konten berdasarkan pilihan di sidebar
    # Cegah akses jika kloter dikunci untuk non-owner
    status = load_kloter_lock_status(st.session_state.current_kloter)
    locked = status.get("locked", False)
    if locked and (st.session_state.role or "").lower() != "owner":
        st.error("🔒 Kloter ini dikunci oleh Owner. Fitur tidak dapat digunakan.")
        return
    
    if kloter_menu == "➕ Tambah Order":
        show_add_order()
    elif kloter_menu == "📋 Data Order":
        show_data_order()
    elif kloter_menu == "✅ Approval Order Sales":
        show_sales_approval_page()
    elif kloter_menu == "🏭 Production":
        show_production_page()
    elif kloter_menu == "🚚 Distribution":
        show_distribution_page()
    elif kloter_menu == "💰 Operasional":
        show_operational_enhanced()
    elif kloter_menu == "📈 Profit":
        show_profit()
    elif kloter_menu == "📋 Laporan Pembagian":
        show_profit_sharing_report()
    elif kloter_menu == "🧾 Struk & Invoice":
        show_receipt_invoice()
    elif kloter_menu == "👥 Data Pelanggan":
        show_customers()
    elif kloter_menu == "📊 Rekapan Kloter":
        show_kloter_summary()
    elif kloter_menu == "👥 Kontribusi Sales":
        show_sales_contrib_admin()

# ===================== FUNGSI-FUNGSI YANG DIPERBAIKI =====================

# ===================== SUBPAGE: TAMBAH ORDER =====================
def show_add_order():
    """Tambah order dengan form yang tidak reset - DARI V4"""
    st.markdown(f"<h2 style='color: #D4AF37;'>➕ Add New Order</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #888;'>Batch: <strong>{st.session_state.current_kloter}</strong></p>", unsafe_allow_html=True)
    
    # Load settings untuk produk
    settings = load_settings()
    products = list(settings.get("products", {}).keys())
    prices = settings.get("prices", {})
    sizes = settings.get("sizes", {})
    colors = settings.get("colors", {})
    
    # Load daftar pelanggan untuk reuse data
    customers_df = None
    customer_options = ["New Customer"]
    customer_option_map = {}
    if CUSTOMERS_FILE.exists() and CUSTOMERS_FILE.stat().st_size > 0:
        customers_df = pd.read_csv(CUSTOMERS_FILE)
        for idx, row in customers_df.iterrows():
            display = f"{row.get('nama_customer','')} ({row.get('telepon','')})"
            customer_options.append(display)
            customer_option_map[display] = idx
    
    if not products:
        st.warning("No products defined. Please add products in Settings first.")
        return
    
    # Pilih mode desain di luar form agar toggle langsung responsif
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">🎨 Design Type</div>', unsafe_allow_html=True)
    design_mode = st.radio(
        "Select Design Type",
        ["DS ORIGINAL", "CUST. REQUEST", "CUSTMR. DESIGN", "ORIGINAL - EDIT"],
        index=0,
        horizontal=True,
        key="design_mode"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Form dengan styling modern
    with st.form("add_order_form", clear_on_submit=False):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown('<div class="form-title">👤 Customer Data</div>', unsafe_allow_html=True)
            
            selected_customer_display = st.selectbox("Select Customer", customer_options, index=0)
            prefill_nama = ""
            prefill_alamat = ""
            prefill_telepon = ""
            if selected_customer_display != "New Customer" and customers_df is not None:
                sel_idx = customer_option_map.get(selected_customer_display, None)
                if sel_idx is not None:
                    prefill_nama = str(customers_df.at[sel_idx, "nama_customer"])
                    prefill_alamat = str(customers_df.at[sel_idx, "alamat"])
                    prefill_telepon = str(customers_df.at[sel_idx, "telepon"])
            
            nama_customer = st.text_input("Customer Name*", 
                                         placeholder="Customer full name",
                                         value=prefill_nama)
            
            alamat_customer = st.text_area("Customer Address", 
                                          placeholder="Full address for delivery",
                                          height=80,
                                          value=prefill_alamat)
            
            telepon_customer = st.text_input("Customer Phone", 
                                            placeholder="Phone/WhatsApp number",
                                            value=prefill_telepon)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown('<div class="form-title">🎨 Design Data</div>', unsafe_allow_html=True)

            original_options = settings.get("original_designs", [])
            tipe_desain = st.session_state.get("design_mode", "DS ORIGINAL")

            nama_desain = ""
            design_upload = None
            if tipe_desain == "DS ORIGINAL" and original_options:
                nama_desain = st.selectbox("Design Name*", original_options, key="order_design_name")
                files_map = settings.get("original_design_files", {})
                fname = files_map.get(nama_desain, "")
                if fname:
                    fp = ORIGINAL_DESIGNS_DIR / fname
                    if fp.exists() and str(fp).lower().endswith((".png",".jpg",".jpeg",".gif")):
                        st.image(str(fp), caption=nama_desain, use_column_width=True)
                    elif fp.exists() and str(fp).lower().endswith(".pdf"):
                        st.caption(f"PDF file available: {fname}")
            else:
                nama_desain = st.text_input("Design Name / Code*", placeholder="Design name or code")
                design_upload = st.file_uploader("Upload Design (optional)", type=["png","jpg","jpeg","pdf"], key="order_design_upload")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown('<div class="form-title">👕 Product Data</div>', unsafe_allow_html=True)
            
            jenis_produk = st.selectbox("Product Type*", products)
            
            # Warna: tampilkan semua warna, validasi terhadap produk
            warna = st.selectbox("Color*", COMPLETE_COLORS)
            available_colors_for_product = colors.get(jenis_produk, [])
            invalid_color = False
            if available_colors_for_product and warna not in available_colors_for_product:
                st.warning("Color is not available for this product")
                invalid_color = True
            
            # Ukuran: tampilkan semua opsi XS-5XL, tetapi validasi terhadap produk
            all_sizes = ["XS","S","M","L","XL","2XL","3XL","4XL","5XL"]
            ukuran = st.selectbox("Size*", all_sizes)
            available_sizes_for_product = sizes.get(jenis_produk, [])
            invalid_size = False
            if available_sizes_for_product and ukuran not in available_sizes_for_product:
                st.warning("Size is not available for this product")
                invalid_size = True
            
            jumlah = st.number_input("Quantity (pcs)*", min_value=1, value=1, step=1)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown('<div class="form-title">💰 Payment</div>', unsafe_allow_html=True)
            
            diskon_lusin_option = st.selectbox("Dozen Discount", 
                                              ["None", "2 Dozen", "3 Dozen"])
            
            bayar = st.number_input("Payment / Down Payment (Rp)*", 
                                   min_value=0, 
                                   value=0, 
                                   step=1000,
                                   help="Enter 0 if unpaid")
            
            keterangan = st.text_area("Additional Notes", 
                                     height=100,
                                     placeholder="Additional notes about this order")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close custom-card
        
        st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            col_cek, col_submit = st.columns(2)
            
            with col_cek:
                check_total_clicked = st.form_submit_button("🔍 **Check Total**", type="secondary", use_container_width=True)
            
            with col_submit:
                submit_order = st.form_submit_button("✅ **Add Order**", type="primary", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Cek total jika tombol ditekan
        if check_total_clicked:
            if invalid_size:
                st.warning("Size is not available for this product")
            elif invalid_color:
                st.warning("Color is not available for this product")
            elif not nama_customer or not nama_desain or not tipe_desain:
                st.warning("⚠️ Please fill Customer Name and Design Name")
            else:
                # Hitung harga
                base_price = prices.get(jenis_produk, 0)
                diskon_map = {"2 Dozen": 5000, "3 Dozen": 10000, "None": 0}
                diskon = diskon_map.get(diskon_lusin_option, 0)
                
                # Extra untuk ukuran besar
                size_extra = 0
                if ukuran == "3XL":
                    size_extra = 5000
                elif ukuran == "4XL":
                    size_extra = 10000
                elif ukuran == "5XL":
                    size_extra = 15000
                
                harga_per_pcs = base_price + size_extra - diskon
                total_biaya = harga_per_pcs * jumlah
                
                with st.container(border=True):
                    st.markdown("### 📊 Preview Order")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Customer:** {nama_customer}")
                        st.write(f"**Design:** {nama_desain} ({tipe_desain})")
                        st.write(f"**Product:** {jenis_produk}")
                        st.write(f"**Specs:** {warna} | {ukuran} | {jumlah} pcs")
                    
                    with col2:
                        st.write(f"**Price per piece:** Rp {harga_per_pcs:,}")
                        st.write(f"**Discount per piece:** Rp {diskon:,}")
                        st.write(f"**Total cost:** **Rp {total_biaya:,}**")
        
        # Submit order
        if submit_order:
            if invalid_size:
                st.error("❌ Size is not available for this product")
            elif invalid_color:
                st.error("❌ Color is not available for this product")
            elif not nama_customer or not nama_desain or not tipe_desain:
                st.error("❌ Please fill Customer Name and Design Name")
            else:
                # Hitung harga
                base_price = prices.get(jenis_produk, 0)
                diskon_map = {"2 Dozen": 5000, "3 Dozen": 10000, "None": 0}
                diskon = diskon_map.get(diskon_lusin_option, 0)
                
                size_extra = 0
                if ukuran == "3XL":
                    size_extra = 5000
                elif ukuran == "4XL":
                    size_extra = 10000
                elif ukuran == "5XL":
                    size_extra = 15000
                
                harga_per_pcs = base_price + size_extra - diskon
                total_biaya = harga_per_pcs * jumlah
                remaining = max(total_biaya - bayar, 0)
                
                # Tentukan status pembayaran
                if bayar >= total_biaya:
                    payment_status = "LUNAS"
                elif bayar > 0:
                    payment_status = "PANJAR"
                else:
                    payment_status = "BELUM BAYAR"
                
                # Generate invoice number
                invoice_number = generate_invoice_number(st.session_state.current_kloter)
                
                # Tambah ke data pelanggan jika belum ada
                if telepon_customer:
                    add_customer_if_not_exists(nama_customer, telepon_customer, alamat_customer)
                
                # Hitung harga beli produk untuk operasional
                harga_beli_per_pcs = calculate_product_buy_price(jenis_produk, warna, ukuran)
                
                # Buat order baru
                new_order = pd.DataFrame([{
                    "tgl_order": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "nama_customer": nama_customer,
                    "alamat_customer": alamat_customer,
                    "telepon_customer": telepon_customer,
                    "nama_desain": nama_desain,
                    "tipe_desain": tipe_desain,
                    "jenis_produk": jenis_produk,
                    "warna": warna,
                    "ukuran": ukuran,
                    "jumlah": int(jumlah),
                    "harga_per_pcs": harga_per_pcs,
                    "harga_beli_per_pcs": harga_beli_per_pcs,
                    "total_harga_beli": harga_beli_per_pcs * jumlah,
                    "diskon_lusin": diskon,
                    "total_biaya": total_biaya,
                    "total_bayar": bayar,
                    "remaining_payment": remaining,
                    "payment_status": payment_status,
                    "status_produksi": "PENDING",
                    "status_distribusi": "BELUM KIRIM",
                    "keterangan_lainnya": keterangan,
                    "kloter_id": st.session_state.current_kloter,
                    "invoice_number": invoice_number,
                    "created_by": st.session_state.username
                }])
                
                # Simpan desain custom/edit per order jika ada upload
                if design_upload is not None:
                    ext = Path(design_upload.name).suffix.lower()
                    content, err = prepare_upload_bytes(design_upload, ext)
                    if err:
                        st.error(err)
                    else:
                        safe_invoice = re.sub(r"[^a-zA-Z0-9_-]+", "_", invoice_number)
                        dest_dir = ORDER_DESIGNS_DIR / safe_invoice
                        dest_dir.mkdir(exist_ok=True, parents=True)
                        dest = dest_dir / f"design{ext}"
                        with open(dest, "wb") as f:
                            f.write(content)
                        new_order.loc[0, "design_file"] = str(dest)
                        new_order.loc[0, "design_source"] = "original-edit" if tipe_desain == "DS ORIGINAL - EDIT" else "custom"
                elif tipe_desain in ["DS ORIGINAL"]:
                    files_map = settings.get("original_design_files", {})
                    fname = files_map.get(nama_desain, "")
                    if fname:
                        new_order.loc[0, "design_file"] = str(ORIGINAL_DESIGNS_DIR / fname)
                        new_order.loc[0, "design_source"] = "original"
                
                # Tambah ke session state
                if st.session_state.df.empty:
                    st.session_state.df = new_order
                else:
                    st.session_state.df = pd.concat([st.session_state.df, new_order], ignore_index=True)
                
                # Simpan ke file
                save_kloter_data(st.session_state.current_kloter, st.session_state.df)
                
                st.success(f"""
                ✅ Order added!
                - **Customer:** {nama_customer}
                - **Invoice:** {invoice_number}
                - **Total:** **Rp {total_biaya:,}**
                - **Status:** **{payment_status}**
                """)
                # time.sleep(1) # Removed for performance
                st.rerun()

def show_sales_add_order():
    if not ((st.session_state.role or "").lower() == "sales" or check_capability("SALES_ADD_ORDER")):
        st.error("❌ Akses ditolak.")
        return
    st.markdown(f"<h2 style='color: #D4AF37;'>📝 Tambah Order Sales</h2>", unsafe_allow_html=True)
    settings = load_settings()
    products = list(settings.get("products", {}).keys())
    sizes = settings.get("sizes", {})
    colors = settings.get("colors", {})
    with st.form("sales_add_order_form", clear_on_submit=True):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            nama_customer = st.text_input("Nama Customer")
            telepon_customer = st.text_input("Telepon")
            alamat_customer = st.text_area("Alamat", height=80)
            nama_desain = st.text_input("Nama Desain")
            tipe_desain = st.selectbox("Tipe Desain", ["DS ORIGINAL", "CUST. REQUEST", "CUSTMR. DESIGN", "DS ORIGINAL - EDIT"])
        with col2:
            jenis_produk = st.selectbox("Jenis Produk", products)
            warna = st.selectbox("Warna", colors.get(jenis_produk, COMPLETE_COLORS))
            ukuran = st.selectbox("Ukuran", sizes.get(jenis_produk, ["S","M","L","XL","2XL","3XL","4XL","5XL"]))
            jumlah = st.number_input("Jumlah (pcs)", min_value=1, value=1, step=1)
            keterangan = st.text_area("Keterangan Tambahan", height=80)
            design_upload = st.file_uploader("Upload Desain (opsional)", type=["png","jpg","jpeg","pdf"])
        st.markdown('</div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("Kirim Order ke Admin", type="primary", use_container_width=True)
        if submitted:
            try:
                timestamp = int(time.time())
                file_name = f"sales_order_{st.session_state.username}_{timestamp}.csv"
                dest_file = SALES_PENDING_DIR / file_name
                df = pd.DataFrame([{
                    "tgl_order": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "sales_username": st.session_state.username,
                    "nama_customer": nama_customer,
                    "telepon_customer": telepon_customer,
                    "alamat_customer": alamat_customer,
                    "nama_desain": nama_desain,
                    "tipe_desain": tipe_desain,
                    "jenis_produk": jenis_produk,
                    "warna": warna,
                    "ukuran": ukuran,
                    "jumlah": int(jumlah),
                    "keterangan": keterangan,
                    "status": "PENDING_APPROVAL",
                    "sales_commission": 7000,
                    "created_by": st.session_state.username
                }])
                df.to_csv(dest_file, index=False)
                if design_upload is not None:
                    ext = Path(design_upload.name).suffix.lower()
                    content, err = prepare_upload_bytes(design_upload, ext)
                    if err:
                        st.error(err)
                    else:
                        design_dest = ORDER_DESIGNS_DIR / f"{Path(file_name).stem}{ext}"
                        with open(design_dest, "wb") as f:
                            f.write(content)
                st.success("✅ Order sales dikirim untuk persetujuan admin.")
                # time.sleep(1) # Removed for performance
                st.session_state.active_tab = "SalesOrders"
                st.rerun()
            except Exception as e:
                st.error(f"Gagal menyimpan order: {e}")

def show_sales_orders():
    if not ((st.session_state.role or "").lower() == "sales" or check_capability("SALES_VIEW_ORDERS")):
        st.error("❌ Akses ditolak.")
        return
    st.markdown(f"<h2 style='color: #D4AF37;'>📋 Orderan Saya</h2>", unsafe_allow_html=True)
    pending_files = list(SALES_PENDING_DIR.glob("sales_order_*.csv"))
    pending_rows = []
    for f in pending_files:
        try:
            df = pd.read_csv(f)
            df["__srcfile"] = f.name
            df = df[df["sales_username"] == st.session_state.username]
            if not df.empty:
                pending_rows.append(df)
        except:
            pass
    if pending_rows:
        pending_df = pd.concat(pending_rows, ignore_index=True)
    else:
        pending_df = pd.DataFrame(columns=[
            "tgl_order","sales_username","nama_customer","telepon_customer","alamat_customer",
            "nama_desain","tipe_desain","jenis_produk","warna","ukuran","jumlah","keterangan","status","sales_commission","__srcfile"
        ])
    approved_orders = []
    for f in ORDERS_DIR.glob("K*.csv"):
        try:
            dfk = pd.read_csv(f)
            if "sales_username" in dfk.columns:
                mine = dfk[dfk["sales_username"] == st.session_state.username].copy()
                if not mine.empty:
                    mine["kloter_id"] = f.stem
                    approved_orders.append(mine)
        except:
            pass
    if approved_orders:
        approved_df = pd.concat(approved_orders, ignore_index=True)
    else:
        approved_df = pd.DataFrame(columns=[
            "tgl_order","nama_customer","nama_desain","jenis_produk","warna","ukuran","jumlah","total_biaya","payment_status","invoice_number","kloter_id"
        ])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Pending Approval**")
        st.dataframe(pending_df[["tgl_order","nama_customer","jenis_produk","jumlah","status"]], use_container_width=True)
    with col2:
        st.markdown("**Sudah Diapprove**")
        st.dataframe(approved_df[["tgl_order","nama_customer","jenis_produk","jumlah","total_biaya","invoice_number","kloter_id"]], use_container_width=True)
    total_approved = len(approved_df) if not approved_df.empty else 0
    total_commission = total_approved * 7000
    st.markdown("---")
    st.markdown(f"**Total Diapprove:** {total_approved}")
    st.markdown(f"**Total Komisi:** Rp {total_commission:,}")

def show_sales_approval_page():
    if not (check_capability("APPROVE_SALES_ORDER") or (st.session_state.role or "").lower() == "owner"):
        st.error("❌ Akses ditolak.")
        return
    st.markdown(f"<h2 style='color: #D4AF37;'>✅ Approval Order Sales</h2>", unsafe_allow_html=True)
    files = list(SALES_PENDING_DIR.glob("sales_order_*.csv"))
    if not files:
        st.info("Tidak ada order sales pending.")
        return
    all_kloters = get_all_kloters()
    for f in files:
        try:
            df = pd.read_csv(f)
            row = df.iloc[0].to_dict()
        except:
            continue
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown(f"**{row.get('nama_customer','-')}** • {row.get('jenis_produk','-')} • {row.get('jumlah',0)} pcs")
        st.caption(f"Sales: {row.get('sales_username','-')} • Tgl: {row.get('tgl_order','-')}")
        kloter_choice = st.selectbox("Pilih Kloter", all_kloters, key=f"kloter_for_{f.name}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Setujui", key=f"approve_{f.name}", type="primary", use_container_width=True):
                try:
                    settings = load_settings()
                    base_price = int(settings.get("prices", {}).get(row["jenis_produk"], 0))
                    size_extra = 0
                    if str(row.get("ukuran","")).upper() in ["3XL","4XL","5XL"]:
                        size_extra = {"3XL": 5000, "4XL": 10000, "5XL": 15000}.get(str(row.get("ukuran","")).upper(), 0)
                    harga_per_pcs = base_price + size_extra
                    jumlah = int(row.get("jumlah", 1))
                    total_biaya = harga_per_pcs * jumlah
                    harga_beli_per_pcs = calculate_product_buy_price(row["jenis_produk"], row.get("warna",""), row.get("ukuran",""))
                    total_harga_beli = harga_beli_per_pcs * jumlah
                    invoice_number = generate_invoice_number(kloter_choice)
                    new_order = pd.DataFrame([{
                        "tgl_order": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "nama_customer": row.get("nama_customer",""),
                        "alamat_customer": row.get("alamat_customer",""),
                        "telepon_customer": row.get("telepon_customer",""),
                        "nama_desain": row.get("nama_desain",""),
                        "tipe_desain": row.get("tipe_desain",""),
                        "jenis_produk": row.get("jenis_produk",""),
                        "warna": row.get("warna",""),
                        "ukuran": row.get("ukuran",""),
                        "jumlah": jumlah,
                        "harga_per_pcs": harga_per_pcs,
                        "harga_beli_per_pcs": harga_beli_per_pcs,
                        "total_harga_beli": total_harga_beli,
                        "diskon_lusin": 0,
                        "total_biaya": total_biaya,
                        "total_bayar": 0,
                        "remaining_payment": total_biaya,
                        "payment_status": "BELUM BAYAR",
                        "status_produksi": "PENDING",
                        "status_distribusi": "BELUM KIRIM",
                        "keterangan_lainnya": row.get("keterangan",""),
                        "kloter_id": kloter_choice,
                        "invoice_number": invoice_number,
                        "created_by": st.session_state.username,
                        "sales_username": row.get("sales_username","")
                    }])
                    target_path = ORDERS_DIR / f"{kloter_choice}.csv"
                    if target_path.exists() and target_path.stat().st_size > 0:
                        current_df = pd.read_csv(target_path)
                    else:
                        current_df = pd.DataFrame()
                    merged = pd.concat([current_df, new_order], ignore_index=True)
                    save_kloter_data(kloter_choice, merged)
                    approved_file = SALES_APPROVED_DIR / f"approved_{Path(f.name).stem}.csv"
                    out = pd.DataFrame([{
                        "invoice_number": invoice_number,
                        "kloter_id": kloter_choice,
                        "sales_username": row.get("sales_username",""),
                        "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "approved_by": st.session_state.username,
                        "total_biaya": total_biaya
                    }])
                    out.to_csv(approved_file, index=False)
                    try:
                        notif_file = SALES_NOTIFICATIONS_DIR / f"sales_notifications_{row.get('sales_username','')}.json"
                        existing = []
                        if notif_file.exists() and notif_file.stat().st_size > 0:
                            with open(notif_file, "r") as nf:
                                existing = json.load(nf)
                        existing.append({
                            "type": "APPROVED",
                            "invoice_number": invoice_number,
                            "kloter_id": kloter_choice,
                            "message": "Order Anda disetujui",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                        with open(notif_file, "w") as nf:
                            json.dump(existing, nf, indent=2)
                    except:
                        pass
                    try:
                        op = load_operational_data(kloter_choice)
                        lain = op.get("biaya_lainnya", [])
                        lain.append({"keterangan": f"Komisi Sales {row.get('sales_username','')}", "jumlah": 7000})
                        op["biaya_lainnya"] = lain
                        try:
                            t = int(float(str(op.get("total", 0)).replace(",", ""))) if str(op.get("total", 0)).strip() else 0
                        except:
                            t = 0
                        op["total"] = t + 7000
                        op["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        op["updated_by"] = st.session_state.username
                        save_operational_data(kloter_choice, op)
                    except:
                        pass
                    try:
                        record_cash_flow("KOMISI SALES", 7000, "OUT", f"Komisi {row.get('sales_username','')} untuk {invoice_number}", kloter_choice)
                    except:
                        pass
                    try:
                        f.unlink()
                    except:
                        pass
                    st.success(f"✅ Disetujui • {invoice_number}")
                    # time.sleep(1) # Removed for performance
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal menyetujui: {e}")
        with col2:
            if st.button("Tolak", key=f"reject_{f.name}", use_container_width=True):
                try:
                    notif_file = SALES_NOTIFICATIONS_DIR / f"sales_notifications_{row.get('sales_username','')}.json"
                    existing = []
                    if notif_file.exists() and notif_file.stat().st_size > 0:
                        with open(notif_file, "r") as nf:
                            existing = json.load(nf)
                    existing.append({
                        "type": "REJECTED",
                        "invoice_number": None,
                        "kloter_id": None,
                        "message": "Order Anda ditolak",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    with open(notif_file, "w") as nf:
                        json.dump(existing, nf, indent=2)
                except:
                    pass
                try:
                    f.unlink()
                except:
                    pass
                st.info("Order ditolak")
                # time.sleep(1) # Removed for performance
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def show_sales_contrib_admin():
    if not ((st.session_state.role or "").lower() == "owner" or check_capability("APPROVE_SALES_ORDER")):
        st.error("❌ Akses ditolak.")
        return
    st.markdown(f"<h2 style='color: #D4AF37;'>👥 Kontribusi Sales</h2>", unsafe_allow_html=True)
    rows = []
    for f in ORDERS_DIR.glob("K*.csv"):
        try:
            df = pd.read_csv(f)
            if "sales_username" in df.columns:
                df = df[~df["sales_username"].isna()]
                if not df.empty:
                    rows.append(df)
        except:
            pass
    if rows:
        all_df = pd.concat(rows, ignore_index=True)
        summary = all_df.groupby("sales_username").agg({
            "invoice_number": "count",
            "total_biaya": "sum"
        }).reset_index().rename(columns={"invoice_number": "approved_orders"})
        summary["estimated_commission"] = summary["approved_orders"].astype(int) * 7000
        st.dataframe(summary[["sales_username","approved_orders","estimated_commission","total_biaya"]], use_container_width=True)
        csv = summary.to_csv(index=False).encode("utf-8")
        st.download_button("Unduh Rekap Sales (CSV)", data=csv, file_name="rekap_sales.csv", mime="text/csv")
    else:
        st.info("Belum ada kontribusi sales.")

def add_customer_if_not_exists(nama, telepon, alamat):
    """Tambahkan pelanggan baru jika belum ada - DARI V4"""
    # Load existing customers
    if CUSTOMERS_FILE.exists() and CUSTOMERS_FILE.stat().st_size > 0:
        customers_df = pd.read_csv(CUSTOMERS_FILE)
    else:
        customers_df = pd.DataFrame(columns=[
            "nama_customer", "telepon", "alamat", "total_order", 
            "total_belanja", "tgl_pertama", "tgl_terakhir"
        ])
    
    # Cek apakah pelanggan sudah ada
    if telepon and telepon in customers_df["telepon"].values:
        # Update existing customer
        mask = customers_df["telepon"] == telepon
        customers_df.loc[mask, "alamat"] = alamat
        customers_df.loc[mask, "tgl_terakhir"] = datetime.now().strftime("%Y-%m-%d")
        customers_df.loc[mask, "total_order"] += 1
    else:
        # Add new customer
        new_customer = pd.DataFrame([{
            "nama_customer": nama,
            "telepon": telepon,
            "alamat": alamat,
            "total_order": 1,
            "total_belanja": 0,
            "tgl_pertama": datetime.now().strftime("%Y-%m-%d"),
            "tgl_terakhir": datetime.now().strftime("%Y-%m-%d")
        }])
        customers_df = pd.concat([customers_df, new_customer], ignore_index=True)
    
    customers_df.to_csv(CUSTOMERS_FILE, index=False)

def delete_customer_record(nama=None, telepon=None):
    """Hapus data pelanggan berdasarkan telepon (prioritas) atau nama"""
    if CUSTOMERS_FILE.exists() and CUSTOMERS_FILE.stat().st_size > 0:
        customers_df = pd.read_csv(CUSTOMERS_FILE)
    else:
        return False
    if telepon and telepon in customers_df["telepon"].values:
        customers_df = customers_df[customers_df["telepon"] != telepon]
    elif nama:
        customers_df = customers_df[customers_df["nama_customer"] != nama]
    else:
        return False
    customers_df.to_csv(CUSTOMERS_FILE, index=False)
    return True

# ===================== SUBPAGE: DATA ORDER (DIPERBAIKI) =====================
def show_data_order():
    """Halaman data order dengan fitur lengkap yang sudah diperbaiki"""
    st.markdown(f"<h2 style='color: #D4AF37;'>📋 Data Order</h2>", unsafe_allow_html=True)
    
    if st.session_state.df.empty:
        st.info("Belum ada order. Tambahkan di halaman 'Tambah Order'.")
        return
    
    # Filters dengan styling modern
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_status = st.selectbox(
            "Status Bayar",
            ["Semua", "LUNAS", "PANJAR", "BELUM BAYAR"],
            key="filter_status_order"
        )
    
    with col2:
        filter_produksi = st.selectbox(
            "Status Produksi",
            ["Semua", "PENDING", "PROSES", "SELESAI"],
            key="filter_produksi_order"
        )
    
    with col3:
        filter_distribusi = st.selectbox(
            "Status Distribusi",
            ["Semua", "BELUM KIRIM", "SEDANG KIRIM", "TERKIRIM"],
            key="filter_distribusi_order"
        )
    
    with col4:
        search_term = st.text_input("🔍 Cari (nama/desain/invoice)", key="search_order")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = st.session_state.df.copy()
    
    if filter_status != "Semua":
        filtered_df = filtered_df[filtered_df["payment_status"] == filter_status]
    
    if filter_produksi != "Semua":
        filtered_df = filtered_df[filtered_df["status_produksi"] == filter_produksi]
    
    if filter_distribusi != "Semua":
        filtered_df = filtered_df[filtered_df["status_distribusi"] == filter_distribusi]
    
    if search_term:
        mask = (filtered_df["nama_customer"].str.contains(search_term, case=False) |
                filtered_df["nama_desain"].str.contains(search_term, case=False) |
                filtered_df["invoice_number"].str.contains(search_term, case=False))
        filtered_df = filtered_df[mask]
    
    # Summary dengan styling modern
    total_orders = len(filtered_df)
    total_revenue = filtered_df["total_biaya"].sum()
    total_piutang = filtered_df["remaining_payment"].sum()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_orders}</div>
            <div class="metric-label">Total Order</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {total_revenue:,}</div>
            <div class="metric-label">Total Pendapatan</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {total_piutang:,}</div>
            <div class="metric-label">Total Piutang</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Tombol aksi cepat
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export ke Excel", use_container_width=True, key="export_excel_order"):
            export_to_excel(filtered_df)
    
    with col2:
        if st.button("📊 Analisis", use_container_width=True, key="analisis_order"):
            # Pindah ke tab Profit
            show_profit()
    
    with col3:
        if st.button("🔄 Refresh Data", use_container_width=True, key="refresh_order"):
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown(f"### 📋 Daftar Order ({len(filtered_df)} order)")
    if filtered_df.empty:
        st.info("Tidak ada order yang sesuai dengan filter.")
        return
    display_df = filtered_df[[
        "tgl_order","nama_customer","nama_desain","jenis_produk","warna","ukuran","jumlah",
        "harga_per_pcs","total_biaya","total_bayar","remaining_payment","payment_status",
        "status_produksi","status_distribusi","invoice_number","created_by"
    ]].copy()
    st.dataframe(display_df.sort_values("tgl_order", ascending=False), use_container_width=True)
    st.markdown("---")
    order_list = filtered_df.copy()
    order_list["display"] = order_list.apply(
        lambda x: f"{x['invoice_number']} - {x['nama_customer']} - Rp {x['total_biaya']:,}",
        axis=1
    )
    selected_display = st.selectbox("Pilih Order", order_list["display"].tolist(), key="select_order_for_action")
    actions = st.radio("Aksi", ["Pelunasan", "Approval Pelunasan", "Edit", "Hapus", "Lihat Desain"], horizontal=True, key="order_actions")
    if selected_display:
        selected_idx = order_list[order_list["display"] == selected_display].index[0]
        selected_invoice = order_list.loc[selected_idx, "invoice_number"]
        if actions == "Pelunasan":
            handle_payment_for_invoice(selected_invoice)
        elif actions == "Approval Pelunasan":
            handle_payment_approval_for_invoice(selected_invoice)
        elif actions == "Edit":
            handle_edit_for_invoice(selected_invoice)
        elif actions == "Hapus":
            handle_delete_for_invoice(selected_invoice)
        elif actions == "Lihat Desain":
            show_design_view_for_invoice(selected_invoice)

def show_order_actions(idx, order):
    return ""

def handle_payment_for_invoice(invoice_number):
    df = st.session_state.df
    if df.empty:
        return
    if not check_capability("ORDER_PAY"):
        st.error("❌ Anda tidak memiliki izin untuk melakukan pelunasan order.")
        return
    order_idx = df[df["invoice_number"] == invoice_number].index[0]
    order = df.loc[order_idx]
    with st.form(f"payment_form_single_{invoice_number}"):
        st.markdown(f"### Pelunasan: {invoice_number}")
        st.write(f"Total: Rp {order['total_biaya']:,}")
        st.write(f"Sudah Bayar: Rp {order['total_bayar']:,}")
        st.write(f"Sisa: Rp {order['remaining_payment']:,}")
        jumlah_bayar = st.number_input("Jumlah Bayar (Rp)", min_value=0, max_value=int(order['remaining_payment']), value=int(order['remaining_payment']), step=1000, key=f"jumlah_bayar_single_{invoice_number}")
        metode_bayar = st.selectbox("Metode Bayar", ["CASH","TRANSFER","QRIS"], key=f"metode_bayar_single_{invoice_number}")
        keterangan_bayar = st.text_input("Keterangan", key=f"ket_bayar_single_{invoice_number}")
        proof = st.file_uploader("Upload Bukti Pelunasan (opsional)", type=["png","jpg","jpeg","pdf"], key=f"proof_{invoice_number}")
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Proses"):
                process_payment(order_idx, jumlah_bayar, metode_bayar, keterangan_bayar)
                if proof:
                    ext = Path(proof.name).suffix.lower()
                    content, err = prepare_upload_bytes(proof, ext)
                    if err:
                        st.error(err)
                    else:
                        dest = PAYMENT_PROOFS_DIR / f"{invoice_number}{ext}"
                        with open(dest, "wb") as f:
                            f.write(content)
                        st.session_state.df.at[order_idx, "payment_proof_file"] = str(dest)
                        st.session_state.df.at[order_idx, "payment_approval_status"] = "PENDING"
                        save_kloter_data(st.session_state.current_kloter, st.session_state.df)
                st.rerun()
        with col2:
            if st.form_submit_button("Batal"):
                st.rerun()

def handle_payment_approval_for_invoice(invoice_number):
    if (st.session_state.role or "").lower() != "owner":
        st.error("❌ Hanya owner yang dapat approval pelunasan.")
        return
    df = st.session_state.df
    if df.empty:
        return
    order_idx = df[df["invoice_number"] == invoice_number].index[0]
    order = df.loc[order_idx]
    proof = order.get("payment_proof_file", "")
    with st.form(f"approval_form_single_{invoice_number}"):
        st.markdown(f"### Approval Pelunasan: {invoice_number}")
        if proof and Path(proof).exists():
            if str(proof).lower().endswith((".png",".jpg",".jpeg",".gif")):
                st.image(proof, caption="Bukti Pelunasan", use_column_width=True)
            else:
                st.caption(f"Bukti tersedia: {Path(proof).name}")
        else:
            st.warning("Belum ada bukti pelunasan terupload.")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.form_submit_button("✅ Approve", type="primary"):
                st.session_state.df.at[order_idx, "payment_approval_status"] = "APPROVED"
                # Jika sudah lunas nominal, pastikan status LUNAS
                if st.session_state.df.at[order_idx, "remaining_payment"] <= 0:
                    st.session_state.df.at[order_idx, "payment_status"] = "LUNAS"
                save_kloter_data(st.session_state.current_kloter, st.session_state.df)
                st.success("✅ Pelunasan di-approve")
                # time.sleep(1) # Removed for performance
                st.rerun()
        with col2:
            if st.form_submit_button("❌ Reject"):
                st.session_state.df.at[order_idx, "payment_approval_status"] = "REJECTED"
                save_kloter_data(st.session_state.current_kloter, st.session_state.df)
                st.warning("Pelunasan ditolak")
                # time.sleep(1) # Removed for performance
                st.rerun()
        with col3:
            if st.form_submit_button("Batal"):
                st.rerun()

def show_design_view_for_invoice(invoice_number):
    df = st.session_state.df
    if df.empty:
        return
    order_idx = df[df["invoice_number"] == invoice_number].index[0]
    order = df.loc[order_idx]
    file = order.get("design_file", "")
    if file and Path(file).exists():
        if str(file).lower().endswith((".png",".jpg",".jpeg",".gif")):
            st.image(file, caption=f"Desain - {order['nama_desain']}", use_column_width=True)
        elif str(file).lower().endswith(".pdf"):
            with open(file, "rb") as f:
                st.download_button(
                    label="📥 Download Desain (PDF)",
                    data=f.read(),
                    file_name=Path(file).name,
                    mime="application/pdf",
                    key=f"download_design_{invoice_number}"
                )
        else:
            st.caption("Format desain tidak didukung untuk preview")
    else:
        st.info("Tidak ada file desain untuk order ini.")

def handle_edit_for_invoice(invoice_number):
    df = st.session_state.df
    if df.empty:
        return
    if not check_capability("ORDER_EDIT"):
        st.error("❌ Anda tidak memiliki izin untuk mengedit order.")
        return
    order_idx = df[df["invoice_number"] == invoice_number].index[0]
    order = df.loc[order_idx]
    with st.form(f"edit_form_single_{invoice_number}"):
        st.markdown(f"### Edit: {invoice_number}")
        col1, col2 = st.columns(2)
        with col1:
            nama_customer = st.text_input("Nama Customer", value=order['nama_customer'], key=f"edit_nama_single_{invoice_number}")
            alamat_customer = st.text_area("Alamat", value=order['alamat_customer'], height=80, key=f"edit_alamat_single_{invoice_number}")
            telepon_customer = st.text_input("Telepon", value=order['telepon_customer'], key=f"edit_telp_single_{invoice_number}")
        with col2:
            nama_desain = st.text_input("Nama Desain", value=order['nama_desain'], key=f"edit_desain_single_{invoice_number}")
            tipe_desain = st.selectbox("Tipe Desain", ["DS ORIGINAL","CUST. REQUEST","CUSTMR. DESIGN","DS ORIGINAL - EDIT"], index=["DS ORIGINAL","CUST. REQUEST","CUSTMR. DESIGN","DS ORIGINAL - EDIT"].index(order['tipe_desain']), key=f"edit_tipe_single_{invoice_number}")
            jumlah = st.number_input("Jumlah", min_value=1, value=int(order['jumlah']), key=f"edit_jumlah_single_{invoice_number}")
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Simpan"):
                st.session_state.df.at[order_idx, "nama_customer"] = nama_customer
                st.session_state.df.at[order_idx, "alamat_customer"] = alamat_customer
                st.session_state.df.at[order_idx, "telepon_customer"] = telepon_customer
                st.session_state.df.at[order_idx, "nama_desain"] = nama_desain
                st.session_state.df.at[order_idx, "tipe_desain"] = tipe_desain
                st.session_state.df.at[order_idx, "jumlah"] = jumlah
                if jumlah != order['jumlah']:
                    harga_per_pcs = order['harga_per_pcs']
                    total_biaya = harga_per_pcs * jumlah
                    st.session_state.df.at[order_idx, "total_biaya"] = total_biaya
                    st.session_state.df.at[order_idx, "remaining_payment"] = total_biaya - order['total_bayar']
                save_kloter_data(st.session_state.current_kloter, st.session_state.df)
                st.success("Order berhasil diupdate")
                # time.sleep(1) # Removed for performance
                st.rerun()
        with col2:
            if st.form_submit_button("Batal"):
                st.rerun()

def handle_delete_for_invoice(invoice_number):
    df = st.session_state.df
    if df.empty:
        return
    if not check_capability("ORDER_DELETE"):
        st.error("❌ Anda tidak memiliki izin untuk menghapus order.")
        return
    order_idx = df[df["invoice_number"] == invoice_number].index[0]
    order = df.loc[order_idx]
    with st.form(f"delete_form_single_{invoice_number}"):
        st.markdown(f"### Hapus: {invoice_number} - {order['nama_customer']}")
        st.write(f"Total: Rp {order['total_biaya']:,}")
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Ya, Hapus"):
                delete_order(order_idx)
                st.rerun()
        with col2:
            if st.form_submit_button("Batal"):
                st.rerun()

def show_payment_modal(idx, order):
    """Modal untuk input pembayaran yang berfungsi"""
    st.markdown("---")
    with st.form(f"payment_form_{idx}_{order['invoice_number']}"):
        st.markdown(f"### 💰 Pelunasan Order: {order['invoice_number']}")
        
        st.write(f"**Customer:** {order['nama_customer']}")
        st.write(f"**Total Order:** Rp {order['total_biaya']:,}")
        st.write(f"**Sudah Bayar:** Rp {order['total_bayar']:,}")
        st.write(f"**Sisa:** Rp {order['remaining_payment']:,}")
        
        jumlah_bayar = st.number_input(
            "Jumlah Bayar (Rp)",
            min_value=0,
            max_value=int(order['remaining_payment']),
            value=int(order['remaining_payment']),
            step=1000,
            key=f"jumlah_bayar_{idx}_{order['invoice_number']}"
        )
        
        metode_bayar = st.selectbox("Metode Bayar", ["CASH", "TRANSFER", "QRIS"], 
                                   key=f"metode_bayar_{idx}_{order['invoice_number']}")
        keterangan_bayar = st.text_input("Keterangan Pembayaran", 
                                        key=f"keterangan_bayar_{idx}_{order['invoice_number']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("💳 Proses Pembayaran", type="primary"):
                process_payment(idx, jumlah_bayar, metode_bayar, keterangan_bayar)
                st.session_state[f"show_payment_{idx}"] = False
                # time.sleep(1) # Removed for performance
                st.rerun()
        
        with col2:
            if st.form_submit_button("❌ Batal"):
                st.session_state[f"show_payment_{idx}"] = False
                st.rerun()

def process_payment(order_idx, jumlah_bayar, metode_bayar, keterangan):
    """Proses pembayaran order yang benar"""
    if order_idx < len(st.session_state.df):
        # Update pembayaran
        st.session_state.df.at[order_idx, "total_bayar"] += jumlah_bayar
        st.session_state.df.at[order_idx, "remaining_payment"] -= jumlah_bayar
        
        # Update status pembayaran
        if st.session_state.df.at[order_idx, "remaining_payment"] <= 0:
            st.session_state.df.at[order_idx, "payment_status"] = "LUNAS"
        elif st.session_state.df.at[order_idx, "total_bayar"] > 0:
            st.session_state.df.at[order_idx, "payment_status"] = "PANJAR"
        else:
            st.session_state.df.at[order_idx, "payment_status"] = "BELUM BAYAR"
        
        st.session_state.df.at[order_idx, "payment_by"] = st.session_state.username
        prev = st.session_state.df.at[order_idx, "payment_history"] if "payment_history" in st.session_state.df.columns else ""
        if pd.isna(prev) or not isinstance(prev, str):
            prev = "" if pd.isna(prev) else str(prev)
        logline = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}|{st.session_state.username}|{jumlah_bayar}|{metode_bayar}|{keterangan}"
        st.session_state.df.at[order_idx, "payment_history"] = (prev + "\n" + logline).strip()
        # Catat di kas flow
        if jumlah_bayar > 0:
            record_cash_flow(
                "PEMBAYARAN",
                jumlah_bayar,
                "IN",
                f"Pelunasan order {st.session_state.df.at[order_idx, 'invoice_number']} - {metode_bayar} - {keterangan}",
                st.session_state.current_kloter
            )
        
        # Simpan perubahan
        save_kloter_data(st.session_state.current_kloter, st.session_state.df)
        st.success(f"✅ Pembayaran Rp {jumlah_bayar:,} berhasil dicatat!")

def show_edit_order_modal(idx, order):
    """Modal untuk edit order"""
    st.markdown("---")
    with st.form(f"edit_form_{idx}_{order['invoice_number']}"):
        st.markdown(f"### ✏️ Edit Order: {order['invoice_number']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nama_customer = st.text_input("Nama Customer", value=order['nama_customer'],
                                         key=f"edit_nama_{idx}_{order['invoice_number']}")
            alamat_customer = st.text_area("Alamat", value=order['alamat_customer'],
                                          height=80, key=f"edit_alamat_{idx}_{order['invoice_number']}")
            telepon_customer = st.text_input("Telepon", value=order['telepon_customer'],
                                            key=f"edit_telp_{idx}_{order['invoice_number']}")
        
        with col2:
            nama_desain = st.text_input("Nama Desain", value=order['nama_desain'],
                                       key=f"edit_desain_{idx}_{order['invoice_number']}")
            tipe_desain = st.selectbox("Tipe Desain", 
                                      ["DS ORIGINAL", "CUST. REQUEST", "CUSTMR. DESIGN", "DS ORIGINAL - EDIT"],
                                      index=["DS ORIGINAL", "CUST. REQUEST", "CUSTMR. DESIGN", "DS ORIGINAL - EDIT"].index(order['tipe_desain']),
                                      key=f"edit_tipe_{idx}_{order['invoice_number']}")
            jumlah = st.number_input("Jumlah", min_value=1, value=int(order['jumlah']),
                                    key=f"edit_jumlah_{idx}_{order['invoice_number']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("💾 Simpan Perubahan", type="primary"):
                # Update data
                st.session_state.df.at[idx, "nama_customer"] = nama_customer
                st.session_state.df.at[idx, "alamat_customer"] = alamat_customer
                st.session_state.df.at[idx, "telepon_customer"] = telepon_customer
                st.session_state.df.at[idx, "nama_desain"] = nama_desain
                st.session_state.df.at[idx, "tipe_desain"] = tipe_desain
                st.session_state.df.at[idx, "jumlah"] = jumlah
                
                # Hitung ulang total jika jumlah berubah
                if jumlah != order['jumlah']:
                    harga_per_pcs = order['harga_per_pcs']
                    total_biaya = harga_per_pcs * jumlah
                    st.session_state.df.at[idx, "total_biaya"] = total_biaya
                    st.session_state.df.at[idx, "remaining_payment"] = total_biaya - order['total_bayar']
                
                save_kloter_data(st.session_state.current_kloter, st.session_state.df)
                st.success("✅ Order berhasil diupdate!")
                st.session_state[f"show_edit_{idx}"] = False
                # time.sleep(1) # Removed for performance
                st.rerun()
        
        with col2:
            if st.form_submit_button("❌ Batal"):
                st.session_state[f"show_edit_{idx}"] = False
                st.rerun()

def show_delete_confirmation(idx, order):
    """Konfirmasi hapus order"""
    st.markdown("---")
    with st.form(f"delete_confirm_{idx}_{order['invoice_number']}"):
        st.markdown(f"### ❌ Konfirmasi Hapus Order")
        st.warning(f"Yakin ingin menghapus order: {order['invoice_number']} - {order['nama_customer']}?")
        st.write(f"**Total:** Rp {order['total_biaya']:,}")
        st.write(f"**Status:** {order['payment_status']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("✅ Ya, Hapus", type="primary"):
                delete_order(idx)
                st.session_state[f"show_delete_{idx}"] = False
                # time.sleep(1) # Removed for performance
                st.rerun()
        
        with col2:
            if st.form_submit_button("❌ Batal"):
                st.session_state[f"show_delete_{idx}"] = False
                st.rerun()

def delete_order(order_idx):
    """Hapus order dengan benar"""
    if order_idx < len(st.session_state.df):
        invoice = st.session_state.df.at[order_idx, "invoice_number"]
        # Hapus dari DataFrame
        st.session_state.df = st.session_state.df.drop(order_idx).reset_index(drop=True)
        # Simpan ke file
        save_kloter_data(st.session_state.current_kloter, st.session_state.df)
        st.success(f"✅ Order {invoice} berhasil dihapus!")

def export_to_excel(df):
    """Export data ke Excel - DARI V4"""
    import io
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Orders')
    
    buffer.seek(0)
    st.download_button(
        label="📥 Download Excel",
        data=buffer,
        file_name=f"orders_{st.session_state.current_kloter}_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_excel_order"
    )

# ===================== FUNGSI YANG DIPERBAIKI: OPERASIONAL ENHANCED =====================
def show_operational_enhanced():
    """Halaman biaya operasional yang sudah diperbaiki"""
    st.markdown(f"<h2 style='color: #D4AF37;'>💰 Biaya Operasional</h2>", unsafe_allow_html=True)
    
    if st.session_state.df.empty:
        st.info("Belum ada order untuk dihitung biaya operasional.")
        return
    
    # Load operational data dengan error handling
    operational_data = load_operational_data(st.session_state.current_kloter)
    # Normalisasi formula DTF dan komisi sesuai aturan terbaru
    try:
        meter = float(str(operational_data.get("dtf_meter", operational_data.get("panjang_dtf", 0.0))).replace(",", "")) if str(operational_data.get("dtf_meter", operational_data.get("panjang_dtf", 0.0))).strip() else 0.0
    except:
        meter = 0.0
    desain_unik = operational_data.get("dtf_unique_design_count", 0)
    try:
        desain_unik = int(float(str(desain_unik).replace(",", ""))) if str(desain_unik).strip() else 0
    except:
        desain_unik = 0
    biaya_dtf_should = int(meter * 35000) if meter > 0 else 0
    komisi_should = int(meter * 2500) + int(desain_unik * 1000)
    current_biaya_dtf = operational_data.get("biaya_dtf", 0)
    try:
        current_biaya_dtf = int(float(str(current_biaya_dtf).replace(",", ""))) if str(current_biaya_dtf).strip() else 0
    except:
        current_biaya_dtf = 0
    current_comm = int(operational_data.get("dtf_operator_commission", 0) or 0)
    needs_update = (current_biaya_dtf != biaya_dtf_should) or (current_comm != komisi_should)
    if needs_update and meter > 0:
        operational_data["biaya_dtf"] = biaya_dtf_should
        operational_data["dtf_total_cost"] = biaya_dtf_should
        operational_data["dtf_operator_commission"] = komisi_should
        bl = operational_data.get("biaya_lainnya", [])
        if not isinstance(bl, list):
            bl = []
        bl = [it for it in bl if str(it.get("keterangan","")).strip().lower() != "komisi operator dtf (otomatis)"]
        bl.append({"keterangan": "Komisi Operator DTF (otomatis)", "jumlah": komisi_should})
        operational_data["biaya_lainnya"] = bl
        save_operational_data(st.session_state.current_kloter, operational_data)
        ensure_dtf_cash_flow(st.session_state.current_kloter, biaya_dtf_should, meter, desain_unik)
        ensure_dtf_commission_cash_flow(st.session_state.current_kloter, komisi_should, meter, desain_unik)
    
    # Hitung otomatis biaya produk dari semua order
    total_harga_beli_produk = st.session_state.df["total_harga_beli"].sum()
    
    # Hitung otomatis biaya sablon (Rp 5,000 per sablon)
    total_jumlah_produk = st.session_state.df["jumlah"].sum()
    biaya_sablon_otomatis = total_jumlah_produk * 5000
    
    tabs = st.tabs(["💰 Biaya Operasional", "🎨 Operator DTF"])
    with tabs[0]:
        # Form untuk input biaya manual
        with st.form("operational_enhanced_form_fixed"):
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="form-title">💰 Biaya Operasional</div>', unsafe_allow_html=True)
            st.markdown("### Biaya Otomatis")
        
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Total Harga Beli Produk:** Rp {total_harga_beli_produk:,}")
                st.caption(f"Dihitung otomatis dari {len(st.session_state.df)} order")
            with col2:
                st.info(f"**Biaya Sablon:** Rp {biaya_sablon_otomatis:,}")
                st.caption(f"Rp 5,000 × {total_jumlah_produk} pcs = Rp {biaya_sablon_otomatis:,}")
            # Tampilkan biaya DTF sebagai bagian dari biaya otomatis
            biaya_dtf_current = operational_data.get("biaya_dtf", 0)
            try:
                biaya_dtf_current = int(float(str(biaya_dtf_current).replace(",", ""))) if str(biaya_dtf_current).strip() else 0
            except:
                biaya_dtf_current = 0
            st.info(f"**Biaya DTF (otomatis):** Rp {biaya_dtf_current:,}")
            st.caption("Diatur dari tab Operator DTF: Rp 35.000/meter")
            st.markdown("---")
            st.markdown("### Biaya Manual")
        
            col1, col2 = st.columns(2)
            with col1:
                ongkir_supplier = st.number_input(
                    "Ongkir Supplier (Rp)",
                    min_value=0,
                    value=int(operational_data.get("ongkir_supplier", 70000)),
                    step=1000,
                    key="ongkir_supplier_input_op_fixed"
                )
            with col2:
                st.write("**Biaya Lainnya:**")
                biaya_lainnya_list = operational_data.get("biaya_lainnya", [])
                new_biaya_lainnya = []
                for i in range(5):  # Maks 5 entries
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        if i < len(biaya_lainnya_list):
                            ket = st.text_input(
                                f"Keterangan {i+1}",
                                value=biaya_lainnya_list[i].get("keterangan", ""),
                                key=f"ket_lain_op_fixed_{i}"
                            )
                        else:
                            ket = st.text_input(
                                f"Keterangan {i+1}",
                                value="",
                                key=f"ket_lain_op_fixed_{i}"
                            )
                    with col_b:
                        if i < len(biaya_lainnya_list):
                            default_jumlah = biaya_lainnya_list[i].get("jumlah", 0)
                            try:
                                default_jumlah = int(float(str(default_jumlah).replace(",", ""))) if str(default_jumlah).strip() else 0
                            except:
                                default_jumlah = 0
                            jumlah_val = st.number_input(
                                f"Biaya {i+1}",
                                min_value=0,
                                value=default_jumlah,
                                step=1000,
                                key=f"biaya_lain_op_fixed_{i}"
                            )
                        else:
                            jumlah_val = st.number_input(
                                f"Biaya {i+1}",
                                min_value=0,
                                value=0,
                                step=1000,
                                key=f"biaya_lain_op_fixed_{i}"
                            )
                    if ket or jumlah_val > 0:
                        new_biaya_lainnya.append({"keterangan": ket, "jumlah": jumlah_val})
            catatan = st.text_area("Catatan Operasional",
                                  value=operational_data.get("catatan", ""),
                                  height=100,
                                  placeholder="Catatan penting tentang operasional kloter ini",
                                  key="catatan_operasional_op_fixed")
            st.markdown('</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_operational = st.form_submit_button("💾 **Simpan Biaya Operasional**", type="primary", use_container_width=True)
            if submit_operational:
                if not check_capability("CASH_RECORD"):
                    st.error("❌ Anda tidak memiliki izin untuk menyimpan biaya operasional.")
                    return
                total_biaya_lainnya = sum(item["jumlah"] for item in new_biaya_lainnya)
                total_otomatis = (total_harga_beli_produk + biaya_dtf_current + biaya_sablon_otomatis)
                total_manual = (ongkir_supplier + total_biaya_lainnya)
                total_operational = (total_harga_beli_produk +
                                    biaya_dtf_current +
                                    biaya_sablon_otomatis + 
                                    ongkir_supplier + 
                                    total_biaya_lainnya)
                operational_data = {
                    "biaya_produk": total_harga_beli_produk,
                    "panjang_dtf": operational_data.get("panjang_dtf", 0.0),
                    "biaya_dtf": biaya_dtf_current,
                    "biaya_sablon": biaya_sablon_otomatis,
                    "ongkir_supplier": ongkir_supplier,
                    "biaya_lainnya": new_biaya_lainnya,
                    "total": total_operational,
                    "total_otomatis": total_otomatis,
                    "total_manual": total_manual,
                    "catatan": catatan,
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "updated_by": st.session_state.username
                }
                save_operational_data(st.session_state.current_kloter, operational_data)
                # Catat cash flow hanya untuk biaya manual agar tidak menambah biaya DTF berulang
                if total_manual > 0:
                    record_cash_flow(
                        "OPERASIONAL",
                        total_manual,
                        "OUT",
                        f"Biaya operasional MANUAL kloter {st.session_state.current_kloter}: {catatan}",
                        st.session_state.current_kloter
                    )
                st.success("✅ Biaya operasional berhasil disimpan!")
                # time.sleep(1) # Removed for performance
                st.rerun()
    
    with tabs[1]:
        show_dtf_operator_tab(operational_data)
    
    # Tampilkan summary
    st.markdown("---")
    st.markdown("### 📊 Summary Biaya Operasional")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {total_harga_beli_produk:,}</div>
            <div class="metric-label">Harga Beli Produk</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {biaya_sablon_otomatis:,}</div>
            <div class="metric-label">Biaya Sablon</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        biaya_dtf = operational_data.get("biaya_dtf", 0)
        try:
            biaya_dtf = int(float(str(biaya_dtf).replace(",", ""))) if str(biaya_dtf).strip() else 0
        except:
            biaya_dtf = 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {biaya_dtf:,}</div>
            <div class="metric-label">Biaya DTF</div>
        </div>
        """, unsafe_allow_html=True)
        
        ongkir = operational_data.get('ongkir_supplier', 0)
        try:
            ongkir = int(float(str(ongkir).replace(",", ""))) if str(ongkir).strip() else 0
        except:
            ongkir = 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {ongkir:,}</div>
            <div class="metric-label">Ongkir Supplier</div>
        </div>
        """, unsafe_allow_html=True)
        
        perkiraan_transfer = total_harga_beli_produk + biaya_dtf + ongkir
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {perkiraan_transfer:,}</div>
            <div class="metric-label">Perkiraan Transfer ke Supplier</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_lainnya = 0
        for item in operational_data.get("biaya_lainnya", []):
            try:
                val = int(float(str(item.get("jumlah", 0)).replace(",", ""))) if str(item.get("jumlah", 0)).strip() else 0
            except:
                val = 0
            total_lainnya += val
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {total_lainnya:,}</div>
            <div class="metric-label">Biaya Lainnya</div>
        </div>
        """, unsafe_allow_html=True)
        
        total_operational = operational_data.get('total', 0)
        try:
            total_operational = int(float(str(total_operational).replace(",", ""))) if str(total_operational).strip() else 0
        except:
            total_operational = 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {total_operational:,}</div>
            <div class="metric-label">TOTAL OPERASIONAL</div>
        </div>
        """, unsafe_allow_html=True)
        # Tampilkan pemisahan otomatis vs manual
        total_otomatis = operational_data.get('total_otomatis', total_harga_beli_produk + biaya_sablon_otomatis + operational_data.get("biaya_dtf", 0))
        total_manual = operational_data.get('total_manual', ongkir + total_lainnya)
        try:
            total_otomatis = int(float(str(total_otomatis).replace(",", ""))) if str(total_otomatis).strip() else 0
        except:
            total_otomatis = 0
        try:
            total_manual = int(float(str(total_manual).replace(",", ""))) if str(total_manual).strip() else 0
        except:
            total_manual = 0
        st.markdown(f"""
        <div class="metric-card" style="margin-top:0.5rem;">
            <div class="metric-value">Rp {total_otomatis:,}</div>
            <div class="metric-label">Total Otomatis</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card" style="margin-top:0.5rem;">
            <div class="metric-value">Rp {total_manual:,}</div>
            <div class="metric-label">Total Manual</div>
        </div>
        """, unsafe_allow_html=True)
    
    if operational_data.get("catatan"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("**📝 Catatan:**")
        st.write(operational_data["catatan"])
        st.caption(f"Terakhir update: {operational_data.get('updated_at', '-')}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🛠️ Kelola Biaya Manual")
    current_manual = operational_data.get("biaya_lainnya", [])
    if current_manual:
        display_items = [f"{it.get('keterangan','')} • Rp {int(it.get('jumlah',0)):,}" for it in current_manual]
        sel = st.selectbox("Pilih item biaya untuk diedit/dihapus", display_items, index=0, key="manage_manual_select")
        idx = display_items.index(sel) if sel in display_items else -1
        if idx >= 0:
            edit_ket = st.text_input("Ubah keterangan", value=current_manual[idx].get("keterangan",""), key="manage_manual_ket")
            edit_jml = st.number_input("Ubah jumlah (Rp)", min_value=0, value=int(current_manual[idx].get("jumlah",0)), step=1000, key="manage_manual_jml")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("💾 Simpan Perubahan Item", type="primary"):
                    current_manual[idx] = {"keterangan": edit_ket, "jumlah": int(edit_jml)}
                    operational_data["biaya_lainnya"] = current_manual
                    save_operational_data(st.session_state.current_kloter, operational_data)
                    st.success("✅ Item biaya manual diperbarui")
                    # time.sleep(1) # Removed for performance
                    st.rerun()
            with col_b:
                if st.button("🗑️ Hapus Item"):
                    operational_data["biaya_lainnya"] = [it for i, it in enumerate(current_manual) if i != idx]
                    save_operational_data(st.session_state.current_kloter, operational_data)
                    st.success("✅ Item biaya manual dihapus")
                    # time.sleep(1) # Removed for performance
                    st.rerun()
    else:
        st.info("Belum ada item biaya manual.")

# ===================== FUNGSI PRODUCTION =====================
def show_production_page():
    """Halaman monitoring produksi - DARI V4"""
    st.markdown(f"<h2 style='color: #D4AF37;'>🏭 Production Tracking</h2>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">🧾 Buat SPK Baru</div>', unsafe_allow_html=True)

    @st.cache_data(ttl=60)
    def load_materials_df():
        rows = []
        polos_file = STOCK_DIR / "stock_polos.csv"
        if polos_file.exists() and polos_file.stat().st_size > 0:
            try:
                dfp = pd.read_csv(polos_file)
                for _, r in dfp.iterrows():
                    rows.append({
                        "source": "polos",
                        "item": f"{r.get('jenis_produk','')} • {r.get('warna','')} • {r.get('ukuran','')}",
                        "jenis_produk": r.get('jenis_produk',''),
                        "warna": r.get('warna',''),
                        "ukuran": r.get('ukuran',''),
                        "available": int(r.get('jumlah', 0) or 0),
                        "unit": "pcs",
                        "cost_price": float(r.get('harga_beli', 0) or 0)
                    })
            except:
                pass
        dtf_file = STOCK_DIR / "stock_dtf.csv"
        if dtf_file.exists() and dtf_file.stat().st_size > 0:
            try:
                dfd = pd.read_csv(dtf_file)
                for _, r in dfd.iterrows():
                    rows.append({
                        "source": "dtf",
                        "item": f"{r.get('nama_desain','')} • {r.get('cocok_warna','')} • {r.get('ukuran_sablon','')}",
                        "nama_desain": r.get('nama_desain',''),
                        "cocok_warna": r.get('cocok_warna',''),
                        "ukuran_sablon": r.get('ukuran_sablon',''),
                        "available": int(r.get('jumlah', 0) or 0),
                        "unit": "pcs",
                        "cost_price": float(r.get('harga_beli', 0) or 0)
                    })
            except:
                pass
        return pd.DataFrame(rows)

    def deduct_material(selected_row, qty_used):
        if selected_row.get('source') == 'polos':
            polos_file = STOCK_DIR / "stock_polos.csv"
            dfp = pd.read_csv(polos_file) if polos_file.exists() and polos_file.stat().st_size > 0 else pd.DataFrame()
            mask = (
                (dfp['jenis_produk'] == selected_row.get('jenis_produk')) &
                (dfp['warna'] == selected_row.get('warna')) &
                (dfp['ukuran'] == selected_row.get('ukuran'))
            )
            if not mask.any():
                return False, "Item tidak ditemukan"
            idx = dfp[mask].index[0]
            available = int(dfp.loc[idx, 'jumlah'])
            if qty_used > available:
                return False, "Stok tidak cukup"
            new_qty = available - qty_used
            if new_qty <= 0:
                dfp = dfp.drop(index=idx)
            else:
                dfp.loc[idx, 'jumlah'] = new_qty
            dfp.to_csv(polos_file, index=False)
            return True, None
        elif selected_row.get('source') == 'dtf':
            dtf_file = STOCK_DIR / "stock_dtf.csv"
            dfd = pd.read_csv(dtf_file) if dtf_file.exists() and dtf_file.stat().st_size > 0 else pd.DataFrame()
            mask = (
                (dfd['nama_desain'] == selected_row.get('nama_desain')) &
                (dfd['cocok_warna'] == selected_row.get('cocok_warna')) &
                (dfd['ukuran_sablon'] == selected_row.get('ukuran_sablon'))
            )
            if not mask.any():
                return False, "Item tidak ditemukan"
            idx = dfd[mask].index[0]
            available = int(dfd.loc[idx, 'jumlah'])
            if qty_used > available:
                return False, "Stok tidak cukup"
            new_qty = available - qty_used
            if new_qty <= 0:
                dfd = dfd.drop(index=idx)
            else:
                dfd.loc[idx, 'jumlah'] = new_qty
            dfd.to_csv(dtf_file, index=False)
            return True, None
        return False, "Sumber tidak dikenal"

    def record_stock_history(entry):
        history_file = STOCK_DIR / "stock_history.csv"
        if history_file.exists() and history_file.stat().st_size > 0:
            try:
                hdf = pd.read_csv(history_file)
            except:
                hdf = pd.DataFrame(columns=[
                    "tanggal","spk_id","source","item","qty","unit","cost_price","total_cost","description","created_by"
                ])
        else:
            hdf = pd.DataFrame(columns=[
                "tanggal","spk_id","source","item","qty","unit","cost_price","total_cost","description","created_by"
            ])
        new_row = pd.DataFrame([entry])
        hdf = pd.concat([hdf, new_row], ignore_index=True)
        hdf.to_csv(history_file, index=False)

    materials_df = load_materials_df()
    if materials_df.empty:
        st.info("Belum ada material di stok mentah untuk digunakan.")
    else:
        materials_df["display"] = materials_df.apply(lambda x: f"{x['item']} • {x['available']} {x['unit']}", axis=1)
        selected_display = st.selectbox("Pilih Material", list(materials_df["display"]))
        selected_row = materials_df[materials_df["display"] == selected_display].iloc[0].to_dict()
        qty_used = st.number_input("Quantity Used", min_value=1, value=1, step=1)
        total_cost = float(selected_row.get('cost_price', 0)) * qty_used
        st.write(f"Biaya Bahan Baku: Rp {int(total_cost):,}")
        spk_id = f"SPK-{st.session_state.current_kloter}-{int(time.time())%10000:04d}"
        if st.button("Simpan SPK", type="primary"):
            ok, err = deduct_material(selected_row, qty_used)
            if not ok:
                st.error(err or "Gagal mengurangi stok")
            else:
                record_stock_history({
                    "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "spk_id": spk_id,
                    "source": selected_row.get('source'),
                    "item": selected_row.get('item'),
                    "qty": int(qty_used),
                    "unit": selected_row.get('unit'),
                    "cost_price": float(selected_row.get('cost_price', 0)),
                    "total_cost": int(total_cost),
                    "description": f"Used for Production {spk_id}",
                    "created_by": st.session_state.username
                })
                st.success(f"SPK {spk_id} disimpan. Material dikurangi dan dicatat di history.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.df.empty:
        st.info("Belum ada order untuk diproduksi.")
        return
    
    # Filter berdasarkan role
    if check_role_access("produksi") or check_role_access("admin") or check_role_access("owner"):
        # Tampilkan semua untuk role yang memiliki akses
        production_df = st.session_state.df.copy()
    else:
        # Untuk role lain, hanya tampilkan yang belum selesai
        production_df = st.session_state.df[
            st.session_state.df["status_produksi"].isin(["PENDING", "PROSES"])
        ].copy()
    
    if production_df.empty:
        st.success("🎉 Semua order sudah selesai diproduksi!")
        return
    
    # Status summary
    pending_count = len(production_df[production_df["status_produksi"] == "PENDING"])
    proses_count = len(production_df[production_df["status_produksi"] == "PROSES"])
    selesai_count = len(production_df[production_df["status_produksi"] == "SELESAI"])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{pending_count}</div>
            <div class="metric-label">⏳ Pending</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{proses_count}</div>
            <div class="metric-label">⚡ In Progress</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{selesai_count}</div>
            <div class="metric-label">✅ Completed</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs untuk masing-masing status
    tab1, tab2, tab3 = st.tabs(["⏳ Pending", "⚡ In Progress", "✅ Completed"])
    
    with tab1:
        show_production_by_status("PENDING")
    
    with tab2:
        show_production_by_status("PROSES")
    
    with tab3:
        show_production_by_status("SELESAI")

def show_production_by_status(status):
    """Tampilkan order berdasarkan status produksi - DARI V4"""
    df_by_status = st.session_state.df[st.session_state.df["status_produksi"] == status].copy()
    
    if df_by_status.empty:
        st.info(f"Tidak ada order dengan status {status}")
        return
    
    for idx, order in df_by_status.iterrows():
        payment_status = order['payment_status']
        status_class = "status-lunas" if payment_status == "LUNAS" else "status-panjar" if payment_status == "PANJAR" else "status-pending"
        
        prod_status = order['status_produksi']
        prod_class = "status-selesai" if prod_status == "SELESAI" else "status-proses" if prod_status == "PROSES" else "status-pending"
        
        # Tampilkan order card
        st.markdown(f"""
        <div class="order-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 2;">
                    <strong style="color: white; font-size: 1.1rem;">{order['nama_customer']}</strong><br>
                    <span style="color: #888; font-size: 0.9rem;">{order['nama_desain']} • {order['jenis_produk']}</span><br>
                    <span style="color: #888; font-size: 0.8rem;">{order['warna']} | {order['ukuran']} | {order['jumlah']} pcs</span>
                </div>
                <div style="flex: 1; text-align: center;">
                    <div style="margin-bottom: 0.5rem;">
                        <span class="status-badge {status_class}">{order['payment_status']}</span>
                    </div>
                    <div style="color: #D4AF37; font-size: 1.1rem;">Rp {order['total_biaya']:,}</div>
                </div>
                <div style="flex: 1; text-align: right;">
                    <div style="margin-bottom: 0.5rem;">
                        <span class="status-badge {prod_class}">{order['status_produksi']}</span>
                    </div>
                    <div style="color: #888; font-size: 0.8rem;">{order['tgl_order'].split()[0]}</div>
                </div>
            </div>
            <div style="margin-top: 1rem; display: flex; gap: 0.5rem; justify-content: flex-end;">
        """, unsafe_allow_html=True)
        
        # Tombol aksi dengan Streamlit
        col1, col2 = st.columns(2)
        
        with col1:
            if check_capability("PRODUCTION_UPDATE"):
                if status == "PENDING":
                    if st.button("▶️ Mulai Produksi", key=f"start_{idx}_{order['invoice_number']}",
                               use_container_width=True):
                        update_production_status(idx, "PROSES")
                elif status == "PROSES":
                    if st.button("✅ Selesai", key=f"finish_{idx}_{order['invoice_number']}",
                               use_container_width=True):
                        update_production_status(idx, "SELESAI")
                elif status == "SELESAI":
                    if st.button("↩️ Buka Kembali", key=f"reopen_{idx}_{order['invoice_number']}",
                               use_container_width=True):
                        update_production_status(idx, "PROSES")
        
        st.markdown("</div></div>", unsafe_allow_html=True)

def update_production_status(order_idx, new_status):
    if order_idx < len(st.session_state.df):
        st.session_state.df.at[order_idx, "status_produksi"] = new_status
        st.session_state.df.at[order_idx, "produksi_by"] = st.session_state.username
        prev = st.session_state.df.at[order_idx, "produksi_history"] if "produksi_history" in st.session_state.df.columns else ""
        if pd.isna(prev) or not isinstance(prev, str):
            prev = "" if pd.isna(prev) else str(prev)
        st.session_state.df.at[order_idx, "produksi_history"] = (prev + f"\n{datetime.now().strftime('%Y-%m-%d %H:%M')}|{st.session_state.username}|{new_status}").strip()
        try:
            if new_status == "SELESAI":
                order = st.session_state.df.loc[order_idx].to_dict()
                jumlah_order = int(order.get("jumlah", 1) or 1)
                polos_selected = {
                    "source": "polos",
                    "jenis_produk": order.get("jenis_produk"),
                    "warna": order.get("warna"),
                    "ukuran": order.get("ukuran")
                }
                ok_p, err_p = deduct_material(polos_selected, jumlah_order)
                if not ok_p and err_p:
                    try:
                        st.warning(f"Gagal mengurangi stok polos: {err_p}")
                    except:
                        pass
                design_src = str(order.get("design_source", order.get("tipe_desain", ""))).lower()
                is_original = ("original" in design_src) or (str(order.get("tipe_desain","")).upper() == "DS ORIGINAL")
                if is_original:
                    dtf_selected = {
                        "source": "dtf",
                        "nama_desain": order.get("nama_desain"),
                        "cocok_warna": order.get("warna"),
                        "ukuran_sablon": order.get("ukuran_sablon", "-")
                    }
                    ok_d, err_d = deduct_material(dtf_selected, jumlah_order)
                    if not ok_d and err_d:
                        try:
                            st.warning(f"Gagal mengurangi stok DTF: {err_d}")
                        except:
                            pass
        except Exception:
            pass
        save_kloter_data(st.session_state.current_kloter, st.session_state.df)
        st.success(f"Status produksi diubah menjadi {new_status}")
        # time.sleep(1) # Removed for performance
        st.rerun()

# ===================== FUNGSI DISTRIBUTION =====================
def show_distribution_page():
    """Halaman monitoring distribusi - DARI V4"""
    st.markdown(f"<h2 style='color: #D4AF37;'>🚚 Distribution Tracking</h2>", unsafe_allow_html=True)
    
    if st.session_state.df.empty:
        st.info("Belum ada order untuk didistribusikan.")
        return
    
    # Filter: hanya order dengan produksi SELESAI dan belum TERKIRIM
    distribution_df = st.session_state.df[
        (st.session_state.df["status_produksi"] == "SELESAI") &
        (st.session_state.df["status_distribusi"] != "TERKIRIM")
    ].copy()
    
    # Batasi untuk user non-manajemen: hanya tampilkan yang sudah lunas
    if not check_feature_access("Management Kloter"):
        distribution_df = distribution_df[distribution_df["payment_status"] == "LUNAS"]
    
    if distribution_df.empty:
        st.success("🎉 Semua order sudah terkirim!")
        return
    
    # Status summary
    belum_kirim = len(distribution_df[distribution_df["status_distribusi"] == "BELUM KIRIM"])
    sedang_kirim = len(distribution_df[distribution_df["status_distribusi"] == "SEDANG KIRIM"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{belum_kirim}</div>
            <div class="metric-label">📦 Belum Kirim</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{sedang_kirim}</div>
            <div class="metric-label">🚚 Sedang Kirim</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tombol aksi massal berdasarkan capability
    if check_capability("DISTRIBUTION_MASS"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📦 Tandai Semua Siap Kirim", use_container_width=True, key="mark_all_ready_dist"):
                for idx in distribution_df.index:
                    st.session_state.df.at[idx, "status_distribusi"] = "SEDANG KIRIM"
                save_kloter_data(st.session_state.current_kloter, st.session_state.df)
                st.success("Semua order ditandai SEDANG KIRIM")
                # time.sleep(1) # Removed for performance
                st.rerun()
        
        with col2:
            if st.button("✅ Tandai Semua Terkirim", use_container_width=True, key="mark_all_delivered_dist"):
                for idx in distribution_df.index:
                    st.session_state.df.at[idx, "status_distribusi"] = "TERKIRIM"
                save_kloter_data(st.session_state.current_kloter, st.session_state.df)
                st.success("Semua order ditandai TERKIRIM")
                # time.sleep(1) # Removed for performance
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tampilkan order berdasarkan status
    for status in ["BELUM KIRIM", "SEDANG KIRIM"]:
        status_df = distribution_df[distribution_df["status_distribusi"] == status]
        
        if not status_df.empty:
            st.markdown(f"### {status}")
            
            for idx, order in status_df.iterrows():
                payment_status = order['payment_status']
                status_class = "status-lunas" if payment_status == "LUNAS" else "status-panjar"
                
                dist_status = order['status_distribusi']
                dist_class = "status-proses" if dist_status == "SEDANG KIRIM" else "status-pending"
                
                # Tampilkan order card
                st.markdown(f"""
                <div class="order-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 2;">
                            <strong style="color: white; font-size: 1.1rem;">{order['nama_customer']}</strong><br>
                            <span style="color: #888; font-size: 0.9rem;">📍 {order['alamat_customer'][:50]}...</span><br>
                            <span style="color: #888; font-size: 0.8rem;">📱 {order['telepon_customer']}</span>
                        </div>
                        <div style="flex: 1; text-align: center;">
                            <div style="margin-bottom: 0.5rem;">
                                <span class="status-badge {status_class}">{order['payment_status']}</span>
                            </div>
                            <div style="color: #D4AF37; font-size: 1.1rem;">{order['jumlah']} pcs</div>
                        </div>
                        <div style="flex: 1; text-align: right;">
                            <div style="margin-bottom: 0.5rem;">
                                <span class="status-badge {dist_class}">{order['status_distribusi']}</span>
                            </div>
                            <div style="color: #888; font-size: 0.8rem;">Rp {order['total_biaya']:,}</div>
                        </div>
                    </div>
                    <div style="margin-top: 1rem; display: flex; gap: 0.5rem; justify-content: flex-end;">
                """, unsafe_allow_html=True)
                
                # Tombol aksi dengan Streamlit
                col1, col2 = st.columns(2)
                
                with col1:
                    if check_capability("DISTRIBUTION_UPDATE"):
                        if status == "BELUM KIRIM":
                            if st.button("🚚 Mulai Kirim", key=f"ship_{idx}_{order['invoice_number']}",
                                       use_container_width=True):
                                update_distribution_status(idx, "SEDANG KIRIM")
                        elif status == "SEDANG KIRIM":
                            upload_ship = st.file_uploader("Upload Bukti Pengiriman (opsional)", type=["png","jpg","jpeg","pdf"], key=f"shipproof_{idx}_{order['invoice_number']}")
                            if st.button("✅ Tandai Terkirim", key=f"deliver_{idx}_{order['invoice_number']}",
                                       use_container_width=True):
                                if upload_ship:
                                    ext = Path(upload_ship.name).suffix.lower()
                                    content, err = prepare_upload_bytes(upload_ship, ext)
                                    if err:
                                        st.error(err)
                                    else:
                                        dest = SHIPPING_PROOFS_DIR / f"{order['invoice_number']}{ext}"
                                        with open(dest, "wb") as f:
                                            f.write(content)
                                        st.session_state.df.at[idx, "shipping_proof_file"] = str(dest)
                                update_distribution_status(idx, "TERKIRIM")
                
                st.markdown("</div></div>", unsafe_allow_html=True)

def update_distribution_status(order_idx, new_status):
    if order_idx < len(st.session_state.df):
        if new_status == "TERKIRIM":
            # Cegah terkirim jika belum LUNAS atau belum approval
            pay_status = st.session_state.df.at[order_idx, "payment_status"]
            approval = st.session_state.df.at[order_idx, "payment_approval_status"] if "payment_approval_status" in st.session_state.df.columns else ""
            if pay_status != "LUNAS":
                st.error("❌ Tidak bisa tandai TERKIRIM. Pelunasan belum LUNAS.")
                return
            if approval and approval != "APPROVED":
                st.error("❌ Tidak bisa tandai TERKIRIM. Pelunasan belum di-approve owner.")
                return
        st.session_state.df.at[order_idx, "status_distribusi"] = new_status
        st.session_state.df.at[order_idx, "distribusi_by"] = st.session_state.username
        prev = st.session_state.df.at[order_idx, "distribusi_history"] if "distribusi_history" in st.session_state.df.columns else ""
        if pd.isna(prev) or not isinstance(prev, str):
            prev = "" if pd.isna(prev) else str(prev)
        st.session_state.df.at[order_idx, "distribusi_history"] = (prev + f"\n{datetime.now().strftime('%Y-%m-%d %H:%M')}|{st.session_state.username}|{new_status}").strip()
        save_kloter_data(st.session_state.current_kloter, st.session_state.df)
        st.success(f"Status distribusi diubah menjadi {new_status}")
        # time.sleep(1) # Removed for performance
        st.rerun()

# ===================== FUNGSI PROFIT YANG DIPERBAIKI =====================
def show_profit():
    """Halaman analisis profit yang sudah diperbaiki"""
    st.markdown(f"<h2 style='color: #D4AF37;'>📈 Profit Analysis</h2>", unsafe_allow_html=True)
    tabs = st.tabs(["🤝 Profit Sharing", "🎨 Operator DTF"])
    with tabs[0]:
        if st.session_state.df.empty:
            st.info("Belum ada data untuk analisis.")
        else:
            operational_data = load_operational_data(st.session_state.current_kloter)
            total_operational = operational_data.get("total", 0)
            total_revenue = st.session_state.df["total_biaya"].sum()
            total_cost = total_operational
            total_profit = total_revenue - total_cost
            total_piutang = st.session_state.df["remaining_payment"].sum()
            profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">Rp {total_revenue:,}</div>
                    <div class="metric-label">Total Revenue</div>
                    <div style="margin-top: 0.5rem; color: #888; font-size: 0.8rem;">Kloter {st.session_state.current_kloter}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">Rp {total_cost:,}</div>
                    <div class="metric-label">Total Cost</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                profit_color = '#2ecc71' if total_profit > 0 else '#e74c3c'
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">Rp {total_profit:,}</div>
                    <div class="metric-label">Net Profit</div>
                    <div style="margin-top: 0.5rem; color: {profit_color}; font-size: 0.9rem;">
                        Margin: {profit_margin:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">Rp {total_piutang:,}</div>
                    <div class="metric-label">Outstanding</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Revenue by Product")
                revenue_by_product = st.session_state.df.groupby("jenis_produk")["total_biaya"].sum()
                if not revenue_by_product.empty:
                    fig, ax = plt.subplots(figsize=(8, 5))
                    colors = ['#D4AF37', '#FFC107', '#FFD700', '#FFEC8B', '#FFFACD']
                    revenue_by_product.plot(kind='bar', ax=ax, color=colors[:len(revenue_by_product)])
                    ax.set_ylabel("Revenue (Rp)")
                    ax.set_title("Revenue by Product Type")
                    ax.set_facecolor('#1A1D23')
                    fig.patch.set_facecolor('#0E1117')
                    ax.tick_params(colors='white')
                    ax.spines['bottom'].set_color('#444')
                    ax.spines['top'].set_color('#444')
                    ax.spines['right'].set_color('#444')
                    ax.spines['left'].set_color('#444')
                    ax.yaxis.label.set_color('white')
                    ax.xaxis.label.set_color('white')
                    ax.title.set_color('white')
                    plt.xticks(rotation=45, ha='right', color='white')
                    plt.yticks(color='white')
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info("Belum ada data revenue per produk")
            with col2:
                st.markdown("### Payment Status Distribution")
                payment_status_counts = st.session_state.df["payment_status"].value_counts()
                if not payment_status_counts.empty:
                    fig, ax = plt.subplots(figsize=(8, 5))
                    colors = ['#2ecc71', '#f39c12', '#e74c3c']
                    ax.pie(payment_status_counts.values, labels=payment_status_counts.index, autopct='%1.1f%%',
                          colors=colors[:len(payment_status_counts)], startangle=90)
                    ax.set_title("Payment Status Distribution")
                    plt.setp(ax.texts, color="white")
                    ax.title.set_color('white')
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info("Belum ada data status pembayaran")
            st.markdown("---")
            st.markdown("### 🧾 Rincian Biaya Operasional")
            try:
                total_harga_beli_produk = st.session_state.df["total_harga_beli"].sum()
            except Exception:
                total_harga_beli_produk = 0
            try:
                total_jumlah_produk = st.session_state.df["jumlah"].sum()
            except Exception:
                total_jumlah_produk = 0
            biaya_sablon_otomatis = int(total_jumlah_produk * 5000)
            biaya_dtf_val = operational_data.get("biaya_dtf", 0)
            try:
                biaya_dtf_val = int(float(str(biaya_dtf_val).replace(",", ""))) if str(biaya_dtf_val).strip() else 0
            except:
                biaya_dtf_val = 0
            ongkir_supplier_val = operational_data.get("ongkir_supplier", 0)
            try:
                ongkir_supplier_val = int(float(str(ongkir_supplier_val).replace(",", ""))) if str(ongkir_supplier_val).strip() else 0
            except:
                ongkir_supplier_val = 0
            komisi_dtf = int(operational_data.get("dtf_operator_commission", 0) or 0)
            total_lainnya = 0
            for it in operational_data.get("biaya_lainnya", []):
                try:
                    ket = str(it.get("keterangan",""))
                    jml = int(float(str(it.get("jumlah",0)).replace(",",""))) if str(it.get("jumlah",0)).strip() else 0
                except:
                    ket = ""
                    jml = 0
                if "komisi operator dtf" in ket.lower():
                    continue
                total_lainnya += jml
            breakdown_rows = pd.DataFrame([
                {"Item":"Biaya beli produk","Jumlah": int(total_harga_beli_produk)},
                {"Item":"Biaya sablon","Jumlah": biaya_sablon_otomatis},
                {"Item":"Biaya DTF","Jumlah": biaya_dtf_val},
                {"Item":"Komisi Operator DTF","Jumlah": komisi_dtf},
                {"Item":"Ongkir Supplier","Jumlah": ongkir_supplier_val},
                {"Item":"Biaya Lainnya","Jumlah": total_lainnya},
                {"Item":"TOTAL OPERASIONAL","Jumlah": int(operational_data.get("total", 0))}
            ])
            st.dataframe(breakdown_rows, use_container_width=True)
            st.markdown("---")
            st.markdown("### 🤝 Profit Sharing & Kinerja Tim")
            settings = load_settings()
            profit_settings = settings.get("profit_sharing_settings", {})
            owner_pct = profit_settings.get("owner_percent", 55)
            coo_pct = profit_settings.get("coo_percent", 10)
            smos_pct = profit_settings.get("smos_percent", 15)
            pool_pct = profit_settings.get("pool_percent", 20)
            total_profit = total_revenue - total_operational
            owner_share = (owner_pct/100) * total_profit
            coo_share = (coo_pct/100) * total_profit
            smos_share = (smos_pct/100) * total_profit
            pool_share = (pool_pct/100) * total_profit
            points_data = calculate_kloter_points(st.session_state.df, st.session_state.current_kloter)
            total_points_all = sum(data['total'] for data in points_data.values())
            pool_distribution = {}
            if total_points_all > 0:
                for user, data in points_data.items():
                    percent = (data['total'] / total_points_all) * 100
                    pool_value = (percent / 100) * pool_share
                    pool_distribution[user] = {
                        'percent': percent,
                        'value': pool_value,
                        'order_points': data['order'],
                        'distribution_points': data['distribution'],
                        'dtf_points': data.get('dtf', 0),
                        'total_points': data['total']
                    }
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Owner (55%)", f"Rp {owner_share:,.0f}")
            with col2:
                st.metric("COO (10%)", f"Rp {coo_share:,.0f}")
            with col3:
                st.metric("SMOS (15%)", f"Rp {smos_share:,.0f}")
            with col4:
                st.metric("Pool (20%)", f"Rp {pool_share:,.0f}")
            if pool_distribution:
                st.markdown("#### 📊 Detail Pool Kinerja")
                pool_df = pd.DataFrame.from_dict(pool_distribution, orient='index')
                pool_df.reset_index(inplace=True)
                pool_df.rename(columns={'index': 'Username'}, inplace=True)
                st.dataframe(pool_df[['Username', 'order_points', 'distribution_points', 'dtf_points', 'total_points', 'percent', 'value']])
            st.markdown("#### 💰 Total Diterima per User")
            total_data = []
            for user in set(list(points_data.keys()) + ['owner', 'coo', 'smos']):
                user_row = {}
                user_row['Username'] = user
                if user == 'owner':
                    user_row['Bagian Tetap'] = owner_share
                elif user == 'coo':
                    user_row['Bagian Tetap'] = coo_share
                elif user == 'smos':
                    user_row['Bagian Tetap'] = smos_share
                else:
                    user_row['Bagian Tetap'] = 0
                pool_info = pool_distribution.get(user, {})
                user_row['Bagian Pool'] = pool_info.get('value', 0)
                user_row['Total'] = user_row['Bagian Tetap'] + user_row['Bagian Pool']
                total_data.append(user_row)
            total_df = pd.DataFrame(total_data)
            st.dataframe(total_df)
            if st.button("💾 Simpan Pembagian ke History"):
                user_data_list = []
                for user in total_data:
                    user_data_list.append({
                        'username': user['Username'],
                        'bagian_tetap': user['Bagian Tetap'],
                        'order_points': points_data.get(user['Username'], {}).get('order', 0),
                        'distribution_points': points_data.get(user['Username'], {}).get('distribution', 0),
                        'total_points': points_data.get(user['Username'], {}).get('total', 0),
                        'percent_from_pool': pool_distribution.get(user['Username'], {}).get('percent', 0),
                        'nilai_pool': user['Bagian Pool'],
                        'total_diterima': user['Total']
                    })
                save_profit_sharing_history(
                    kloter_id=st.session_state.current_kloter,
                    calculation_date=datetime.now().strftime("%Y-%m-%d"),
                    user_data_list=user_data_list,
                    calculated_by=st.session_state.username
                )
                st.success("✅ Pembagian hasil telah disimpan ke history.")
            st.markdown("---")
            st.markdown("### Visualisasi Pembagian")
            labels = ['Owner','COO','SMOS','Pool']
            sizes = [owner_pct, coo_pct, smos_pct, pool_pct]
            colors = ['#D4AF37','#3498db','#2ecc71','#9b59b6']
            try:
                fig1, ax1 = plt.subplots(figsize=(5,5))
                ax1.pie(
                    sizes,
                    labels=labels,
                    colors=colors,
                    autopct='%1.1f%%',
                    startangle=90,
                    textprops={'color': 'white', 'fontsize': 10}
                )
                ax1.axis('equal')
                ax1.set_facecolor('#0E1117')
                fig1.patch.set_facecolor('#0E1117')
                legend_labels = [f"{lbl} ({pct:.1f}%)" for lbl, pct in zip(labels, sizes)]
                leg = ax1.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0.5))
                for text in leg.get_texts():
                    text.set_color('white')
                st.pyplot(fig1)
                plt.close(fig1)
            except Exception:
                pass
            try:
                users = [r["Username"] for r in total_data]
                totals = [r["Total"] for r in total_data]
                fig2, ax2 = plt.subplots(figsize=(8,5))
                ax2.bar(users, totals, color='#D4AF37')
                ax2.set_ylabel("Total (Rp)")
                ax2.set_title("Total Diterima per User")
                ax2.set_facecolor('#1A1D23')
                fig2.patch.set_facecolor('#0E1117')
                ax2.tick_params(colors='white')
                ax2.spines['bottom'].set_color('#444')
                ax2.spines['top'].set_color('#444')
                ax2.spines['right'].set_color('#444')
                ax2.spines['left'].set_color('#444')
                ax2.yaxis.label.set_color('white')
                ax2.xaxis.label.set_color('white')
                ax2.title.set_color('white')
                plt.xticks(rotation=45, ha='right', color='white')
                plt.yticks(color='white')
                plt.tight_layout()
                st.pyplot(fig2)
                plt.close(fig2)
            except Exception:
                pass
    with tabs[1]:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">🎨 Laporan Operator DTF</div>', unsafe_allow_html=True)
        all_kloters = get_all_kloters()
        selected_kloter = st.selectbox("Pilih Kloter", all_kloters, index=all_kloters.index(st.session_state.current_kloter) if st.session_state.current_kloter in all_kloters else 0, key="dtf_report_kloter_select_profit")
        op = load_operational_data(selected_kloter)
        meter = op.get("dtf_meter", op.get("panjang_dtf", 0.0))
        try:
            meter = float(str(meter).replace(",", "")) if str(meter).strip() else 0.0
        except:
            meter = 0.0
        desain_unik = op.get("dtf_unique_design_count", 0)
        try:
            desain_unik = int(float(str(desain_unik).replace(",", ""))) if str(desain_unik).strip() else 0
        except:
            desain_unik = 0
        total_biaya_dtf = op.get("dtf_total_cost", op.get("biaya_dtf", 0))
        try:
            total_biaya_dtf = int(float(str(total_biaya_dtf).replace(",", ""))) if str(total_biaya_dtf).strip() else 0
        except:
            total_biaya_dtf = 0
        komisi_dtf = int(op.get("dtf_operator_commission", 0) or 0)
        updated_by = op.get("dtf_updated_by", "-")
        updated_at = op.get("dtf_updated_at", "-")
        if meter <= 0 and total_biaya_dtf <= 0:
            st.info(f"Belum ada data DTF untuk kloter {selected_kloter}.")
        else:
            df_view = pd.DataFrame([{
                "kloter_id": selected_kloter,
                "tanggal_update": updated_at,
                "operator": updated_by,
                "dtf_meter": meter,
                "desain_unik": desain_unik,
                "total_biaya_dtf": total_biaya_dtf,
                "komisi_operator_dtf": komisi_dtf
            }])
            st.dataframe(df_view, use_container_width=True)
            csv_bytes = df_view.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Export CSV", data=csv_bytes, file_name=f"dtf_report_{selected_kloter}.csv", mime="text/csv")
# ===================== FUNGSI YANG DIPERBAIKI: STRUK & INVOICE =====================
def show_receipt_invoice():
    """Halaman untuk cetak struk dan invoice yang sudah diperbaiki"""
    st.markdown(f"<h2 style='color: #D4AF37;'>🧾 Struk & Invoice</h2>", unsafe_allow_html=True)
    
    if st.session_state.df.empty:
        st.info("Belum ada order untuk dicetak.")
        return
    
    # Pilih order untuk dicetak
    order_list = st.session_state.df.copy()
    order_list["display"] = order_list.apply(
        lambda x: f"{x['invoice_number']} - {x['nama_customer']} - Rp {x['total_biaya']:,}", 
        axis=1
    )
    
    selected_order_display = st.selectbox(
        "Pilih Order untuk Cetak",
        order_list["display"].tolist(),
        key="receipt_order_select"
    )
    
    if selected_order_display:
        selected_idx = order_list[order_list["display"] == selected_order_display].index[0]
        order = st.session_state.df.loc[selected_idx]
        
        # Preview struk
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">📋 Preview Struk</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Info Studio dari settings
            settings = load_settings()
            studio_info = settings.get("studio_info", {})
            
            st.markdown(f"**{studio_info.get('nama_studio', 'DALUASE CLOTHING STUDIO')}**")
            st.markdown(f"{studio_info.get('alamat', 'SANGIHE, Kab. Kepl. Sangihe')}")
            st.markdown(f"Prov. Sulawesi Utara")
            st.markdown(f"Telp: {studio_info.get('telepon', '-')}")
            st.markdown("---")
            
            st.markdown(f"**Invoice:** {order['invoice_number']}")
            st.markdown(f"**Tanggal:** {order['tgl_order'].split()[0]}")
            st.markdown(f"**Customer:** {order['nama_customer']}")
            if order['telepon_customer']:
                st.markdown(f"**Telp:** {order['telepon_customer']}")
        
        with col2:
            st.markdown("**Rincian Order:**")
            st.markdown(f"- {order['jenis_produk']}")
            st.markdown(f"- Desain: {order['nama_desain']} ({order['tipe_desain']})")
            st.markdown(f"- {order['warna']} | {order['ukuran']} | {order['jumlah']} pcs")
            st.markdown(f"- Harga/pcs: Rp {order['harga_per_pcs']:,}")
            st.markdown("---")
            
            st.markdown(f"**Total:** Rp {order['total_biaya']:,}")
            st.markdown(f"**Bayar:** Rp {order['total_bayar']:,}")
            st.markdown(f"**Sisa:** Rp {order['remaining_payment']:,}")
            
            # Status badge
            payment_status = order['payment_status']
            status_class = "status-lunas" if payment_status == "LUNAS" else "status-panjar" if payment_status == "PANJAR" else "status-pending"
            st.markdown(f"<span class='status-badge {status_class}'>{order['payment_status']}</span>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tombol aksi yang berfungsi
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🖨️ Cetak Struk", 
                       use_container_width=True, 
                       key=f"print_{order['invoice_number']}",
                       type="primary"):
                # Generate dan download struk
                receipt_content = generate_receipt_text(order, studio_info)
                
                # Tombol download akan muncul setelah tombol cetak diklik
                st.download_button(
                    label="📥 Download Struk (.txt)",
                    data=receipt_content,
                    file_name=f"Struk_{order['invoice_number']}_{order['nama_customer']}.txt",
                    mime="text/plain",
                    key=f"download_receipt_{order['invoice_number']}"
                )
        
        with col2:
            if st.button("📧 Kirim Invoice", 
                       use_container_width=True, 
                       key=f"email_{order['invoice_number']}",
                       type="secondary"):
                # Simulasi pengiriman email/WhatsApp
                email_content = generate_email_content(order, studio_info)
                st.info("📨 Invoice siap dikirim ke customer")
                with st.expander("📋 Preview Email/WhatsApp"):
                    st.code(email_content)
                
                # Tombol untuk copy teks
                if st.button("📋 Copy untuk WhatsApp", key=f"copy_wa_{order['invoice_number']}"):
                    st.code(email_content[:500] + "...")
                    st.success("Teks berhasil disalin! Tempel di WhatsApp")
        
        with col3:
            if check_capability("INVOICE_PDF") and st.button("💾 Simpan PDF", 
                       use_container_width=True, 
                       key=f"pdf_{order['invoice_number']}",
                       type="secondary"):
                pdf_bytes = generate_receipt_pdf(order, studio_info)
                if pdf_bytes:
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_bytes,
                        file_name=f"Invoice_{order['invoice_number']}.pdf",
                        mime="application/pdf",
                        key=f"download_pdf_{order['invoice_number']}"
                    )
                else:
                    st.info("Install 'reportlab' atau 'fpdf' untuk fitur PDF.")
            elif not check_capability("INVOICE_PDF"):
                st.caption("Owner belum mengizinkan fitur simpan PDF.")
        
        st.markdown('</div>', unsafe_allow_html=True)

def generate_receipt_text(order, studio_info):
    """Generate teks struk untuk download"""
    receipt = f"""
{'='*40}
{studio_info.get('nama_studio', 'DALUASE CLOTHING STUDIO').center(40)}
{studio_info.get('alamat', 'SANGIHE').center(40)}
Telp: {studio_info.get('telepon', '-')}
{'='*40}

Invoice: {order['invoice_number']}
Tanggal: {order['tgl_order'].split()[0]}
Customer: {order['nama_customer']}
Telp: {order['telepon_customer'] or '-'}
{'-'*40}

RINCIAN ORDER:
- Produk: {order['jenis_produk']}
- Desain: {order['nama_desain']} ({order['tipe_desain']})
- Spesifikasi: {order['warna']} | {order['ukuran']} | {order['jumlah']} pcs
- Harga/pcs: Rp {order['harga_per_pcs']:,}
{'-'*40}

TOTAL: Rp {order['total_biaya']:,}
BAYAR: Rp {order['total_bayar']:,}
SISA: Rp {order['remaining_payment']:,}
Status: {order['payment_status']}
{'-'*40}

Terima kasih atas kepercayaan Anda!
{studio_info.get('nama_studio', 'DALUASE CLOTHING STUDIO')}
{'='*40}
"""
    return receipt

def generate_email_content(order, studio_info):
    """Generate konten untuk email/WhatsApp"""
    content = f"""
*INVOICE - {studio_info.get('nama_studio', 'DALUASE CLOTHING STUDIO')}*

Halo {order['nama_customer']},

Berikut detail order Anda:

📋 *Invoice:* {order['invoice_number']}
📅 *Tanggal:* {order['tgl_order'].split()[0]}

👕 *Detail Produk:*
- Produk: {order['jenis_produk']}
- Desain: {order['nama_desain']} ({order['tipe_desain']})
- Spesifikasi: {order['warna']} | {order['ukuran']} | {order['jumlah']} pcs
- Harga/pcs: Rp {order['harga_per_pcs']:,}

💰 *Rincian Pembayaran:*
- Total: *Rp {order['total_biaya']:,}*
- Sudah Bayar: Rp {order['total_bayar']:,}
- Sisa: Rp {order['remaining_payment']:,}
- Status: {order['payment_status']}

🏢 *Info Studio:*
{studio_info.get('nama_studio', 'DALUASE CLOTHING STUDIO')}
{studio_info.get('alamat', 'SANGIHE')}
Telp: {studio_info.get('telepon', '-')}

Terima kasih atas ordernya! 🙏
"""
    return content

def generate_receipt_pdf(order, studio_info):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import mm
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        y = height - 20*mm
        c.setFont("Helvetica-Bold", 14)
        c.drawString(20*mm, y, studio_info.get('nama_studio', 'DALUASE CLOTHING STUDIO'))
        y -= 7*mm
        c.setFont("Helvetica", 10)
        lines = [
            f"Invoice: {order['invoice_number']}",
            f"Tanggal: {order['tgl_order'].split()[0]}",
            f"Customer: {order['nama_customer']}",
            f"Produk: {order['jenis_produk']}",
            f"Desain: {order['nama_desain']} ({order['tipe_desain']})",
            f"Spesifikasi: {order['warna']} | {order['ukuran']} | {order['jumlah']} pcs",
            f"Harga/pcs: Rp {order['harga_per_pcs']:,}",
            f"Total: Rp {order['total_biaya']:,}",
            f"Bayar: Rp {order['total_bayar']:,}",
            f"Sisa: Rp {order['remaining_payment']:,}",
            f"Status: {order['payment_status']}"
        ]
        for line in lines:
            y -= 6*mm
            c.drawString(20*mm, y, line)
        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    except Exception:
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, studio_info.get('nama_studio', 'DALUASE CLOTHING STUDIO'), ln=True)
            for line in [
                f"Invoice: {order['invoice_number']}",
                f"Tanggal: {order['tgl_order'].split()[0]}",
                f"Customer: {order['nama_customer']}",
                f"Produk: {order['jenis_produk']}",
                f"Desain: {order['nama_desain']} ({order['tipe_desain']})",
                f"Spesifikasi: {order['warna']} | {order['ukuran']} | {order['jumlah']} pcs",
                f"Harga/pcs: Rp {order['harga_per_pcs']:,}",
                f"Total: Rp {order['total_biaya']:,}",
                f"Bayar: Rp {order['total_bayar']:,}",
                f"Sisa: Rp {order['remaining_payment']:,}",
                f"Status: {order['payment_status']}"
            ]:
                pdf.cell(0, 8, line, ln=True)
            return pdf.output(dest='S').encode('latin-1')
        except Exception:
            return None

# ===================== FUNGSI CUSTOMERS =====================
def show_customers():
    """Halaman data pelanggan - DARI V4"""
    st.markdown(f"<h2 style='color: #D4AF37;'>👥 Data Pelanggan</h2>", unsafe_allow_html=True)
    
    # Load customers data
    if CUSTOMERS_FILE.exists() and CUSTOMERS_FILE.stat().st_size > 0:
        customers_df = pd.read_csv(CUSTOMERS_FILE)
    else:
        customers_df = pd.DataFrame(columns=[
            "nama_customer", "telepon", "alamat", "total_order", 
            "total_belanja", "tgl_pertama", "tgl_terakhir"
        ])
    
    if customers_df.empty:
        st.info("Belum ada data pelanggan.")
        return
    
    # Update total belanja dari data order
    if not st.session_state.df.empty:
        # Hitung total belanja per customer
        customer_spending = st.session_state.df.groupby("nama_customer").agg({
            "total_biaya": "sum"
        }).reset_index()
        
        for idx, row in customer_spending.iterrows():
            mask = customers_df["nama_customer"] == row["nama_customer"]
            if mask.any():
                customers_df.loc[mask, "total_belanja"] = row["total_biaya"]
    
    # Search and filter
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_customer = st.text_input("🔍 Cari Pelanggan", placeholder="Nama atau telepon", key="search_customer")
    
    with col2:
        min_spending = st.number_input("Min. Total Belanja", min_value=0, value=0, step=100000, key="min_spending")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_customers = customers_df.copy()
    
    if search_customer:
        mask = (filtered_customers["nama_customer"].str.contains(search_customer, case=False) |
                filtered_customers["telepon"].str.contains(search_customer, case=False))
        filtered_customers = filtered_customers[mask]
    
    if min_spending > 0:
        filtered_customers = filtered_customers[filtered_customers["total_belanja"] >= min_spending]
    
    # Display customers
    st.markdown(f"**Total Pelanggan:** {len(filtered_customers)}")
    
    for idx, customer in filtered_customers.iterrows():
        st.markdown(f"""
        <div class="order-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 2;">
                    <strong style="color: white; font-size: 1.1rem;">{customer['nama_customer']}</strong><br>
                    <span style="color: #888; font-size: 0.9rem;">📱 {customer['telepon']}</span><br>
                    <span style="color: #888; font-size: 0.8rem;">📍 {str(customer['alamat'])[:50] if pd.notna(customer['alamat']) else ''}...</span>
                </div>
                <div style="flex: 1; text-align: center;">
                    <div style="color: #D4AF37; font-size: 1.1rem;">Rp {customer['total_belanja']:,}</div>
                    <div style="color: #888; font-size: 0.8rem;">{customer['total_order']} order</div>
                </div>
                <div style="flex: 1; text-align: right;">
                    <div style="color: #888; font-size: 0.9rem;">Terakhir</div>
                    <div style="color: #888; font-size: 0.8rem;">{customer['tgl_terakhir']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tombol aksi di bawah card
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"📞 Hubungi {customer['nama_customer'][:10]}", 
                        key=f"contact_{idx}", use_container_width=True):
                phone = customer['telepon'] if pd.notna(customer['telepon']) else '-'
                st.info(f"📱 Menghubungi {customer['nama_customer']}: {phone}")
                st.caption(f"Klik link berikut untuk WhatsApp: https://wa.me/{phone.replace('+', '')}")
        
        with col2:
            if st.button(f"📋 History {customer['nama_customer'][:10]}", 
                        key=f"history_{idx}", use_container_width=True):
                show_customer_history(customer['nama_customer'])
        
        with col3:
            if check_capability("CUSTOMER_DELETE"):
                if st.button(f"🗑️ Hapus {customer['nama_customer'][:10]}", 
                            key=f"delete_customer_{idx}", use_container_width=True):
                    st.session_state.delete_customer = {
                        "nama": customer['nama_customer'],
                        "telepon": customer['telepon']
                    }
                    st.rerun()

def show_profit_sharing_settings():
    st.markdown(f"<h2 style='color: #D4AF37;'>🤝 Profit Sharing Settings</h2>", unsafe_allow_html=True)
    settings = load_settings()
    pss = settings.get("profit_sharing_settings", {
        "owner_percent": 55,
        "coo_percent": 10,
        "smos_percent": 15,
        "pool_percent": 20,
        "last_updated": "2024-01-01",
        "updated_by": "owner"
    })
    with st.form("profit_sharing_form"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">Persentase Pembagian</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            owner_percent = st.number_input("Owner (%)", min_value=0, max_value=100, value=int(pss.get("owner_percent", 55)))
            coo_percent = st.number_input("COO (%)", min_value=0, max_value=100, value=int(pss.get("coo_percent", 10)))
        with col2:
            smos_percent = st.number_input("SMOS (%)", min_value=0, max_value=100, value=int(pss.get("smos_percent", 15)))
            pool_percent = st.number_input("Pool (%)", min_value=0, max_value=100, value=int(pss.get("pool_percent", 20)))
        st.markdown('</div>', unsafe_allow_html=True)
        submit = st.form_submit_button("💾 Simpan", type="primary")
        if submit:
            total = owner_percent + coo_percent + smos_percent + pool_percent
            if total != 100:
                st.error("Total persentase harus 100%")
            else:
                settings["profit_sharing_settings"] = {
                    "owner_percent": owner_percent,
                    "coo_percent": coo_percent,
                    "smos_percent": smos_percent,
                    "pool_percent": pool_percent,
                    "last_updated": datetime.now().strftime("%Y-%m-%d"),
                    "updated_by": st.session_state.username
                }
                save_settings(settings)
                st.success("Pengaturan profit sharing disimpan")
                st.rerun()


def show_point_settings():
    st.markdown(f"<h2 style='color: #D4AF37;'>🎯 Pengaturan Poin</h2>", unsafe_allow_html=True)
    settings = load_settings()
    pc = settings.get("point_configuration", {
        "stock_update": 1,
        "packaging_update": 1,
        "stock_sale": 5,
        "order_request_edit": 3,
        "order_other": 2,
        "distribution": 1,
        "dtf_operator": 3
    })
    with st.form("point_configuration_form"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">Poin Kloter</div>', unsafe_allow_html=True)
        colA, colB, colC, colD = st.columns(4)
        with colA:
            order_request_edit = st.number_input("Input Order (Cust. Request, Original - Edit)", min_value=0, value=int(pc.get("order_request_edit", 3)))
        with colB:
            order_other = st.number_input("Input Order (DS Original, Custr. Design)", min_value=0, value=int(pc.get("order_other", 2)))
        with colC:
            distribution = st.number_input("Distribusi (status TERKIRIM)", min_value=0, value=int(pc.get("distribution", 1)))
        with colD:
            dtf_operator = st.number_input("Operator DTF (per kloter, user pertama)", min_value=0, value=int(pc.get("dtf_operator", 3)))
        st.markdown('<div class="form-title" style="margin-top:8px;">Poin Stock</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            stock_update = st.number_input("Update Stok (ready/polos/DTF)", min_value=0, value=int(pc.get("stock_update", 1)))
        with col2:
            packaging_update = st.number_input("Update Packaging (maks 1×/14 hari)", min_value=0, value=int(pc.get("packaging_update", 1)))
        with col3:
            stock_sale = st.number_input("Penjualan Stok (per transaksi)", min_value=0, value=int(pc.get("stock_sale", 5)))
        st.markdown('</div>', unsafe_allow_html=True)
        col_s, col_r = st.columns(2)
        submit_save = col_s.form_submit_button("💾 Simpan", type="primary")
        submit_reset = col_r.form_submit_button("♻️ Reset ke Default", type="secondary")
        if submit_save:
            settings["point_configuration"] = {
                "order_request_edit": int(order_request_edit),
                "order_other": int(order_other),
                "distribution": int(distribution),
                "dtf_operator": int(dtf_operator),
                "stock_update": int(stock_update),
                "packaging_update": int(packaging_update),
                "stock_sale": int(stock_sale)
            }
            save_settings(settings)
            st.success("Pengaturan poin disimpan")
            st.rerun()
        if submit_reset:
            settings["point_configuration"] = {
                "order_request_edit": 3,
                "order_other": 2,
                "distribution": 1,
                "dtf_operator": 3,
                "stock_update": 1,
                "packaging_update": 1,
                "stock_sale": 5
            }
            save_settings(settings)
            st.success("Pengaturan poin direset ke default")
            st.rerun()

def show_customer_history(customer_name):
    """Tampilkan history order pelanggan"""
    customer_orders = st.session_state.df[
        st.session_state.df["nama_customer"] == customer_name
    ].copy()
    
    if not customer_orders.empty:
        st.markdown(f"### 📋 History Order: {customer_name}")
        st.dataframe(
            customer_orders[["tgl_order", "nama_desain", "jenis_produk", "jumlah", "total_biaya", "payment_status"]].sort_values("tgl_order", ascending=False),
            use_container_width=True
        )
        
        # Summary
        total_orders = len(customer_orders)
        total_spent = customer_orders["total_biaya"].sum()
        avg_order = total_spent / total_orders if total_orders > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Order", total_orders)
        with col2:
            st.metric("Total Belanja", f"Rp {total_spent:,}")
        with col3:
            st.metric("Rata-rata/Order", f"Rp {avg_order:,.0f}")
    else:
        st.info(f"Belum ada history order untuk {customer_name} di kloter ini.")

# ===================== FUNGSI BARU: REKAPAN KLOTER YANG DIPERBAIKI =====================
def show_kloter_summary():
    """Halaman rekap kloter untuk pemesanan supplier yang sudah diperbaiki"""
    st.markdown(f"<h2 style='color: #D4AF37;'>📊 Rekapan Kloter untuk Supplier</h2>", unsafe_allow_html=True)
    
    if st.session_state.df.empty:
        st.info("Belum ada data order untuk direkap.")
        return
    
    # Load data operasional dengan error handling
    operational_data = load_operational_data(st.session_state.current_kloter)
    panjang_dtf = operational_data.get("panjang_dtf", 0)
    
    # 1. Rekap berdasarkan Jenis Produk
    st.markdown("### 1. Rekap per Jenis Produk")
    produk_summary = st.session_state.df.groupby("jenis_produk").agg({
        "jumlah": "sum",
        "total_biaya": "sum",
        "total_harga_beli": "sum"
    }).reset_index()
    
    produk_summary = produk_summary.rename(columns={
        "jumlah": "Total Pcs",
        "total_biaya": "Total Harga Jual",
        "total_harga_beli": "Total Harga Beli"
    })
    
    # Format currency
    def format_currency(x):
        return f"Rp {x:,.0f}"
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.dataframe(
        produk_summary.style.format({
            "Total Harga Jual": format_currency,
            "Total Harga Beli": format_currency
        }).background_gradient(subset=['Total Harga Jual'], cmap='YlOrRd'),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Pivot Table: Warna x Ukuran per Jenis Produk
    st.markdown("### 2. Pivot Table: Warna × Ukuran")
    
    # Pilih jenis produk untuk pivot
    jenis_produk_list = st.session_state.df["jenis_produk"].unique()
    selected_product = st.selectbox("Pilih Jenis Produk untuk Pivot", jenis_produk_list, key="select_product_pivot")
    
    if selected_product:
        # Filter data untuk produk yang dipilih
        product_data = st.session_state.df[st.session_state.df["jenis_produk"] == selected_product]
        
        # Buat pivot table
        pivot_table = pd.pivot_table(
            product_data,
            values='jumlah',
            index='warna',
            columns='ukuran',
            aggfunc='sum',
            fill_value=0,
            margins=True,
            margins_name='TOTAL'
        )
        
        # Tampilkan pivot table
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.dataframe(pivot_table, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download pivot table
        csv = pivot_table.to_csv()
        st.download_button(
            label="📥 Download Pivot Table (CSV)",
            data=csv,
            file_name=f"pivot_{selected_product}_{st.session_state.current_kloter}.csv",
            mime="text/csv",
            key="download_pivot"
        )
    
    # 3. Ringkasan untuk Supplier
    st.markdown("### 3. Ringkasan Pesanan untuk Supplier")
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_pcs = st.session_state.df["jumlah"].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_pcs:,}</div>
            <div class="metric-label">Total Pcs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_harga_beli = st.session_state.df["total_harga_beli"].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {total_harga_beli:,}</div>
            <div class="metric-label">Total Harga Beli</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{panjang_dtf:.1f}</div>
            <div class="metric-label">Panjang DTF (m)</div>
            <div style="margin-top: 0.5rem; color: #888; font-size: 0.8rem;">Biaya: Rp {panjang_dtf * 35000:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detail per warna
    st.markdown("**Detail per Warna:**")
    warna_summary = st.session_state.df.groupby("warna")["jumlah"].sum().reset_index()
    warna_summary = warna_summary.sort_values("jumlah", ascending=False)
    
    # Tampilkan dalam 3 kolom
    cols = st.columns(3)
    for idx, row in warna_summary.iterrows():
        with cols[idx % 3]:
            st.write(f"**{row['warna']}:** {row['jumlah']:,} pcs")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 4. Export rekap lengkap
    st.markdown("---")
    st.markdown("### 4. Export Rekap Lengkap")
    
    # Buat DataFrame rekap lengkap
    rekap_data = []
    for idx, order in st.session_state.df.iterrows():
        rekap_data.append({
            "Invoice": order["invoice_number"],
            "Customer": order["nama_customer"],
            "Produk": order["jenis_produk"],
            "Desain": order["nama_desain"],
            "Warna": order["warna"],
            "Ukuran": order["ukuran"],
            "Jumlah": order["jumlah"],
            "Harga Beli/pcs": order["harga_beli_per_pcs"],
            "Total Harga Beli": order["total_harga_beli"],
            "Harga Jual/pcs": order["harga_per_pcs"],
            "Total Harga Jual": order["total_biaya"]
        })
    
    rekap_df = pd.DataFrame(rekap_data)
    
    # Tombol export
    if not rekap_df.empty:
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            rekap_df.to_excel(writer, sheet_name='Rekap Detail', index=False)
            produk_summary.to_excel(writer, sheet_name='Summary Produk', index=False)
            
            # Tambah sheet untuk pivot table
            for product in jenis_produk_list:
                product_pivot = pd.pivot_table(
                    st.session_state.df[st.session_state.df["jenis_produk"] == product],
                    values='jumlah',
                    index='warna',
                    columns='ukuran',
                    aggfunc='sum',
                    fill_value=0
                )
                # Potong nama sheet jika terlalu panjang
                sheet_name = f'Pivot {product[:20]}'
                if len(sheet_name) > 31:  # Excel sheet name limit
                    sheet_name = sheet_name[:31]
                product_pivot.to_excel(writer, sheet_name=sheet_name)
        
        buffer.seek(0)
        
        st.download_button(
            label="📥 Download Rekap Lengkap (Excel)",
            data=buffer,
            file_name=f"rekap_kloter_{st.session_state.current_kloter}_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="download_rekap_lengkap"
        )
    else:
        st.info("Tidak ada data untuk diexport")

# ===================== FUNGSI CASH FLOW =====================
def record_cash_flow(jenis, jumlah, tipe, keterangan, kloter_id):
    """Record cash flow entry - DARI V4"""
    cash_flow_file = CASH_DIR / "cash_flow.csv"
    
    if cash_flow_file.exists() and cash_flow_file.stat().st_size > 0:
        try:
            cash_flow_df = pd.read_csv(cash_flow_file)
        except:
            cash_flow_df = pd.DataFrame(columns=[
                "entry_id", "tanggal", "jenis", "jumlah", "tipe", "keterangan", 
                "kloter_id", "created_by"
            ])
    else:
        cash_flow_df = pd.DataFrame(columns=[
            "entry_id", "tanggal", "jenis", "jumlah", "tipe", "keterangan", 
            "kloter_id", "created_by"
        ])
    
    eid = f"CF-{datetime.now().strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(2)}"
    new_entry = pd.DataFrame([{
        "entry_id": eid,
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "jenis": jenis,
        "jumlah": jumlah,
        "tipe": tipe,
        "keterangan": keterangan,
        "kloter_id": kloter_id,
        "created_by": st.session_state.username
    }])
    
    cash_flow_df = pd.concat([cash_flow_df, new_entry], ignore_index=True)
    cash_flow_df.to_csv(cash_flow_file, index=False)

def delete_cash_flow_entry(entry_id):
    cash_flow_file = CASH_DIR / "cash_flow.csv"
    if cash_flow_file.exists() and cash_flow_file.stat().st_size > 0:
        try:
            df = pd.read_csv(cash_flow_file)
            if "entry_id" not in df.columns:
                return False
            df = df[df["entry_id"] != entry_id]
            df.to_csv(cash_flow_file, index=False)
            return True
        except:
            return False
    return False

def update_cash_flow_entry(entry_id, jenis, jumlah, tipe, keterangan, kloter_id):
    cash_flow_file = CASH_DIR / "cash_flow.csv"
    if cash_flow_file.exists() and cash_flow_file.stat().st_size > 0:
        try:
            df = pd.read_csv(cash_flow_file)
            if "entry_id" not in df.columns:
                return False
            mask = df["entry_id"] == entry_id
            if mask.any():
                df.loc[mask, "jenis"] = jenis
                df.loc[mask, "jumlah"] = jumlah
                df.loc[mask, "tipe"] = tipe
                df.loc[mask, "keterangan"] = keterangan
                df.loc[mask, "kloter_id"] = kloter_id
                df.to_csv(cash_flow_file, index=False)
                return True
        except:
            return False
    return False

def ensure_dtf_cash_flow(kloter_id, total_biaya_dtf, dtf_meter, unique_designs):
    cash_flow_file = CASH_DIR / "cash_flow.csv"
    desc = f"Biaya DTF: {dtf_meter} m, {unique_designs} desain (kloter {kloter_id})"
    if cash_flow_file.exists() and cash_flow_file.stat().st_size > 0:
        try:
            df = pd.read_csv(cash_flow_file)
        except:
            df = pd.DataFrame(columns=["entry_id","tanggal","jenis","jumlah","tipe","keterangan","kloter_id","created_by"])
    else:
        df = pd.DataFrame(columns=["entry_id","tanggal","jenis","jumlah","tipe","keterangan","kloter_id","created_by"])
    try:
        mask = (df.get("jenis") == "DTF") & (df.get("kloter_id") == kloter_id)
        if mask.any():
            existing = df[mask].iloc[-1]
            eid = existing.get("entry_id", "")
            existing_ket = existing.get("keterangan", desc)
            if eid:
                update_cash_flow_entry(eid, "DTF", int(total_biaya_dtf), "OUT", existing_ket, kloter_id)
                return
    except:
        pass
    record_cash_flow("DTF", int(total_biaya_dtf), "OUT", desc, kloter_id)

def ensure_dtf_commission_cash_flow(kloter_id, commission_amount, dtf_meter, unique_designs):
    cash_flow_file = CASH_DIR / "cash_flow.csv"
    desc = f"Komisi Operator DTF: {dtf_meter} m, {unique_designs} desain (kloter {kloter_id})"
    if cash_flow_file.exists() and cash_flow_file.stat().st_size > 0:
        try:
            df = pd.read_csv(cash_flow_file)
        except:
            df = pd.DataFrame(columns=["entry_id","tanggal","jenis","jumlah","tipe","keterangan","kloter_id","created_by"])
    else:
        df = pd.DataFrame(columns=["entry_id","tanggal","jenis","jumlah","tipe","keterangan","kloter_id","created_by"])
    try:
        mask = (df.get("jenis") == "DTF KOMISI") & (df.get("kloter_id") == kloter_id)
        if mask.any():
            existing = df[mask].iloc[-1]
            eid = existing.get("entry_id", "")
            existing_ket = existing.get("keterangan", desc)
            if eid:
                update_cash_flow_entry(eid, "DTF KOMISI", int(commission_amount), "OUT", existing_ket, kloter_id)
                return
    except:
        pass
    record_cash_flow("DTF KOMISI", int(commission_amount), "OUT", desc, kloter_id)

# ===================== PAGES LAINNYA =====================

def show_kas_analisis():
    """Halaman kas dan analisis global dengan styling modern"""
    st.markdown(f"<h1 style='color: #D4AF37;'>💰 Kas & Analisis Global</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Kas Global", "📊 Analisis Kloter", "📋 Cash Flow"])
    
    with tab1:
        show_global_cash()
    
    with tab2:
        show_kloter_analysis()
    
    with tab3:
        show_cash_flow()

def show_global_cash():
    """Tampilkan kas global dengan styling modern"""
    st.markdown(f"<h2 style='color: #D4AF37;'>📈 Kas Global</h2>", unsafe_allow_html=True)
    
    # Hitung total dari semua kloter
    all_kloters = get_all_kloters()
    total_revenue = 0
    total_profit = 0
    total_piutang = 0
    
    for kloter in all_kloters:
        kloter_data = load_kloter_data(kloter)
        if not kloter_data.empty:
            total_revenue += kloter_data["total_biaya"].sum()
            total_piutang += kloter_data["remaining_payment"].sum()
    
    # Load operational costs dari semua kloter
    total_operational = 0
    for kloter in all_kloters:
        operational_file = DATA_DIR / f"operational_{kloter}.json"
        if operational_file.exists():
            try:
                operational_data = load_operational_data(kloter)
                total_operational += operational_data.get("total", 0)
            except:
                continue
    
    total_profit = total_revenue - total_operational
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {total_revenue:,}</div>
            <div class="metric-label">Total Revenue</div>
            <div style="margin-top: 0.5rem; color: #888; font-size: 0.8rem;">{len(all_kloters)} kloter</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {total_operational:,}</div>
            <div class="metric-label">Total Operational</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        profit_color = '#2ecc71' if total_profit > 0 else '#e74c3c'
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {total_profit:,}</div>
            <div class="metric-label">Net Profit</div>
            <div style="margin-top: 0.5rem; color: {profit_color}; font-size: 0.9rem;">
                Margin: {(total_profit/total_revenue*100 if total_revenue > 0 else 0):.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Rp {total_piutang:,}</div>
            <div class="metric-label">Total Piutang</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ✍️ Catat Pengeluaran Manual")
    with st.form("global_manual_expense"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            jenis_pengeluaran = st.text_input("Jenis Pengeluaran*", placeholder="Contoh: Operasional Lainnya", key="global_expense_type")
            jumlah_pengeluaran = st.number_input("Jumlah (Rp)*", min_value=0, value=0, step=1000, key="global_expense_amount")
        with col2:
            keterangan_pengeluaran = st.text_area("Keterangan", height=80, key="global_expense_note")
        st.markdown('</div>', unsafe_allow_html=True)
        submit_expense = st.form_submit_button("💾 Catat Pengeluaran", type="primary")
        if submit_expense:
            if not check_capability("CASH_RECORD"):
                st.error("❌ Anda tidak memiliki izin untuk mencatat pengeluaran.")
            elif not jenis_pengeluaran.strip():
                st.warning("Jenis pengeluaran wajib diisi.")
            elif jumlah_pengeluaran <= 0:
                st.warning("Jumlah pengeluaran harus lebih dari 0.")
            else:
                record_cash_flow(jenis_pengeluaran.strip(), int(jumlah_pengeluaran), "OUT", keterangan_pengeluaran.strip(), "GLOBAL")
                st.success("✅ Pengeluaran manual berhasil dicatat ke kas global.")

def show_kloter_analysis():
    """Analisis per kloter dengan styling modern"""
    st.markdown(f"<h2 style='color: #D4AF37;'>📊 Analisis per Kloter</h2>", unsafe_allow_html=True)
    
    all_kloters = get_all_kloters()
    
    if not all_kloters:
        st.info("Belum ada data kloter.")
        return
    
    analysis_data = []
    
    for kloter in all_kloters:
        kloter_data = load_kloter_data(kloter)
        
        if not kloter_data.empty:
            # Hitung metrics
            total_revenue = kloter_data["total_biaya"].sum()
            total_orders = len(kloter_data)
            total_piutang = kloter_data["remaining_payment"].sum()
            
            # Load operational costs
            operational_data = load_operational_data(kloter)
            total_operational = operational_data.get("total", 0)
            
            total_profit = total_revenue - total_operational
            
            analysis_data.append({
                "Kloter": kloter,
                "Total Order": total_orders,
                "Revenue": total_revenue,
                "Operational": total_operational,
                "Profit": total_profit,
                "Piutang": total_piutang,
                "Profit Margin": f"{(total_profit/total_revenue*100):.1f}%" if total_revenue > 0 else "0%"
            })
    
    if analysis_data:
        analysis_df = pd.DataFrame(analysis_data)
        
        # Display table dengan styling
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.dataframe(
            analysis_df.style.format({
                "Revenue": "Rp {:,.0f}",
                "Operational": "Rp {:,.0f}",
                "Profit": "Rp {:,.0f}",
                "Piutang": "Rp {:,.0f}"
            }).background_gradient(subset=['Profit'], cmap='YlOrRd'),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

def show_cash_flow():
    """Tampilkan cash flow detail dengan styling modern"""
    st.markdown(f"<h2 style='color: #D4AF37;'>📋 Cash Flow Detail</h2>", unsafe_allow_html=True)
    
    cash_flow_file = CASH_DIR / "cash_flow.csv"
    
    if cash_flow_file.exists() and cash_flow_file.stat().st_size > 0:
        try:
            cash_flow_df = pd.read_csv(cash_flow_file)
            
            if not cash_flow_df.empty:
                # Filters
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    start_date = st.date_input("Dari Tanggal", 
                                              value=datetime.now() - timedelta(days=30),
                                              key="cash_start_date")
                
                with col2:
                    end_date = st.date_input("Sampai Tanggal", 
                                            value=datetime.now(),
                                            key="cash_end_date")
                
                with col3:
                    filter_type = st.selectbox("Tipe Transaksi", 
                                              ["Semua", "IN", "OUT"],
                                              key="cash_filter_type")
                
                kloter_values = list(cash_flow_df.get("kloter_id", pd.Series(dtype=str)).dropna().unique())
                kloter_values = ["Semua"] + sorted([str(v) for v in kloter_values])
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                filter_kloter = st.selectbox("Sumber/Kloter", kloter_values, key="cash_filter_kloter")
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Apply filters
                cash_flow_df["tanggal"] = pd.to_datetime(cash_flow_df["tanggal"])
                mask = (cash_flow_df["tanggal"].dt.date >= start_date) & \
                       (cash_flow_df["tanggal"].dt.date <= end_date)
                
                filtered_cash_flow = cash_flow_df[mask].copy()
                
                if filter_type != "Semua":
                    filtered_cash_flow = filtered_cash_flow[filtered_cash_flow["tipe"] == filter_type]
                
                if filter_kloter != "Semua" and "kloter_id" in filtered_cash_flow.columns:
                    filtered_cash_flow = filtered_cash_flow[filtered_cash_flow["kloter_id"] == filter_kloter]
                
                # Summary
                total_in = filtered_cash_flow[filtered_cash_flow["tipe"] == "IN"]["jumlah"].sum()
                total_out = filtered_cash_flow[filtered_cash_flow["tipe"] == "OUT"]["jumlah"].sum()
                net_cash = total_in - total_out
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value" style="color: #2ecc71;">Rp {total_in:,}</div>
                        <div class="metric-label">💰 Total Masuk</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value" style="color: #e74c3c;">Rp {total_out:,}</div>
                        <div class="metric-label">💸 Total Keluar</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    net_color = '#2ecc71' if net_cash > 0 else '#e74c3c'
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value" style="color: {net_color};">Rp {net_cash:,}</div>
                        <div class="metric-label">📊 Net Cash Flow</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display data
                st.markdown("### Detail Transaksi")
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.dataframe(
                    filtered_cash_flow.sort_values("tanggal", ascending=False).style.format({
                        "jumlah": "Rp {:,.0f}"
                    }).applymap(lambda x: 'color: #2ecc71' if x == "IN" else 'color: #e74c3c', subset=['tipe']),
                    use_container_width=True,
                    height=400
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("### Kelola Transaksi")
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                full_df = cash_flow_df.copy()
                full_df["display"] = full_df.apply(
                    lambda x: f"{x['tanggal']} • {x['jenis']} • Rp {int(float(x['jumlah'])):,} • {x['tipe']} • {x.get('keterangan','')}", axis=1
                )
                if not full_df.empty:
                    selected_tx = st.selectbox("Pilih transaksi", list(full_df["display"]), key="manage_cash_select")
                    idx = full_df[full_df["display"] == selected_tx].index[0] if selected_tx in list(full_df["display"]) else None
                    if idx is not None:
                        jenis_opt = ["PEMBAYARAN","BELANJA STOK","PENJUALAN STOK","OPERASIONAL","LAINNYA"]
                        current_jenis = str(full_df.loc[idx, "jenis"])
                        new_jenis = st.selectbox("Jenis", jenis_opt, index=jenis_opt.index(current_jenis) if current_jenis in jenis_opt else 0)
                        new_jumlah = st.number_input("Jumlah (Rp)", min_value=0, value=int(float(full_df.loc[idx, "jumlah"])), step=1000)
                        current_tipe = str(full_df.loc[idx, "tipe"])
                        new_tipe = st.selectbox("Tipe", ["IN","OUT"], index=["IN","OUT"].index(current_tipe) if current_tipe in ["IN","OUT"] else 0)
                        new_ket = st.text_input("Keterangan", value=str(full_df.loc[idx, "keterangan"]))
                        new_kloter = st.text_input("Kloter/Source", value=str(full_df.loc[idx, "kloter_id"]))
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("💾 Simpan Perubahan", type="primary", key="btn_save_cash_edit"):
                                if not check_capability("CASH_EDIT"):
                                    st.error("❌ Anda tidak memiliki izin untuk mengedit cash flow.")
                                else:
                                    cash_flow_df.loc[idx, "jenis"] = new_jenis
                                    cash_flow_df.loc[idx, "jumlah"] = new_jumlah
                                    cash_flow_df.loc[idx, "tipe"] = new_tipe
                                    cash_flow_df.loc[idx, "keterangan"] = new_ket
                                    cash_flow_df.loc[idx, "kloter_id"] = new_kloter
                                    cash_flow_df.to_csv(cash_flow_file, index=False)
                                    st.success("✅ Transaksi berhasil diperbarui")
                                    st.rerun()
                        with col_b:
                            if st.button("🗑️ Hapus Transaksi", type="secondary", key="btn_delete_cash"):
                                if not check_capability("CASH_DELETE"):
                                    st.error("❌ Anda tidak memiliki izin untuk menghapus cash flow.")
                                else:
                                    cash_flow_df = cash_flow_df.drop(index=idx)
                                    cash_flow_df.to_csv(cash_flow_file, index=False)
                                    st.success("✅ Transaksi berhasil dihapus")
                                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Belum ada data cash flow.")
        except pd.errors.EmptyDataError:
            st.info("File cash flow kosong.")
    else:
        st.info("Belum ada data cash flow.")

# ===================== FUNGSI STOCK SYSTEM =====================
def show_stock_system():
    """Halaman sistem stok yang lengkap"""
    st.markdown(f"<h1 style='color: #D4AF37;'>📊 Stock System</h1>", unsafe_allow_html=True)
    
    try:
        settings = load_settings()
        pkg_prices = settings.get("packaging_prices", {})
        packaging_file = STOCK_DIR / "packaging.json"
        low_items = []
        if packaging_file.exists():
            with open(packaging_file, 'r') as f:
                pdata = json.load(f)
            for it in pdata.get("items", []):
                name = str(it.get("item",""))
                qty = int(it.get("jumlah", 0) or 0)
                if name and qty < 100:
                    low_items.append(f"{name} ({qty} pcs)")
        if pkg_prices and low_items:
            st.warning("Packaging stok rendah (<100 pcs): " + ", ".join(low_items))
    except:
        pass
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📦 Stock Ready", "⚪ Stock Mentah", "🎁 Stock Packaging",
        "🛒 Penjualan Stok", "🧾 Struk Stok", "💰 Bonus Stock"
    ])
    
    with tab1:
        show_stock_ready_enhanced()
    
    with tab2:
        show_stock_raw_enhanced()
    
    with tab3:
        show_stock_packaging_enhanced()
    
    with tab4:
        show_stock_sales()
    
    with tab5:
        show_stock_receipts()
    
    with tab6:
        show_stock_bonus_page()

def handle_stock_management(file_key, title, dataframe_key):
    if file_key == "ready":
        st.markdown(f"<h2 style='color: #D4AF37;'>{title}</h2>", unsafe_allow_html=True)
        settings = load_settings()
        products = list(settings.get("products", {}).keys())
        stock_file = STOCK_DIR / "stock_ready.csv"
        if stock_file.exists() and stock_file.stat().st_size > 0:
            stock_df = pd.read_csv(stock_file)
        else:
            stock_df = pd.DataFrame(columns=[
                "jenis_produk", "warna", "ukuran", "nama_desain",
                "jumlah", "harga_beli", "harga_jual", "tgl_masuk", "keterangan"
            ])
        with st.form("add_stock_ready_form"):
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="form-title">➕ Add Stock Ready</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                jenis_produk = st.selectbox("Product", products, key="stock_ready_product")
                warna = st.selectbox("Color", COMPLETE_COLORS, key="stock_ready_color")
            with col2:
                available_sizes = settings.get("sizes", {}).get(jenis_produk, ["S", "M", "L", "XL", "2XL", "3XL"])
                ukuran = st.selectbox("Size", available_sizes, key="stock_ready_size")
                design_options = settings.get("original_designs", [])
                nama_desain = st.selectbox("Design Name (optional)", [""] + design_options, key="stock_ready_design")
            with col3:
                jumlah = st.number_input("Quantity", min_value=1, value=1, key="stock_ready_qty")
                harga_beli = st.number_input("Buy Price (Rp)", min_value=0, value=0, step=1000, key="stock_ready_buy")
                harga_jual = st.number_input("Sell Price (Rp)", min_value=0, value=0, step=1000, key="stock_ready_sell")
            keterangan = st.text_area("Notes", key="stock_ready_note")
            st.markdown('</div>', unsafe_allow_html=True)
            if not check_capability("STOCK_ADD"):
                st.error("❌ You don't have permission to add stock.")
            elif st.form_submit_button("➕ Add Stock", type="primary"):
                new_stock = pd.DataFrame([{
                    "jenis_produk": jenis_produk,
                    "warna": warna,
                    "ukuran": ukuran,
                    "nama_desain": nama_desain,
                    "jumlah": jumlah,
                    "harga_beli": harga_beli,
                    "harga_jual": harga_jual,
                    "tgl_masuk": datetime.now().strftime("%Y-%m-%d"),
                    "keterangan": keterangan
                }])
                stock_df = pd.concat([stock_df, new_stock], ignore_index=True)
                stock_df.to_csv(stock_file, index=False)
                settings = load_settings()
                pc = settings.get("point_configuration", {})
                record_stock_point(
                    st.session_state.username,
                    "STOCK_UPDATE",
                    f"{jenis_produk} | {warna} | {ukuran}",
                    int(pc.get("stock_update", 1))
                )
                if harga_beli > 0:
                    record_cash_flow(
                        "BELANJA STOK",
                        harga_beli * jumlah,
                        "OUT",
                        f"Stock purchase: {jenis_produk} {warna} {ukuran} - {nama_desain}",
                        "STOCK"
                    )
                st.success("✅ Stock ready added!")
                st.rerun()
        return
    if file_key == "raw":
        st.markdown(f"<h2 style='color: #D4AF37;'>{title}</h2>", unsafe_allow_html=True)
        settings = load_settings()
        products = list(settings.get("products", {}).keys())
        tab1, tab2 = st.tabs(["Plain Tees", "DTF Prints"])
        with tab1:
            st.markdown("### Plain Tees Ready")
            polos_file = STOCK_DIR / "stock_polos.csv"
            if polos_file.exists() and polos_file.stat().st_size > 0:
                polos_df = pd.read_csv(polos_file)
            else:
                polos_df = pd.DataFrame(columns=[
                    "jenis_produk", "warna", "ukuran", "jumlah",
                    "harga_beli", "tgl_masuk", "keterangan"
                ])
            with st.form("add_stock_polos_form"):
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown('<div class="form-title">➕ Add Plain Tees Stock</div>', unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                with col1:
                    jenis_produk_polos = st.selectbox("Product", products, key="stock_polos_product")
                    warna_polos = st.selectbox("Color", COMPLETE_COLORS, key="stock_polos_color")
                with col2:
                    available_sizes = settings.get("sizes", {}).get(jenis_produk_polos, ["S", "M", "L", "XL", "2XL", "3XL"])
                    ukuran_polos = st.selectbox("Size", available_sizes, key="stock_polos_size")
                    jumlah_polos = st.number_input("Quantity", min_value=1, value=1, key="stock_polos_qty")
                with col3:
                    harga_beli_polos = st.number_input("Buy Price (Rp)", min_value=0, value=0, step=1000, key="stock_polos_price")
                keterangan_polos = st.text_input("Notes", key="stock_polos_note")
                st.markdown('</div>', unsafe_allow_html=True)
                if st.form_submit_button("➕ Add Plain Tees Stock", type="primary"):
                    new_polos = pd.DataFrame([{
                        "jenis_produk": jenis_produk_polos,
                        "warna": warna_polos,
                        "ukuran": ukuran_polos,
                        "jumlah": jumlah_polos,
                        "harga_beli": harga_beli_polos,
                        "tgl_masuk": datetime.now().strftime("%Y-%m-%d"),
                        "keterangan": keterangan_polos
                    }])
                    polos_df = pd.concat([polos_df, new_polos], ignore_index=True)
                    polos_df.to_csv(polos_file, index=False)
                    settings = load_settings()
                    pc = settings.get("point_configuration", {})
                    record_stock_point(
                        st.session_state.username,
                        "STOCK_UPDATE",
                        f"POLOS: {jenis_produk_polos} {warna_polos} {ukuran_polos}",
                        int(pc.get("stock_update", 1))
                    )
                    if harga_beli_polos > 0:
                        record_cash_flow(
                            "BELANJA STOK",
                            harga_beli_polos * jumlah_polos,
                            "OUT",
                            f"Plain tees purchase: {jenis_produk_polos} {warna_polos} {ukuran_polos}",
                            "STOCK"
                        )
                    st.success("✅ Plain tees stock added!")
                    st.rerun()
            if not polos_df.empty:
                st.markdown("### Plain Tees Stock List")
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    filter_product = st.selectbox("Filter Product", ["All"] + list(polos_df["jenis_produk"].unique()), key="filter_polos_product")
                with col2:
                    filter_color = st.selectbox("Filter Color", ["All"] + list(polos_df["warna"].unique()), key="filter_polos_color")
                st.markdown('</div>', unsafe_allow_html=True)
                filtered_polos = polos_df.copy()
                if filter_product != "All":
                    filtered_polos = filtered_polos[filtered_polos["jenis_produk"] == filter_product]
                if filter_color != "All":
                    filtered_polos = filtered_polos[filtered_polos["warna"] == filter_color]
            st.dataframe(
                filtered_polos.style.format({
                    "harga_beli": "Rp {:,.0f}"
                }),
                use_container_width=True
            )
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### Edit Item Kaos Polos")
            polos_df["display"] = polos_df.apply(lambda x: f"{x['jenis_produk']} • {x['warna']} • {x['ukuran']} ({x['jumlah']} pcs)", axis=1)
            edit_polos_option = st.selectbox("Pilih item untuk diedit", list(polos_df["display"]), key="edit_stock_polos_option")
            if not check_capability("STOCK_EDIT"):
                st.error("❌ You don't have permission to edit stock.")
            else:
                peidx = polos_df[polos_df["display"] == edit_polos_option].index[0] if edit_polos_option in list(polos_df["display"]) else None
                if peidx is not None:
                    new_qty_p = st.number_input("Jumlah (pcs)", min_value=0, value=int(polos_df.loc[peidx, "jumlah"]), step=1, key="edit_stock_polos_qty")
                    new_buy_p = st.number_input("Harga Beli (Rp)", min_value=0, value=int(polos_df.loc[peidx, "harga_beli"]), step=1000, key="edit_stock_polos_buy")
                    new_note_p = st.text_input("Keterangan", value=str(polos_df.loc[peidx, "keterangan"]), key="edit_stock_polos_note")
                    if st.button("💾 Simpan Perubahan Kaos Polos", type="primary", key="btn_save_stock_polos"):
                        polos_df.loc[peidx, "jumlah"] = new_qty_p
                        polos_df.loc[peidx, "harga_beli"] = new_buy_p
                        polos_df.loc[peidx, "keterangan"] = new_note_p
                        polos_df.to_csv(polos_file, index=False)
                        st.success("✅ Item kaos polos diperbarui")
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown("### Hapus Item Kaos Polos")
            polos_df["display"] = polos_df.apply(lambda x: f"{x['jenis_produk']} • {x['warna']} • {x['ukuran']} ({x['jumlah']} pcs)", axis=1)
            delete_polos_option = st.selectbox("Pilih item untuk dihapus", list(polos_df["display"]), key="delete_stock_polos_option")
            if not check_capability("STOCK_DELETE"):
                st.error("❌ You don't have permission to delete stock.")
            elif st.button("🗑️ Hapus Item Polos", type="secondary", key="delete_stock_polos_button"):
                del_idx = polos_df[polos_df["display"] == delete_polos_option].index[0]
                polos_df = polos_df.drop(index=del_idx)
                polos_df.to_csv(polos_file, index=False)
                st.success("✅ Item kaos polos telah dihapus")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            if polos_df.empty:
                st.info("Belum ada data stock kaos polos.")
        with tab2:
            st.markdown("### DTF Prints Ready")
            dtf_file = STOCK_DIR / "stock_dtf.csv"
            if dtf_file.exists() and dtf_file.stat().st_size > 0:
                dtf_df = pd.read_csv(dtf_file)
            else:
                dtf_df = pd.DataFrame(columns=[
                    "nama_desain", "cocok_warna", "ukuran_sablon", "jumlah",
                    "harga_beli", "tgl_masuk", "keterangan"
                ])
            with st.form("add_stock_dtf_form"):
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown('<div class="form-title">➕ Add DTF Prints Stock</div>', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    design_options = settings.get("original_designs", [])
                    nama_desain_dtf = st.selectbox("Design Name*", design_options, key="stock_dtf_design")
                    cocok_warna = st.selectbox("Compatible Color", COMPLETE_COLORS, key="stock_dtf_color")
                with col2:
                    ukuran_sablon = "-"
                    jumlah_dtf = st.number_input("Quantity", min_value=1, value=1, key="stock_dtf_qty")
                    harga_beli_dtf = st.number_input("Buy Price (Rp)", min_value=0, value=10000, step=1000, key="stock_dtf_price")
                keterangan_dtf = st.text_input("Notes", key="stock_dtf_note")
                st.markdown('</div>', unsafe_allow_html=True)
                if st.form_submit_button("➕ Add DTF Prints Stock", type="primary"):
                    new_dtf = pd.DataFrame([{
                        "nama_desain": nama_desain_dtf,
                        "cocok_warna": cocok_warna,
                        "ukuran_sablon": ukuran_sablon,
                        "jumlah": jumlah_dtf,
                        "harga_beli": harga_beli_dtf,
                        "tgl_masuk": datetime.now().strftime("%Y-%m-%d"),
                        "keterangan": keterangan_dtf
                    }])
                    dtf_df = pd.concat([dtf_df, new_dtf], ignore_index=True)
                    dtf_df.to_csv(dtf_file, index=False)
                    settings = load_settings()
                    pc = settings.get("point_configuration", {})
                    record_stock_point(
                        st.session_state.username,
                        "STOCK_UPDATE",
                        f"DTF: {nama_desain_dtf} | {cocok_warna}",
                        int(pc.get("stock_update", 1))
                    )
                    if harga_beli_dtf > 0:
                        record_cash_flow(
                            "BELANJA STOK",
                            harga_beli_dtf * jumlah_dtf,
                            "OUT",
                            f"DTF purchase: {nama_desain_dtf} for color {cocok_warna}",
                            "STOCK"
                        )
                    st.success("✅ DTF prints stock has been added!")
                    st.rerun()
            if dtf_df.empty:
                st.info("Belum ada data stock sablon DTF.")
            else:
                st.markdown("### DTF Prints Stock List")
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    filter_design = st.selectbox("Filter Design", ["All"] + list(dtf_df["nama_desain"].unique()), key="filter_dtf_design")
                with col2:
                    filter_color = st.selectbox("Filter Compatible Color", ["All"] + list(dtf_df["cocok_warna"].unique()), key="filter_dtf_color")
                st.markdown('</div>', unsafe_allow_html=True)
                filtered_dtf = dtf_df.copy()
                if filter_design != "All":
                    filtered_dtf = filtered_dtf[filtered_dtf["nama_desain"] == filter_design]
                if filter_color != "All":
                    filtered_dtf = filtered_dtf[filtered_dtf["cocok_warna"] == filter_color]
                st.dataframe(
                    filtered_dtf.style.format({
                        "harga_beli": "Rp {:,.0f}"
                    }),
                    use_container_width=True
                )
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown("### Edit Item DTF Prints")
                dtf_df["display"] = dtf_df.apply(lambda x: f"{x['nama_desain']} • {x['cocok_warna']} • {x['ukuran_sablon']} ({x['jumlah']} pcs)", axis=1)
                edit_dtf_option = st.selectbox("Pilih item untuk diedit", list(dtf_df["display"]), key="edit_stock_dtf_option")
                if not check_capability("STOCK_EDIT"):
                    st.error("❌ You don't have permission to edit stock.")
                else:
                    deidx = dtf_df[dtf_df["display"] == edit_dtf_option].index[0] if edit_dtf_option in list(dtf_df["display"]) else None
                    if deidx is not None:
                        new_qty_d = st.number_input("Jumlah (pcs)", min_value=0, value=int(dtf_df.loc[deidx, "jumlah"]), step=1, key="edit_stock_dtf_qty")
                        new_buy_d = st.number_input("Harga Beli (Rp)", min_value=0, value=int(dtf_df.loc[deidx, "harga_beli"]), step=1000, key="edit_stock_dtf_buy")
                        new_note_d = st.text_input("Keterangan", value=str(dtf_df.loc[deidx, "keterangan"]), key="edit_stock_dtf_note")
                        if st.button("💾 Simpan Perubahan DTF", type="primary", key="btn_save_stock_dtf"):
                            dtf_df.loc[deidx, "jumlah"] = new_qty_d
                            dtf_df.loc[deidx, "harga_beli"] = new_buy_d
                            dtf_df.loc[deidx, "keterangan"] = new_note_d
                            dtf_df.to_csv(dtf_file, index=False)
                            st.success("✅ Item DTF prints diperbarui")
                            st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown("### Hapus Item DTF Prints")
                dtf_df["display"] = dtf_df.apply(lambda x: f"{x['nama_desain']} • {x['cocok_warna']} • {x['ukuran_sablon']} ({x['jumlah']} pcs)", axis=1)
                delete_dtf_option = st.selectbox("Pilih item untuk dihapus", list(dtf_df["display"]), key="delete_stock_dtf_option")
                if not check_capability("STOCK_DELETE"):
                    st.error("❌ You don't have permission to delete stock.")
                elif st.button("🗑️ Hapus Item DTF", type="secondary", key="delete_stock_dtf_button"):
                    del_idx = dtf_df[dtf_df["display"] == delete_dtf_option].index[0]
                    dtf_df = dtf_df.drop(index=del_idx)
                    dtf_df.to_csv(dtf_file, index=False)
                    st.success("✅ Item DTF prints telah dihapus")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        return
    if file_key == "packaging":
        st.markdown(f"<h2 style='color: #D4AF37;'>{title}</h2>", unsafe_allow_html=True)
        settings = load_settings()
        pkg_prices = settings.get("packaging_prices", {})
        packaging_items = [{"nama": n, "satuan": "pcs", "harga": int(pkg_prices.get(n, 0))} for n in sorted(pkg_prices.keys())]
        if not packaging_items:
            st.info("Belum ada item packaging. Tambahkan di Pengaturan → 💲 Harga Packaging.")
            return
        packaging_file = STOCK_DIR / "packaging.json"
        if packaging_file.exists():
            try:
                with open(packaging_file, 'r') as f:
                    current_stock = json.load(f)
                current_items = current_stock.get("items", [])
            except:
                current_items = []
        else:
            current_items = []
        with st.form("update_packaging_form"):
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="form-title">📦 Update Stock Packaging</div>', unsafe_allow_html=True)
            updates = []
            for item in packaging_items:
                col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
                with col1:
                    st.write(f"**{item['nama']}**")
                with col2:
                    st.write(f"{item['satuan']}")
                with col3:
                    current_qty = 0
                    for current_item in current_items:
                        if current_item.get("item") == item["nama"]:
                            current_qty = current_item.get("jumlah", 0)
                            break
                    jumlah = st.number_input(
                        f"Jumlah {item['nama']}",
                        min_value=0,
                        value=current_qty,
                        key=f"pack_{item['nama']}"
                    )
                    updates.append({"item": item['nama'], "jumlah": jumlah})
                with col4:
                    st.write(f"Rp {item['harga']:,}/pcs")
            keterangan = st.text_input("Keterangan Update", placeholder="Misal: Restock dari supplier", key="packaging_note")
            st.markdown('</div>', unsafe_allow_html=True)
            if st.form_submit_button("💾 Update Stock Packaging", type="primary"):
                if not check_capability("PACKAGING_EDIT") and (st.session_state.role or "").lower() != "owner":
                    st.error("❌ Anda tidak memiliki izin untuk mengedit stock packaging.")
                    st.stop()
                can_earn, msg = validate_packaging_point(st.session_state.username)
                pkg_points = 0
                prev_quant = {it.get("item"): int(it.get("jumlah", 0) or 0) for it in current_items}
                total_positive_inc = 0
                low_stock_warn = []
                for u in updates:
                    name = u.get("item")
                    new_qty = int(u.get("jumlah", 0) or 0)
                    old_qty = int(prev_quant.get(name, 0))
                    if new_qty > old_qty:
                        total_positive_inc += (new_qty - old_qty)
                        if new_qty < 100:
                            low_stock_warn.append(f"{name}: {new_qty} pcs (minimal 100)")
                if low_stock_warn:
                    st.warning("Minimal stok per item 100 pcs:\n- " + "\n- ".join(low_stock_warn))
                positive_inc = total_positive_inc > 0
                if not can_earn and positive_inc:
                    st.warning(msg)
                elif can_earn and positive_inc:
                    settings = load_settings()
                    pc = settings.get("point_configuration", {})
                    pkg_points = int(pc.get("packaging_update", 1))
                    record_stock_point(
                        st.session_state.username,
                        "PACKAGING_UPDATE",
                        "Update packaging materials",
                        pkg_points
                    )
                packaging_data = {
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "updated_by": st.session_state.username,
                    "items": updates,
                    "keterangan": keterangan
                }
                price_map = {i["nama"]: i["harga"] for i in packaging_items}
                delta_belanja = 0
                desc_parts = []
                for u in updates:
                    name = u.get("item")
                    new_qty = int(u.get("jumlah", 0) or 0)
                    old_qty = int(prev_quant.get(name, 0))
                    inc = max(new_qty - old_qty, 0)
                    if inc > 0:
                        delta_belanja += inc * int(price_map.get(name, 0))
                        desc_parts.append(f"{name} +{inc} pcs")
                with open(packaging_file, 'w') as f:
                    json.dump(packaging_data, f, indent=2)
                if delta_belanja > 0:
                    try:
                        desc = "Restock packaging: " + ", ".join(desc_parts)
                        record_cash_flow("BELANJA PACKAGING", int(delta_belanja), "OUT", desc, "STOCK")
                    except:
                        pass
                st.success("✅ Packaging updated!" + (f" +{pkg_points} poin" if can_earn else ""))
                st.rerun()
        st.markdown("---")
        st.markdown("### 📋 Stock Packaging Saat Ini")
        if packaging_file.exists():
            try:
                with open(packaging_file, 'r') as f:
                    current_stock = json.load(f)
                stock_data = []
                for item in current_stock.get("items", []):
                    qty = int(item.get("jumlah", 0) or 0)
                    stock_data.append({
                        "Item": item.get("item", ""),
                        "Jumlah": qty,
                        "Satuan": "pcs",
                        "Status": "⚠️ LOW" if qty < 100 else "✅ OK"
                    })
                if stock_data:
                    stock_df = pd.DataFrame(stock_data)
                    st.dataframe(stock_df, use_container_width=True)
                    low_items = [f"{row['Item']} ({row['Jumlah']} pcs)" for row in stock_data if row["Jumlah"] < 100]
                    if low_items:
                        st.warning("Item stok rendah (<100 pcs): " + ", ".join(low_items))
                    total_value = 0
                    price_map = {i["nama"]: i["harga"] for i in packaging_items}
                    for stock_item in current_stock.get("items", []):
                        nm = stock_item.get("item")
                        qty = int(stock_item.get("jumlah", 0) or 0)
                        total_value += qty * int(price_map.get(nm, 0))
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">Rp {total_value:,}</div>
                        <div class="metric-label">Total Nilai Stok Packaging</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.caption(f"Terakhir update: {current_stock.get('updated_at', '-')}")
                if current_stock.get("keterangan"):
                    st.caption(f"Keterangan: {current_stock['keterangan']}")
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.markdown("### Hapus Item Packaging")
                names = [i["nama"] for i in packaging_items]
                del_item = st.selectbox("Pilih item", names, key="delete_packaging_item")
                if st.button("🗑️ Hapus Item (set jumlah 0)", type="secondary", key="btn_delete_packaging"):
                    if not check_capability("PACKAGING_DELETE") and (st.session_state.role or "").lower() != "owner":
                        st.error("❌ Anda tidak memiliki izin untuk menghapus stock packaging.")
                    else:
                        items = current_stock.get("items", [])
                        found = False
                        for it in items:
                            if it.get("item") == del_item:
                                it["jumlah"] = 0
                                found = True
                                break
                        if not found:
                            items.append({"item": del_item, "jumlah": 0})
                        with open(packaging_file, 'w') as f:
                            json.dump({
                                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "updated_by": st.session_state.username,
                                "items": items,
                                "keterangan": current_stock.get("keterangan","")
                            }, f, indent=2)
                        st.success("✅ Item packaging dihapus (jumlah di-set 0)")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            except:
                st.info("Error membaca data packaging")
        else:
            st.info("Belum ada data stock packaging.")
        return

def show_stock_ready_enhanced():
    handle_stock_management("ready", "📦 Stock Ready", "stock_ready")

def show_profit_sharing_report():
    st.markdown(f"<h2 style='color: #D4AF37;'>📋 Laporan Pembagian Profit</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #888;'>Kloter aktif: <strong>{st.session_state.current_kloter}</strong></p>", unsafe_allow_html=True)
    df = load_profit_sharing_history()
    if df.empty:
        st.info("Belum ada data history pembagian.")
        return
    all_kloters = get_all_kloters()
    col1, col2, col3 = st.columns(3)
    with col1:
        sel_kloter = st.selectbox("Pilih Kloter", ["Semua"] + all_kloters, index=0)
    with col2:
        start_date = st.date_input("Dari Tanggal", value=datetime.now() - timedelta(days=30))
    with col3:
        end_date = st.date_input("Sampai Tanggal", value=datetime.now())
    if sel_kloter != "Semua":
        df = load_profit_sharing_history(sel_kloter, start_date, end_date)
    else:
        df = load_profit_sharing_history(None, start_date, end_date)
    if df.empty:
        st.info("Tidak ada data pada rentang ini.")
        return
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.dataframe(df.sort_values(["kloter_id","tanggal_perhitungan","username"]), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    try:
        out = BytesIO()
        with pd.ExcelWriter(out, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="History")
        out.seek(0)
        st.download_button("📥 Export Excel", data=out, file_name="profit_sharing_history.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception:
        try:
            out = BytesIO()
            with pd.ExcelWriter(out, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="History")
            out.seek(0)
            st.download_button("📥 Export Excel", data=out, file_name="profit_sharing_history.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e:
            st.error(f"Gagal export: {e}")
    return
def show_stock_raw_enhanced():
    handle_stock_management("raw", "⚪ Raw Stock", "stock_raw")

def show_stock_bonus_page():
    st.markdown(f"<h2 style='color: #D4AF37;'>💰 Bonus Stock System</h2>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊 Bulan Ini", "📋 Riwayat Bonus", "📝 Riwayat Poin"])
    with tab1:
        show_current_month_bonus()
    with tab2:
        show_bonus_history()
    with tab3:
        show_stock_points_history()

def show_current_month_bonus():
    current_month = datetime.now().strftime("%Y-%m")
    st.markdown(f"### Periode: {current_month}")
    bonus_df = calculate_monthly_stock_bonus(current_month)
    if bonus_df.empty:
        st.info("Belum ada aktivitas stock bulan ini.")
        return
    total_profit = float(bonus_df["profit_from_sale"].sum())
    bonus_pool = total_profit * 0.05
    total_points = int(bonus_df["points_earned"].sum())
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Total Profit", f"Rp {total_profit:,.0f}")
    with col2:
        st.metric("🏦 Bonus Pool (5%)", f"Rp {bonus_pool:,.0f}")
    with col3:
        st.metric("🎯 Total Poin", f"{total_points:,}")
    st.markdown("### Perhitungan per User")
    display_df = bonus_df[[
        "username","points_earned","commission","pool_percent","pool_bonus","total_bonus"
    ]].copy()
    display_df.columns = ["Username","Total Poin","Komisi (5%)","% Pool","Bonus Pool","Total Bonus"]
    st.dataframe(
        display_df.style.format({
            "Komisi (5%)": "Rp {:,.0f}",
            "Bonus Pool": "Rp {:,.0f}",
            "Total Bonus": "Rp {:,.0f}",
            "% Pool": "{:.1f}%"
        }),
        use_container_width=True
    )
    if check_capability("CASH_RECORD"):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Simpan Perhitungan", type="primary", use_container_width=True):
                bonus_id = save_stock_bonus_history(bonus_df)
                st.success(f"✅ Bonus disimpan! ID: {bonus_id}")
                st.rerun()
        with col2:
            if st.button("📥 Export ke Excel", use_container_width=True):
                buffer = BytesIO()
                try:
                    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                        bonus_df.to_excel(writer, sheet_name="Bonus Summary", index=False)
                        points_df = load_stock_points()
                        try:
                            month_points = points_df[pd.to_datetime(points_df["tanggal"]).dt.strftime("%Y-%m") == current_month]
                        except:
                            month_points = points_df
                        if not month_points.empty:
                            month_points.to_excel(writer, sheet_name="Detail Transaksi", index=False)
                except Exception:
                    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                        bonus_df.to_excel(writer, sheet_name="Bonus Summary", index=False)
                        points_df = load_stock_points()
                        try:
                            month_points = points_df[pd.to_datetime(points_df["tanggal"]).dt.strftime("%Y-%m") == current_month]
                        except:
                            month_points = points_df
                        if not month_points.empty:
                            month_points.to_excel(writer, sheet_name="Detail Transaksi", index=False)
                buffer.seek(0)
                st.download_button(
                    label="Download Excel",
                    data=buffer,
                    file_name=f"bonus_stock_{current_month}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

def show_bonus_history():
    history_file = DATA_DIR / "stock_bonus_history.csv"
    if not (history_file.exists() and history_file.stat().st_size > 0):
        st.info("Belum ada riwayat bonus.")
        return
    try:
        df = pd.read_csv(history_file)
    except pd.errors.EmptyDataError:
        st.info("Belum ada riwayat bonus.")
        return
    if df.empty:
        st.info("Belum ada riwayat bonus.")
        return
    st.markdown("### Riwayat Bonus Bulanan")
    months = ["Semua"] + sorted(set(df.get("month_year", "").astype(str)))
    users = ["Semua"] + sorted(set(df.get("username", "").astype(str)))
    col1, col2 = st.columns(2)
    with col1:
        sel_month = st.selectbox("Filter Bulan", months, index=0)
    with col2:
        sel_user = st.selectbox("Filter User", users, index=0)
    show_df = df.copy()
    if sel_month != "Semua":
        show_df = show_df[show_df["month_year"].astype(str) == sel_month]
    if sel_user != "Semua":
        show_df = show_df[show_df["username"].astype(str) == sel_user]
    st.dataframe(show_df.sort_values(["month_year","username"]), use_container_width=True)

def show_stock_points_history():
    points_df = load_stock_points()
    if points_df.empty:
        st.info("Belum ada riwayat poin.")
        return
    st.markdown("### Riwayat Poin Stok")
    try:
        points_df["month"] = pd.to_datetime(points_df["tanggal"]).dt.strftime("%Y-%m")
    except:
        points_df["month"] = ""
    months = ["Semua"] + sorted(points_df["month"].unique())
    users = ["Semua"] + sorted(points_df["username"].astype(str).unique())
    col1, col2 = st.columns(2)
    with col1:
        sel_month = st.selectbox("Filter Bulan", months, index=0)
    with col2:
        sel_user = st.selectbox("Filter User", users, index=0)
    show_df = points_df.copy()
    if sel_month != "Semua":
        show_df = show_df[show_df["month"] == sel_month]
    if sel_user != "Semua":
        show_df = show_df[show_df["username"].astype(str) == sel_user]
    st.dataframe(show_df.sort_values("tanggal", ascending=False), use_container_width=True)

def show_stock_packaging_enhanced():
    handle_stock_management("packaging", "🎁 Stock Packaging", "stock_packaging")

def show_stock_sales():
    st.markdown(f"<h2 style='color: #D4AF37;'>🛒 Penjualan Stok</h2>", unsafe_allow_html=True)
    mode = st.radio("Sumber Penjualan", ["Stock Ready", "Stock Mentah"], index=0, horizontal=True)

    if mode == "Stock Ready":
        stock_file = STOCK_DIR / "stock_ready.csv"
        if stock_file.exists() and stock_file.stat().st_size > 0:
            df = pd.read_csv(stock_file)
        else:
            st.info("Belum ada stock ready.")
            return
        if df.empty:
            st.info("Belum ada stock ready.")
            return
        df["display"] = df.apply(lambda x: f"{x['jenis_produk']} • {x['warna']} • {x['ukuran']} • {x.get('nama_desain','')} ({x['jumlah']} pcs)", axis=1)
        selected = st.selectbox("Pilih Item", df["display"])
        qty = st.number_input("Jumlah Dijual (pcs)", min_value=1, value=1, step=1)
        price_per = st.number_input("Harga Jual per pcs (Rp)", min_value=0, value=0, step=1000)
        buyer = st.text_input("Nama Pembeli")
        buyer_addr = st.text_area("Alamat Pembeli", height=80)
        buyer_phone = st.text_input("Kontak Pembeli")
        metode = st.selectbox("Metode Bayar", ["CASH", "TRANSFER", "QRIS"])
        note = st.text_input("Keterangan")
        if not check_capability("STOCK_SELL"):
            st.error("❌ Anda tidak memiliki izin untuk menjual stok.")
            return
        if st.button("Proses Penjualan", type="primary"):
            idx = df[df["display"] == selected].index[0]
            prod = df.loc[idx, "jenis_produk"]
            color = df.loc[idx, "warna"]
            size = df.loc[idx, "ukuran"]
            design = df.loc[idx, "nama_desain"] if "nama_desain" in df.columns else "-"
            available = int(df.loc[idx, "jumlah"])
            if qty > available:
                st.error("Jumlah melebihi stok yang tersedia")
            else:
                new_qty = available - qty
                if new_qty <= 0:
                    df = df.drop(index=idx)
                else:
                    df.loc[idx, "jumlah"] = new_qty
                df.to_csv(stock_file, index=False)
                total = price_per * qty
                record_cash_flow(
                    "PENJUALAN STOK",
                    int(total),
                    "IN",
                    f"Penjualan stok: {prod} {color} {size} {qty} pcs untuk {buyer}. {note}",
                    "STOCK"
                )
                try:
                    buy_price = int(df.loc[idx, "harga_beli"]) if "harga_beli" in df.columns else 0
                except:
                    buy_price = 0
                if price_per > buy_price:
                    profit_per = price_per - buy_price
                    commission = profit_per * qty * 0.05
                    profit_total = profit_per * qty
                else:
                    commission = 0
                    profit_total = 0
                settings = load_settings()
                pc = settings.get("point_configuration", {})
                sale_points = int(pc.get("stock_sale", 5))
                record_stock_point(
                    st.session_state.username,
                    "STOCK_SALE",
                    f"Jual: {selected} | {qty} pcs",
                    sale_points,
                    float(profit_total),
                    float(commission)
                )
                if commission > 0:
                    st.info(f"💰 Komisi 5%: Rp {commission:,.0f}")
                sales_file = STOCK_DIR / "sales_from_stock.csv"
                if sales_file.exists() and sales_file.stat().st_size > 0:
                    sales_df = pd.read_csv(sales_file)
                else:
                    sales_df = pd.DataFrame(columns=[
                        "sale_id","tanggal","jenis_produk","warna","ukuran","nama_desain","jumlah","harga_jual_per_pcs","total","pembeli","alamat_pembeli","telepon_pembeli","metode","keterangan","payment_proof","created_by"
                    ])
                # Pastikan kolom baru ada
                for col in ["alamat_pembeli","telepon_pembeli","sale_id","payment_proof"]:
                    if col not in sales_df.columns:
                        sales_df[col] = ""
                sale_id = generate_stock_sale_id()
                new_sale = pd.DataFrame([{
                    "sale_id": sale_id,
                    "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "jenis_produk": prod,
                    "warna": color,
                    "ukuran": size,
                    "nama_desain": design,
                    "jumlah": int(qty),
                    "harga_jual_per_pcs": int(price_per),
                    "total": int(total),
                    "pembeli": buyer,
                    "alamat_pembeli": buyer_addr,
                    "telepon_pembeli": buyer_phone,
                    "metode": metode,
                    "keterangan": note,
                    "payment_proof": "",
                    "created_by": st.session_state.username
                }])
                sales_df = pd.concat([sales_df, new_sale], ignore_index=True)
                sales_df.to_csv(sales_file, index=False)
                st.success("✅ Penjualan dari stok ready berhasil diproses")

    elif mode == "Stock Mentah":
        polos_file = STOCK_DIR / "stock_polos.csv"
        dtf_file = STOCK_DIR / "stock_dtf.csv"
        # Load polos
        if polos_file.exists() and polos_file.stat().st_size > 0:
            polos_df = pd.read_csv(polos_file)
        else:
            st.info("Belum ada stock kaos polos.")
            return
        if polos_df.empty:
            st.info("Belum ada stock kaos polos.")
            return
        polos_df["display"] = polos_df.apply(lambda x: f"{x['jenis_produk']} • {x['warna']} • {x['ukuran']} ({x['jumlah']} pcs)", axis=1)
        selected_polos = st.selectbox("Pilih Item Polos", polos_df["display"])
        # Load DTF sablon options (ambil dari daftar DTF Prints Stock List)
        if dtf_file.exists() and dtf_file.stat().st_size > 0:
            dtf_df = pd.read_csv(dtf_file)
        else:
            dtf_df = pd.DataFrame(columns=["nama_desain","cocok_warna","ukuran_sablon","jumlah","harga_beli","tgl_masuk","keterangan"])
        # Hanya tampilkan DTF dengan stok > 0
        dtf_df = dtf_df[dtf_df["jumlah"] > 0] if not dtf_df.empty else dtf_df
        dtf_df["display"] = dtf_df.apply(lambda x: f"{x['nama_desain']} • {x['cocok_warna']} • {x['ukuran_sablon']} ({x['jumlah']} pcs)", axis=1) if not dtf_df.empty else pd.Series(dtype=str)
        polos_idx = polos_df[polos_df["display"] == selected_polos].index[0]
        polos_color = polos_df.loc[polos_idx, "warna"]
        sablon_options = ["Tanpa sablon"] + (list(dtf_df["display"]) if not dtf_df.empty else [])
        selected_sablon = st.selectbox("Pilih Sablon (DTF)", sablon_options)
        qty = st.number_input("Jumlah Dijual (pcs)", min_value=1, value=1, step=1, key="sell_mentah_qty")
        price_per = st.number_input("Harga Jual per pcs (Rp)", min_value=0, value=0, step=1000, key="sell_mentah_price")
        buyer = st.text_input("Nama Pembeli", key="sell_mentah_buyer")
        buyer_addr = st.text_area("Alamat Pembeli", height=80, key="sell_mentah_addr")
        buyer_phone = st.text_input("Kontak Pembeli", key="sell_mentah_phone")
        metode = st.selectbox("Metode Bayar", ["CASH", "TRANSFER", "QRIS"], key="sell_mentah_method")
        note = st.text_input("Keterangan", key="sell_mentah_note")
        if not check_capability("STOCK_SELL"):
            st.error("❌ Anda tidak memiliki izin untuk menjual stok.")
            return
        if st.button("Proses Penjualan Mentah", type="primary"):
            polos_available = int(polos_df.loc[polos_idx, "jumlah"])
            polos_product = polos_df.loc[polos_idx, "jenis_produk"]
            polos_color = polos_df.loc[polos_idx, "warna"]
            polos_size = polos_df.loc[polos_idx, "ukuran"]
            if qty > polos_available:
                st.error("Jumlah melebihi stok kaos polos yang tersedia")
                return
            if selected_sablon != "Tanpa sablon":
                sablon_idx = dtf_df[dtf_df["display"] == selected_sablon].index
                if len(sablon_idx) == 0:
                    st.error("Pilihan sablon DTF tidak valid")
                    return
                sablon_idx = sablon_idx[0]
                dtf_available = int(dtf_df.loc[sablon_idx, "jumlah"])
                dtf_design = dtf_df.loc[sablon_idx, "nama_desain"]
                dtf_size = dtf_df.loc[sablon_idx, "ukuran_sablon"]
                if qty > dtf_available:
                    st.error("Jumlah melebihi stok DTF yang tersedia")
                    return
                # Deduct DTF stock
                new_dtf_qty = dtf_available - qty
                if new_dtf_qty <= 0:
                    dtf_df = dtf_df.drop(index=sablon_idx)
                else:
                    dtf_df.loc[sablon_idx, "jumlah"] = new_dtf_qty
                dtf_df.to_csv(dtf_file, index=False)
            # Deduct polos stock
            new_polos_qty = polos_available - qty
            if new_polos_qty <= 0:
                polos_df = polos_df.drop(index=polos_idx)
            else:
                polos_df.loc[polos_idx, "jumlah"] = new_polos_qty
            polos_df.to_csv(polos_file, index=False)
            total = price_per * qty
            # Cash flow message
            if selected_sablon == "Tanpa sablon":
                cf_msg = f"Penjualan stok mentah (polos): {polos_product} {polos_color} {polos_size} {qty} pcs untuk {buyer}. {note}"
                nama_desain_val = "-"
            else:
                cf_msg = f"Penjualan stok mentah (polos + DTF {dtf_design} {dtf_size}): {polos_product} {polos_color} {polos_size} {qty} pcs untuk {buyer}. {note}"
                nama_desain_val = dtf_design
            record_cash_flow(
                "PENJUALAN STOK",
                int(total),
                "IN",
                cf_msg,
                "STOCK"
            )
            try:
                polos_buy = int(polos_df.loc[polos_idx, "harga_beli"]) if "harga_beli" in polos_df.columns else 0
            except:
                polos_buy = 0
            dtf_buy = 0
            if selected_sablon != "Tanpa sablon":
                try:
                    dtf_buy = int(dtf_df.loc[sablon_idx, "harga_beli"]) if "harga_beli" in dtf_df.columns else 0
                except:
                    dtf_buy = 0
            unit_cost = polos_buy + dtf_buy
            if price_per > unit_cost:
                profit_per = price_per - unit_cost
                commission = profit_per * qty * 0.05
                profit_total = profit_per * qty
            else:
                commission = 0
                profit_total = 0
            item_desc = f"{polos_product} {polos_color} {polos_size}" + (f" + {nama_desain_val}" if nama_desain_val != "-" else "")
            settings = load_settings()
            pc = settings.get("point_configuration", {})
            sale_points = int(pc.get("stock_sale", 5))
            record_stock_point(
                st.session_state.username,
                "STOCK_SALE",
                f"Jual: {item_desc} | {qty} pcs",
                sale_points,
                float(profit_total),
                float(commission)
            )
            if commission > 0:
                st.info(f"💰 Komisi 5%: Rp {commission:,.0f}")
            sales_file = STOCK_DIR / "sales_from_stock.csv"
            if sales_file.exists() and sales_file.stat().st_size > 0:
                sales_df = pd.read_csv(sales_file)
            else:
                sales_df = pd.DataFrame(columns=[
                    "sale_id","tanggal","jenis_produk","warna","ukuran","nama_desain","jumlah","harga_jual_per_pcs","total","pembeli","alamat_pembeli","telepon_pembeli","metode","keterangan","payment_proof","created_by"
                ])
            for col in ["alamat_pembeli","telepon_pembeli","sale_id","payment_proof"]:
                if col not in sales_df.columns:
                    sales_df[col] = ""
            sale_id = generate_stock_sale_id()
            new_sale = pd.DataFrame([{
                "sale_id": sale_id,
                "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "jenis_produk": polos_product,
                "warna": polos_color,
                "ukuran": polos_size,
                "nama_desain": nama_desain_val,
                "jumlah": int(qty),
                "harga_jual_per_pcs": int(price_per),
                "total": int(total),
                "pembeli": buyer,
                "alamat_pembeli": buyer_addr,
                "telepon_pembeli": buyer_phone,
                "metode": metode,
                "keterangan": note,
                "payment_proof": "",
                "created_by": st.session_state.username
            }])
            sales_df = pd.concat([sales_df, new_sale], ignore_index=True)
            sales_df.to_csv(sales_file, index=False)
            st.success("✅ Penjualan stok mentah berhasil diproses")

def show_stock_receipts():
    """Cetak struk dan kelola bukti pembayaran penjualan stok"""
    st.markdown(f"<h2 style='color: #D4AF37;'>🧾 Struk Penjualan Stok</h2>", unsafe_allow_html=True)
    
    sales_file = STOCK_DIR / "sales_from_stock.csv"
    if not (sales_file.exists() and sales_file.stat().st_size > 0):
        st.info("Belum ada penjualan stok.")
        return
    
    try:
        sales_df = pd.read_csv(sales_file)
    except pd.errors.EmptyDataError:
        st.info("Belum ada penjualan stok.")
        return
    
    if sales_df.empty:
        st.info("Belum ada penjualan stok.")
        return
    
    for col in ["sale_id","pembeli","total","tanggal","jenis_produk","warna","ukuran","nama_desain","jumlah","harga_jual_per_pcs","metode","keterangan","payment_proof"]:
        if col not in sales_df.columns:
            sales_df[col] = ""
    
    sales_df["display"] = sales_df.apply(
        lambda x: f"{x.get('sale_id','')} - {x.get('pembeli','')} - Rp {int(x.get('total',0)):,}",
        axis=1
    )
    
    selected_display = st.selectbox("Pilih Penjualan Stok", sales_df["display"].tolist(), key="stock_receipt_select")
    if not selected_display:
        return
    
    sel_idx = sales_df[sales_df["display"] == selected_display].index[0]
    sale = sales_df.loc[sel_idx]
    
    settings = load_settings()
    studio_info = settings.get("studio_info", {})
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">📋 Preview Struk</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"**{studio_info.get('nama_studio', 'DALUASE CLOTHING STUDIO')}**")
        st.markdown(f"{studio_info.get('alamat', 'SANGIHE, Kab. Kepl. Sangihe')}")
        st.markdown(f"Prov. Sulawesi Utara")
        st.markdown(f"Telp: {studio_info.get('telepon', '-')}")
        st.markdown("---")
        st.markdown(f"**ID Penjualan:** {sale.get('sale_id','')}")
        st.markdown(f"**Tanggal:** {str(sale.get('tanggal','')).split()[0]}")
        st.markdown(f"**Customer:** {sale.get('pembeli','')}")
    
    with col2:
        st.markdown("**Rincian Penjualan:**")
        st.markdown(f"- {sale.get('jenis_produk','')}")
        if str(sale.get('nama_desain','')).strip():
            st.markdown(f"- Desain: {sale.get('nama_desain','')}")
        st.markdown(f"- {sale.get('warna','')} | {sale.get('ukuran','')} | {int(sale.get('jumlah',0))} pcs")
        st.markdown(f"- Harga/pcs: Rp {int(sale.get('harga_jual_per_pcs',0)):,}")
        st.markdown("---")
        st.markdown(f"**Total:** Rp {int(sale.get('total',0)):,}")
        st.markdown(f"**Metode:** {sale.get('metode','')}")
        if str(sale.get('keterangan','')).strip():
            st.markdown(f"**Ket.:** {sale.get('keterangan','')}")
        if str(sale.get('payment_proof','')).strip():
            st.caption(f"Bukti pembayaran: {sale.get('payment_proof')}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    colA, colB = st.columns(2)
    with colA:
        if st.button("🖨️ Cetak Struk", use_container_width=True, type="primary", key=f"print_stock_{sale.get('sale_id','')}"):
            receipt_text = generate_stock_receipt_text(sale, studio_info)
            st.download_button(
                label="📥 Download Struk (.txt)",
                data=receipt_text,
                file_name=f"Struk_{sale.get('sale_id','')}_{sale.get('pembeli','')}.txt",
                mime="text/plain",
                key=f"download_stock_receipt_{sale.get('sale_id','')}"
            )
    with colB:
        proof = st.file_uploader("Upload Bukti Pembayaran (opsional)", type=["png","jpg","jpeg","pdf"], key=f"stock_proof_{sale.get('sale_id','')}")
        if st.button("💾 Simpan Bukti", use_container_width=True, key=f"save_proof_{sale.get('sale_id','')}"):
            if proof is None:
                st.warning("Pilih file bukti terlebih dahulu.")
            else:
                ext = os.path.splitext(proof.name)[1].lower()
                content, err = prepare_upload_bytes(proof, ext)
                if err:
                    st.error(err)
                else:
                    safe_id = re.sub(r"[^a-zA-Z0-9_-]+", "_", sale.get('sale_id',''))
                    dest = PAYMENT_PROOFS_DIR / f"{safe_id}{ext}"
                    with open(dest, 'wb') as f:
                        f.write(content)
                    sales_df.at[sel_idx, "payment_proof"] = str(dest)
                    sales_df.to_csv(sales_file, index=False)
                    st.success("✅ Bukti pembayaran disimpan.")
    st.markdown('</div>', unsafe_allow_html=True)

def generate_stock_receipt_text(sale, studio_info):
    """Generate teks struk untuk penjualan stok"""
    receipt = f"""
{'='*40}
{studio_info.get('nama_studio', 'DALUASE CLOTHING STUDIO').center(40)}
{studio_info.get('alamat', 'SANGIHE').center(40)}
Telp: {studio_info.get('telepon', '-')}
{'='*40}

ID Penjualan: {sale.get('sale_id','')}
Tanggal: {str(sale.get('tanggal','')).split()[0]}
Customer: {sale.get('pembeli','')}
{'-'*40}

RINCIAN:
- Produk: {sale.get('jenis_produk','')}
- Desain: {sale.get('nama_desain','-')}
- Spesifikasi: {sale.get('warna','')} | {sale.get('ukuran','')} | {int(sale.get('jumlah',0))} pcs
- Harga/pcs: Rp {int(sale.get('harga_jual_per_pcs',0)):,}
{'-'*40}

TOTAL: Rp {int(sale.get('total',0)):,}
Metode: {sale.get('metode','')}
Ket.: {sale.get('keterangan','')}
{'-'*40}

Terima kasih atas kepercayaan Anda!
{studio_info.get('nama_studio', 'DALUASE CLOTHING STUDIO')}
{'='*40}
"""
    return receipt

def show_team_management():
    """Halaman management tim"""
    st.markdown(f"<h1 style='color: #D4AF37;'>👥 Management Tim</h1>", unsafe_allow_html=True)
    
    if (st.session_state.role or "").lower() != "owner":
        st.error("❌ Akses ditolak. Hanya owner yang dapat mengakses halaman ini.")
        return
    
    tab1, tab2 = st.tabs(["📋 Daftar Anggota", "➕ Tambah Anggota"])
    
    with tab1:
        show_team_list()
    
    with tab2:
        show_add_team_member()

def show_team_list():
    """Tampilkan daftar anggota tim"""
    users_df = load_users()
    
    if users_df.empty:
        st.info("Belum ada anggota tim.")
        return
    
    # Filter hanya user aktif
    active_users = users_df[users_df["status"] == "active"]
    
    st.markdown(f"**Total Anggota Tim:** {len(active_users)}")
    
    for idx, user in active_users.iterrows():
        st.markdown(f"""
        <div class="order-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 2;">
                    <strong style="color: white; font-size: 1.1rem;">{user['full_name']}</strong><br>
                    <span style="color: #888; font-size: 0.9rem;">@{user['username']}</span><br>
                    <span style="color: #888; font-size: 0.8rem;">Bergabung: {user['created_at']}</span>
                    <span style="color: #888; font-size: 0.8rem;">Password Hash: {user.get('password_hash','')}</span>
                    <span style="color: #888; font-size: 0.8rem;">Suspend: {user.get('suspend_mode','none')}</span>
                </div>
                <div style="flex: 1; text-align: center;">
                    <div style="color: #D4AF37; font-size: 1.1rem;">{user['role'].upper()}</div>
                    <div style="color: #888; font-size: 0.8rem;">Status: {user['status']}</div>
                </div>
                <div style="flex: 1; text-align: right;">
                    <div style="display: flex; gap: 0.5rem; justify-content: flex-end;">
        """, unsafe_allow_html=True)
        
        # Tombol aksi
        col1, col2 = st.columns(2)
        with col1:
            if user['username'] != "owner":
                if st.button(f"✏️ Edit {user['username']}", key=f"edit_user_{idx}", use_container_width=True):
                    st.session_state.edit_user = user['username']
                    st.rerun()
        
        with col2:
            if user['username'] != "owner":  # Owner tidak bisa dinonaktifkan
                if st.button(f"🗑️ Nonaktif {user['username']}", key=f"deactivate_{idx}", use_container_width=True):
                    deactivate_user(user['username'])
        
        col3, col4 = st.columns(2)
        with col3:
            if user['username'] != "owner":
                if st.button(f"🔑 Reset Password {user['username']}", key=f"resetpw_{idx}", use_container_width=True):
                    st.session_state.reset_user = user['username']
        with col4:
            if user['username'] != "owner":
                if st.button(f"🚫 Nonaktifkan Sementara {user['username']}", key=f"suspend_{idx}", use_container_width=True):
                    st.session_state.suspend_user = user['username']
        
        st.markdown("</div></div></div>", unsafe_allow_html=True)
    
    # Modal edit user
    if st.session_state.get('edit_user'):
        edit_username = st.session_state.edit_user
        edit_user = users_df[users_df["username"] == edit_username].iloc[0]
        
        with st.form(f"edit_user_{edit_username}"):
            st.markdown(f"### ✏️ Edit User: {edit_user['full_name']}")
            new_fullname = st.text_input("Nama Lengkap", value=edit_user['full_name'], key=f"edit_fullname_{edit_username}")
            new_role = st.text_input("Role (bebas)", value=edit_user['role'], key=f"edit_role_{edit_username}")
            feature_options = [
                "Dashboard","Management Kloter","Kas & Analisis","Stock System",
                "Production","Distribution","Struk & Invoice"
            ]
            feats_raw = edit_user.get('features', '')
            if pd.isna(feats_raw):
                feats_raw = ''
            current_feats = [f.strip() for f in str(feats_raw).split(';') if f.strip() and f.strip() in feature_options]
            selected_feats = st.multiselect("Fitur yang diizinkan", feature_options, default=current_feats, key=f"edit_features_{edit_username}")
            cap_options = get_capability_options()
            caps_raw = edit_user.get('capabilities', '')
            if pd.isna(caps_raw):
                caps_raw = ''
            current_caps = [c.strip() for c in str(caps_raw).split(';') if c.strip() and c.strip() in cap_options]
            selected_caps = st.multiselect("Aksi/kapabilitas yang diizinkan", cap_options, default=current_caps, key=f"edit_caps_{edit_username}")
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Simpan Perubahan", type="primary"):
                    update_user(edit_username, new_fullname, new_role, selected_feats, selected_caps)
            
            with col2:
                if st.form_submit_button("❌ Batal"):
                    st.session_state.edit_user = None
                    st.rerun()
    
    if st.session_state.get('reset_user'):
        target_username = st.session_state.reset_user
        with st.form(f"reset_pw_{target_username}"):
            st.markdown(f"### 🔑 Reset Password: {target_username}")
            new_pw = st.text_input("Password Baru*", type="password", key=f"newpw_{target_username}")
            confirm_pw = st.text_input("Konfirmasi Password*", type="password", key=f"confpw_{target_username}")
            gen = st.checkbox("Generate password sementara", key=f"genpw_{target_username}")
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("💾 Simpan Password", type="primary"):
                    final_pw = new_pw
                    if gen or not final_pw:
                        final_pw = generate_temp_password(10)
                    else:
                        if new_pw != confirm_pw:
                            st.error("❌ Password dan konfirmasi tidak cocok")
                            final_pw = None
                    if final_pw:
                        users_df2 = load_users()
                        mask = users_df2["username"] == target_username
                        if mask.any():
                            users_df2.loc[mask, "password_hash"] = hash_password(final_pw)
                            users_df2.to_csv(USERS_FILE, index=False)
                            st.success("✅ Password berhasil direset")
                            st.warning("Simpan password ini. Tidak akan ditampilkan lagi.")
                            st.code(final_pw)
                            st.session_state.reset_user = None
                        else:
                            st.error("❌ User tidak ditemukan")
            with col2:
                if st.form_submit_button("❌ Batal"):
                    st.session_state.reset_user = None
    
    if st.session_state.get('suspend_user'):
        target_username = st.session_state.suspend_user
        with st.form(f"suspend_form_{target_username}"):
            st.markdown(f"### 🚫 Nonaktifkan Sementara: {target_username}")
            mode = st.radio("Pilih mode suspend", ["login_block","readonly"], index=0, key=f"suspend_mode_{target_username}")
            note = st.text_area("Catatan (opsional)", placeholder="Alasan suspend...", key=f"suspend_note_{target_username}")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.form_submit_button("💾 Simpan", type="primary"):
                    if set_user_suspension(target_username, mode, note):
                        st.success("✅ Status suspend disimpan")
                        st.session_state.suspend_user = None
                        st.rerun()
                    else:
                        st.error("❌ User tidak ditemukan")
            with col2:
                if st.form_submit_button("♻️ Pulihkan Akses"):
                    if set_user_suspension(target_username, "none", ""):
                        st.success("✅ Akses dipulihkan")
                        st.session_state.suspend_user = None
                        st.rerun()
                    else:
                        st.error("❌ User tidak ditemukan")
            with col3:
                if st.form_submit_button("❌ Batal"):
                    st.session_state.suspend_user = None

def show_add_team_member():
    """Form tambah anggota tim baru"""
    st.markdown(f"<h2 style='color: #D4AF37;'>➕ Tambah Anggota Tim Baru</h2>", unsafe_allow_html=True)
    
    with st.form("add_team_member_form"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">👤 Data Anggota Baru</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username*", placeholder="Nama pengguna untuk login", key="new_username")
            full_name = st.text_input("Nama Lengkap*", placeholder="Nama lengkap anggota", key="new_fullname")
        
        with col2:
            password = st.text_input("Password*", type="password", key="new_password")
            confirm_password = st.text_input("Konfirmasi Password*", type="password", key="new_confirm_password")
            role = st.text_input("Role (bebas)*", placeholder="contoh: admin, kurir, dsb.", key="new_role")
        is_sales = st.checkbox("Tambahkan sebagai Sales/Reseller", key="new_is_sales")
        feature_options = [
            "Dashboard","Management Kloter","Kas & Analisis","Stock System",
            "Production","Distribution","Struk & Invoice"
        ]
        selected_features = st.multiselect("Fitur yang diizinkan untuk user ini", feature_options, key="new_features")
        cap_options = get_capability_options()
        selected_caps = st.multiselect("Aksi/kapabilitas yang diizinkan", cap_options, key="new_caps")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.form_submit_button("➕ Tambah Anggota", type="primary"):
            # Validasi
            if not username or not full_name or not password:
                st.error("❌ Semua field bertanda * harus diisi")
            elif password != confirm_password:
                st.error("❌ Password dan konfirmasi password tidak cocok")
            else:
                # Cek apakah username sudah ada
                users_df = load_users()
                if username in users_df["username"].values:
                    st.error("❌ Username sudah terdaftar")
                else:
                    # Tambah user baru
                    if is_sales:
                        role = "sales"
                        selected_features = ["Dashboard","Management Sales Order"]
                        selected_caps = ["SALES_ADD_ORDER","SALES_VIEW_ORDERS"]
                    new_user = pd.DataFrame([{
                        "username": username,
                        "password_hash": hash_password(password),
                        "role": role,
                        "full_name": full_name,
                        "created_at": datetime.now().strftime("%Y-%m-%d"),
                        "status": "active",
                        "features": ";".join(selected_features),
                        "capabilities": ";".join(selected_caps)
                    }])
                    
                    users_df = pd.concat([users_df, new_user], ignore_index=True)
                    users_df.to_csv(USERS_FILE, index=False)
                    
                    st.success(f"✅ Anggota tim '{full_name}' berhasil ditambahkan!")
                    st.rerun()

def update_user(username, full_name, role, features=None, capabilities=None):
    """Update data user"""
    users_df = load_users()
    mask = users_df["username"] == username
    
    if mask.any():
        users_df.loc[mask, "full_name"] = full_name
        users_df.loc[mask, "role"] = role
        if features is not None:
            users_df.loc[mask, "features"] = ";".join(features)
        if capabilities is not None:
            users_df.loc[mask, "capabilities"] = ";".join(capabilities)
        users_df.to_csv(USERS_FILE, index=False)
        
        st.success(f"✅ User {username} berhasil diupdate!")
        st.session_state.edit_user = None
        st.rerun()

def deactivate_user(username):
    """Nonaktifkan user"""
    users_df = load_users()
    mask = users_df["username"] == username
    
    if mask.any():
        users_df.loc[mask, "status"] = "inactive"
        users_df.to_csv(USERS_FILE, index=False)
        
        st.success(f"✅ User {username} berhasil dinonaktifkan!")
        st.rerun()

def set_user_suspension(username, mode, note=""):
    """Set status suspend sementara untuk user: mode 'login_block' atau 'readonly' atau 'none'"""
    users_df = load_users()
    mask = users_df["username"] == username
    if mask.any():
        users_df.loc[mask, "suspend_mode"] = mode
        users_df.loc[mask, "ban_note"] = note or ""
        users_df.to_csv(USERS_FILE, index=False)
        return True
    return False

def show_settings():
    """Halaman pengaturan"""
    st.markdown(f"<h1 style='color: #D4AF37;'>⚙️ Pengaturan</h1>", unsafe_allow_html=True)
    
    if (st.session_state.role or "").lower() != "owner":
        st.error("❌ Akses ditolak. Hanya owner yang dapat mengakses halaman ini.")
        return
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📦 Produk & Harga", "🏢 Studio Info", "🎨 Original Design", "🤝 Profit Sharing", "🎯 Pengaturan Poin", "🔒 Keamanan", "💲 Harga Packaging"])
    
    with tab1:
        show_products_settings()
    
    with tab2:
        show_studio_settings()
    
    with tab3:
        show_original_design_settings()
    
    with tab4:
        show_profit_sharing_settings()
    
    with tab5:
        show_point_settings()
    
    with tab6:
        show_security_settings()
    
    with tab7:
        show_packaging_price_settings()

def show_packaging_price_settings():
    st.markdown(f"<h2 style='color: #D4AF37;'>💲 Pengaturan Harga Packaging</h2>", unsafe_allow_html=True)
    settings = load_settings()
    prices = settings.get("packaging_prices", {})
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">Daftar Item Packaging</div>', unsafe_allow_html=True)
    with st.form("packaging_price_form"):
        edited = {}
        for name in sorted(prices.keys()):
            edited[name] = st.number_input(f"Harga {name} (Rp)", min_value=0, value=int(prices.get(name, 0)), step=50, key=f"pkg_price_{name}")
        st.markdown("---")
        new_name = st.text_input("Tambah Item Packaging", placeholder="Nama item baru", key="new_pkg_name")
        new_price = st.number_input("Harga Item Baru (Rp)", min_value=0, value=0, step=50, key="new_pkg_price")
        save_btn = st.form_submit_button("💾 Simpan Harga Packaging", type="primary")
        if save_btn:
            for name, val in edited.items():
                prices[name] = int(val)
            if new_name.strip():
                prices[new_name.strip()] = int(new_price)
            settings["packaging_prices"] = prices
            save_settings(settings)
            st.success("Harga packaging disimpan.")
            # time.sleep(1) # Removed for performance
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_security_settings():
    st.markdown(f"<h2 style='color: #D4AF37;'>🔒 Keamanan</h2>", unsafe_allow_html=True)
    settings = load_settings()
    sec = settings.get("security_settings", {})
    enabled = bool(sec.get("owner_recovery_enabled", False))
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">Recovery Token Owner</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if not enabled:
            if st.button("🪪 Generate Recovery Token", type="primary", key="btn_generate_owner_token"):
                token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(20))
                settings["security_settings"]["owner_recovery_enabled"] = True
                settings["security_settings"]["owner_recovery_hash"] = hashlib.sha256(token.encode()).hexdigest()
                settings["security_settings"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
                settings["security_settings"]["updated_by"] = st.session_state.username
                save_settings(settings)
                st.warning("Simpan token berikut di tempat aman. Token tidak akan ditampilkan lagi.")
                st.code(token)
        else:
            st.info("Recovery token aktif. Anda dapat menonaktifkannya di kanan.")
    with col_b:
        if enabled:
            if st.button("🚫 Nonaktifkan Recovery Token", key="btn_disable_owner_token"):
                settings["security_settings"]["owner_recovery_enabled"] = False
                settings["security_settings"]["owner_recovery_hash"] = ""
                settings["security_settings"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
                settings["security_settings"]["updated_by"] = st.session_state.username
                save_settings(settings)
                st.success("Recovery token dinonaktifkan.")
                # time.sleep(1) # Removed for performance
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    up = settings.get("upload_settings", {})
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">Batas Maksimal Upload</div>', unsafe_allow_html=True)
    with st.form("upload_limits_form"):
        max_img = st.number_input("Maksimal Gambar (MB)", min_value=1, max_value=20, value=int(up.get("max_image_mb", 3)))
        max_pdf = st.number_input("Maksimal PDF (MB)", min_value=1, max_value=50, value=int(up.get("max_pdf_mb", 5)))
        save_ul = st.form_submit_button("💾 Simpan Batas Upload", type="primary")
        if save_ul:
            settings["upload_settings"] = {
                "max_image_mb": int(max_img),
                "max_pdf_mb": int(max_pdf)
            }
            save_settings(settings)
            st.success("Batas upload disimpan.")
    st.markdown('</div>', unsafe_allow_html=True)
    with st.form("owner_password_change_form"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">Ganti Password Owner</div>', unsafe_allow_html=True)
        current_pw = st.text_input("Password Saat Ini", type="password", key="owner_current_pw")
        new_pw = st.text_input("Password Baru", type="password", key="owner_new_pw")
        confirm_pw = st.text_input("Konfirmasi Password Baru", type="password", key="owner_confirm_pw")
        st.markdown('</div>', unsafe_allow_html=True)
        submit = st.form_submit_button("💾 Simpan Password", type="primary")
        if submit:
            if not current_pw or not new_pw or not confirm_pw:
                st.error("Semua field wajib diisi.")
            elif new_pw != confirm_pw:
                st.error("Konfirmasi password tidak cocok.")
            else:
                ok, msg = change_user_password("owner", current_pw, new_pw)
                if ok:
                    st.success("Password berhasil diubah. Anda akan logout otomatis.")
                    st.session_state.authenticated = False
                    st.session_state.username = None
                    st.session_state.role = None
                    # time.sleep(1) # Removed for performance
                    st.rerun()
                else:
                    st.error(msg)

def show_products_settings():
    """Pengaturan produk dan harga"""
    st.markdown(f"<h2 style='color: #D4AF37;'>📦 Manajemen Produk & Harga</h2>", unsafe_allow_html=True)
    
    settings = load_settings()
    products = settings.get("products", {})
    prices = settings.get("prices", {})
    sizes = settings.get("sizes", {})
    colors = settings.get("colors", {})
    
    # Daftar produk saat ini
    if products:
        st.markdown("### 📋 Produk Saat Ini")
        
        for product_name, category in products.items():
            st.markdown(f"""
            <div class="order-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 2;">
                        <strong style="color: white; font-size: 1.1rem;">{product_name}</strong><br>
                        <span style="color: #888; font-size: 0.9rem;">Kategori: {category}</span><br>
                        <span style="color: #888; font-size: 0.8rem;">Harga: Rp {prices.get(product_name, 0):,}</span>
                    </div>
                    <div style="flex: 1; text-align: center;">
                        <div style="color: #D4AF37; font-size: 1rem;">{len(sizes.get(product_name, []))} Ukuran</div>
                        <div style="color: #888; font-size: 0.8rem;">{len(colors.get(product_name, []))} Warna</div>
                    </div>
                    <div style="flex: 1; text-align: right;">
                        <div style="display: flex; gap: 0.5rem; justify-content: flex-end;">
            """, unsafe_allow_html=True)
            
            # Tombol aksi
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✏️ {product_name[:10]}", key=f"edit_prod_{product_name}", use_container_width=True):
                    st.session_state.edit_product = product_name
                    st.rerun()
            
            with col2:
                if st.button(f"🗑️ {product_name[:10]}", key=f"delete_prod_{product_name}", use_container_width=True):
                    st.session_state.delete_product = product_name
                    st.rerun()
            
            st.markdown("</div></div></div>", unsafe_allow_html=True)
    
    # Form tambah/edit produk
    st.markdown("---")
    
    if st.session_state.get('edit_product'):
        product_to_edit = st.session_state.edit_product
        st.markdown(f"<h3>✏️ Edit Produk: {product_to_edit}</h3>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h3>➕ Tambah Produk Baru</h3>", unsafe_allow_html=True)
    
    with st.form("product_form"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        if st.session_state.get('edit_product'):
            product_name = st.text_input("Nama Produk", value=product_to_edit, key="edit_product_name")
        else:
            product_name = st.text_input("Nama Produk*", placeholder="Contoh: Premium Cotton T-shirt 7200", key="new_product_name")
        
        harga_dasar = st.number_input("Harga Dasar (Rp)*", 
                                     min_value=0, 
                                     value=prices.get(product_to_edit, 120000) if st.session_state.get('edit_product') else 120000, 
                                     step=1000,
                                     key="product_price")
        
        # Ukuran valid
        st.write("**Ukuran Valid:**")
        all_sizes = ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL"]
        default_sizes = sizes.get(product_to_edit, ["S", "M", "L", "XL", "2XL"]) if st.session_state.get('edit_product') else ["S", "M", "L", "XL", "2XL"]
        default_sizes = [s for s in default_sizes if s in all_sizes]
        selected_sizes = st.multiselect("Pilih ukuran yang valid", all_sizes, default=default_sizes, key="product_sizes")
        
        # Warna valid - menggunakan daftar lengkap
        st.write("**Warna Valid:**")
        default_colors = colors.get(product_to_edit, ["WHITE", "BLACK"]) if st.session_state.get('edit_product') else ["WHITE", "BLACK"]
        color_alias = {
            "HITAM": "BLACK", "PUTIH": "WHITE", "MERAH": "RED", "BIRU": "BLUE", "HIJAU": "GREEN",
            "KUNING": "YELLOW", "ORANYE": "ORANGE", "ORANGE": "ORANGE", "UNGU": "PURPLE", "PINK": "PINK",
            "COKLAT": "BROWN", "ABU-ABU": "GRAY", "ABU": "GRAY", "NAVY": "NAVY", "MAROON": "MAROON",
            "TEAL": "TEAL", "OLIVE": "OLIVE", "EMAS": "GOLD", "PERAK": "SILVER", "BEIGE": "BEIGE",
            "CREAM": "CREAM", "AQUA": "AQUA", "TURQUOISE": "TURQUOISE", "LIME": "LIME",
            "MAGENTA": "MAGENTA", "CYAN": "CYAN"
        }
        mapped_defaults = [color_alias.get(str(c).upper(), str(c).upper()) for c in default_colors]
        default_colors = [c for c in mapped_defaults if c in COMPLETE_COLORS] or ["BLACK", "WHITE"]
        selected_colors = st.multiselect("Pilih warna yang valid", COMPLETE_COLORS, default=default_colors, key="product_colors")
        manual_default = ""
        if st.session_state.get('edit_product'):
            existing_colors = colors.get(product_to_edit, [])
            manual_extras = [c for c in existing_colors if str(c).upper() not in COMPLETE_COLORS]
            manual_default = ", ".join(manual_extras)
        manual_colors_input = st.text_input("Tambahkan warna manual (pisahkan dengan koma)", value=manual_default, key="product_colors_manual")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("💾 Simpan Produk", type="primary"):
                if product_name and selected_sizes and selected_colors:
                    # Update settings
                    settings["products"][product_name] = "T-Shirt"  # Default category
                    settings["prices"][product_name] = harga_dasar
                    settings["sizes"][product_name] = selected_sizes
                    manual_colors = [c.strip() for c in manual_colors_input.split(",") if c.strip()]
                    final_colors = list(dict.fromkeys(selected_colors + manual_colors))
                    settings["colors"][product_name] = final_colors
                    
                    save_settings(settings)
                    
                    if st.session_state.get('edit_product') and product_to_edit != product_name:
                        # Hapus produk lama jika nama berubah
                        if product_to_edit in settings["products"]:
                            del settings["products"][product_to_edit]
                        if product_to_edit in settings["prices"]:
                            del settings["prices"][product_to_edit]
                        if product_to_edit in settings["sizes"]:
                            del settings["sizes"][product_to_edit]
                        if product_to_edit in settings["colors"]:
                            del settings["colors"][product_to_edit]
                        save_settings(settings)
                    
                    st.success(f"✅ Produk '{product_name}' berhasil disimpan!")
                    st.session_state.edit_product = None
                    # time.sleep(1) # Removed for performance
                    st.rerun()
                else:
                    st.error("❌ Nama produk, ukuran, dan warna harus diisi")
        
        with col2:
            if st.session_state.get('edit_product'):
                if st.form_submit_button("❌ Batal Edit"):
                    st.session_state.edit_product = None
                    st.rerun()

def show_studio_settings():
    """Pengaturan info studio"""
    st.markdown(f"<h2 style='color: #D4AF37;'>🏢 Informasi Studio</h2>", unsafe_allow_html=True)
    
    settings = load_settings()
    studio_info = settings.get("studio_info", {})
    
    with st.form("studio_info_form"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">🏢 Data Studio</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            nama_studio = st.text_input("Nama Studio", 
                                       value=studio_info.get("nama_studio", "Daluase Clothing Studio"),
                                       key="studio_name")
            
            pemilik = st.text_input("Nama Pemilik", 
                                   value=studio_info.get("pemilik", "Jovi Lombongaris"),
                                   key="studio_owner")
            
            alamat = st.text_area("Alamat", 
                                 value=studio_info.get("alamat", "SANGIHE, Kab. Kepl. Sangihe, Prov. Sulawesi Utara"),
                                 height=100,
                                 key="studio_address")
        
        with col2:
            email = st.text_input("Email", 
                                 value=studio_info.get("email", "daluasest@gmail.com"),
                                 key="studio_email")
            
            telepon = st.text_input("Telepon", 
                                   value=studio_info.get("telepon", "-"),
                                   key="studio_phone")
            
            website = st.text_input("Website", 
                                   value=studio_info.get("website", "-"),
                                   key="studio_website")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        uploaded_logo = st.file_uploader("Upload Logo (PNG/JPG)", type=["png","jpg","jpeg"], key="studio_logo")
        if uploaded_logo:
            ext = Path(uploaded_logo.name).suffix.lower()
            content, err = prepare_upload_bytes(uploaded_logo, ext)
            if err:
                st.error(err)
            else:
                logo_path = DATA_DIR / "logo.png"
                with open(logo_path, "wb") as f:
                    f.write(content)
                st.success("Logo berhasil diunggah")
        
        if st.form_submit_button("💾 Simpan Perubahan", type="primary"):
            studio_info = {
                "nama_studio": nama_studio,
                "pemilik": pemilik,
                "alamat": alamat,
                "email": email,
                "telepon": telepon,
                "website": website
            }
            
            settings["studio_info"] = studio_info
            save_settings(settings)
            
            st.success("✅ Informasi studio berhasil disimpan!")

def show_original_design_settings():
    """Pengaturan daftar desain original dan upload file"""
    st.markdown(f"<h2 style='color: #D4AF37;'>🎨 Original Design</h2>", unsafe_allow_html=True)
    settings = load_settings()
    original_designs = settings.get("original_designs", [])
    original_design_files = settings.get("original_design_files", {})
    if original_designs:
        st.markdown("### 📋 Daftar Desain Original")
        for name in original_designs:
            file_name = original_design_files.get(name, "")
            file_path = ORIGINAL_DESIGNS_DIR / file_name if file_name else None
            st.markdown(f"""
            <div class="order-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 2;">
                        <strong style="color: white; font-size: 1.1rem;">{name}</strong><br>
                        <span style="color: #888; font-size: 0.8rem;">File: {file_name or '-'}</span>
                    </div>
                    <div style="flex: 1; text-align: right;">
                        <div style="display: flex; gap: 0.5rem; justify-content: flex-end;">
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if file_path and file_path.exists():
                    if str(file_path).lower().endswith((".png",".jpg",".jpeg",".gif")):
                        st.image(str(file_path), caption=name, use_column_width=True)
                else:
                    st.caption("Belum ada file")
            with col2:
                if st.button(f"🗑️ Hapus {name[:10]}", key=f"del_orig_{name}", use_container_width=True):
                    original_designs = [d for d in original_designs if d != name]
                    if name in original_design_files:
                        del original_design_files[name]
                    settings["original_designs"] = original_designs
                    settings["original_design_files"] = original_design_files
                    save_settings(settings)
                    st.success("✅ Desain original dihapus")
                    st.rerun()
            st.markdown("</div></div></div>", unsafe_allow_html=True)
    else:
        st.info("Belum ada desain original terdaftar.")
    st.markdown("---")
    with st.form("add_original_design_form"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-title">➕ Tambah Desain Original</div>', unsafe_allow_html=True)
        name = st.text_input("Nama/Kode Desain*", key="new_original_name")
        file = st.file_uploader("Upload File Desain (PNG/JPG/PDF)", type=["png","jpg","jpeg","pdf"], key="new_original_file")
        st.markdown('</div>', unsafe_allow_html=True)
        if st.form_submit_button("💾 Simpan", type="primary"):
            if not name:
                st.error("❌ Nama desain harus diisi")
            else:
                if name not in original_designs:
                    original_designs.append(name)
                saved_file_name = original_design_files.get(name, "")
                if file:
                    ext = Path(file.name).suffix.lower()
                    content, err = prepare_upload_bytes(file, ext)
                    if err:
                        st.error(err)
                    else:
                        safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", name) + ext
                        dest = ORIGINAL_DESIGNS_DIR / safe_name
                        with open(dest, "wb") as f:
                            f.write(content)
                        saved_file_name = safe_name
                original_design_files[name] = saved_file_name
                settings["original_designs"] = original_designs
                settings["original_design_files"] = original_design_files
                save_settings(settings)
                st.success("✅ Desain original tersimpan")
                st.rerun()

# ===================== MAIN APP FLOW =====================
def main():
    """Main application flow dengan navigasi hybrid"""
    
    # Jika belum login, tampilkan halaman login
    if not st.session_state.authenticated:
        show_login()
        return
    
    # Tampilkan top navigation bar
    show_top_navigation()
    
    # Atur sidebar state berdasarkan halaman aktif
    if st.session_state.active_tab == "Management Kloter":
        # Expand sidebar hanya untuk Management Kloter
        st.sidebar.empty()  # Clear previous sidebar content
        show_kloter_management()
    else:
        # Untuk halaman lain, sembunyikan sidebar
        st.sidebar.empty()
    
    # Tampilkan konten utama berdasarkan halaman aktif
    if st.session_state.active_tab == "Dashboard":
        show_dashboard()
    elif st.session_state.active_tab == "Management Kloter":
        # Already handled in sidebar
        pass
    elif st.session_state.active_tab == "Kas & Analisis":
        show_kas_analisis()
    elif st.session_state.active_tab == "Stock System":
        show_stock_system()
    elif st.session_state.active_tab == "Management Tim":
        show_team_management()
    elif st.session_state.active_tab == "Pengaturan":
        show_settings()
    elif st.session_state.active_tab == "SalesAdd":
        show_sales_add_order()
    elif st.session_state.active_tab == "SalesOrders":
        show_sales_orders()
    elif st.session_state.active_tab == "Logout":
        # Handle logout
        st.query_params.clear()
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.df = pd.DataFrame()
        st.rerun()
        
    # Ringkasan kinerja tim singkat di Dashboard
    if st.session_state.active_tab == "Dashboard" and not st.session_state.df.empty:
        contrib = {}
        for _, row in st.session_state.df.iterrows():
            add_by = row.get("created_by", "")
            if add_by:
                contrib[("Order", add_by)] = contrib.get(("Order", add_by), 0) + 1
            prod_by = row.get("produksi_by", "")
            if prod_by:
                contrib[("Produksi", prod_by)] = contrib.get(("Produksi", prod_by), 0) + 1
            dist_by = row.get("distribusi_by", "")
            if dist_by:
                contrib[("Distribusi", dist_by)] = contrib.get(("Distribusi", dist_by), 0) + 1
        if contrib:
            st.markdown("---")
            st.markdown("### 👥 Kinerja Tim (ringkas)")
            data = [{"Tugas": k[0], "User": k[1], "Jumlah": v} for k, v in contrib.items()]
            st.dataframe(pd.DataFrame(data).sort_values(["Tugas","Jumlah"], ascending=[True, False]), use_container_width=True)
            
            # Detail kontribusi tim
            detail_rows = []
            # Payments: hitung jumlah transaksi dan total nominal per user dari payment_history
            for _, row in st.session_state.df.iterrows():
                hist = str(row.get("payment_history", "") or "").strip()
                if hist:
                    for line in hist.split("\n"):
                        parts = [p.strip() for p in line.split("|")]
                        if len(parts) >= 4:
                            user = parts[1]
                            try:
                                amount = int(float(parts[2]))
                            except:
                                amount = 0
                            if user:
                                detail_rows.append({"Kategori":"Pembayaran","User":user,"Detail":"Transaksi","Jumlah":1})
                                detail_rows.append({"Kategori":"Pembayaran","User":user,"Detail":"Nominal","Jumlah":amount})
                # Produksi: hitung status perubahan per user dari produksi_history
                prod_hist = str(row.get("produksi_history", "") or "").strip()
                if prod_hist:
                    for line in prod_hist.split("\n"):
                        parts = [p.strip() for p in line.split("|")]
                        if len(parts) >= 3:
                            user = parts[1]
                            status = parts[2]
                            if user:
                                detail_rows.append({"Kategori":"Produksi","User":user,"Detail":status,"Jumlah":1})
                # Distribusi: hitung status perubahan per user dari distribusi_history
                dist_hist = str(row.get("distribusi_history", "") or "").strip()
                if dist_hist:
                    for line in dist_hist.split("\n"):
                        parts = [p.strip() for p in line.split("|")]
                        if len(parts) >= 3:
                            user = parts[1]
                            status = parts[2]
                            if user:
                                detail_rows.append({"Kategori":"Distribusi","User":user,"Detail":status,"Jumlah":1})
            if detail_rows:
                df_detail = pd.DataFrame(detail_rows)
                # Agregasi: gabungkan baris per (Kategori, User, Detail)
                agg_detail = df_detail.groupby(["Kategori","User","Detail"], as_index=False)["Jumlah"].sum()
                # Urutan prioritas tampilan
                order_map = {"Pembayaran":0,"Produksi":1,"Distribusi":2}
                agg_detail["__order"] = agg_detail["Kategori"].map(order_map).fillna(99)
                agg_detail = agg_detail.sort_values(["__order","User","Kategori","Detail"], ascending=[True, True, True, True]).drop(columns="__order")
                st.markdown("### 📌 Kinerja Tim (detail)")
                st.dataframe(agg_detail, use_container_width=True)
    
    st.markdown('<div class="custom-footer">© 2025 Daluase Clothing Studio — Internal Management System</div>', unsafe_allow_html=True)

# ===================== RUN APP =====================
if __name__ == "__main__":
    main()
